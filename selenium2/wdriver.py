# -*- coding:UTF-8 -*-
import os
from selenium2 import webdriver 
from time import sleep

command = 'adb shell am startservice -a com.iflytek.xiri2.START --es startmode text --es text 打开优酷'
print command.decode("utf-8").encode("gbk")
os.popen(command.decode("utf-8").encode("gbk"))
sleep(2)
content = "adb shell am start -n com.fiberhome.iptv/.FHIptv --es intentMsg " + "\"" + "http://itvmkt.ah163.net/youku/detail.html?video_id=3943" + "\""
print content
os.popen(content)
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
print driver.page_source
