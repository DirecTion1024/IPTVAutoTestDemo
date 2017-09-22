# -*- coding:UTF-8 -*-
import os
from selenium2 import webdriver 
from time import sleep
import linecache
import re
import subprocess


def open_url(url):
    content = "adb shell am start -n com.fiberhome.iptv/.FHIptv --es intentMsg " + "\"" + str(url) + "\""
    os.system(content)
        
def youku_search(filepath,linenum):
    print filepath
    print linenum
    content = linecache.getline(str(filepath),int(linenum))
    #command = content.decode("utf-8").encode("gbk")
    print content
    return content   
        
def read_id(content):
    m = re.search(r'[^=]+$', content)
    if m:
        id = m.group(0)
        return id[0:-1]
    else:
        return 'not search'
        
def wirte_youku_file(urlid,content,filepath):
    filelocation = filepath +urlid +".txt"
    fhandle = open(str(filelocation),'w')
    source = content.encode("utf-8")
    fhandle.write(source)
    fhandle.close()
        
def open_youku():
    command = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 打开优酷'
    os.popen(command.decode("utf-8").encode("gbk"))

def open_chrome_driver():
    subprocess.Popen("chromedriver.exe --url-base=wd/hub --port=8000 --adb-port=5037")    

def shutdown_chrome_driver():
    os.popen("TASKKILL /F /IM chromedriver.exe /T")       

def line_number(filelocation):
    fobj = open(filelocation,'r')        
    row_len = len(fobj.readlines())
    return row_len

looptime = line_number("f:\youku.txt")
print looptime
open_youku()
print("open youku SUCCESS")
sleep(2)
for i in range(1,looptime+1):
    print("开始第" +str(i) +"次爬取")
    open_chrome_driver()
    print("start chrome_driver SUCCESS")
    sleep(1)
#command = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 打开优酷'
#print command.decode("utf-8").encode("gbk")
#os.popen(command.decode("utf-8").encode("gbk"))
    open_url(youku_search("F:\youku.txt",i))
#content = "adb shell am start -n com.fiberhome.iptv/.FHIptv --es intentMsg " + "\"" + "http://itvmkt.ah163.net/youku/detail.html?video_id=3943" + "\""
#print content
#os.popen(content)
    print("openurl:"+youku_search("F:\youku.txt",i))
    sleep(2)
    driver = webdriver.Remote("http://127.0.0.1:8000/wd/hub", {"desiredCapabilities":
                                                          {"chromeOptions":
                                                           {"androidPackage":"com.fiberhome.iptv",
                                                            "androidUseRunningApp":True,
                                                            "androidProcess":"com.fiberhome.iptv",
                                                            "androidDeviceSerial":"10.1.171.26:5555"
                                                            }
                                                           }
                                                          }
                          )
    print("get driver SUCCESS")
    driver.switch_to_frame("mainWin")
#print driver.page_source
    print("swtich frame SUCCESS")
    sleep(2)
    wirte_youku_file(read_id(youku_search("F:\youku.txt",i)),driver.page_source,"F:\\youku\\")
    print("wirte file SUCCESS")
    print("file content is:"+driver.page_source)
    shutdown_chrome_driver()
    print("shutdown chrome_driver SUCCESS")
    print("第" +str(i) +"次爬取结束")
print("全部爬取结束")
print("共爬取页面："+str(looptime))




