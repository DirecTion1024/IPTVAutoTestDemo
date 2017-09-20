# -*- coding: utf-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
import cmd
from AppiumServer import WindowsAppiumServer
import subprocess
import sys
import os
import time
import logging
from MonitorHander import MonitorHander
import shutil
from datetime import datetime
import PictureCompare
from UIcheckReport import UIcheckReport
import sys
reload(sys)
print sys.setdefaultencoding('utf-8')


class UICaptureTool():

    def __init__(self):

        self.sourceApkDir = ''
        self.resolutionRatio = ['']
        self.skinPath = ""
        self.skinFlag = 0
        self.layoutSet = ['']
        self.appiumpath = ''
        self.monitorpath = ''
        self.scriptpath = ''
        self.picspath = ''
        self.adrsend = ''

    def parser_uicheckconfig(self, filepath):
        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse(filepath)
        root = DOMTree.documentElement

        # 在集合中获取basic
        basic = root.getElementsByTagName('basic')[0]
        # 获取basic中sourceApkDir信息
        sourceApk = basic.getElementsByTagName('sourceApkDir')[0]
        if sourceApk.hasChildNodes():
            self.sourceApkDir = sourceApk.childNodes[0].data

        # 在集合中获取uiCheckConfig
        uiCheckConfig = root.getElementsByTagName('uiCheckConfig')[0]
        # 获取uiCheckConfig中resolutionRatio分辨率信息
        resolu = uiCheckConfig.getElementsByTagName('resolutionRatio')[0]
        self.resolutionRatio.remove('')
        if resolu.hasChildNodes():
            resolution = resolu.childNodes[0].data
            list = resolution.strip().split(',')
            if len(list) > 0:
                for li in list:
                    if len(li) != 0:
                        self.resolutionRatio.append(li)
        # 获取uiCheckConfig中skinPath皮肤信息
        ski = uiCheckConfig.getElementsByTagName('skinPath')[0]
        if ski.hasChildNodes():
            self.skinPath = ski.childNodes[0].data
        # 获取uiCheckConfig中skinFlag默认皮肤开关信息
        skinF = uiCheckConfig.getElementsByTagName('skinFlag')[0]
        if skinF.hasChildNodes():
            self.skinFlag = skinF.childNodes[0].data
        # 获取uiCheckConfig中skinPath皮肤信息
        lay = uiCheckConfig.getElementsByTagName('layoutSet')[0]
        self.layoutSet.remove('')
        if lay.hasChildNodes():
            layout = lay.childNodes[0].data
            llist = layout.strip().split(',')
            if len(llist) > 0:
                for li in llist:
                    if len(li) != 0:
                        self.layoutSet.append(li)

        return self.sourceApkDir, self.resolutionRatio, self.skinPath, self.skinFlag, self.layoutSet

    def parser_basicconfig(self, filepath):
        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse(filepath)
        root = DOMTree.documentElement

        # 在集合中获取basic
        basicpath = root.getElementsByTagName('basicPath')[0]
        # 获取basicPath中appiumpath、monitorpath、scriptpath、picspath信息
        appiumP = basicpath.getElementsByTagName('appiumpath')[0]
        if appiumP.hasChildNodes():
            self.appiumpath = appiumP.childNodes[0].data

        monitorP = basicpath.getElementsByTagName('monitorpath')[0]
        if monitorP.hasChildNodes():
            self.monitorpath = monitorP.childNodes[0].data

        scriptP = basicpath.getElementsByTagName('scriptpath')[0]
        if scriptP.hasChildNodes():
            self.scriptpath = scriptP.childNodes[0].data

        picsP = basicpath.getElementsByTagName('picspath')[0]
        if picsP.hasChildNodes():
            self.picspath = picsP.childNodes[0].data

        # 在集合中获取mail
        mailConfig = root.getElementsByTagName('mail')[0]
        # 获取mail中收件人信息
        mailTo = mailConfig.getElementsByTagName('to')[0]
        if mailTo.hasChildNodes():
            self.adrsend = mailTo.childNodes[0].data

        return self.appiumpath, self.monitorpath, self.scriptpath, self.picspath, self.adrsend

    def del_files(self, path, suffix):
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith(suffix):
                    os.remove(os.path.join(root, name))
        print ("Delete File: " + os.path.join(root, name))

    def is_exit_task(self):
        devices = monitorH.getConnectedDevices()
        print devices
        if len(devices) != 0:
            for device in devices:
                if device[:11] == '127.0.0.1:6':
                    isidle = WindowsAppiumServer().isDeivceIdle(device)
                    if isidle:
                        # 删除模拟器进程
                        print u'杀死该进程'
                        cmd = u"taskkill /F /IM NoxVMHandle.exe"
                        print [cmd]
                        os.system(cmd)
                        time.sleep(5)
                    else:
                        try:
                            sys.exit(0)
                        except:
                            print 'die'

