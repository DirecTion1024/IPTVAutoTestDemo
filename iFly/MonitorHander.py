#-*- coding: UTF-8 -*-
"""

(C) Copyright 2016 wei_cloud@126.com

"""
import subprocess
import time
import os
from AppiumServer import AppiumServer
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class MonitorHander(object):

    def __init__(self, udid=None):
        self.timeout = 90  # 单位s
        self.interval = 5

    def startMonitor(self, path, args):
        """
        """
        self.stopMonitor(path)
        befdevices = self.getConnectedDevices()
        print befdevices
        cmd = path + "  " + args
        print cmd
        self.process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(10)

        start = time.time()
        print start
        timeout = self.timeout
        isconnect = False
        while not isconnect:
            end = time.time()
            if (end - start) * 1 > timeout:
                raise AssertionError(u"Monitor not started after %s s")
            aftdevices = self.getConnectedDevices()
            print aftdevices
            device = self._is_device_in_list(befdevices, aftdevices)
            if device != '0':
                isconnect = True
                return device
            else:
                isconnect = False
            time.sleep(self.interval)

    def _is_device_in_list(self, befdevices, aftdevices):
        if len(aftdevices) > len(befdevices):
            for device in aftdevices:
                if device not in befdevices and device[:3] == '127':
                    if device[:11] == '127.0.0.1:6':
                        return device
        else:
            return '0'

    def stopMonitor(self, path, index=None):
        if index == None:
            cmd = path + " -quit"
        else:
            cmd = path + "  -clone:Nox_%s  -quit" % index
        print cmd
#         os.system(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.communicate()

    def getConnectedDevices(self):
        """
        """
        devices = []
        cmd = "adb devices"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        out = out[out.index("List of devices attached"):]
        lines = out.splitlines()
        for line in lines[1:]:
            if line.strip() and not line.startswith('*'):
                deviceId, status = line.split()
                if status.lower() == 'device':
                    devices.append(deviceId)
        return devices

    def installTestApk(self, udid, apkdir):
        pacname = "com.iflytek.inputmethod"
        cmd = "adb -s  %s uninstall %s" % (udid, pacname)
        print cmd
        os.system(cmd)
        time.sleep(2)
        apkdir = "\"" + apkdir + "\""
        cmd = "adb -s %s install %s" % (udid, apkdir)
        print cmd
        os.system(cmd)
        time.sleep(2)

if __name__ == '__main__':
    print 'start'
