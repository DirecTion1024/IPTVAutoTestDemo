#-*- coding:UTF-8 -*-
import os
import sys
reload(sys)

class MyClass(object):
    def __init__(self):
        pass
 
    def printMsg(self,msg):
        print "hello "+msg
    
    def rc_down(self):
        os.popen('adb shell input keyevent 20')
    
    def rc_up(self):
        os.popen('adb shell input keyevent 19')
    
    def rc_left(self):
        os.popen('adb shell input keyevent 21')
    
    def rc_right(self):
        os.popen('adb shell input keyevent 22')
    
    def rc_backkey(self):
        os.popen('adb shell input keyevent 4')
    	
    def searchContent(self,content):
        search = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text '+content
        print search
        fhandle = open('f:\search.txt')
        os.system(fhandle.read())   
    
    def make_odd(self,startnum,endnum):
        while startnum <= endnum:
            if startnum % 2 == 1:
                list.append(startnum)
            startnum + 1
        return list
    
    def make_even(self,startnum,endnum):
        while startnum <= endnum:
            if startnum % 2 == 0:
                list.append(startnum)
            startnum + 1
        return list
    
    def read_file(self,filelocation):
        fhandle = open(filelocation)
        print fhandle.read()
    
    
     
    