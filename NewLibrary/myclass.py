#-*- coding:UTF-8 -*-
import os
import linecache
from time import sleep
from AppiumLibrary import AppiumLibrary
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
    
    def rc_ok(self):
        os.popen('adb shell input keyevent 23')	
     
        
    def searchContent(self,filelocation):
        #search = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text '+content
        #print search
        #os.popen('adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 周星驰的电影')
        fhandle = open(filelocation)
        os.popen(fhandle.read())
    
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
    
    def wirte_file(self,filelocation,content):
        fhandle = open(filelocation,'w')
        fhandle.write(str)
    
    def read_wirte(self,filelocation): 
        readhandle = open(filelocation)
        content = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text '+readhandle.read()
        print content
        readhandle.close()
        wirtehandle = open(filelocation,'w')
        wirtehandle.write(content)
    
    
    def get_page(self,content):
        page = content[1]
        return page
    
    def callCommand(self):
    #执行命令并返回该命令的输出，支持中文命令
        command = u"adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 周星驰的电影"
        print command
        return os.popen(command.decode('utf-8').encode('gbk')).readlines()  
        
    def wait_and_screenshot(self, filename=None):
        """
        等待页面元素显示后截屏
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐X |
        |        | timeout:  | 等待时间， 默认10s，单位s |
        |        | filename: |  保持的文件名称 |

        example:
        |   Wait and Screenshot | xpath=//android.widget.EditText |
        |   Wait and Screenshot | xpath=//android.widget.EditText | filename=${CURDIR}/ScreenShot/Homepage.png |
        """
        self.capture_page_screenshot(filename)   
    
    def read_by_line(self):
        for i in range(0,3):
            readhandle = open('f:\search.txt')
            content =  'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text '+readhandle.readlines()[i]
            print content
            readhandle.close()
            wirtehandle = open('f:\search.txt','a')
            wirtehandle.seek(i)
            wirtehandle.write(content)
            readhandle.close()
            
        
        #print fobj.readlines()
        #f = open('f:\search.txt')
        #for i in f.readlines()[line]:
           # print i
    def read_line_content(self):
        #readhandle = open('f:\search.txt')
        print (linecache.getline(r'f:\search.txt',1))
     
    def sx_autotest(self):
        for i in range (1,4):
            print linecache.getline(r'f:\search.txt',i)
            os.popen(linecache.getline(r'f:\search.txt',i))
            sleep(2)
            os.popen('adb shell input keyevent 23')
            sleep(2)
            
    def sx_python_test(self):
        for i in range (1,4):
            content = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text '+linecache.getline('f:\search.txt',i)
            os.popen(content)
            sleep(2)
            os.popen('adb shell input keyevent 23')
            sleep(1)
            pagenumber = 'screenshot'+str(i)+'.png'
            os.popen('adb shell screencap -p /sdcard/'+pagenumber)
            sleep(1)
            os.popen('adb pull /sdcard/'+pagenumber+' d:/'+pagenumber)
            
    def sx_search(self,filepath,linenum):
        print filepath
        print linenum
        content = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text '+linecache.getline(str(filepath),int(linenum))
        print content
        os.popen(content) 
               
    def sx_screen_shot(self,picnumber):
        pagenumber = 'screenshot'+str(picnumber)+'.png'
        os.popen('adb shell /system/bin/screencap -p /sdcard/'+pagenumber)
        os.popen('adb pull /sdcard/'+pagenumber+' d:/'+pagenumber)
        
        
        
    def line_number(self,filelocation):
        fobj = open(filelocation,'r')        
        row_len = len(fobj.readlines())
        return row_len
        
        
        
        
        