#-*- coding:utf-8 -*-
"""

(C) Copyright 2016 wei_cloud@126.com

"""
import re
import json
from robot.api import logger
from copy import deepcopy

class iFlyLogBaseList(list):
    """
    """
    
    def __init__(self, log, appiumui='gui', parser=None):
        list.__init__(self)
        self.log = log
        self.appiumui = appiumui
        self.parser = parser if parser is not None else iFlyLogBase
        self.index = -1
        self._parse(log)
        self.recon_model = 'RETTON'
        self.speech_model= 'TtsService'
    
    def _parse(self, log):
        i = len(log) - 1
        while i >= 0:
            parsinglog = log[i]
            parsedlog = None
            try:
                parsedlog = self.parser(parsinglog, self.appiumui)
            except AttributeError:
                parsinglog = deepcopy(log[i])
                parsinglog['message'] = log[i-1]['message'] + log[i]['message']
                i -= 1
                try:
                    parsedlog = self.parser(parsinglog, self.appiumui)
                except AttributeError:
                    logger.debug(u'Log can not be parsed: %s' % parsinglog['message'])
                    i -= 1
                    continue
            if parsedlog:
                self.insert(0, parsedlog)
            i -= 1
            
    def get_recon_result(self):
        for i in range(len(self), 0, -1):
            log = self[i-1]
            if log.model == self.recon_model:
                reconResult = self.parser.recon_parser(log.content)
                if reconResult:
                    return reconResult
                
    def get_speech_info(self, lastonly=True):
        speechlist = []
        for i in range(len(self), 0, -1):
            log = self[i-1]
            if log.model == self.speech_model:
                speechinfo = self.parser.speech_parser(log.content)
                if speechinfo:
                    if lastonly:
                        logger.info(speechinfo)
                        return speechinfo
                    speechlist.insert(0, speechinfo)
        logger.info(speechlist)
        return speechlist

class iFlyLogBase(object):
    """
    01-03 10:33:22.150  2676 32647 I RETTON  : Thread:55|onSrMsgProc|----------------S R:RecognizerResult [mVersion=1.1, mTtsText=, mEngine=16, mConfidence=0, mFocus=music, mContent=\u8fd9\u9996\u57ce\u5e02, mJsonResult={"bislocalresult":"1","language":"zh_cn_mandarin","nlocalconfidencescore":"0","operation":"","pk_score":1,"rc":0,"semantic":{"slots":{"intention":"clear","song":"\u57ce\u5e02","songOrig":"\u57ce\u5e02"}},"service":"music","text":"\u8fd9\u9996\u57ce\u5e02","version":"3.5.0.1190"}
    """
    def __init__(self, log, appiumui='gui', parser=None):
        self.log = log['message']
        self.appiumui = appiumui
        self.parser = parser
        self._parse(self.log)
        self.timestamp = log['timestamp']
    
    def _parse(self, log):
        if self.appiumui == 'gui':
            re_loghead = re.compile(r'''(?P<level>\w)/
                                         ((?P<model>[\w/\.\-\+\:\$\[\]]+?))\s*\(\s*(?P<thread>\d+)\)\:\s*
                                         (?P<content>.*$)
                                         ''', re.X)
        else:
            re_loghead = re.compile(r'''[\d\-]+\s+[\d\:\.]+\s+\d+\s+\d+\s+
                                        (?P<level>\w)\s+
                                         ((?P<model>[\w/\.\-\+\:\$\[\]]+?))\s*\:\s*
                                         (?P<content>.*$)
                                         ''', re.X)
        ret = re_loghead.match(log).groupdict()
        self.level, self.model, self.content = ret['level'], ret['model'], ret['content']
        if self.parser:
            self.update(self.parser(self.content))
            
    def update(self, dict):
        for k, v in dict.items():
            self.__setattr__(k, v)
            
    def __str__(self):
        return self.log.encode('utf-8')
    
    def __unicode__(self):
        return self.__str__()

