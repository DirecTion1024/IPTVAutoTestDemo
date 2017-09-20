#coding=utf-8

import datetime,time
import logging
from pprint import pprint 
logging.basicConfig(level=logging.INFO)
from keywordgroup import KeywordGroup
import pymongo
from robot.libraries.DateTime import *
from robot.libraries.BuiltIn import BuiltIn
import re
from serverlib.GetdcLib import GetdcLib

class _OsspDetailLogHelper(KeywordGroup):
    DB_CONN = {
        "host": "172.16.82.114",
        "port": 27017,
        "log_db_ime": "log_db_ime",
        "log_db_ime_detail": "log_db_detail_ime",
    }
    
    MAX_CTM_DELTA_SECONDS = int(BuiltIn().get_variable_value("${MAX_CTM_DELTA_SECONDS}")) if BuiltIn().get_variable_value("${MAX_CTM_DELTA_SECONDS}") else 120
    
    def __init__(self):
        self.client = pymongo.MongoClient(self.DB_CONN["host"], self.DB_CONN["port"])
        self.ime = self.client[self.DB_CONN["log_db_ime"]]
        self.ime_detail = self.client[self.DB_CONN["log_db_ime_detail"]]
        self.ossplog = {}
        
    def find_one(self,ins,logtype,record):
        table = ins[logtype]
        test_case = dict([(k.lower(), v) for (k, v) in record.items()])
#         del test_case["ctm"]
        check_result = table.find_one(test_case)
        return check_result
    
    def find_all(self,ins,logtype,record):
        table = ins[logtype]
        test_case = dict([(k.lower(), v) for (k, v) in record.items()])
#         print table.count(), table.find(test_case).count()
        result = table.find(test_case).sort("ctm",pymongo.DESCENDING)
        return result
    
    def check_all_detail_log(self,*args,**kw):
        
        result = self.find_all(self.ime,"interfacelog", {"uid":"160721143455174984","ctm":{"$gte":"2017-03-14 14:01:30.880","$lt":"2017-03-14 15:27:27.827"}})
        
#         timeout = self.MAX_CTM_DELTA_SECONDS
#         result = self.find_all(self.ime,"interfacelog",kw)
        
#         print 'wait ossp log with left seconds:%d'%(timeout)
#         while(result.count() <= 0):
#             time.sleep(1)
#             timeout -= 1
#             print 'wait ossp log with left seconds:%d'%(timeout)
#             result = self.find_all(self.ime,"interfacelog",kw)
#             if(timeout <= 0):
#                 raise AssertionError(u"Ossp Log can not be found with keys %s after %s s" % (str(kw), self.MAX_CTM_DELTA_SECONDS))
        
        
        num = 0
        for item in result:
            d = {}
            detailid = item['detailid']
            if(item["cmd"] in args):
                print '-'*20,'Detailid:',detailid
                d=dict(d.items() + item.items())
                detail = self.find_all(self.ime_detail,"interfacelog", {"detailid":detailid})
                
                for detail_item in detail:
    #                 print detail_item
                    d=dict(d.items() + detail_item.items())
                
                num += 2
                if(num > 0):
                    break
                
                print '-'*20,'Parsed keys:'
                pprint(self.ossplog)
    
    def wait_ossp_detail_log(self,*args,**kw):
        self.ossplog = {}
        
        #"cmd":"getdc",
        print '-'*20,'Args:'
        print kw
        if("ctm") in kw.keys():
            ctm = kw["ctm"]
            print ctm
            del kw["ctm"]
            print kw
            print add_time_to_date(ctm, datetime.timedelta(seconds=120))
            print subtract_time_from_date(ctm, datetime.timedelta(seconds=120))
            kw["ctm"] = {"$gte":subtract_time_from_date(ctm, datetime.timedelta(seconds=120)),
                         "$lt":add_time_to_date(ctm, datetime.timedelta(seconds=120))
                         }
            print kw
#         result = self.find_all(self.ime,"interfacelog", {"uid":"160721143455174984","cmd":"getconfig","ctm":{"$gte":"2017-03-10","$lt":"2017-03-12"}})
        
        timeout = self.MAX_CTM_DELTA_SECONDS
        result = self.find_all(self.ime,"interfacelog",kw)
        
        print 'wait ossp log with left seconds:%d'%(timeout)
        while(result.count() <= 0):
            time.sleep(1)
            timeout -= 1
            print 'wait ossp log with left seconds:%d'%(timeout)
            result = self.find_all(self.ime,"interfacelog",kw)
            if(timeout <= 0):
                raise AssertionError(u"Ossp Log can not be found with keys %s after %s s" % (str(kw), self.MAX_CTM_DELTA_SECONDS))
        
        d = {}
        num = 0
        for item in result:
            detailid = item['detailid']
            print '-'*20,'Detailid:',detailid
            d=dict(d.items() + item.items())
            detail = self.find_all(self.ime_detail,"interfacelog", {"detailid":detailid})
            
            for detail_item in detail:
                print detail_item
                d=dict(d.items() + detail_item.items())
            
            num += 1
            if(num > 0):
                break
        print '-'*20,'Parsed keys:'
        self.ossplog = d
        pprint(self.ossplog)
