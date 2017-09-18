#-*- coding:UTF-8 -*-
import os
import linecache
import shutil
from time import sleep
from AppiumLibrary import AppiumLibrary
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
import subprocess
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, WebDriverException
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

class MyClass(AppiumLibrary):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'

    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot'):
        AppiumLibrary.__init__(self, timeout, run_on_failure)
    
    def switch_window(self):
        self.driver = self._current_application()
        whandles = self.driver.window_handles
        for whandle in whandles:
            logger.info("whandle")
            self.driver.switch_to_window(whandle)
            logger.info(self.driver.title)
            logger.info(self.driver.current_url)
            
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
     
    def rc_home(self):
        os.popen('adb shell input keyevent 3')
        
    def searchContent(self):
        command = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 周星驰的电影'
        print command.decode("utf-8").encode("gbk")
        os.popen(command.decode("utf-8").encode("gbk"))
        
    def open_youku(self):
        command = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 打开优酷'
        print command.decode("utf-8").encode("gbk")
        os.popen(command.decode("utf-8").encode("gbk"))
    
    
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
        fhandle = open("F:\search.txt",'w')
        fhandle.write(content)
    
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
            sleep(1)
            os.popen('adb shell input keyevent 23')
            sleep(1)
            
    def sx_python_test(self):
        for i in range (1,11):
            content = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text '+linecache.getline('f:\search.txt',i)
            os.popen(content)
            sleep(1)
            os.popen('adb shell input keyevent 23')
            sleep(1)
            pagenumber = 'screenshot'+str(i)+'.png'
            os.popen('adb shell screencap -p /sdcard/'+pagenumber)
            os.popen('adb pull /sdcard/'+pagenumber+' d:/'+pagenumber)
            
    def sx_search(self,filepath,linenum):
        print filepath
        print linenum
        content = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text '+linecache.getline(str(filepath),int(linenum))
        #command = content.decode("utf-8").encode("gbk")
        print content
        os.popen(content) 
               
    def sx_screen_shot(self,picnumber):
        pagenumber = 'screenshot'+str(picnumber)+'.png'
        os.popen('adb shell /system/bin/screencap -p /sdcard/'+pagenumber)
        os.popen('adb pull /sdcard/'+pagenumber+' d:/testshot/'+pagenumber)
        
        
    def line_number(self,filelocation):
        fobj = open(filelocation,'r')        
        row_len = len(fobj.readlines())
        return row_len
        
    def open_live(self):
        command = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 我要看直播'
        os.system(command.decode("utf-8").encode("gbk"))   
        
    def judge_content(self):
        content = "测试3"
        text = content.decode("utf-8").encode("gbk")
        AppiumLibrary.page_should_contain_text(self, text)
     
    def send_email(self,receiver_mail,email_content):
        sender = '1021249576@qq.com'  
        receiver = receiver_mail  
        subject = 'python email test'  
        smtpserver = 'smtp.qq.com'  
        username = '1021249576@qq.com'  
        password = 'itgyuoifwkyfbbgi'  
    
        msgRoot = MIMEMultipart('related')  
        msgRoot['Subject'] = email_content  
  
        #构造附件  
        att = MIMEText(open('d:\\testshot\\screenshotliveshot.png', 'rb').read(), 'base64', 'utf-8')  
        att["Content-Type"] = 'application/octet-stream'  
        att["Content-Disposition"] = 'attachment; filename="screenshotliveshot.png"'  
        msgRoot.attach(att)  
          
        smtp = smtplib.SMTP()  
        smtp.connect('smtp.qq.com')  
        smtp.login(username, password)  
        smtp.sendmail(sender, receiver, msgRoot.as_string())  
        smtp.quit()  
     
    def page_source(self):
        print 'in page_source'
        driver = self._current_application()
        page_source = driver.page_source()
        print page_source
        return page_source       
    
    def read_line(self,filepath,linenum):
         return linecache.getline(str(filepath),int(linenum)).decode("utf-8").encode("gbk")
        
    def read_size(self,filepath):
        return os.path.getsize(filepath)
         
    def file_number(self,filepath):
        ls = os.listdir(filepath)
        count = 0
        for i in ls:
            if os.path.isfile(os.path.join(filepath,i)):
                count += 1
        return count   
    
    def move_file(self,srcpath,targetpath):
        shutil.move(srcpath, targetpath)
    
    def switch_to_frame(self):
        self.driver = self._current_application()
        print (dir(self.driver))
        self.driver.switch_to_frame("mainWin")

    def open_url(self,url):
        content = "adb shell am start -n com.fiberhome.iptv/.FHIptv --es intentMsg " + str(url)
        print content
        os.system(content)
        
        
        
        
        