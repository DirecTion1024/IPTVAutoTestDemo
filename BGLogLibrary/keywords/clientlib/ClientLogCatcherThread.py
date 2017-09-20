#-*- coding:utf-8 -*-
import threading
import time,os,sys,subprocess,codecs,datetime,traceback
from robot.libraries.BuiltIn import BuiltIn

class ClientLogCatcherThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ClientLogCatcherThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
        self.interval = 1
        self.observers = []
        self.observersTags = []
        self.end_flag = False
        self.is_logcat_thread_starts = False
        self.device_id = BuiltIn().get_variable_value("${UDID}")
        
    def timeout_command(self, command, timeout):
        start = datetime.datetime.now()
        process = subprocess.Popen(command, bufsize=10000, stdout=subprocess.PIPE, close_fds=True)
        while process.poll() is None:
            time.sleep(0.1)
            now = datetime.datetime.now()
            if (now - start).seconds> timeout:
                try:
                    process.terminate()
                except Exception,e:
                    return None
            return None
        out = process.communicate()[0]
        if process.stdin:
            process.stdin.close()
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
        try:
            process.kill()
        except OSError:
            pass
        return out
    
    def clear(self):
        cmd = subprocess.Popen("adb logcat -c".split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        
    def run(self):
        num = 0
#         cmd = subprocess.Popen("adb logcat -c".split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#         print cmd.stdout.readlines()
        
        self.is_logcat_thread_starts = True
        
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            print time.time()
            #cmd = subprocess.Popen("adb logcat -v time -s OperationManager -s OperationResultFactory -s PermissionBizHelper -s AssistHandler".split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            cmd = subprocess.Popen(("adb -s %s logcat -v time"%(self.device_id)).split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            
            line = cmd.stdout.readline()
            
            fw = open('%d.txt'%(num), 'w+')
            while(line):
                try:
#                     print line,
                    line = u''+line[:-2]
                    fw.write('#'*20)
                    fw.write(line)
#                     line = '''04-15 17:21:50.225 D/ContexualWidgetMonitor( 2891): pkg =null'''
                    l = line.split(': ',1)
                    if(len(l) == 2):
                        left,msg = l
                        fw.write(str(len(l))+str(l)+'\n')
                    else:
                        sys.stderr.write("-"*50+'\n')
                        sys.stderr.write(line)
                        line = cmd.stdout.readline()
                        fw.write("-"*5+"1:--"+line)
                        fw.flush()
                        continue
                    l = left.split(' ',2)
                    if(len(l) == 3):
                        date_str,time_str,tag_str = l
                        fw.write(str(len(l))+str(l)+'\n')
                    else:
                        sys.stderr.write("-"*50+'\n')
                        sys.stderr.write(line)
                        line = cmd.stdout.readline()
                        fw.write("-"*5+"2:--"+line)
                        fw.flush()
                        continue
                    
                    pc_time = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
                    tag = tag_str.split('/',1)[1].split('(',1)[0]
                    
                    if(tag not in line):
                        fw.write('-----tag:'+tag+'\n')
                        fw.write('-----line:'+line)
                        print '--tag not in line:',tag
                        print line,
                    
#                     if(tag in self.observersTags):
#                     print line,tag,pc_time,date_str,time_str,msg
                    for obs in self.observers:
                        obs.onTagFound(line,tag.strip(),pc_time,date_str,time_str,msg)
                        pass
                    line = cmd.stdout.readline()
                    if(self.end_flag):
                        break
                except Exception, _ex:
                    traceback.print_exc()
                    print 'ClientLogCatcherThread Warn: %s, line:%s' % (str(_ex),line)
#                     pass
#                     e_msg = 'ERROR: %s, line:%s' % (str(_ex),line)
#                     fw.write(e_msg+'\n')
                    pass
                    line = cmd.stdout.readline()
                fw.flush()
            fw.close()
            
            time.sleep(self.interval)
            num += 1
            
    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False
        self.is_logcat_thread_starts = False
    def regiterObserver(self,observer):
        if(observer not in self.observers):
            self.observers.append(observer)
            for tag in observer.allTags:
                if(tag not in self.observersTags):
                    self.observersTags.append(tag)
    
if __name__ == '__main__':
    a = ClientLogCatcherThread()
    a.start()
    time.sleep(3)
#     a.pause()
#     time.sleep(3)
#     a.resume()
#     time.sleep(3)
#     a.pause()
#     time.sleep(2)
    a.stop()
    print 'ends'