class JHLog(iFlyLogBase):
    
    @staticmethod
    def recon_parser(content):
        """
        Thread:55|onSrMsgProc|----------------S R:RecognizerResult [mVersion=1.1, mTtsText=, mEngine=16, mConfidence=0, mFocus=music, mContent=这首城市, mJsonResult={"bislocalresult":"1","language":"zh_cn_mandarin","nlocalconfidencescore":"0","operation":"","pk_score":1,"rc":0,"semantic":{"slots":{"intention":"clear","song":"城市","songOrig":"城市"}},"service":"music","text":"这首城市","version":"3.5.0.1190"}
        RecognizerResult [mVersion=1.1, mTtsText=, mEngine=16, mConfidence=0, mFocus=music, mContent=这首城市, 
        mJsonResult={"bislocalresult":"1","language":"zh_cn_mandarin","nlocalconfidencescore":"0","operation":"","pk_score":1,"rc":0,"semantic":{"slots":{"intention":"clear","song":"城市","songOrig":"城市"}},"service":"music","text":"这首城市","version":"3.5.0.1190"}
        """
        result = {}
        re_recon = re.compile(r'''RecognizerResult\s+\[(?P<result>.*$)\]*''', re.X)
        m = re_recon.search(content)
        if not m:
            return result
        retstr = m.groupdict()['result']
        attrs = retstr.split(', ')
        for attr in attrs:
            k, v = attr.split('=')
            if k == 'mJsonResult':
                result[k] = json.loads(v)
            else:
                result[k] = v
        return result
    
    @staticmethod
    def speech_parser(content):
        """
        D/TtsUtil ( 2676): Thread:36|d|start speak 没有听懂您说话，我可以帮您打电话、找音乐或者打开电台。
        D/getprop ( 2676): Thread:36|d|persist.sys.autofly.speaker 9
        D/TtsService( 2778): Thread:60|startSpeak|start Speak com.iflytek.autofly.voicecore.aidl.VoiceServiceId@41a088d0 : [m9]没有听懂您说话，我可以帮您打电话、找音乐或者打开电台。
        """
        result = {}
        re_speech = re.compile(r'''startSpeak\|start\s+Speak\s+(?P<serviceName>[\w\.]+?)
                                \@(?P<serviceId>\w+?)\s*\:\s*
                                (?P<voiceType>(\[\w+?\]\s*)+)\s*
                                (?P<voiceText>.*$)''', re.X)
        m = re_speech.search(content)
        if not m:
            return result
        return m.groupdict()

class JHLogList(iFlyLogBaseList):
    
    def __init__(self, log, appiumui='gui', parser=JHLog):
        iFlyLogBaseList.__init__(self, log, appiumui, parser)
        self.recon_model = 'RETTON'
        self.speech_model = 'TtsService'
    
    def get_recon_value(self):
        return self.get_recon_result()['mContent']

class XZDLog(iFlyLogBase):
    
    @staticmethod
    def recon_parser(content):
        """
        -----RecognizeFilter#convertToObject:{"nlp_score":0.51172000169754,"normal_text":"打开导航",
        "operation":"LAUNCH",
        "pk_fea":{"gram_type":"GENERAL","last_service":"","used_hist_depth":0},
        "pkscore":0.79720818148118,"rc":0,"score":1,"semantic":{"slots":{"name":"导航"}},
        "service":"app","serviceType":"nlu","text":"打开导航。",
        "uuid":"dda21a3c4d0a98b71168f5dbc4091a96query","wstext":"打开/VI//  导航/VI//  。/W_WJ//"}
        """    
        result = {}
        re_recon = re.compile(r'''RecognizeFilter\#convertToObject\:(?P<result>\{.*\})''', re.X)
        m = re_recon.search(content)
        if not m:
            return result
        retstr = m.groupdict()['result']
        return json.loads(retstr)

    @staticmethod
    def speech_parser(content):
        """
        D TtsSession_0: start Speak IFLYTEK_TTS_1451609200406 : 可能网络不太好，请稍后再试试吧
        """
        result = {}
        re_speech = re.compile(r'''start\s+Speak\s+(?P<ttsid>\w+?)\s*\:\s*
                                (?P<voiceText>.*$)''', re.X)
        m = re_speech.search(content)
        if not m:
            return result
        return m.groupdict()
    
