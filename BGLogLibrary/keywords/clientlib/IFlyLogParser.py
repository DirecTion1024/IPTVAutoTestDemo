#-*- coding:utf-8 -*-
import re,json
from xml.dom.minidom import parseString
from robot.api import logger

class RequestLogParser(dict):
    def __init__(self, log):
        """
        """
        dict.__init__(self)
        self._logtype = ''
        logger.debug("RequestLogParser", False)
        logger.debug(log, False)
        if log:
            if(log.startswith('postStatistics url = ')):
                self._logtype = 'realtimelog'
                log = log.strip()
                html_url = log.split('postStatistics url = ')[1]
                logger.debug(html_url, False)
                self._parse_url(html_url)
            elif 'type =' in log and ', result' in log:
                self._logtype = 'interfacelog'
                self.type = log.split('type = ')[1].split(',')[0]
                re_xmlstr = re.compile(r'''\<\?xml.*?\<\/request\>''', re.X)
                xmlstr = re_xmlstr.findall(log)[0]
                self._parse(parseString(xmlstr))
            
            elif "\"opcode\":\"FT" in log:
                self._logtype = 'opcodelog'
                logger.debug(log, False)
                re_jsonstr = re.compile(r'''{.*}''', re.X)
                logger.debug(re_jsonstr, False)
                
                jsonstr = re_jsonstr.findall(log)[0]
                logger.debug(jsonstr, False)
                self._parse_json(jsonstr)
                logger.debug(str(self.items()), False)
            else:
                re_xmlstr = re.compile(r'''\<\?xml.*?\<\/request\>''', re.X)
                xmlstr = re_xmlstr.findall(log)[0]
                self._parse(parseString(xmlstr))
    def _parse_url(self, html_url):
        _url,_params = html_url.split('?',1)
        self['_url'] = _url
        for node in _params.split('&'):
            k,v = node.split('=')
            self[k] = v
                
    def _parse_json(self, jsonstr):
        d = json.loads(jsonstr)
        for k,v in d.items():
            self[k] = v
            
    def _parse(self, xml):
        if xml.hasChildNodes():
            for child in xml.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    self[xml.tagName] = child.data
                self._parse(child)
                
class ResponseLogParser(dict):
    def __init__(self, log):
        dict.__init__(self)
        log_type = 'xml'
#         print '--'+log+'--'
        if log:
            if('<result>' in log):
                #logcat日志可能会被截断,待处理，根节点不是result的情况
                if('</result>' not in log):
                    log_will_cast = log.rsplit('</',1)[1].split('>',1)[1]
                    log = log.replace(log_will_cast,'')
                    
                    re_xmlstr = re.compile(r'''<.*?>''', re.X)
                    re_list = re_xmlstr.findall(log)
                    for node in re_list[::-1]:
                        if(not node.startswith('<?') and not node.startswith('</')):
                            if(node.replace('<','</') not in log):
                                log += node.replace('<','</')
                    
                    print 'log casted:',log
            else:
                log_type = 'json'
#             print [log_type]
            if(log_type == 'xml'):
                re_xmlstr = re.compile(r'''\<\?xml.*?\<\/result\>''', re.X)
                xmlstr = re_xmlstr.findall(log)[0]
                node = parseString(u'{0}'.format(xmlstr).encode('utf-8'))
            
                self._parse(parseString(u'{0}'.format(xmlstr).encode('utf-8')))
            else:
                re_jsonstr = re.compile(r'''{.*}''', re.X)
                jsonstr = re_jsonstr.findall(log)[0]
                self._parse_json(jsonstr)
    def _parse_json(self, jsonstr):
        d = json.loads(jsonstr)
        for k,v in d.items():
            self[k] = v
            
    def _parse(self, xml):
        """
        """
        
        if xml.hasChildNodes():
            for child in xml.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    self[xml.tagName] = child.data
                self._parse(child)
        '''
        configlist = xml.getElementsByTagName('config')
        for config in configlist:
            keys = config.getElementsByTagName('key')
            values = config.getElementsByTagName('value')
            for k, v in zip(keys, values):
                print [k.childNodes[0].data,v.childNodes[0].data]
                self[k.childNodes[0].data] = v.childNodes[0].data
        '''