if __name__ == '__main__':
    # 参数
    #     path = sys.path[0]
    #     if os.path.isdir(path):
    #         curdir = path
    #     elif os.path.isfile(path):
    #         curdir = os.path.dirname(path)
    #     scriptpath = curdir + "/../InputTest/UICaptureTool"
    #     print scriptpath
    locpath = "E:/UICheckTool"
    outpath = locpath + "/" + "checkResult"
    monitorH = MonitorHander()
#     appiumpath = "C:/Users/admin/AppData/Roaming/npm/appium"
    # 判断是否存在正在执行任务的模拟器
#     UICaptureTool().is_exit_task()
    # 解析配置文件
    appiumpath, monitorpath, scriptpath, picspath, adrsend = UICaptureTool(
    ).parser_basicconfig(locpath + "/" + "config.xml")
    scriptpath = scriptpath + "/InputTest/UICaptureTool"
    sourceApkDir, resolutionRatio, skinPath, skinFlag, layoutSet = UICaptureTool(
    ).parser_uicheckconfig(locpath + "/" + "config.xml")
    version = sourceApkDir.split('\\')[-1]
    print sourceApkDir, resolutionRatio, skinPath, skinFlag, layoutSet
    # 创建截图文件夹
    curtime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    index = version.find('.apk')
    filename = outpath + "/" + curtime + "_" + version[:index]
    os.mkdir(filename)
    # 邮件展示截图和对比图片路径
    caplinkp = picspath  + "\\\\" + curtime + "_" + \
        version[:index] + "\\\\capturePics"
    comlinkp = picspath  + "\\\\" + curtime + "_" + \
        version[:index] + "\\\\exceptPics"

    cappath = filename + "/capturePics"
    os.mkdir(cappath)
    exceptpath = filename + "/exceptPics"
    os.mkdir(exceptpath)
    comppath = filename + "/comparePics"
    os.mkdir(comppath)
    reportpath = filename + "/Reports"
    os.mkdir(reportpath)
    # 对日志的输出格式及方式做相关配置
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename=filename + '/myapp.log', filemode='w')
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-12s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info(u'脚本路径：%s' % scriptpath)
    logging.info(u'本地checkResult路径：%s' % outpath)
    logging.info(u'appium路径：%s' % appiumpath)
    logging.info(u'sourceApkDir:%s, resolutionRation:%s, skinPath:%s, skinFlag:%s, layoutSet:%s' % (
        sourceApkDir, resolutionRatio, skinPath, skinFlag, layoutSet))
    # 拷贝config配置文件
    logging.info(u'拷贝config配置文件......')
    if os.path.exists(locpath + "/" + "config.xml"):
        shutil.copy(locpath + "/" + "config.xml", filename)
    # 拷贝apk文件
    # UICaptureTool().del_files(locpath, ".apk")
    logging.info(u'拷贝apk文件......')
    if os.path.exists(sourceApkDir):
        shutil.copy(sourceApkDir, filename)
    # 拷贝预期图片文件夹(判断预期文件夹是否存在，不存在需邮件提示)
    logging.info(u'拷贝预期图片文件夹......')
    exceptpicts = locpath + "/" + "exceptPics"
    if os.path.exists(exceptpicts):
        list = os.listdir(exceptpicts)
        for map in list:
            mappath = exceptpicts + "/" + map
            srcmap = mappath.decode('gbk')
            shutil.copy(srcmap, exceptpath)
