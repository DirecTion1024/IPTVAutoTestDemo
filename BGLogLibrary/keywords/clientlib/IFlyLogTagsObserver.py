#-*- coding: UTF-8 -*- 
import os,time,sys
from robot.libraries import DateTime
from robot.libraries.BuiltIn import BuiltIn
from ClientLogNode import ClientLogNode
from robot.api import logger

class IFlyLogTagsObserver():
    def __init__(self):
        self.root_path = BuiltIn().get_variable_value("${OUTPUT DIR}") if BuiltIn().get_variable_value("${OUTPUT DIR}") else "."
        self.is_mark = False
        
        self.mResponseTags      = []
        self.mRequestTags       = []
        self.mClienthandlerTags = []
        self.allTags           = []
        
        self.mResponseTagsLog      = {}
        self.mRequestTagsLog       = {}
        self.mClienthandlerTagsLog = {}
        self.allTagsLogs           = {}
        if(not os.path.isdir(self.root_path)):
            os.makedirs(self.root_path)
        self.detail_log = open(os.path.join(self.root_path,'other_all.log'),'w+')
        self.tags_log = open(os.path.join(self.root_path,'other_tags.log'),'w+')
        self.mark_log = None
        self.test_begin_time_year = BuiltIn().get_variable_value("${TEST_BEGIN_BY_CLIENT_TIME}")
        
    def _get_tags_log(self,d):
        l = []
        for k,v in d.items():
            for item in v:
                l.append(item)
        return l
    
    def _get_tags_log2(self,d):
        l = []
        for k,v in d.items():
            for item in v:
                l.append(item)
        return l
    
    def get_request_log(self):
        group_log_list = []
#         print self._get_tags_log(self.mRequestTagsLog)
        cNode = None
#         print 'mRequestTagsLog',self.mRequestTagsLog
        #self.mRequestTagsLog[tag_str].append((tag_str,pc_time,client_time,msg))
        for tag_str,nodes in self.mRequestTagsLog.items():
            for node in nodes:
                tag_str, pc_time, client, msg = node
                if(tag_str in ['NewUserLogHandler', 'LogPool', "MenuStateLogCollect", 'SearchSuggestionConfigDataProcessor', 'statssdk_LogController']):
                    cNode = ClientLogNode(tag_str, pc_time, client, msg)
                    group_log_list.append(cNode)
                else:
                    is_single_line = True
                    if(msg.startswith('postStatistics url = ')):
                        cNode = ClientLogNode(tag_str,pc_time,client,msg)
                        group_log_list.append(cNode)
                        is_single_line = True
                    elif msg.startswith('sRequst '):
                        cNode = ClientLogNode(tag_str,pc_time,client,msg)
                        group_log_list.append(cNode)
                        is_single_line = False
                    else:
                        if(group_log_list and not is_single_line):
                            group_log_list[-1].msg += msg
                        else:
                            cNode = ClientLogNode(tag_str,pc_time,client,msg)
                            group_log_list.append(cNode)
        return group_log_list
    
    def get_response_log(self):
        group_log_list = []
#         print self._get_tags_log(self.mResponseTagsLog)
        cNode = None
#         print 'mResponseTagsLog',self.mResponseTagsLog
        for node in self._get_tags_log(self.mResponseTagsLog):
