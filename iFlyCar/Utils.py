#-*- coding: UTF-8 -*- 
"""

(C) Copyright 2016 wei_cloud@126.com

"""
import md5
from robot.libraries import BuiltIn
from robot.api import logger
import traceback
from Crypto.Cipher import AES
import json
from copy import deepcopy
from types import *
from robot.libraries.DateTime import Date, Time
from robot.utils import is_falsy, timestr_to_secs
from datetime import timedelta

BUILTIN = BuiltIn.BuiltIn()

class Utils(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'
    
    def __init__(self):
        self.test_teardown_steps = []
        
    @staticmethod 
    def calc_md5(text):
        m = md5.new()
        m.update(text)
        return m
    
    def init_test_teardown(self):
        self.test_teardown_steps = []
    
    def add_test_teardown(self, index, name, *args):
        self.test_teardown_steps.insert(int(index), [name, args])
    
    def pop_test_teardown(self, index):
        self.test_teardown_steps.pop(int(index))
    
    def execute_test_teardown(self):
        for name, args in self.test_teardown_steps:
            try:
                BUILTIN.run_keyword(name, *args)
            except Exception, e:
                logger.error(e.message.encode('utf-8')) 
                logger.info(traceback.format_exc())
        self.test_teardown_steps = []
        
    @staticmethod    
    def AES_ECB_encrypt(aeskey, src, encoding='UTF-8'):
        if isinstance(src, dict):
            src = json.dumps(src, encoding=encoding, separators=(',', ':'))
        else:
            try:
                src = src.encode(encoding)
            except UnicodeDecodeError:
                pass
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        key=aeskey.decode('base64')
        cipher = AES.new(key)
        encrypted = cipher.encrypt(pad(src))
        return encrypted
    
    @staticmethod
    def AES_ECB_decrypt(aeskey, src):
        unpad = lambda s : s[0:-ord(s[-1])]
        key=aeskey.decode('base64')
        cipher = AES.new(key)
        decrypted = unpad(cipher.decrypt(src))
        return decrypted
    
    @staticmethod
    def UpdateDict(dstdict, srcdict):
        for k, v in srcdict.items():
            if v == '*None*': #internal use only for testing purpose
                continue
            target = None
            next = dstdict
            keys = isinstance(k, basestring) and k.split('.') or [k]
            for key in keys:
                if next.has_key(key):
                    target = next
                    next = next[key]
                else:
                    target = None
                    break
            if target:
                if type(target[key]) in [BooleanType, IntType, LongType, StringType, UnicodeType]:
                    target[key] = type(target[key])(srcdict[k])
                else:
                    target[key] = srcdict[k]
        return dstdict
   
    @staticmethod
    def ArgsToKws(*args, **kws):
        for arg in args:
            if arg.count('=') == 1:
                k, v = arg.split('=')
                kws[k] = v
        return kws
    
    @staticmethod
    def substract_list(srclist, attrname, length=None):
        length = int(length) if length else len(srclist)
        return [Utils.get_sub_attr(item, attrname) for item in srclist][:length]
        
    @staticmethod
    def get_sub_attr(item, attrname):
        attrlist = attrname.split('.')
        ret = item
        for a in attrlist:
            ret = getattr(ret, a)
        return ret
    
    @staticmethod
    def update_json(src, **kws):
        if isinstance(src, basestring):
            src = json.loads(src, encoding='utf-8')
        dst = deepcopy(src)
        Utils.UpdateDict(dst, kws)
        return json.dumps(dst, encoding='utf-8', separators=(',', ':'))
    
    @staticmethod
    def get_current_week(time_zone='local', increment=0,
                         result_format='timestamp', exclude_millis=False):
        """
        """
        weeklist = [u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期天']
        if time_zone.upper() == 'LOCAL':
            dt = datetime.now()
        elif time_zone.upper() == 'UTC':
            dt = datetime.utcnow()
        else:
            raise ValueError("Unsupported timezone '%s'." % time_zone)
        if isinstance(increment, timedelta):
            sec = increment.days * 24 * 60 * 60 + increment.seconds + increment.microseconds / 1e6
        else:
            sec = timestr_to_secs(increment, round_to=None)
        delta = timedelta(seconds=float(sec))
        new = dt + delta
        if result_format.upper() == 'TIMESTAMP':
            return weeklist[new.weekday()]
        if result_format.upper() == 'STANDERD':
            return new.weekday()
        if result_format.upper() == 'ISO':
            return new.isoweekday()
        