class XZDLogList(iFlyLogBaseList):
    
    def __init__(self, log, appiumui='gui', parser=XZDLog):
        iFlyLogBaseList.__init__(self, log, appiumui, parser)
        self.recon_model = 'RETTON'
        self.speech_model = 'TtsSession_0'
    
    def get_recon_value(self):
        return self.get_recon_result()['normal_text']
    
    def get_speech_info(self, lastonly=True):
        speechlist = []
        for i in range(len(self), 0, -1):
            log = self[i-1]
            if log.model == self.speech_model:
                speechinfo = self.parser.speech_parser(log.content)
                if speechinfo and speechinfo['voiceText'].strip():
                    if lastonly:
                        logger.info(speechinfo)
                        return speechinfo
                    speechlist.insert(0, speechinfo)
        logger.info(speechlist)
        return speechlist

class MIALog(iFlyLogBase):
    
    @staticmethod
    def recon_parser(content):
        """
        D/SrSolution( 2791): ++++++++=========
        {"sid":"cid6f190c1f@ch00b80c8081500101c4","text":"播放音乐",
        "answer":{"text":"听下张靓颖的陪你走到底吧"},
        "state":{"bg::musicX::default::playing":{"state":"playing"},"bg::weather::default::default":{"state":"default"},"bg::radio::default::paused":{"state":"paused"},"fg::cmd::default::default":{"state":"default"}},
        "score":1,"data":{}
        """    
        result = {}
        if not content.startswith('++++++++========='):
            return result
        re_recon = re.compile(r'''\"sid\"\:\"(?P<sid>.*?)\"\,\"text\"\:\"(?P<text>.*?)\"\,\"answer\"\:(?P<answer>\{.*?\})\,''', re.X)
        m = re_recon.search(content)
        if not m:
            return result
        return m.groupdict()

    @staticmethod
    def speech_parser(content):
        """
        D TtsSession_0: start Speak IFLYTEK_TTS_1451609200406 : 可能网络不太好，请稍后再试试吧
        """
        #TODO
        raise RuntimeError("Not Implemented Yet!")
        result = {}
        re_speech = re.compile(r'''start\s+Speak\s+(?P<ttsid>\w+?)\s*\:\s*
                                (?P<voiceText>.*$)''', re.X)
        m = re_speech.search(content)
        if not m:
            return result
        return m.groupdict()
    
class MIALogList(iFlyLogBaseList):
    
    def __init__(self, log, appiumui='gui', parser=MIALog):
        iFlyLogBaseList.__init__(self, log, appiumui, parser)
        self.recon_model = 'SrSolution'
        #TODO
        self.speech_model = 'TtsSession_0'
    
    def get_recon_value(self):
        return self.get_recon_result()['text']
    
    def get_speech_info(self, lastonly=True):
        #TODO
        raise RuntimeError("Not Implemented Yet!")
        speechlist = []
        for i in range(len(self), 0, -1):
            log = self[i-1]
            if log.model == self.speech_model:
                speechinfo = self.parser.speech_parser(log.content)
                if speechinfo and speechinfo['voiceText'].strip():
                    if lastonly:
                        logger.info(speechinfo)
                        return speechinfo
                    speechlist.insert(0, speechinfo)
        logger.info(speechlist)
        return speechlist
    
class AIUILog(iFlyLogBase):
    
    @staticmethod
    def recon_parser(content):
        """
        D/SrSolution( 2803): ++++++++=========
        {"sid":"cid6f1c78d6@ch00270c9198d3010292","text":"播放音乐",
        "state":{"bg::mapU::poiSearch::moreTarget":{"state":"moreTarget"},"bg::mapU::navi::navigation":{"state":"navigation"},"bg::musicX::default::paused":{"state":"paused"},"fg::cmd::default::default":{"state":"default"},"bg::weather::default::default":{"state":"default"}},
        "score":1,"semantic":{"slots":{"viewCmd":"音乐","operation":"VIEWCMD"}},
        "debug":{"version":{"agent":"1.2.1019"}},
        "cid":"cid6f1c78d6@ch00270c91525d000000","operation":"VIEWCMD","engine_time":2.04,
        "service":"cmd","orig_semantic":{"slots":null},"uuid":"atn00205d13@un0a440c9198d56f2601",
        "array_index":0}
        """    
        result = {}
        re_recon = re.compile(r'''++++++++=========\{(?P<result>.*)\}''', re.X)
        m = re_recon.search(content)
        if not m:
            return result
        return json.loads(m.groupdict()['result'])

    @staticmethod
    def speech_parser(content):
        """
        D/TtsService( 2803): start Speak com.iflytek.autofly.voicecore.aidl.VoiceServiceId@41b701b8 : [m65180]已切换到随机播放模式
        """
        result = {}
        re_speech = re.compile(r'''start\s+Speak\s+(?P<serviceName>[\w\.]+?)
                                \@(?P<serviceId>\w+?)\s*\:\s*
                                (?P<voiceType>(\[\w+?\]\s*)+)\s*
                                (?P<voiceText>.*$)''', re.X)
        m = re_speech.search(content)
        if not m:
            return result
        return m.groupdict()
    
