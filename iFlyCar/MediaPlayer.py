#-*- coding: UTF-8 -*- 

import time, os
import pygame
import pyttsx
import winsound
from robot.api import logger

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class MediaPlayer(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'
    
    def __init__(self):
        self.engine = pyttsx.init()
        self.set_speech_rate(120)
        self.voicemap = {}
        self.voicedir = PATH('../VoiceData')

    def play_media(self, mfile, wait=True):
        if not os.path.exists(mfile):
            raise RuntimeError("File not found %s" % mfile)
        logger.info("Playing %s" % mfile)
        if os.name == 'nt':
            winsound.PlaySound(mfile, winsound.SND_ALIAS)
        else:
            pygame.mixer.init()
            track = pygame.mixer.music.load(mfile)
            pygame.mixer.music.play()
            if wait:
                self.wait_unitl_play_finished()

    def stop_play(self):
        if os.name != 'nt':
            pygame.mixer.music.stop()
        
    def wait_unitl_play_finished(self):
        if os.name != 'nt':
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            self.stop_play()
        
    def play_text(self, text, name=None):
        logger.info("Text to speech: %s" % text)
        self.engine.say(unicode(text), name)
        self.engine.runAndWait()
        
    def stop_speech(self):
        self.engine.stop()
        
    def get_speech_property(self, name):
        return self.engine.getProperty(name)

    def set_speech_property(self, name, value):
        self.engine.setProperty(name, int(value))
        
    def set_speech_rate(self, rate):
        old = self.get_speech_property('rate')
        self.set_speech_property('rate', rate)
        logger.info('Speech rate set to %s, original: %s' % (rate, old))
        return old
    
    def play_media_with_text(self, text, wait=True):
        mfile = self._get_media_path(text)
        self.play_media(mfile, wait)
    
    def _get_media_path(self, text):
        vp = self._load_voice_map()
        if not vp.has_key(text) or not os.path.exists(os.path.join(self.voicedir, vp[text])):
            raise RuntimeError("Voice Resource for %s Not found in %s" % (text, self.voicedir))
        else:
            return os.path.join(self.voicedir, vp[text])

    def _load_voice_map(self):
        if self.voicemap:
            return self.voicemap
        with open(os.path.join(self.voicedir, 'VoiceMap.txt'), 'rb') as fp:
            lines = fp.readlines()
        for line in lines:
            if line.strip():
                k, v = line.strip().split(',')
                self.voicemap[k.decode('utf-8')] = v.decode('utf-8')
        return self.voicemap

if __name__ == '__main__':
    p = MediaPlayer()
    p.play_media_with_text('加油站'.decode('utf-8'))
    #p.play_text(u'测试', r'C:\Work\TestTech\AutoDriver\BVT/../VoiceData')
    #p.play_media(r'C:\Work\TestTech\Record\onetime.mp3')
    #p.wait_unitl_play_finished()
    
    print('play finished!')