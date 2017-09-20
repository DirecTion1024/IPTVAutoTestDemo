#coding=utf-8

import datetime
import logging
from pprint import pprint 
logging.basicConfig(level=logging.INFO)
from keywordgroup import KeywordGroup
import pymongo
from robot.libraries.DateTime import *

class _OsspDetailLogHelper(KeywordGroup):
    DB_CONN = {
        "host": "172.16.82.116",
        "port": 27017,
        "log_db_ime": "log_db_ime",
        "log_db_ime_detail": "log_db_detail_ime",
    }
    
    MAX_CTM_DELTA_SECONDS = 60        
    
    def __init__(self):
        self.client = pymongo.MongoClient(self.DB_CONN["host"], self.DB_CONN["port"])
        self.ime = self.client[self.DB_CONN["log_db_ime"]]
        self.ime_detail = self.client[self.DB_CONN["log_db_ime_detail"]]
        
    def find_one(self,ins,logtype,record):
        table = ins[logtype]
        test_case = dict([(k.lower(), v) for (k, v) in record.items()])
#         del test_case["ctm"]
        check_result = table.find_one(test_case)
        return check_result
    
    def find_all(self,ins,logtype,record):
        table = ins[logtype]
        test_case = dict([(k.lower(), v) for (k, v) in record.items()])
        print test_case
        print table.count(), table.find(test_case).count()
        result = table.find(test_case).sort("ctm",pymongo.DESCENDING)
        return result
    
    def find_all_details(self,*args,**kw):
        #"cmd":"getdc",
        print '-'*20
        print kw
        if("ctm") in kw.keys():
            ctm = kw["ctm"]
            print ctm
            del kw["ctm"]
            print kw
            print add_time_to_date(ctm, datetime.timedelta(minutes=10))
            print subtract_time_from_date(ctm, datetime.timedelta(minutes=10))
            kw["ctm"] = {"$gte":subtract_time_from_date(ctm, datetime.timedelta(minutes=10)),
                         "$lt":add_time_to_date(ctm, datetime.timedelta(minutes=10))
                         }
            print kw
#         result = self.find_all(self.ime,"interfacelog", {"uid":"160721143455174984","cmd":"getconfig","ctm":{"$gte":"2017-03-10","$lt":"2017-03-12"}})
        result = self.find_all(self.ime,"interfacelog",kw)
        print '#'*20
        d = {}
        num = 0
        for item in result:
            detailid = item['detailid']
            print '-'*20,detailid
            print item
            d=dict(d, **item)
            detail = self.find_all(self.ime_detail,"interfacelog", {"detailid":detailid})
            
            for item in detail:
                print item
                d=dict(d, **item)
            
            pprint(d)
            print d['ctm']
            num += 1
            if(num > 5):
                break
        return d
    
    
    def find_all_details2(self):
        #[u'plugin', u'theme', u'getadinfo', u'getcardcontent', u'getconfig', u'version', u'expression', u'otherres', u'permsoftconfig', u'HCI', u'permsofts', u'querysugconfig', u'getdc', u'active', u'uplog', u'clientinfo', u'getsmscategory', u'getappadinfo', u'getrdinfo', u'getrcmdctg', u'simpleres', u'hotword', u'themectg', u'thesaurus', u'feedback', u'expressionctg', u'upmd', u'appsug', u'commonres', u'ressearch', u'downres', u'anonlogin', u'querysug', u'config', u'gettagres', u'gettags']
        ossp_log_type_should_checks    = ['getconfig', 'version', 'permsoftconfig', 'HCI', 'permsofts', 'getdc', 'active', 'uplog', 'clientinfo',  'upmd', 'downres', 'anonlogin']
        ossp_log_type_already_requests = ossp_log_type_should_checks
        result = self.find_all(self.ime,
                               "interfacelog",
                               #{u'cmd': u'getconfig', u'uid': u'160721143455174984'}
                                {'uid': '161013152258886723'}
                               #{ 'cmd': 'getconfig', 'uid': '160721143455174984'}
                               #2017-03-22 15:24:13.062
                               #{'cmd': 'active', 'uid': '161114084005990424','ctm': {'$gte': '2017-03-22 15:22:13.141', '$lt': '2017-03-22 15:26:13.141'} }
#                                {'ctm': {'$gte': '2017-03-22 15:58:09.914', '$lt': '2017-03-22 16:02:09.914'}, u'cmd': u'getconfig', u'uid': u'160721143455174984'}
                               )
        print '#'*20
        d = {}
        num = 0
        cmd_list = []
        for item in result:
            detailid = item['detailid']
            cmd = item['cmd']
#             print '-'*20,detailid,cmd
            if(cmd not in cmd_list):
                cmd_list.append(cmd)
            continue
            d=dict(d, **item)
            detail = self.find_all(self.ime_detail,"interfacelog", {"detailid":detailid})
            
            for item in detail:
                print item
                d=dict(d, **item)
            
            pprint(d)
            print d['ctm']
            num+=1
            if(num > 2):
                break
        print cmd_list
        return d
def main():
    osspLog = _OsspDetailLogHelper()
    osspLog.find_all_details2()
    
if __name__ == '__main__':
    main()