#         shutil.copytree(exceptpicts, filename + "/" + "exceptPics123")
    # 解析所配置的皮肤文件路径，拷贝theme文件夹
    logging.info(u'拷贝皮肤theme文件夹......')
    skinList = ['']
    skinList.remove('')
    if int(skinFlag) == 1:
        skinList.append(u'默认')
    if len(skinPath.strip()) != 0:
        if os.path.exists(filename):
            shutil.copytree(skinPath, filename + "/" + "theme")
            list = os.listdir(filename + "/" + "theme")
            if len(list) != 0:
                for i in range(0, len(list)):
                    path = os.path.join(filename + "/" + "theme", list[i])
                    zhui = list[i][-2:]
                    if os.path.isfile(path) and zhui == 'it':
                        skinList.append(path)
    elif len(skinList) == 0:
        logging.error(u'皮肤缺少配置')
        raise AssertionError(u'皮肤缺少配置')
    else:
        pass

    if len(layoutSet) == 0:
        layoutSet.append(u'默认')

    # 进行遍历操作
    logging.info(u'开始遍历......')
    monitorindex = 0
    reportindex = 1
    for resolution in resolutionRatio:
        # 将模拟器分辨率信息写入txt
        filepath = filename + '/' + 'keyboardRegion.txt'
        if not os.path.exists(filepath):
            file = open(filepath, 'w')
            file.close()
        file = open(filepath, 'a')
        file.write(u"resolution:%s" % resolution)
        file.write("\n")
        file.flush()
        file.close
        # 启动模拟器，返回模拟器udid
        logging.info(u'启动模拟器，分辨率：%s' % resolution)
#         path = "\"D:/Program Files/Nox/bin/Nox.exe\""
        path = "\"" + monitorpath + "\""

        swidth = resolution.strip().split('x')[0]
        height = resolution.strip().split('x')[1]
        if float(swidth) < float(height):
            dpi = int(400.0 * float(swidth) / 1080.0)
        else:
            dpi = int(400.0 * float(height) / 1080.0)
        apks = "  -apk:%s" % (filename + "/" + version)
#         args = "  -screen:vertical  -root:true -resolution:%s  -dpi:%s" % (
#             resolution, dpi)
        monitorindex = monitorindex + 1
        args = "  -clone:Nox_%s  -root:true  -resolution:%s  -dpi:%s" % (
            monitorindex, resolution, dpi)