#             print 'node',node
            tag_str,pc_time,client,msg = node
            if msg.startswith('type '):
                cNode = ClientLogNode(tag_str,pc_time,client,msg)
                group_log_list.append(cNode)
            else:
                if(group_log_list):
                    group_log_list[-1].msg += msg
        return group_log_list
    
    def get_clienthandler_log(self):
        return self._get_tags_log(self.mClienthandlerTagsLog)
        
    def mark(self):
        if(self.is_mark):
            pass
        else:
            self.is_mark = True
            self.detail_log.write('LOG-TEST-INFO:mark\n')
            self.detail_log.flush()
            
    def unmark(self):
        self.is_mark = False
        self.detail_log.write('LOG-TEST-INFO:unmark\n')
        self.detail_log.flush()
        
    def regiter_tag_response(self,tag):
        if(tag not in self.mResponseTags):
            self.mResponseTags.append(tag)
        if(tag not in self.allTags):
            self.allTags.append(tag)
        return self
    
    def regiter_tag_request(self,tag):
        if(tag not in self.mRequestTags):
            self.mRequestTags.append(tag)
        if(tag not in self.allTags):
            self.allTags.append(tag)
        return self
    
    def regiter_tag_clienthandler(self,tag):
        if(tag not in self.mClienthandlerTags):
            self.mClienthandlerTags.append(tag)
        if(tag not in self.allTags):
            self.allTags.append(tag)
        return self
    
    def log(self,log,tag):
        self.detail_log.write(log)
        self.detail_log.flush()
        if(tag in self.allTags):
            self.tags_log.write(log)
            self.tags_log.flush()
            if(self.is_mark):
                self.mark_log.write(log)
                self.mark_log.flush()
    
    def _get_pc_time(self):
        return DateTime.get_current_date()
    
    def onTagFound(self,line,tag,pc_time,date_str,time_str,msg):
        pc_time = self._get_pc_time()
        client_time = "%s\t%s\t%s"%(self.test_begin_time_year, date_str, time_str)
        self.log("%s\t%s\t%s\t%s"%(pc_time,client_time,tag,msg),tag)
        
#         print 'onTagFound',line,tag,pc_time,client_time,msg
        cNode = ClientLogNode(tag, pc_time, client_time, msg)
        if(tag in self.mRequestTags):
            self.onRequestTagFound(tag, pc_time, client_time, msg)
        elif(tag in self.mResponseTags):
            self.onResponseTagFound(tag, pc_time, client_time, msg)
        elif(tag in self.mClienthandlerTags):
            self.onClientHandlerTagFound(tag, pc_time, client_time, msg)
        else:
            pass
#             sys.stderr.write('err in onTagFound:\n')
#             sys.stderr.write(tag + pc_time + date_str + time_str + msg)
            
    def onRequestTagFound(self,tag_str,pc_time,client_time,msg):
        if(tag_str not in self.mRequestTagsLog.keys()):
            self.mRequestTagsLog[tag_str] = []
        self.mRequestTagsLog[tag_str].append((tag_str,pc_time,client_time,msg))
        
    def onResponseTagFound(self,tag_str,pc_time,client_time,msg):
        if(tag_str not in self.mResponseTagsLog.keys()):
            self.mResponseTagsLog[tag_str] = []
        self.mResponseTagsLog[tag_str].append((tag_str,pc_time,client_time,msg))
    
    def onClientHandlerTagFound(self,tag_str,pc_time,client_time,msg):
        if(tag_str not in self.mClienthandlerTagsLog.keys()):
            self.mClienthandlerTagsLog[tag_str] = []
        self.mClienthandlerTagsLog[tag_str].append((tag_str,pc_time,client_time,msg))
    
    def onTestCase(self,rootpath,casepath,casename):
        path = os.path.join(rootpath,casepath)
        if(not os.path.isdir(path)):
            os.makedirs(path)
        print '-'*10,rootpath
        self.file_path_detail = os.path.join(path,casename+'_detail.log')
        self.file_path_tags = os.path.join(path,casename+'_tags.log')
        self.file_path_marks = os.path.join(path,casename+'_marks.log')
        self.file_path_tags_sort = os.path.join(path,casename+'_tags_sort.log')
        self.detail_log = open(self.file_path_detail, 'w+')
        self.tags_log = open(self.file_path_tags, 'w+')
        self.mark_log = open(self.file_path_marks, 'w+')
        
        self.mResponseTagsLog      = {}
        self.mRequestTagsLog       = {}
        self.mClienthandlerTagsLog = {}
        self.allTagsLogs           = {}
if __name__ == '__main__':
    pass