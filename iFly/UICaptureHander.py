#-*- coding:utf-8 -*-

from robot.api import logger
from LogParser import *
from iFly.Keyboard import Keyboard
import time
import os
import datetime
import traceback

from selenium.common.exceptions import WebDriverException

from Report import Report
from iFly.AppiumLib import AppiumLib
"""

(C) Copyright 2016 wei_cloud@126.com

"""


class UICapturelib():

    def __init__(self):
        self.log = ''
        self.keylog = None
        self.appiumui = 'gui'
        self.logcat_buf = ''
        self.om = ['']
        self.orf = ['']
        self.ps = ['']
        self.try_times = 0
        self.search_logcat = ''
        self.filepath = BuiltIn().get_variable_value("${FILEPATH}", '')

    def _parser_config_xml(self):
        # 解析UI校验工具配置文件
        pass