#         filep = (
#             path[1:len(path) - 9] + "/BignoxVMS" + "/Nox_%s") % monitorindex
#         print filep
#         exit = os.path.exists(filep)
#         if exit:
#             shutil.rmtree(filep)
#         udid = monitorH.startMonitor(path, args + apks)
#         print udid
#         time.sleep(50)
#         monitorH.stopMonitor(path, monitorindex)
#         time.sleep(10)
        udid = monitorH.startMonitor(path, args + apks)
        print udid
        logging.info(u'启动模拟器指令：%s' % (path + "  " + args + apks))
        logging.info(u'模拟器启动成功，udid：%s' % udid)
        # 向模拟器中安装输入法apk
        logging.info(u'向模拟器安装输入法apk')
        monitorH.installTestApk(udid, filename + "/" + version)
        # 根据设备udid启动appium
        logging.info(u'针对模拟器启动appium，udid：%s' % udid)
        port = WindowsAppiumServer().StartServer(appiumpath, udid)
        print port
        logging.info(u'appium启动成功，port：%s' % port)

        # 遍历皮肤和布局
        for skinpath in skinList:
            cmd = "adb -s %s shell rm -rf %s" % (udid,
                                                 "/mnt/sdcard/iFlyIME/skin")
            os.system(cmd)
            if skinpath != u'默认':
                cmd = "adb -s %s shell  mkdir %s" % (
                    udid, "/mnt/sdcard/iFlyIME/skin")
                os.system(cmd)
                cmd = "adb -s %s shell  mkdir %s" % (
                    udid, "/mnt/sdcard/iFlyIME/skin/theme")
                os.system(cmd)
                cmd = "adb -s %s push %s %s" % (udid,
                                                skinpath, "/mnt/sdcard/iFlyIME/skin/theme")
                os.system(cmd)
                skinname = os.path.basename(skinpath)
            else:
                skinname = skinpath
            print skinname
            logging.info(u'遍历皮肤:%s' % skinname)
            for layout in layoutSet:
                # 执行自动截图脚本
                logging.info(u'遍历布局:%s' % layout)
                newreportp = reportpath + "/" + "report" + str(reportindex)
                os.mkdir(newreportp)
                cmd1 = "pybot -v udid:%s -v serverurl:http://localhost:%s/wd/hub -v cappath:%s -v resolution:%s -v skinname:%s -v layout:%s -d %s --loglevel debug  %s" % (
                    udid, port, cappath, resolution, skinname, layout, newreportp, scriptpath)
                reportindex = reportindex + 1
                print type(cmd1)
                cmd = cmd1.decode('utf-8').encode('gbk')
                print type(cmd)
                print cmd
                logging.info(u'执行脚本指令：%s' % cmd1)
                os.system(cmd)

                logging.info(u'执行自动截图脚本......reportindex:%s' %
                             (reportindex - 1))
        # 根据设备udid关闭appium
        out = WindowsAppiumServer().StopServer(udid)
        print out
        logging.info(u'根据设备udid关闭appium')
        # 退出模拟器
        time.sleep(5)
        if monitorindex == 0:
            monitorH.stopMonitor(path)
        else:
            monitorH.stopMonitor(path, monitorindex)
#         monitorindex = monitorindex + 1
        logging.info(u'关闭模拟器')
        time.sleep(5)

    # 截图图片匹配
    logging.info(u'截图图片匹配......')
    list = os.listdir(cappath)
    for map in list:
        if os.path.exists(exceptpath + '/' + map):
            result = PictureCompare.pictureCom(
                cappath + '/' + map, exceptpath + '/' + map, comppath)
            print result
    # 发送邮件
#     adr_send = 'yfwang13@iflytek.com'
    comparelist = os.listdir(comppath)
    status = ''
    if len(comparelist) == 0:
        status = '通过'
    else:
        status = '失败'
    resolutions = ''
    for resolu in resolutionRatio:
        resolutions = resolutions + ',' + resolu
    resolutions = resolutions[1:]
    skins = ''
    for skin in skinList:
        skins = skins + skin + '<br>'
    skins = skins.strip()
    layouts = ''
    for layout in layoutSet:
        layouts = layouts + ',' + layout
    layouts = layouts[1:]
    exceptlist = os.listdir(exceptpath)
    isdeploy = ''
    if len(exceptlist) == 0:
        isdeploy = '未配置'
    else:
        isdeploy = '已配置'
    capturelist = os.listdir(cappath)
    isabnormal = ''
    caplen = len(capturelist)
    actrullen = len(resolutionRatio) * len(skinList) * len(layoutSet) * 13
    if caplen >= actrullen:
        isabnormal = '正常'
    else:
        isabnormal = '异常'
    versionnum = version.strip().split('_')[-1]
    versionnum = versionnum[1:-4]
    UIcheckReport().sendUICheckResult(versionnum, adrsend, status, resolutions,
                                      skins, layouts, isdeploy, isabnormal, caplinkp, comlinkp)