class AIUILogList(iFlyLogBaseList):
    
    def __init__(self, log, appiumui='gui', parser=AIUILog):
        iFlyLogBaseList.__init__(self, log, appiumui, parser)
        self.recon_model = 'SrSolution'
        self.speech_model = 'TtsService'
    
    def get_recon_value(self):
        return self.get_recon_result()['text']
    
    def get_speech_info(self, lastonly=True):
        speechlist = []
        for i in range(len(self), 0, -1):
            log = self[i-1]
            if log.model == self.speech_model:
                speechinfo = self.parser.speech_parser(log.content)
                if speechinfo and speechinfo['voiceText'].strip():
                    if lastonly:
                        logger.info(speechinfo)
                        return speechinfo
                    speechlist.insert(0, speechinfo)
        logger.info(speechlist)
        return speechlist

if __name__ == '__main__':
    lines = [{u'timestamp': 1494300414595L, u'message': u'01-03 10:33:22.090  2131  2131 D AudioTrack: Timothy->createTrack_l() is called, 3, 44100, 1, 4233, 0, 0', u'level': u'ALL'}, {u'timestamp': 1494300414595L, u'message': u'01-03 10:33:22.090  2131  2131 V AudioSystem: getLatency() streamType 3, output 2, latency 80', u'level': u'ALL'}, {u'timestamp': 1494300414595L, u'message': u'01-03 10:33:22.090  2131  2131 V AudioSystem: getFrameCount() streamType 3, output 2, frameCount 1152', u'level': u'ALL'}, {u'timestamp': 1494300414595L, u'message': u'01-03 10:33:22.090  2131  2131 V AudioSystem: getOutputSamplingRate() reading from output desc', u'level': u'ALL'}, {u'timestamp': 1494300414595L, u'message': u'01-03 10:33:22.090  2131  2131 V AudioSystem: getSamplingRate() streamType 3, output 2, sampling rate 48000', u'level': u'ALL'}, {u'timestamp': 1494300414595L, u'message': u'01-03 10:33:22.090  2131  2131 V AudioTrack: createTrack_l() output 2 afLatency 80', u'level': u'ALL'}, {u'timestamp': 1494300414595L, u'message': u'01-03 10:33:22.090  2131  2131 V AudioTrack: afFrameCount=1152, minBufCount=3, afSampleRate=48000, afLatency=80', u'level': u'ALL'}, {u'timestamp': 1494300414600L, u'message': u'01-03 10:33:22.090  2131  2131 V AudioTrack: minFrameCount: 3175, afFrameCount=1152, minBufCount=3, sampleRate=44100, afSampleRate=48000, afLatency=80', u'level': u'ALL'}, {u'timestamp': 1494300414600L, u'message': u'01-03 10:33:22.090  2131  2131 W AudioPolicyManagerBase: getOutput() device 2, stream 3, samplingRate 0, format 0, channelMask 3, flags 0', u'level': u'ALL'}, {u'timestamp': 1494300414600L, u'message': u'01-03 10:33:22.090  2131  2131 V AudioSystem: getOutputSamplingRate() reading from output desc', u'level': u'ALL'}, {u'timestamp': 1494300414600L, u'message': u'01-03 10:33:22.090  2131  2131 V AudioSystem: getSamplingRate() streamType 3, output 2, sampling rate 48000', u'level': u'ALL'}, {u'timestamp': 1494300414600L, u'message': u'01-03 10:33:22.090  2131  2131 D AudioSink: start', u'level': u'ALL'}, {u'timestamp': 1494300414600L, u'message': u'01-03 10:33:22.090  2131  6527 V AudioTrack: obtainBuffer(1411) returned 4233 = 1411 + 2822 err 0', u'level': u'ALL'}, {u'timestamp': 1494300414601L, u'message': u'01-03 10:33:22.100  2676  3436 I SPEECH_SoundManager: Thread:38|i|playSound ok', u'level': u'ALL'}, {u'timestamp': 1494300414607L, u'message': u'01-03 10:33:22.100  2131  6527 E AudioSink: received unknown event type: 1 inside CallbackWrapper !', u'level': u'ALL'}, {u'timestamp': 1494300414609L, u'message': u'01-03 10:33:22.100  2131  6527 V AudioTrack: obtainBuffer(1411) returned 2822 = 1411 + 1411 err 0', u'level': u'ALL'}, {u'timestamp': 1494300414616L, u'message': u'01-03 10:33:22.110  2131  6527 V AudioTrack: obtainBuffer(1411) returned 1411 = 1411 + 0 err 0', u'level': u'ALL'}, {u'timestamp': 1494300414628L, u'message': u'01-03 10:33:22.120  2676 32647 D SrAdaptListener: Thread:55|d|ISS_SR_MSG_Result(20009):', u'level': u'ALL'}, {u'timestamp': 1494300414628L, u'message': u'01-03 10:33:22.120  2676 32647 D SrAdaptListener: {"bislocalresult":"1","language":"zh_cn_mandarin","nlocalconfidencescore":"0","operation":"","pk_score":1,"rc":0,"semantic":{"slots":{"intention":"clear","song":"\u57ce\u5e02","songOrig":"\u57ce\u5e02"}},"service":"music","text":"\u8fd9\u9996\u57ce\u5e02","version":"3.5.0.1190"}', u'level': u'ALL'}, {u'timestamp': 1494300414628L, u'message': u'01-03 10:33:22.120  2676 32647 D SrAdaptListener: Thread:55|d|sr cost time: 2697', u'level': u'ALL'}, {u'timestamp': 1494300414628L, u'message': u'01-03 10:33:22.120  2676 32647 D SrAdaptListener: Thread:55|d|Process local result:', u'level': u'ALL'}, {u'timestamp': 1494300414628L, u'message': u'01-03 10:33:22.120  2676 32647 D SrAdaptListener: {"bislocalresult":"1","language":"zh_cn_mandarin","nlocalconfidencescore":"0","operation":"","pk_score":1,"rc":0,"semantic":{"slots":{"intention":"clear","song":"\u57ce\u5e02","songOrig":"\u57ce\u5e02"}},"service":"music","text":"\u8fd9\u9996\u57ce\u5e02","version":"3.5.0.1190"}', u'level': u'ALL'}, {u'timestamp': 1494300414633L, u'message': u'01-03 10:33:22.120  2676 32647 D ViaFly_ResultsAnalyser: Thread:55|d|getMscResults result  {"bislocalresult":"1","language":"zh_cn_mandarin","nlocalconfidencescore":"0","operation":"","pk_score":1,"rc":0,"semantic":{"slots":{"intention":"clear","song":"\u57ce\u5e02","songOrig":"\u57ce\u5e02"}},"service":"music","text":"\u8fd9\u9996\u57ce\u5e02","version":"3.5.0.1190"}', u'level': u'ALL'}, {u'timestamp': 1494300414636L, u'message': u'01-03 10:33:22.130  2131  6527 V AudioTrack: obtainBuffer(1411) returned 2116 = 1411 + 705 err 0', u'level': u'ALL'}, {u'timestamp': 1494300414641L, u'message': u'01-03 10:33:22.130  2131  6527 V AudioTrack: obtainBuffer(1411) returned 705 = 705 + 0 err 0', u'level': u'ALL'}, {u'timestamp': 1494300414654L, u'message': u'01-03 10:33:22.150  2676 32647 I RETTON  : Thread:55|onSrMsgProc|----------------S R:RecognizerResult [mVersion=1.1, mTtsText=, mEngine=16, mConfidence=0, mFocus=music, mContent=\u8fd9\u9996\u57ce\u5e02, mJsonResult={"bislocalresult":"1","language":"zh_cn_mandarin","nlocalconfidencescore":"0","operation":"","pk_score":1,"rc":0,"semantic":{"slots":{"intention":"clear","song":"\u57ce\u5e02","songOrig":"\u57ce\u5e02"}},"service":"music","text":"\u8fd9\u9996\u57ce\u5e02","version":"3.5.0.1190"}', u'level': u'ALL'}, {u'timestamp': 1494300414654L, u'message': u'01-03 10:33:22.150  2676 32647 I RETTON  : , mEntryMode=0, mEntryType=0, mPromptMode=0, mIsLocalResult=1]', u'level': u'ALL'}, {u'timestamp': 1494300414654L, u'message': u'01-03 10:33:22.150  2131  6527 V AudioTrack: obtainBuffer(1411) returned 705 = 705 + 0 err 0', u'level': u'ALL'}, {u'timestamp': 1494300414655L, u'message': u'01-03 10:33:22.150  2131  6527 V AudioTrack: obtainBuffer(706) returned 0 = 0 + 0 err -11', u'level': u'ALL'}, {u'timestamp': 1494300414662L, u'message': u'01-03 10:33:22.150  2676 32647 D BusinessProcessor: Thread:55|d|onResults', u'level': u'ALL'}, {u'timestamp': 1494300414662L, u'message': u'01-03 10:33:22.150  2676  3434 D MessageEntity: Thread:36|d|handlerMessage, tag = IRecognitionListener', u'level': u'ALL'}, {u'timestamp': 1494300414662L, u'message': u'01-03 10:33:22.150  2676  3434 D BusinessProcessor: Thread:36|d|ON_RESULT_MSG 182002165', u'level': u'ALL'}, {u'timestamp': 1494300414662L, u'message': u'01-03 10:33:22.150  2676  3434 D BusinessProcessor: Thread:36|d|sr time 461', u'level': u'ALL'}, {u'timestamp': 1494300414662L, u'message': u'01-03 10:33:22.150  2676  3434 D SpeechWaitingResultState: Thread:36|d|onResult', u'level': u'ALL'}, {u'timestamp': 1494300414662L, u'message': u'01-03 10:33:22.160  2676  3434 D BusinessProcessor: Thread:36|d|current speech state: SpeechWaitingResultState', u'level': u'ALL'}, {u'timestamp': 1494300414662L, u'message': u'01-03 10:33:22.160  2676  3434 D BusinessProcessor: Thread:36|d|set current state: SpeechWaitingResultState=========>>SpeechResultHandleState', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2676  3434 D SpeechWaitingResultState: Thread:36|d|clear 182002167', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2676  3434 D SPEECH_SoundManager: Thread:36|d|stopWaitSound', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2676  3436 D SPEECH_SoundManager: Thread:38|d|WaitTimer cancel', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2676  3436 D MessageEntity: Thread:38|d|SPEECH_SoundManager message is not exist !', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2676  3436 D MessageEntity: Thread:38|d|SPEECH_SoundManager message is not exist !', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2676  3436 D MessageEntity: Thread:38|d|SPEECH_SoundManager message is not exist !', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2131  6527 V AudioTrack: obtainBuffer(706) returned 0 = 0 + 0 err -4', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2676  3434 D SPEECH_SoundManager: Thread:36|d|stopWaitSound end', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2676  3434 D MessageEntity: Thread:36|d|on_response_time_up message remove ok !', u'level': u'ALL'}, {u'timestamp': 1494300414663L, u'message': u'01-03 10:33:22.160  2676  3436 D SPEECH_SoundManager: Thread:38|d|MediaPlayer stop', u'level': u'ALL'}, {u'timestamp': 1494300414668L, u'message': u'01-03 10:33:22.160  2676  3436 D SPEECH_SoundManager: Thread:38|d|MediaPlayer is not playing', u'level': u'ALL'}, {u'timestamp': 1494300414696L, u'message': u'01-03 10:33:22.190  2676  2683 D dalvikvm: GC_CONCURRENT freed 1069K, 23% free 4025K/5212K, paused 2ms+10ms, total 164ms', u'level': u'ALL'}, {u'timestamp': 1494300414696L, u'message': u'01-03 10:33:22.190  2676  3434 D dalvikvm: WAIT_FOR_CONCURRENT_GC blocked 30ms', u'level': u'ALL'}, {u'timestamp': 1494300414696L, u'message': u'01-03 10:33:22.190  2676  3434 D MessageEntity: Thread:36|d|on_response_time_up message is not exist !', u'level': u'ALL'}, {u'timestamp': 1494300414696L, u'message': u'01-03 10:33:22.190  2676  3434 D MessageEntity: Thread:36|d|on_response_time_up message is not exist !', u'level': u'ALL'}, {u'timestamp': 1494300414696L, u'message': u'01-03 10:33:22.190  2676  3434 D SpeechResultHandleState: Thread:36|d|handleResult 95610486', u'level': u'ALL'}, {u'timestamp': 1494300414696L, u'message': u'01-03 10:33:22.190  2676  3434 D SpeechResultHandleState: Thread:36|d|start update view', u'level': u'ALL'}, {u'timestamp': 1494300414696L, u'message': u'01-03 10:33:22.190  2676 32647 D dalvikvm: WAIT_FOR_CONCURRENT_GC blocked 29ms', u'level': u'ALL'}, {u'timestamp': 1494300414699L, u'message': u'01-03 10:33:22.190  2676  2676 D MessageEntity: Thread:1|d|handlerMessage, tag = SpeechResultHandleState', u'level': u'ALL'}, {u'timestamp': 1494300414701L, u'message': u'01-03 10:33:22.190  2676 32647 D Dispatch: Thread:55|d|delay 0ms ,IRecognitionListener, true', u'level': u'ALL'}, {u'timestamp': 1494300414721L, u'message': u'01-03 10:33:22.200  2676  3434 D SpeechResultHandleState: Thread:36|d|playTone', u'level': u'ALL'}, {u'timestamp': 1494300414722L, u'message': u'01-03 10:33:22.200  2676  3436 I SPEECH_SoundManager: Thread:38|i|playSound start type = 3', u'level': u'ALL'}, {u'timestamp': 1494300414722L, u'message': u'01-03 10:33:22.200  2676  3436 D SPEECH_SoundManager: Thread:38|d|get sound resource start', u'level': u'ALL'}, {u'timestamp': 1494300414722L, u'message': u'01-03 10:33:22.200  2676  3436 D SPEECH_SoundManager: Thread:38|d|setDataSource(fd) start', u'level': u'ALL'}, {u'timestamp': 1494300414722L, u'message': u'01-03 10:33:22.200  2676  3434 D getprop : Thread:36|d|persist.sys.autofly.srecho true', u'level': u'ALL'}, {u'timestamp': 1494300414722L, u'message': u'01-03 10:33:22.200  2778  2975 D SksSolution: Thread:60|getCurrentSkServiceId|current session is null', u'level': u'ALL'}, {u'timestamp': 1494300414722L, u'message': u'01-03 10:33:22.200  2676  3436 D TimothyMediaUtils: isSourceNav() is called', u'level': u'ALL'}, {u'timestamp': 1494300414722L, u'message': u'01-03 10:33:22.200  2676  3436 D TimothyMediaUtils: isSourceNav() mCmdlineFile:/proc/2676/cmdline', u'level': u'ALL'}, {u'timestamp': 1494300414722L, u'message': u'01-03 10:33:22.210  2676  3436 D TimothyMediaUtils: isSourceNav() Name:com.iflytek.autofly.speechclient\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd', u'level': u'ALL'}]
    loglist = iFlyLogBaseList(lines, appiumui='commandline')
    for l in loglist:
        print l.level, l.model, l
    content = '''    Thread:55|onSrMsgProc|----------------S R:RecognizerResult [mVersion=1.1, mTtsText=, mEngine=16, mConfidence=0, mFocus=music, mContent=这首城市, mJsonResult={"bislocalresult":"1","language":"zh_cn_mandarin","nlocalconfidencescore":"0","operation":"","pk_score":1,"rc":0,"semantic":{"slots":{"intention":"clear","song":"城市","songOrig":"城市"}},"service":"music","text":"这首城市","version":"3.5.0.1190"}'''
    ret = recon_parser(content)
    for k, v in ret.items():
        print k,'=', str(v)
    content = """    D/TtsService( 2778): Thread:60|startSpeak|start Speak com.iflytek.autofly.voicecore.aidl.VoiceServiceId@41a088d0 : [m9]没有听懂您说话，我可以帮您打电话、找音乐或者打开电台。"""
    ret = speech_parser(content)
    for k, v in ret.items():
        print k,'=', str(v)