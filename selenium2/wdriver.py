# -*- coding:UTF-8 -*-
import os
from selenium2 import webdriver 
from time import sleep
import linecache
import re
def open_url(url):
    content = "adb shell am start -n com.fiberhome.iptv/.FHIptv --es intentMsg " + "\"" + str(url) + "\""
    print content
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
        
def wirte_youku_file(urlid,content):
    filelocation = "F:\\youku\\" +urlid +".txt"
    print filelocation
    fhandle = open(str(filelocation),'w')
    source = content.encode("utf-8")
    fhandle.write(source)
    fhandle.close()
        
def open_youku():
    command = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 打开优酷'
    print command.decode("utf-8").encode("gbk")
    os.popen(command.decode("utf-8").encode("gbk"))

def open_chrome_driver():
    os.popen("chromedriver.exe --url-base=wd/hub --port=8000 --adb-port=5037")
   

open_chrome_driver()
sleep(1)
open_youku()
sleep(2)
open_url(youku_search("F:\youku.txt",1))
#command = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 打开优酷'
#print command.decode("utf-8").encode("gbk")
#os.popen(command.decode("utf-8").encode("gbk"))

#content = "adb shell am start -n com.fiberhome.iptv/.FHIptv --es intentMsg " + "\"" + "http://itvmkt.ah163.net/youku/detail.html?video_id=3943" + "\""
#print content
#os.popen(content)
sleep(2)
driver = webdriver.Remote("http://127.0.0.1:8000/wd/hub", {"desiredCapabilities":
                                                          {"chromeOptions":
                                                           {"androidPackage":"com.fiberhome.iptv",
                                                            "androidUseRunningApp":True,
                                                            "androidProcess":"com.fiberhome.iptv",
                                                            "androidDeviceSerial":"10.1.171.83:5555"
                                                            }
                                                           }
                                                          }
                          )

driver.switch_to_frame("mainWin")
sleep(2)
wirte_youku_file(read_id(youku_search("F:\youku.txt",1)),driver.page_source)
#print driver.page_source
driver.close()



