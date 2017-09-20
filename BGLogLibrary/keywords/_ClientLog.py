#-*- coding:utf-8 -*-
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

import os,sys,time,urllib
from pprint import pprint
reload(sys)
sys.setdefaultencoding('utf-8')

from clientlib.IFlyLogTagsObserver import IFlyLogTagsObserver
from clientlib.ClientLogCatcherThread import ClientLogCatcherThread
from clientlib.iFlyClientLogBase import iFlyClientLogBase
from clientlib.IFlyLogParser import RequestLogParser,ResponseLogParser
from keywordgroup import KeywordGroup
from clientlib.ClientLogNode import ClientLogNode
from serverlib.GetdcLib import GetdcLib

class _ClientLog(KeywordGroup):
    def __init__(self):
        self.appiumui ='gui'
        self.TIMEOUT_REQUEST_LOG       = 60#0
        self.TIMEOUT_RESPONSE_LOG      = 90#0
        self.TIMEOUT_CLIENTHANDLER_LOG = 20#0
        self.INTERVAL = 5
        
        self.iFlyLogTagsObserver = IFlyLogTagsObserver()
        self.iFlyLogTagsObserver.regiter_tag_response("OperationResultFactory") \
            .regiter_tag_response("PermissionBizHelper") \
            .regiter_tag_request("OperationManager") \
            .regiter_tag_clienthandler("AssistHandler")\
            .regiter_tag_request("NewUserLogHandler")\
            .regiter_tag_request("LogPool")\
            .regiter_tag_request("MenuStateLogCollect")\
            .regiter_tag_request("SearchSuggestionConfigDataProcessor")\
            .regiter_tag_request("statssdk_LogController")\

        self.clientLogCatcherThread = ClientLogCatcherThread()
        self.clientLogCatcherThread.regiterObserver(self.iFlyLogTagsObserver)
#         self.clientLogCatcherThread.start()\
        logger.info('ClientLog init', True, False)
        print 'ClientLog init',self.clientLogCatcherThread.is_logcat_thread_starts
        self.is_logcat_thread_starts = self.clientLogCatcherThread.is_logcat_thread_starts
        
    def client_log_set_buffer_empty(self):
        time.sleep(1)
        self.iFlyLogTagsObserver.mClienthandlerTagsLog = {}
        self.iFlyLogTagsObserver.mRequestTagsLog       = {}
        self.iFlyLogTagsObserver.mResponseTagsLog      = {}
        time.sleep(2)
        
    def client_log_print(self):
        pprint(self.iFlyLogTagsObserver.mClienthandlerTagsLog)
        pprint(self.iFlyLogTagsObserver.mRequestTagsLog)
        pprint(self.iFlyLogTagsObserver.mResponseTagsLog)
        
    def start_client_log_thread(self):
        """Starts logcat thread background.
        """
        print 'start_client_log_thread',self.is_logcat_thread_starts
        if(not self.is_logcat_thread_starts):
            self.clientLogCatcherThread.setDaemon(True)
            self.clientLogCatcherThread.start()
            self.is_logcat_thread_starts = self.clientLogCatcherThread.is_logcat_thread_starts
            self.clientLogCatcherThread.end_flag = False
        else:
            print "Client Log Thread Already Starts"
        
    def end_client_log_thread(self):
        """Ends logcat thread background.
        """
        print 'Starts logcat thread background.'
        self.clientLogCatcherThread.stop()
        self.is_logcat_thread_starts = self.clientLogCatcherThread.is_logcat_thread_starts
        self.clientLogCatcherThread.end_flag = True
    
    def client_log_file_links(self):
        """Link with logcat local file.
        There are three types:Detail,Tags,Marks
        """
        #file_path_detail,file_path_tags,file_path_marks
        
        html_templet = ur'''Logcat 详细日志：<a href="%s" target="_blank" title="LOGCAT">Logcat Detail</a>
Logcat Tag日志 ：<a href="%s" target="_blank" title="LOGCAT">Logcat Tags</a>
Logcat Mark日志：<a href="%s" target="_blank" title="LOGCAT">Logcat Marks</a>
                        '''
        obs = self.iFlyLogTagsObserver
        html_rst = html_templet%(os.path.abspath(obs.file_path_detail),
                                 os.path.abspath(obs.file_path_tags),
                                 os.path.abspath(obs.file_path_marks)
                                       )
        print html_rst
        logger.info(html_rst, True, False)
        pass
    
    def on_testcase(self,rootpath,casepath, casename):
        """Notice testcase begins,Often used in Testcase Setup
        """
        print os.path.abspath(rootpath)
        self.iFlyLogTagsObserver.onTestCase(rootpath, casepath, casename)
    
    def mark_log(self):
        """Mark logcat,Notice Testcase Logcat starts,Often used with unmark_log
        """
        self.iFlyLogTagsObserver.mark()
    
    def unmark_log(self):
        """UnMark logcat,Notice Testcase Logcat starts,Often used with mark_log
        """
        self.iFlyLogTagsObserver.unmark()
        