#         BuiltIn().set_global_variable("&{CUR_OSSP_DETAIL_LOG}",str(d))
        return d
    
    def find_all_details(self,logtype,*args,**kw):
        result = self.find_all(self.ime,logtype, {"uid":"160721143455174984","cmd":"getconfig","ctm":{'$gte': '2017-03-14 12:48:19.688', '$lt': '2017-03-14 12:52:19.688'}})
#         result = self.find_all(self.ime,logtype, {"uid":"160721143455174984"})
#         result = self.find_all(self.ime,"interfacelog",{"ctm":{"$gte":"2017-03-10"}})
#         print '#'*20
        d = {}
        num = 0
        for item in result:
            detailid = item['detailid']
#             print '-'*20,detailid
#             print item
            d=dict(d, **item)
            detail = self.find_all(self.ime_detail,"logtype", {"detailid":detailid})
            
            for item in detail:
#                 print item
                d=dict(d, **item)
            
#             pprint(d)
#             print d['ctm']
            if(num > 20):
                break
        return d
    
    def ossplog_check_uid_legal(self,value=None):
        '''长度大于等于15，小于等于18之间
        '''
        if(not value):
            value = self.ossplog["uid"]
        print value
        length = len(value)
        if(length < 15 or length > 18):
            return False
        
    def ossplog_check_version_legal(self,value=None):
        '''合法：7.1.4719 或 7.1.4719.ossptest 
        '''
        if(not value):
            value = self.ossplog["cver"]
        print value
        if re.match("^[0-9]\\.[0-9]\\.[0-9]{4}(|.ossptest)",value):
            return True
        else:
            return False
        
    def ossplog_check_downfrom_legal(self,value=None):
        '''合法：匹配^[0-9]{8}$
        '''
        if(not value):
            value = self.ossplog["df"]
        print value    
        if re.match("^[0-9]{8}$",value):
            return True
        else:
            return False
        
    def ossplog_check_ip_legal(self,value=None):
        '''匹配：(2[0-4][0-9]|25[0-5]|1[0-9][0-9]|[1-9]?[0-9])(\.(2[0-4][0-9]|25[0-5]|1[0-9][0-9]|[1-9]?[0-9])){3}
        '''
        if(not value):
            value = self.ossplog["localip"]
        print value    
        if re.match("(2[0-4][0-9]|25[0-5]|1[0-9][0-9]|[1-9]?[0-9])(\.(2[0-4][0-9]|25[0-5]|1[0-9][0-9]|[1-9]?[0-9])){3}",value):
            return True
        else:
            return False
        
    def ossplog_should_contains_keys(self,*keys):
        '''
        '''
        print 'keys should contains:',keys
        print 'keys actual contains:',self.ossplog.keys()
        d = self.ossplog
        for key in keys:
            if key not in d.keys():
                print 'false',key
                return False
            else:
                print key,":",self.ossplog[key]
        print 'true'
        return True
    
    def ossplog_keys_should_not_be_empty(self,*keys,**kws):
        '''
        '''
        print 'keys should not be empty:',keys
        d = self.ossplog
        for key in keys:
            if key not in d or not key:
                return False
        
        return True
    
    def _clear_uid(self,ins,logtype,record):
        table = self.client[ins][logtype]
        print ''
        print '-'*10,ins,logtype
        test_case = dict([(k, v) for (k, v) in record.items()])
        print test_case
        print table.count(), table.find(test_case).count()
        result = table.find(test_case)#.sort("ctm",pymongo.DESCENDING)
        for item in result:
            print '#'*3,item
        if(table.find(test_case).count()):
            table.remove(test_case)
        print '-'*10,'Delete'
        print table.count(), table.find(test_case).count()
        for item in result:
            print '#'*3,item
        return result
    def clear_server_uid_storage(self,uid):
        print 'uid:',uid
        result = self._clear_uid("OSSP10","BizUserExtend",{'Uid': uid})
        result = self._clear_uid("OSSP10","Devices",{'Uid': uid})
        result = self._clear_uid("OSSP10","DevicesExtend",{'Uid': uid})
        result = self._clear_uid("OSSP10","Devices_copy",{'Uid': uid})
        result = self._clear_uid("OSSP10Extend","DevicesExtend",{'Uid': uid})
        result = self._clear_uid("OSSP10_imei_null","BizUserExtend",{'Uid': uid})
        result = self._clear_uid("OSSP10_imeiinterface","BizUserExtend",{'Uid': uid})
    def config_server_getdc(self,getdc_local_dir):
        ftp=GetdcLib('172.16.82.100')
        ftp.Login('ydhl','123456')
        ftp.ftp.cwd("/data/logs/getdc")
        new_path = ftp.getNewPath()
        ftp.createNewPath(new_path)
        ftp.UpLoadFileTree(getdc_local_dir, "/data/logs/getdc/"+new_path)
        ftp.close()
        import urllib
        print "http://172.16.82.108:8089/ossp-synctool-service/getdc?c=getdc&type=1&filedir=%s"%(new_path)
        f=urllib.urlopen("http://172.16.82.108:8089/ossp-synctool-service/getdc?c=getdc&type=1&filedir=%s"%(new_path))
        s=f.read()
        print s
        if(s.strip() != 'true'):
            raise AssertionError(u"Config server env failed!")
def main():
    osspLog = _OsspDetailLogHelper()
#     d = osspLog.find_all_details("statelog")
#     pprint(d)
    osspLog.clear_server_uid_storage("170419171335724948")
if __name__ == '__main__':
    main()