#-*- coding:UTF-8 -*-

import os
class MyClass(object):
    def __init__(self):
        pass
 
    def printMsg(self,msg):
        print "hello "+msg
    
    def rc_down(self):
        os.popen('adb shell input keyevent 20')
		
    def searchContent(self,content):
        search = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text '+content
        print search
        os.popen('adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text ���ǳ۵ĵ�Ӱ')    
    
    def rc_right(self):
        os.popen('adb shell input keyevent 20')