#         self.iFlyLogTagsObserver.onTestCase(".", "BgLog", "setup")
#         time.sleep(5)
#         print 'over1'
# #         self.iFlyLogTagsObserver.onTestCase(".", "BgLog", "setup2")
#         self.iFlyLogTagsObserver.mark()
#         time.sleep(5)
#         print 'over2'
#         print '-'*50
#         
#         pprint(self.get_request_log())
#         print self.wait_request_log("<cmd>getconfig</cmd>")
#         print self.wait_request_log("<cmd>upmd</cmd>")
#         print self.wait_request_log("<cmd>notice</cmd>")
#         requestlog = self.wait_request_log("<cmd>upmd</cmd>")
#         self.request_key_attribute_should_be(requestlog,"cmd", "upmd")
#          
#         responselog = self.wait_response_log("type = 50")
#         print '@@',responselog,'@@'
#         print self.response_key_attribute_should_be(responselog, "status", "000000")
#         print self.response_key_attribute_should_be(responselog, "descinfo", "上传成功")
#         print self.response_key_attribute_should_in(responselog, "status", "000000|success")
#         
#         self.iFlyLogTagsObserver.unmark()
        
    def get_request_log(self):
        return self.iFlyLogTagsObserver.get_request_log()
    def get_response_log(self):
        return self.iFlyLogTagsObserver.get_response_log()
    def get_clienthandler_log(self):
        return self.iFlyLogTagsObserver.get_clienthandler_log()
    
    def _is_keys_in_loglist(self, keys, loglist):
        '''
        增加了contains和notcontains参数。notcontains参数前以[NotContains]标识
        '''
        should_contains     = []
        should_not_contains = []
        for key in keys:
            print key
        
        for key in keys:
            if(key.startswith('[NotContains]')):
                should_not_contains.append(key.split('[NotContains]',1)[1])
            else:
                should_contains.append(key)
#         print 'loglist',loglist
        for node in loglist:
            log = node.msg
            key_in_log = True
            for key in should_contains:
#                 if key not in log['message']:
                if key not in log:
                    key_in_log = False
                    break
            for key in should_not_contains:
                if key in log:
                    key_in_log = False
                    break
            if key_in_log:
                return node
        return False
    
    def i(self,msg):
#         logger.info(msg, True, False)
        logger.info(msg, False, True)
    
    def d(self,msg):
