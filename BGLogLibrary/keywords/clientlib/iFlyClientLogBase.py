#-*- coding:utf-8 -*-
class iFlyClientLogBase(dict):
    """diff between iFlyLogContentBase And iFlyLogBase is:
        iFlyLogContentBase Log is Log Content
    """
    def __init__(self, log, appiumui='gui', parser=None):
        dict.__init__(self)
        self.log = log
        self.appiumui = appiumui
        self.parser = parser
        self._parse(self.log)
    def _parse(self, log):
        if self.parser:
            self.update(self.parser(log))
            