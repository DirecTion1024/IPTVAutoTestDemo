#-*- coding: UTF-8 -*-
"""

(C) Copyright 2016 wei_cloud@126.com

"""
import urllib, urllib2
import cookielib
import rsa, base64
import os, random
import gzip
import StringIO
import json
from datetime import timedelta, datetime
from robot.api import logger
from pprint import pprint
from platform import platform

class ImeServerVoiceCloudLib(object):
    public_key_conf = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDNzh69KDi0KQUh5g3G0oeTzSTg
X039du+Eq4d+w/F2WTPM5pprzIUR0fKzA2ETCT7VHhD6evA7TFjD3pp+PdLnzPrD
LHF+Iv3HhcDC+hiwRXR33Gm7gY2pbgpVy1Jj5aGBty1sH8tiZuvZKubPzBOOQWs9
un/QRzfdKWKSxAd7cwIDAQAB
-----END PUBLIC KEY-----'''
    
    def __init__(self):
        self.defaultCodec = 'UTF-8'
        self.defaultHeads = {'User-Agent': 'Chrome/46.0.2486.0',
                             'Content-Type': 'application/x-www-form-urlencoded; charset=%s' % self.defaultCodec,
                             'Pragma': 'no-cache',
                             'Accept': '*/*',
                             'Connection': 'Keep-Alive',}
        self.baseUrl = 'http://ossptest.voicecloud.cn'
        ck = cookielib.CookieJar()
        self.ck = ck
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ck))
        self.sessionId = ''
        
    def set_home_url(self, homeurl):
        old = self.baseUrl
        self.baseUrl = homeurl
        return old
      
    def _parse_url(self, url):
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return self.baseUrl + url
      
    def _read_page(self, resp, unzip=True):
        page = resp.read()
#         print '-'*20,'read page start'
#         print dir(resp)
#         print resp.info()
#         print page
#         print '-'*20,'read page over'
        if unzip and resp.headers.get('Content-Encoding') == 'gzip':
            page = gzip.GzipFile(fileobj=StringIO.StringIO(page)).read()
        if not unzip and resp.headers.get('Content-Encoding') == 'gzip':
            return page
        if not isinstance(page, unicode):
            page = unicode(page, self.defaultCodec)
#         logger.debug(page)
        return page
    
    def _get_page(self, url, args={}, heads={}, expectCode=200):
        url = self._parse_url(url)
        para = urllib.urlencode(args) if isinstance(args, dict) else args
        logger.debug("Post Request %s with %s" % (url, para))
        rheads = {}
        rheads.update(self.defaultHeads)
        rheads.update(heads)
        
        url = url + '?' + para
        request = urllib2.Request(url, headers=rheads)
        resp = self.opener.open(request)
        if resp.getcode() != expectCode:
            raise AssertionError("Server Failure! Response code %s" % resp.getcode())
        page = self._read_page(resp)
        resp.close()
        return page
        
    def _post_page(self, url, data, heads={}, expectCode=200):
        url = self._parse_url(url)
#         print url
        para = urllib.urlencode(data) if isinstance(data, dict) else data
        logger.debug("Post Request %s with %s" % (url, para))
        rheads = {}
        rheads.update(self.defaultHeads)
        rheads.update(heads)
        
#         pprint(rheads)
        request = urllib2.Request(url, para, rheads)
        resp = self.opener.open(request)
        
        if resp.getcode() != expectCode:
            raise AssertionError("Server Failure! Response code %s" % resp.getcode())
        page = self._read_page(resp)
        resp.close()
        return page
    
    def login_ossptest_voicecloud(self, username, passwd, url='/auth/login?oredirect=null', heads={}):
        values = {'loginName':username,
                'password':self._enc_passwd(passwd),
#                   'password':'V2CKryVs3GiTgmHrMb+lBkofOyxi7vJapw4Eaxv6xv3d5QQAF7fl/2N2s5RkHolutukfQqR8Wy5+SXqKbKhXt/iY+Ptua761Z4wI5hzi43Nfmsw6i6xsCfIJ5ix1eY32QD7IZG5W1gSt65cMR3zn/XPaGTu8Wo0QhZV8wcsKm8M='
                 }
        ck = cookielib.CookieJar()
        self.ck = ck
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ck))
        
        page = self._post_page(url, values, heads)
        if page.find(u'错误：') != -1:
            raise RuntimeError('Login Failed!')
        self.sessionId = self.get_session_id()
    
    
    def login_menu_web(self, username, passwd, url='/auth/menu/permitSubMenus', heads={}):
        values = {"loginName":"ydhl",
                  "parentId":"2002",
                  "fetchSub":"true",
                 }
        
#         ck = cookielib.CookieJar()
#         self.ck = ck
#         self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ck))
        
        page = self._post_page(url, values, heads)
        if page.find(u'错误：') != -1:
            raise RuntimeError('Login Failed!')
        self.sessionId = self.get_session_id()
        
    def login_plan_web(self, username, passwd, url='/ygxt/keyword/planManage.do', heads={}):
        values = {'loginName':username,
                  'password':self._enc_passwd(passwd),
                 }
        
        ck = cookielib.CookieJar()
        self.ck = ck
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ck))
        
        page = self._post_page(url, values, heads)
        if page.find(u'错误：') != -1:
            raise RuntimeError('Login Failed!')
        self.sessionId = self.get_session_id()
    
    def _enc_passwd(self, passwd):
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(self.public_key_conf)
        return base64.encodestring(rsa.encrypt(passwd, public_key))
   
    def _get_cookie_value(self, cookies, skey):
        val = ''
        if not isinstance(cookies, dict):
            return ''
        for key, value in cookies.items():
            if key == skey:
                val = value
                break
            val = self._get_cookie_value(value, skey)
            if val: break
        return val
   
    def get_cookie_item(self, skey):
        ck = None
        
        for handler in self.opener.handlers:
            if isinstance(handler, urllib2.HTTPCookieProcessor):
                ck = handler.cookiejar._cookies
                break
        
        if not ck:
            return ''
#         logger.debug(ck)
        return self._get_cookie_value(ck, skey)
    
    def get_session_id(self):
        sessionId = self.get_cookie_item('SHAREJSESSIONID').value
        if not sessionId:
            raise RuntimeError("Can not find session id in cookies!")
        return sessionId
    
    def ygxt_keyword_changestatus(self,plan_id,status,opt):
        print "ygxt_keyword_changestatus:",plan_id,status,opt
        url = "/ygxt/keyword/changeStatus"
        values = {"id":plan_id,
                  "status":status,
                  "opt":opt}
        rheaders = {"Accept":"application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding":"gzip, deflate",
                    "Accept-Language":"zh-CN,zh;q=0.8",
                    "Content-Length":"37",
                    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                    "Host":"ossptest.voicecloud.cn",
                    "Origin":"http://ossptest.voicecloud.cn",
                    "Referer":"http://ossptest.voicecloud.cn/ygxt/keyword/planManage.do",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                    "X-Requested-With":"XMLHttpRequest",
                    }
        page = self._post_page(url, values, rheaders)
    
    def getSearchCandidatePlanById(self,id_input):
        
        url = "/ygxt/keyword/planListPageQuery"
        status = None
        flag = False
        for i in range(0,20):
            values = {"sEcho":"%d"%(2*i-1),
                      "iColumns":"12",
                      "sColumns":"",
                      "iDisplayStart":"%d"%(10*i),
                      "iDisplayLength":"10",
                      "iSortingCols":"0",
                      "bSortable_0":"false",
                      "bSortable_1":"false",
                      "bSortable_2":"false",
                      "bSortable_3":"false",
                      "bSortable_4":"false",
                      "bSortable_5":"false",
                      "bSortable_6":"false",
                      "bSortable_7":"false",
                      "bSortable_8":"false",
                      "bSortable_9":"false",
                      "bSortable_10":"false",
                      "bSortable_11":"false",
                      "bizId":"100IME",
                      "osId":"Android",
                      "status":"",
                      "partner":"",
                      "text":""
            }
            
            rheaders = {"Accept":"application/json, text/javascript, */*; q=0.01",
                        "Accept-Encoding":"gzip, deflate",
                        "Accept-Language":"zh-CN,zh;q=0.8",
                        "Content-Length":"346",
                        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                        "Host":"ossptest.voicecloud.cn",
                        "Origin":"http://ossptest.voicecloud.cn",
                        "Referer":"http://ossptest.voicecloud.cn/ygxt/keyword/planManage.do",
                        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                        "X-Requested-With":"XMLHttpRequest",
                        }
            page = self._post_page(url, values, rheaders)
#             print page
            r = json.loads(page, encoding=self.defaultCodec)
            status = None
            for id,product,platform,name,firm,status,time,id2,item1,item2,item3,item4 in r["aaData"]:
#                 print id,product,platform,name,firm,status,time,id2,item1,item2,item3,item4
#                 print [id,id_input]
                if(id == id_input):
                    flag = True
                    break
            if(flag):
                break
        print id,product,platform,name,firm,status,time,id2,item1,item2,item3,item4
#         print '--status',status
        if flag:
            return {"id":id,"status":status}
        else:
            return {}
    
    def setSearchCandidatePlan(self,id_input,target):
        
        node = self.getSearchCandidatePlanById(id_input)
        status = node["status"] if node else None
        if(not status):
            raise AssertionError("Config server failed:setSearchCandidatePlan")
        #open plan
        if(target == 1):
            if(status == "9"):
                pass
            elif(status == "6"):
                self.ygxt_keyword_changestatus(id_input,"3","初审")
                self.ygxt_keyword_changestatus(id_input,"4","审批")
            elif(status == "3"):
                self.ygxt_keyword_changestatus(id_input,"4","审批")
            print '-'*100
        #close plan
        elif(target == 0):
            #close plan
            if(status == "1"):
                self.ygxt_keyword_changestatus(id_input,"6","暂停")
            print '-'*100
        else:
            raise AssertionError("Param target must in 0[close],1[open]")
        return True
    
if __name__ == '__main__':
    username = 'ydhl'
    passwd = 'ydhl'
    CL = ImeServerVoiceCloudLib()
    CL.login_ossptest_voicecloud(username, passwd)
#     print '#'*100
    
    request = urllib2.Request("http://ossptest.voicecloud.cn/auth/")
    resp = CL.opener.open(request)
#     print resp.read()
     
    CL.login_menu_web(username, passwd)
     
    request = urllib2.Request("http://ossptest.voicecloud.cn/ygxt/keyword/planManage.do")
    resp = CL.opener.open(request)
#     print resp.read()
    
    CL.setSearchCandidatePlan(96,1)
    CL.setSearchCandidatePlan(93,1)
    CL.setSearchCandidatePlan(92,1)

    print CL.getSearchCandidatePlanById(96)
    print CL.getSearchCandidatePlanById(93)
    print CL.getSearchCandidatePlanById(92)
    