#         logger.debug(msg, True)
        logger.debug(msg, False)
        
    def wait_request_log(self, *keys, **kws):
        """Wait request Log with contains *keys

        Examples:
        | Wait Request Log | <cmd>getconfig</cmd>
        """
        
        BuiltIn().set_global_variable("${CUR_Client_LOG_MSG}","")
        BuiltIn().set_global_variable("${CUR_Client_LOG_PCTIME}","")
        BuiltIn().set_global_variable("${CUR_Client_LOG_CLIENTTIME}","")
        start = time.time()
        timeout = int(kws.get('timeout', self.TIMEOUT_REQUEST_LOG))
        print 'keys:',[keys]
        rst_log = self._is_keys_in_loglist(keys, self.get_request_log())
        while not rst_log:
            end = time.time()
            if (end-start)*1 > timeout:
                raise AssertionError(u"Request Log can not be found with keys %s after %s s" % (keys, timeout))
            time.sleep(self.INTERVAL)
            rst_log = self._is_keys_in_loglist(keys, self.get_request_log())
        print rst_log
        print rst_log.msg
        BuiltIn().set_global_variable("${CUR_Client_LOG_MSG}",rst_log.msg)
        BuiltIn().set_global_variable("${CUR_Client_LOG_PCTIME}",rst_log.pc_time)
        BuiltIn().set_global_variable("${CUR_Client_LOG_CLIENTTIME}",rst_log.client_time)
        return rst_log
    
    def wait_response_log(self, *keys, **kws):
        """Wait Response Log with contains *keys

        Examples:
        | Wait Response Log | type \= 54 | result \=
        """
        is_check_response_log = BuiltIn().get_variable_value("${is_check_response_log}")
        if(not is_check_response_log):
            return True
        
        BuiltIn().set_global_variable("${CUR_Client_LOG_MSG}","")
        BuiltIn().set_global_variable("${CUR_Client_LOG_PCTIME}","")
        
        start = time.time()
        timeout = int(kws.get('timeout', self.TIMEOUT_RESPONSE_LOG))
#         print '#',keys,timeout
#         print '##',kws
        rst_log = self._is_keys_in_loglist(keys, self.get_response_log())
        while not rst_log:
            end = time.time()
            if (end-start)*1 > timeout:
                raise AssertionError(u"Response Log can not be found with keys %s after %s s" % (keys, timeout))
            time.sleep(self.INTERVAL)
            print 'sleep',self.INTERVAL,timeout
            rst_log = self._is_keys_in_loglist(keys, self.get_response_log())
        print rst_log
        print rst_log.msg
        BuiltIn().set_global_variable("${CUR_Client_LOG_MSG}",rst_log.msg)
        BuiltIn().set_global_variable("${CUR_Client_LOG_PCTIME}",rst_log.pc_time)
        return rst_log
        
    def wait_clienthandler_log(self):
        pass
    
    def request_key_attribute_should_be(self, *keys, **kws):
        print kws
        print [kws]
        print str(kws)
        self.d(u"----------校验字段及期望值:\n"+str(kws))
        if(keys):
            cur_bg_log = keys[0]
        else:
            cur_bg_log = str(kws.get('CUR_Client_LOG_MSG', BuiltIn().get_variable_value("${CUR_Client_LOG_MSG}")))
        
        self.d(u"----------待校验log:\n"+cur_bg_log)
        
        logitem = iFlyClientLogBase(cur_bg_log, self.appiumui, parser=RequestLogParser)
        self.d(u"----------log解析结果:\n"+str(logitem))
        
        for element,value in kws.items():
            if(element in logitem.keys()):
                if(not logitem[element] == value):
                    raise AssertionError(u"Attribute not euqals! except:%s, actual:%s"%(value,logitem[element]))
            else:
                raise AssertionError(u"Request Log not found with element:%s"%(element))
        
    def request_key_attribute_should_in(self, *keys, **kws):
        print kws
        print [kws]
        print str(kws)
        self.d(u"----------校验字段及期望值:\n"+str(kws).replace('|',' or '))
        if(keys):
            cur_bg_log = keys[0]
        else:
            cur_bg_log = str(kws.get('CUR_Client_LOG_MSG', BuiltIn().get_variable_value("${CUR_Client_LOG_MSG}")))
        
        self.d(u"----------待校验log:\n"+cur_bg_log)
        logitem = iFlyClientLogBase(cur_bg_log, self.appiumui, parser=RequestLogParser)
        self.d(u"----------log解析结果:\n"+str(logitem))
        
        for element,value in kws.items():
            if(element in logitem.keys()):
                if(logitem[element] not in value.split('|')):
                    raise AssertionError(u"Attribute not euqals! except:%s, actual:%s"%(value.replace('|',' or '),logitem[element]))
            else:
                raise AssertionError(u"Request Log not found with element:%s"%(element))
