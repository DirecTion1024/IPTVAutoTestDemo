#-*- coding: UTF-8 -*- 

from AppiumLib import AppiumLib
from robot.api import logger
from LogHander import iFlyLoglib
from ImageLib import ImageLib

class IflyAppiumLib(AppiumLib, iFlyLoglib, ImageLib):
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'
    
    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot'):
        AppiumLib.__init__(self, timeout, run_on_failure)
        iFlyLoglib.__init__(self)
        ImageLib.__init__(self)
        
