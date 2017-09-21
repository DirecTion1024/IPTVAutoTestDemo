from selenium import webdriver

# driver = webdriver.Remote("http://127.0.0.1:8000/wd/hub",{"desiredCapabilities":
#                                                                   {"chromeOptions":
#                                                                    {"androidPackage":"com.iflytek.inputmethod",
#                                                                     "androidUseRunningApp":True,
#                                                                     "androidProcess":"com.iflytek.inputmethod.mmp",
#                                                                     "androidDeviceSerial":"a5809d4"}
#                                                                    }
#                                                                   })
driver = webdriver.Remote("http://127.0.0.1:8000/wd/hub",{"desiredCapabilities":
                                                          {"chromeOptions":
                                                           {"androidPackage":"com.fiberhome.iptv",
                                                            "androidUseRunningApp":True,
                                                            "androidProcess":"com.fiberhome.iptv",
                                                            "androidDeviceSerial":"10.1.171.215:5555"
                                                            }
                                                           }
                                                          }
                          )

#driver.switch_to_frame("mainWin")
print driver.page_source
