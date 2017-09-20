#-*- coding: UTF-8 -*- 
"""

(C) Copyright 2016 wei_cloud@126.com

"""
from AppiumLibrary import AppiumLibrary
import os, time, base64
from appium.webdriver.common.touch_action import TouchAction
from robot.api import logger
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime, timedelta
from robot.libraries import BuiltIn

BUILTIN = BuiltIn.BuiltIn()

class AppiumLib(AppiumLibrary):
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'
    
    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot'):
        AppiumLibrary.__init__(self, timeout, run_on_failure)
        self.keyboard = None
        self.keypress_interval = 0.5
        self.log = ''
        
    def open_application(self, remote_url, alias=None, **kwargs):
        """Opens a new application to given Appium server.
        Capabilities of appium server, Android and iOS,
        Please check http://appium.io/slate/en/master/?python#appium-server-capabilities
        | *Option*            | *Man.* | *Description*     |
        | remote_url          | Yes    | Appium server url |
        | alias               | no     | alias             |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=iOS      | platformVersion=7.0            | deviceName='iPhone Simulator'           | app=your.app                         |
        | Open Application | http://localhost:4723/wd/hub | platformName=Android | platformVersion=4.2.2 | deviceName=192.168.56.101:5555 | app=${CURDIR}/demoapp/OrangeDemoApp.apk | appPackage=com.netease.qa.orangedemo | appActivity=MainActivity |
        """
        for k in kwargs.keys():
            if not kwargs[k]:
                kwargs.pop(k)
        AppiumLibrary.open_application(self, remote_url, alias, **kwargs)
        
    def reset_application(self, appPackage=None):
        """ Reset application """
        driver = self._current_application()
        driver.reset(appPackage)
        
    def install_app(self, app_path):
        """Install the application found at `app_path` on the device.

        :Args:
         - app_path - the local or remote path to the application to install
        """
        driver = self._current_application()
        driver.install_app(app_path)
        
    def swipe_up(self, locator=None, duration=1000, wait=1):
        """
        向上滑屏
        | ARGS:  |  duration:  |  滑动持续时间，默认1s，单位ms |
        
        example:
        |   Swipe Up |
        |   Swipe Up | 1000 |
        """
        driver = self._current_application()
        if locator:
            rect = self.get_element_rect(locator)
            offsetx = rect[0]
            offsety = rect[1]
            sizedict = {'width':rect[2]-rect[0], 'height':rect[3]-rect[1]}
        else:
            sizedict = driver.get_window_size()
            offsetx = offsety = 0
        self.swipe(offsetx+sizedict['width']/2, offsety+sizedict['height']*3/4, offsetx+sizedict['width']/2, offsety+sizedict['height']/4, duration)
        if wait:
            time.sleep(float(wait))
    
    def swipe_down(self, locator=None, duration=1000, wait=1):
        """
        向下滑屏
        | ARGS:  | duration:  | 滑动持续时间，默认1s，单位ms |
        """
        driver = self._current_application()
        if locator:
            rect = self.get_element_rect(locator)
            offsetx = rect[0]
            offsety = rect[1]
            sizedict = {'width':rect[2]-rect[0], 'height':rect[3]-rect[1]}
        else:
            sizedict = driver.get_window_size()
            offsetx = offsety = 0
        self.swipe(offsetx+sizedict['width']/2, offsety+sizedict['height']/4, offsetx+sizedict['width']/2, offsety+sizedict['height']*3/4, duration)
        if wait:
            time.sleep(float(wait))
    
    def swipe_left(self, locator=None, duration=1000, wait=1):
        """
        向左滑屏
        | ARGS:  | duration:  | 滑动持续时间，默认1s，单位ms |
        """
        driver = self._current_application()
        if locator:
            rect = self.get_element_rect(locator)
            offsetx = rect[0]
            offsety = rect[1]
            sizedict = {'width':rect[2]-rect[0], 'height':rect[3]-rect[1]}
        else:
            sizedict = driver.get_window_size()
            offsetx = offsety = 0
        self.swipe(offsetx+sizedict['width']*3/4, offsety+sizedict['height']/2, offsetx+sizedict['width']/4, offsety+sizedict['height']/2, duration)
        if wait:
            time.sleep(float(wait))
            
    def swipe_right(self, locator=None, duration=1000, wait=1):
        """
        向右滑屏
        | ARGS:  | duration: |  滑动持续时间，默认1s，单位ms |
        """
        driver = self._current_application()
        if locator:
            rect = self.get_element_rect(locator)
            offsetx = rect[0]
            offsety = rect[1]
            sizedict = {'width':rect[2]-rect[0], 'height':rect[3]-rect[1]}
        else:
            sizedict = driver.get_window_size()
            offsetx = offsety = 0
        self.swipe(offsetx+sizedict['width']/4, offsety+sizedict['height']/2, offsetx+sizedict['width']*3/4, offsety+sizedict['height']/2, duration)
        if wait:
            time.sleep(float(wait))
            
    def swipe_down_to(self, locator, element=None, duration=1000, maxdepth=10):
        """
        向下滑屏到指定的元素
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐XPATH |
        |        | duration: |  滑动持续时间，默认1s，单位ms |
        |        | maxdepth: |  最多滑屏次数，默认10次 |
        
        example:
        |   Swipe Down To locator | xpath=//android.widget.EditText |
        |   Swipe Down To locator | xpath=//android.widget.EditText | 500 | 5 |
        """
        moved = False
        counter = 0
        while not self._is_element_present(locator) and counter < maxdepth:
            self.swipe_down(element, duration)
            counter += 1
            moved = True
            
        if not self._is_element_present(locator):
            raise AssertionError("Could not find element on page '%s' " % locator)
        if moved:
            time.sleep(1)
            self._current_application().page_source
    
    def swipe_up_to(self, locator, element=None, duration=1000, maxdepth=10):
        """
        向上滑屏到指定的元素
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐XPATH |
        |        | duration: |  滑动持续时间，默认1s，单位ms |
        |        | maxdepth: |  最多滑屏次数，默认10次 |
        
        example:
        |   Swipe Up To locator | xpath=//android.widget.EditText |
        """
        moved = False
        counter = 0
        while not self._is_element_present(locator) and counter < maxdepth:
            self.swipe_up(element, duration)
            counter += 1
            moved = True
            
        if not self._is_element_present(locator):
            raise AssertionError("Could not find element on page '%s' " % locator)
        if moved:
            time.sleep(1)
            self._current_application().page_source
    
    def wait_and_tap(self, locator, timeout=10):
        """
        等待元素在页面显示后再点击
        | ARGS:  | locator: |  请参考 Appium元素定位部分，推荐XPATH |
        |        | timeout: |  等待时间， 默认10s，单位s |
        
        example:
        |   Wait and Tap | xpath=//android.widget.EditText |
        |   Wait and Tap | xpath=//android.widget.EditText | 5 |
        """
        self.wait_until_page_contains_element(locator, timeout)
        self.tap(locator)
        
    def tap_and_wait_page_load(self, locator, retry=3, timeout=30):
        """
        点击后等待页面加载，加载失败后进行重试。
        | ARGS:  | locator: |  请参考 Appium元素定位部分，只支持XPATH，或者使用文本定位 |
        |        | retry:   |  重试次数， 默认3次 |
        |        | timeout: |  等待时间， 默认10s，单位s |
        
        example:
        |   Tap And Wait Page Load | xpath=//android.widget.EditText |
        |   Tap And Wait Page Load | 词库 | 5 | 10 |
        """
        if not locator.startswith('xpath='):
            locator = "xpath=//*[@text='%s']" % locator
        self.tap(locator)
        reloadlocator = "xpath=//android.widget.TextView[@text='点击重新加载']"
        for i in range(int(retry)):
            time.sleep(0.5)
            self.wait_until_page_does_not_contain(u'正在加载', timeout)
            if self._is_element_present(reloadlocator):
                self.tap(reloadlocator)
            else:
                break
        self.page_should_not_contain_text(u'正在加载')
        if self._is_element_present(reloadlocator):
            raise AssertionError(u"Loading page failed! please check your network connectivity! Locator: %s" % locator)

    def wait_until_element_contains(self, locator, attribute, value, timeout=30):
        """
        等待页面元素的状态变化，例如下载是否完成等。
        | ARGS:  | locator: |  请参考 Appium元素定位部分，推荐XPATH |
        |        | attribute: |  属性 |
        |        | value: |  期望值 |
        |        | timeout: |  等待时间， 默认30s，单位s，需大于２s |
        
        example:
        |   Wait Until Element Contains | xpath=//android.widget.EditText | text | 文本 |
        """
        starttime = time.time()
        endtime = starttime
        while (endtime - starttime) < int(timeout):
            v = self.get_element_attribute(locator, attribute)
            if v.find(value) != -1:
                break
            endtime = time.time()
            time.sleep(1)
        if v.find(value) == -1:
            raise TimeoutException("Can not find %s at %s after %s Seconds!" % (value, locator, timeout))
        
    def tap_text(self, text):
        """
        点击页面文本
        | ARGS: |  text:  | 文本 |
        
        example:
        |   Tap Text | 皮肤  |
        """
        locator = "xpath=//*[@text='%s']" % text
        self.tap(locator)
        
    def tap_button(self, text):
        """
        点击按钮
        | ARGS: |  text: |  按钮文本 |
        
        example:
        |   Tap Button | 确定 |
        """
        locator =  "xpath=//android.widget.Button[@text='%s']" % text
        self.tap(locator)
        
    def tap_element_contains_text(self, text):
        """
        点击页面中包含文本的元素
        | ARGS: |  text: |  文本 |
        
        example:
        |   Tap Element Contains Text | 讯飞 |
        """
        locator = "xpath=//*[contains(@text,'%s')]" % text
        self.tap(locator)
    
    def start_activity(self, app_package, app_activity, alternate_activity=None, **opts):
        """
        启动指定的Activity
        | ARGS:  | app_package:  | Package名称 |
        |        | app_activity: |  Activity名称 |
        |        | alternate_activity: |  备用activity，部分机型可能会出现无法启动非launchable的activity，可通过此参数设置备选方案 |
        
        example:
        |   Start Activity | com.forimetest | .MainActivity |
        
        WebDriverException: Message: An unknown server-side error occurred while processing the command. Original error: Error occured while starting App. Original error: Activity used to start app doesn't exist or cannot be launched! Make sure it exists and is a launchable activity
        """
        driver = self._current_application()
        try:
            driver.start_activity(app_package, app_activity, **opts)
        except WebDriverException:
            if alternate_activity:
                driver.start_activity(app_package, alternate_activity, **opts)
            else:
                raise
        
    def activate_ime_engine(self, engine):
        """
        弹出输入法键盘，注意，这里弹出的输入法键盘最上面一栏导航可能无法显示，请慎用，建议慎用点击输入框弹出
        | ARGS:  | engine:  | 输入法引擎 |
        
        example:
        |   Activate Ime Engine | com.iflytek.inputmethod/.FlyIME |
        """
        driver = self._current_application()
        driver.activate_ime_engine(engine)
        
    def ime_engine_should_be_enabled(self, engine):
        """
        检查当前使用的输入法引擎
        | ARGS: |  engine:  | 输入法引擎 |
        
        example:
        |   Ime Engine Should Be Enabled | com.iflytek.inputmethod/.FlyIME |
        """
        driver = self._current_application()
        if not driver.is_ime_active() or driver.active_ime_engine != engine:
            raise AssertionError("IME not activate as expected! Current IME: %s" % driver.active_ime_engine)

    def wait_and_screenshot(self, locator, timeout=10, filename=None):
        """
        等待页面元素显示后截屏
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐XPATH |
        |        | timeout:  | 等待时间， 默认10s，单位s |
        |        | filename: |  保持的文件名称 |
        
        example:
        |   Wait and Screenshot | xpath=//android.widget.EditText |
        |   Wait and Screenshot | xpath=//android.widget.EditText | filename=${CURDIR}/ScreenShot/Homepage.png |
        """
        self.wait_until_page_contains_element(locator, timeout)
        self.capture_page_screenshot(filename)
    
    def init_testdata(self, casename):
        driver = self._current_application()
        sizedict = driver.get_window_size()
        filename = '_'.join([casename, str(sizedict['width']), str(sizedict['height'])])
        with open(filename, 'wb') as fp:
            fp.write('')
    
    def check_locations(self, casename, *locators):
        """
        检查元素位置信息，与上次执行的结果进行对比。
        
        Check Locations
        """
        driver = self._current_application()
        sizedict = driver.get_window_size()
        filename = '_'.join([casename, str(sizedict['width']), str(sizedict['height'])])
        buf = ''
        for locator in locators:
            location = self.get_element_location(locator)
            size = self.get_element_size(locator)
            buf += ' '.join([locator, str(location), str(size), '\n'])
        if not os.path.exists(filename):
            with open(filename, 'ab') as fp:
                fp.write(buf.encode('GBK'))
        else:
            with open(filename, 'rb') as fp:
                data = fp.read().decode('GBK')
            if not buf == data:
                raise AssertionError("UI Changed!")
            
    def tap_if_present(self, locator):
        """
        点击可能显示的页面元素，如果没有显示则无操作
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐XPATH |
        
        example:
        |   Tap If Present | xpath=//android.widget.EditText |
        """
        if self._is_element_present(locator):
            self.tap(locator)
            return True
        return False
            
    def swipe_element_to_top(self, locator, duration=1000):
        """
        将元素滑动到页面顶端
        | ARGS: |  locator:  | 请参考 Appium元素定位部分，推荐XPATH |
        |       | duration:  | 持续时间，默认1s，单位ms |
        example:
        |   Swipe Element to Top | xpath=//android.widget.EditText |
        """
        location = self.get_element_location(locator)
        if location['y'] > 100:
            self.swipe(200, location['y'], 200, 100, duration)

    def element_attribute_should_not_match(self, locator, attr_name, match_pattern, regexp=False):
        """
        检查页面元素
        | ARGS:  | locator:       |  请参考 Appium元素定位部分，推荐XPATH |
        |        | attr_name:     | 属性名称 |
        |        | match_pattern: |  期望结果，可以是正则表达式 |
        |        | regexp:        | 是否为正则表达式，默认为否 |
        
        example:
        |   Element Attribute Should Not Match | xpath=//android.widget.EditText | Text | 文本 |
        """
        try:
            self.element_attribute_should_match(locator, attr_name, match_pattern, regexp=regexp)
        except AssertionError:
            pass
        else:
            raise AssertionError("Element '%s' attribute '%s' should not be '%s' " % (locator, attr_name, match_pattern))

    def swipe_element(self, locator, x, y, duration=500):
        """
        滑动选定的元素
        """
        loc = self.get_element_location(locator)
        size = self.get_element_size(locator)
        startx = loc['x'] + size['width']/2
        starty = loc['y'] + size['height']/2
        self.swipe(startx, starty, startx+int(x), starty+int(y), duration)
        
    def tap_element(self, el):
        """
        点击元素
        """
        driver = self._current_application()
        action = TouchAction(driver)
        action.tap(el).perform()
        
    def long_press(self, locator):
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        if isinstance(element, tuple):
            long_press = TouchAction(driver).long_press(None, element[0], element[1])
        else:
            long_press = TouchAction(driver).long_press(element)
        long_press.perform()
        
    def delete_path(self, path):
        """
        删除设备上的文件
        
        example:
        |   Delete Path | /sdcard/test.txt
        """
        driver = self._current_application()
        driver.delete_path(path)
        
    def set_device_time(self, days=0, seconds=0, minutes=0, hours=0, weeks=0):
        """
        修改设备的时间，按照当前时间的偏移量计算。需要手机有root权限，否则无法执行
        | ARGS: |  days:   | 偏移天数  |
        |       | seconds: |  偏移秒数 |
        |       | minutes: |  偏移分钟数 |
        |       | hours:   |  偏移小时数 |
        |       | weeks:   |  偏移周数 |
        
        example:
        |   Set Device Time | 
        |   Set Device Time | days=1 | weeks=1 |
        |   Set Device Time | hours=2 |
        """
        now = datetime.now()
        delta = timedelta(days=int(days), seconds=int(seconds), minutes=int(minutes), hours=int(hours), weeks=int(weeks))
        driver = self._current_application()
        driver.set_device_time((now + delta).strftime('%Y%m%d.%H%M%S'))
        
    def push_data(self, path, data, encode=False):
        """
        """
        driver = self._current_application()
        if encode:
            data = base64.b64encode(data)
        driver.push_file(path, data)
        
    def push_file(self, path, localpath):
        """
        """
        with open(localpath, 'rb') as fp:
            data = fp.read()
        self.push_data(path, data, encode=True)
        
    def pull_file(self, path, localpath=None, decode=False):
        """
        """
        driver = self._current_application()
        theFile = driver.pull_file(path)
        if decode or localpath:
            theFile = base64.b64decode(theFile)
        if not localpath:
            return theFile
        else:
            with open(localpath, 'wb') as fp:
                fp.write(theFile)
            return localpath
        
    def get_element_rect(self, locator):
        (prefix, criteria) = self._element_finder._parse_locator(locator)
        if prefix == 'rect':
            return map(int, criteria.split(','))
        elif prefix == 'point':
            raise RuntimeError("Point Not Supported!")
        else:
            element = self._element_find(locator, True, True)
            element_loc = element.location
            element_size = element.size
            self._debug("Element '%s' location: %s " % (locator, element_loc))
            return (element_loc['x'], element_loc['y'], element_loc['x']+element_size['width'], element_loc['y']+element_size['height'])
    
    def page_should_contain_elements(self, *locators):
        for locator in locators:
            self.page_should_contain_element(locator)
            
    def wait_until_element_attribute_match(self, locator, attr_name, match_pattern, regexp=False, timeout=None, error=None):

        def check_present():
            try:
                self.element_attribute_should_match(locator, attr_name, match_pattern, regexp)
            except AssertionError:
                return error or "Element %s attribute %s not match '%s' in %s" % (locator, attr_name, match_pattern, self._format_timeout(timeout))
            else:
                return
            
        self._wait_until_no_error(timeout, check_present)
        
    def run_keyword_and_retry(self, retry=2, *keywords):
        """
        """
        keywordgroup = self._split_run_keywords(list(keywords))
        if len(keywordgroup) < 2:
           raise RuntimeError('At least two keywords should be provided!')
        mkw, margs = keywordgroup[0]
        BUILTIN.run_keyword(mkw, *margs)
        passed = self._run_keywords_and_return_status(keywordgroup[1:])
        retried = 1
        while not passed and retried < int(retry):
            retried += 1
            BUILTIN.run_keyword(mkw, *margs)
            passed = self._run_keywords_and_return_status(keywordgroup[1:])
        if not passed:
            logger.info(keywords)
            raise AssertionError("Keyword failed after retried %s times" % retry)
    
    def _run_keywords_and_return_status(self, iterable):
        passed = True
        for kw, args in iterable:
            status = BUILTIN.run_keyword_and_return_status(kw, *args)
            if not status:
                passed = False
        return passed
    
    def _split_run_keywords(self, keywords):
        keywordgroup = []
        if 'AND' not in keywords:
            for name in BUILTIN._variables.replace_list(keywords):
                keywordgroup.append((name, ()))
        else:
            for name, args in BUILTIN._split_run_keywords_from_and(keywords):
                keywordgroup.append((name, args))
        return keywordgroup
    
    def drag_and_drop_element(self, element, target):
        """
        """
        action = TouchAction(self._current_application())
        element_rect = self.get_element_rect(element)
        action.press(x=(element_rect[0]+element_rect[2])/2,y=(element_rect[1]+element_rect[3])/2)
        action.wait(ms=1000)
        target_rect = self.get_element_rect(target)
        action.move_to(x=(target_rect[0]+target_rect[2])/2,y=(target_rect[1]+target_rect[3])/2)
        action.wait(ms=500).release()
        action.perform()