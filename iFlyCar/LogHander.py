#-*- coding:utf-8 -*-

from robot.api import logger
import LogParser
import time
import re
"""

(C) Copyright 2016 wei_cloud@126.com

"""
class iFlyLoglib():
    
    def __init__(self):
        self.log = ''
        self.appiumui = 'gui'
        self.product = 'JH'
        
    def set_appium_type(self, uitype, product='JH'):
        """
        设置Appium的模式，Appium在命令行模式和GUI模式下会输出不同的日志格式，因此需要在连接设备前指定模式
        
        支持模式： GUI   commandline
        支持产品: JH（江淮）    XZD（小终端）
        example:
        |   Set Appium Type | commandline | JH |
        """
        self.appiumui = uitype.lower()
        self.product = product

    def get_device_log(self):
        """
        获取设备日志
        """
        driver = self._current_application()
        log = driver.get_log('logcat')
        self.log = log
        logger.debug(log)
        return log
    
    def clear_device_log(self):
        """
        清空设备日志
        """
        driver = self._current_application()
        driver.get_log('logcat')
        self.log = ''
        
    def log_last_device_log(self, loglevel='INFO'):
        """
        记录最后的操作日志，一般用于测试失败时保留设置日志时使用
        """
        self._log("=====Latest Device Log=====", loglevel.upper())
        self.get_device_log()
        self._log(self.log, loglevel.upper())
        return self.log
        
    def search_device_log(self, keystr):
        """
        按关键字搜索设备日志，返回搜索到的日志列表
        | ARGS:  | keystr:  | search keyword |
        
        example:
        |   Search Device Log | KEY_LOCATION |
        """
        ret = []
        for log in self.log:
            if log['message'].find(keystr) != -1:
                ret.append(log)
        return ret
    
    def get_search_page_number(self):
        pageNumber=0
        results=[]
        for log in self.log:
            if re.findall("mPageTotalNumber",log):
               results.append(log)
            else:
               continue 
        for result in results:
            page=result.split()
            pageNumber=int(page[5])
        return pageNumber
             
    
    def _append_device_log(self):
        """
        """
        driver = self._current_application()
        log = driver.get_log('logcat')
        self.log.extend(log)
        return log
    
    def wait_until_log_contains(self, *keys, **kws):
        """
        等待特定日志出现
        | ARGS:  | keys:  | 搜索关键字列表，可输入多个  |
        |        | kws:   | 可用于指定超时时间，单位ms，例如：timeout=1200 |
        
        example:
        |   Wait Until Log Contains | KEY_LOCATION | timeout=2000
        |   Wait Until Log Contains | OperationManager | sRequst | timeout=2000
        """
        start = time.time()
        timeout = int(kws.get('timeout', 2000))
        log = self.get_device_log()
        
        while not self._is_keys_in_log(keys, log):
            end = time.time()
            if (end-start)*1000 > timeout:
                raise AssertionError(u"Log can not be found with keys %s after %s ms" % (keys, timeout))
            time.sleep(0.2)
            log = self._append_device_log()
        return self.log
    
    def _is_keys_in_log(self, keys, loglist):
        for log in loglist:
            for key in keys:
                key_in_log = True
                if key not in log['message']:
                    key_in_log = False
                    break
            if key_in_log:
                return log
        return False
    
    def log_should_contains(self, *keys):
        log = self._get_log_buff()
        if not self._is_keys_in_log(keys, log):
            raise AssertionError(u"Log can not be found with keys %s" % keys)
    
    def get_recon_result_from_log(self):
        """
        [mVersion=1.1, mTtsText=, mEngine=16, mConfidence=0, mFocus=music, mContent=这首城市, 
        mJsonResult={"bislocalresult":"1","language":"zh_cn_mandarin","nlocalconfidencescore":"0","operation":"","pk_score":1,"rc":0,"semantic":{"slots":{"intention":"clear","song":"城市","songOrig":"城市"}},"service":"music","text":"这首城市","version":"3.5.0.1190"}
        """
        loglist = getattr(LogParser, '%sLogList' % self.product)(self._get_log_buff(), self.appiumui)
        return loglist.get_recon_result()
        
    def recon_text_should_match(self, text):
        """
        recon_reult_should_be(mContent="这首城市")
        recon_reult_should_be(mFocus="music")
        """
        loglist = getattr(LogParser, '%sLogList' % self.product)(self._get_log_buff(), self.appiumui)
        try:
            recon_text = loglist.get_recon_value()
        except TypeError:
            raise RuntimeError("No recognition log found in log!")
        
        self._bi.should_match(recon_text, text,
                            msg="Recognition text not match, expect:%s, got: %s" % (text, recon_text),
                            values=False)
        
    def get_speech_info_from_log(self, lastonly=True):
        
        """
        """
        loglist = getattr(LogParser, '%sLogList' % self.product)(self._get_log_buff(), self.appiumui)
        return loglist.get_speech_info(lastonly)
    
    def speech_text_should_match(self, text):
        info = self.get_speech_info_from_log()
        if not info:
            raise RuntimeError("No speech found in log!")
        if isinstance(info, list):
            value = info[-1]['voiceText']
        else:
            value = info['voiceText']
        self._bi.should_match(value, text,
                            msg="Speech text not match, expect:%s, got: %s" % (text, value),
                            values=False)
        
    def should_try_again(self):
        info=self.get_speech_info_from_log()
        if not info:
            raise RuntimeError("No speech found in log!")
        
            

    def _get_log_buff(self):
        if self.log:
            return self.log
        return self.get_device_log()