#         print u"属性:",element,u' 期望结果:',value.replace('|',' or ')
#         logitem = iFlyClientLogBase(requestlog, self.appiumui, parser=RequestLogParser)
#         pprint(logitem)
#         if(element in logitem.keys()):
#             if(logitem[element] not in value.split('|')):
#                 raise AssertionError(u"Attribute not euqals! except:%s, actual:%s"%(value.replace('|',' or '),logitem[element]))
#         else:
#             raise AssertionError(u"Request Log not found with element:%s"%(element))
#         print u' 实际结果:',logitem[element]
#         return True
    
    def response_key_attribute_should_be(self, *keys, **kws):
        is_check_response_log = BuiltIn().get_variable_value("${is_check_response_log}")
        if(not is_check_response_log):
            return True
        
        self.d(u"----------校验字段及期望值:\n"+str(kws))
        if(keys):
            cur_bg_log = keys[0]
        else:
            cur_bg_log = str(kws.get('CUR_Client_LOG_MSG', BuiltIn().get_variable_value("${CUR_Client_LOG_MSG}")))
        
        self.d(u"----------待校验log:\n"+cur_bg_log)
        
        logitem = iFlyClientLogBase(cur_bg_log, self.appiumui, parser=ResponseLogParser)
        self.d(u"----------log解析结果:\n"+str(logitem))
        
        for element,value in kws.items():
            if(element in logitem.keys()):
                if(not logitem[element] == value):
                    raise AssertionError(u"Attribute not euqals! except:%s, actual:%s"%(value,logitem[element]))
            else:
                raise AssertionError(u"Response Log not found with element:%s"%(element))
    
    def response_key_attribute_should_in(self,*keys, **kws):
        is_check_response_log = BuiltIn().get_variable_value("${is_check_response_log}")
        if(not is_check_response_log):
            return True
        
        self.d(u"----------校验字段及期望值:\n"+str(kws).replace('|',' or '))
        if(keys):
            cur_bg_log = keys[0]
        else:
            cur_bg_log = str(kws.get('CUR_Client_LOG_MSG', BuiltIn().get_variable_value("${CUR_Client_LOG_MSG}")))
        
        self.d(u"----------待校验log:\n"+cur_bg_log)
        
        logitem = iFlyClientLogBase(cur_bg_log, self.appiumui, parser=ResponseLogParser)
        self.d(u"----------log解析结果:\n"+str(logitem))
        
        for element,value in kws.items():
            if(element in logitem.keys()):
                if(logitem[element] not in value.split('|')):
                    raise AssertionError(u"Attribute not euqals! except:%s, actual:%s"%(value.replace('|',' or '),logitem[element]))
            else:
                raise AssertionError(u"Request Log not found with element:%s"%(element))
        '''
        print u"属性:",element,u' 期望结果:',value.replace('|',' or ')
        logitem = iFlyClientLogBase(responselog, self.appiumui, parser=ResponseLogParser)
        pprint(logitem)
        if(element in logitem.keys()):
            if(logitem[element] not in value.split('|')):
                raise AssertionError(u"Attribute not euqals! except:%s, actual:%s"%(value.replace('|',' or '),logitem[element]))
        else:
            raise AssertionError(u"Request Log not found with element:%s"%(element))
        print u' 实际结果:',logitem[element]
        return True
        '''
    def config_server_getdc(self,getdc_local_dir):
        ftp=GetdcLib('172.16.82.100')
        ftp.Login('ydhl','123456')
        ftp.ftp.cwd("/data/logs/getdc")
        new_path = ftp.getNewPath()
        ftp.createNewPath(new_path)
        ftp.UpLoadFileTree(getdc_local_dir, "/data/logs/getdc/"+new_path)
        ftp.close()
        self.d("http://172.16.82.108:8089/ossp-synctool-service/getdc?c=getdc&type=1&filedir=%s"%(new_path))
        f=urllib.urlopen("http://172.16.82.108:8089/ossp-synctool-service/getdc?c=getdc&type=1&filedir=%s"%(new_path))
        s=f.read()
        self.d(s)
        if(s.strip() == 'true'):
            pass
        else:
            raise AssertionError(u"Config Server Getdc Failed!")
if __name__ == '__main__':
    clientLog = _ClientLog()
    
    
    
    
    
    
    