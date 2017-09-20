#coding=utf-8

import logging
from pprint import pprint 
logging.basicConfig(level=logging.INFO)
from keywordgroup import KeywordGroup
from robot.libraries.BuiltIn import BuiltIn
from serverlib.ImeServerVoiceCloudLib import ImeServerVoiceCloudLib

import urllib2

class _ServerManager(KeywordGroup):
    def __init__(self):
        self.IServer = None
    
    def set_search_candidate_plan(self,plan_id,target):
        """Config Server Env:set search candidate plan

        :Args:
         - id_input:96(顶部悬浮窗)、93（临时悬浮窗）、92（候选栏图标）
         - target：0(close)、1(open)
        """
        username = 'ydhl'
        passwd = 'ydhl'
        plan_id = int(plan_id)
        self.IServer = ImeServerVoiceCloudLib()
        IServer = self.IServer
        IServer.login_ossptest_voicecloud(username, passwd)
        
        request = urllib2.Request("http://ossptest.voicecloud.cn/auth/")
        resp = IServer.opener.open(request)
         
        IServer.login_menu_web(username, passwd)
         
        request = urllib2.Request("http://ossptest.voicecloud.cn/ygxt/keyword/planManage.do")
        resp = IServer.opener.open(request)
        
        IServer.setSearchCandidatePlan(plan_id,int(target))

    def get_search_candidate_plan_by_id(self,plan_id):
        """Config Server Env:set search candidate plan
           Return : Search Candidate Plan in dict
           
        :Args:
         - id_input:96(顶部悬浮窗)、93（临时悬浮窗）、92（候选栏图标）
         - target：0(close)、1(open)
        """
        plan_id = int(plan_id)
        if(self.IServer):
            d = self.IServer.getSearchCandidatePlanById(plan_id)
            if(d):
                return d
        return {}
    
def main():
    osspLog = _ServerManager()
    osspLog.set_search_candidate_plan("96","0")
    osspLog.get_search_candidate_plan_by_id(96)
    
if __name__ == '__main__':
    main()

