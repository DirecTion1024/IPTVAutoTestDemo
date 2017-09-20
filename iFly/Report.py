# -*- coding: utf-8 -*-

# from models.TestingResultDao import *
import json
import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib
# from GenerateReport import SendHtmlReport
import sys


class Report():

    def sendLogCheckResult(self, version, adr_send, status, checkedpannel, nocheckpannel, errparsed, errparsedMes, notfound, notfoundMes, notinit, notinitMes, textempty, textemptyMes):
        authInfo = {}
        authInfo['server'] = 'mail.iflytek.com'
        authInfo['user'] = 'ydhl_cis_noreply@iflytek.com'
        authInfo['password'] = 'ifly!2015'
        fromAdd = 'ydhl_cis_noreply@iflytek.com'
        subject = 'logcat日志校验报告: ' + version + '【' + status + '】'
#         adr_send = 'yfwang13@iflytek.com'

        html = '''<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>IFlyTek</title>
        <style type="text/css">       
            * {
                margin: 0;
                padding: 0;
            }
            table {
                width: 100%%;
                word-break:break-all;
            }
            th,td {
                overflow: hidden;
                text-align: center;
                padding: 5px 10px;
                border-right: 1px solid #888888;
                border-bottom: 1px solid #888888;
                vertical-align: middle;
                word-break: break-all;
                font-size：small;
            }
 
            .caption{
                text-align: center;
                background:#add8e6;
                padding: 5px 10px;
                border-right: 1px solid #888888;
                border-bottom: 1px solid #888888;
                vertical-align: middle;
            }
        </style></head>
        <body bgcolor="#E0E0E0">
        <table  cellspacing="0" cellpadding="0">
            <colgroup>
               <col width=25%%></col>
               <col width=25%%></col>
               <col width=25%%></col>
               <col width=25%%></col>
            </colgroup>
              <tr>
               <th bgcolor="#ACD6FF" colspan="8">基本信息</th>
            </tr>
        <tr>
            <th bgcolor="#add8e6" width="25%%">版本号</th>
            <td bgcolor="#ffffff" width="25%%">%s</td>
            <th bgcolor="#add8e6" width="25%%">状态</th>
            <td bgcolor="#ffffff" width="25%%">%s</td>
        </tr>
       <tr>
           <th bgcolor="#add8e6">已验证面板</th>
           <td bgcolor="#ffffff" colspan="7"><div style="text-align:left; margin-left:8%%">%s</div></td>
        </tr>
        <tr>
           <th bgcolor="#add8e6">未验证面板</th>
           <td bgcolor="#ffffff" colspan="7"><div style="text-align:left; margin-left:8%%">%s</div></td>
        </tr>
        
            <tr>
               <th bgcolor="#ACD6FF" colspan="8">校验详情</th>
            </tr>
        <tr>
           <th bgcolor="#add8e6">日志格式异常</th>
      <td bgcolor="#ffffff" colspan="1">%s</td>
           <td bgcolor="#ffffff" colspan="5"><div style="text-align:left; margin-left:8%%">%s</div></td>
        </tr>
        <tr>
           <th bgcolor="#add8e6">日志缺失或id与预期不符</th>
      <td bgcolor="#ffffff" colspan="1">%s</td>
           <td bgcolor="#ffffff" colspan="5"><div style="text-align:left; margin-left:8%%">%s</div></td>
        </tr>
        <tr>
           <th bgcolor="#add8e6">日志id没有初始化</th>
      <td bgcolor="#ffffff" colspan="1">%s</td>
           <td bgcolor="#ffffff" colspan="5"><div style="text-align:left; margin-left:8%%">%s</div></td>
        </tr>
        <tr>
           <th bgcolor="#add8e6">设置项或切换项text为空或null</th>
      <td bgcolor="#ffffff" colspan="1">%s</td>
           <td bgcolor="#ffffff" colspan="5"><div style="text-align:left; margin-left:8%%">%s</div></td>
        </tr>
        </table>
   </body>
</html>''' % (version, status, checkedpannel, nocheckpannel, errparsed, errparsedMes, notfound, notfoundMes, notinit, notinitMes, textempty, textemptyMes)

        htmlText = html
        print html

        toAdd = adr_send.split(',')
        strFrom = fromAdd
        strTo = ','.join(toAdd)
        server = authInfo.get('server')
        user = authInfo.get('user')
        passwd = authInfo.get('password')
        if not (server and user and passwd):
            # print 'incomplete login info, exit now'
            return
        # 设定root信息
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
        msgRoot.preamble = 'This is a multi-part message in MIME format.'
        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        # 设定纯文本信息

        # 设定HTML信息
        msgText = MIMEText(htmlText, 'html', 'utf-8')
        msgAlternative.attach(msgText)
       # 设定内置图片信息
       # 发送邮件
        smtp = smtplib.SMTP()
       # 设定调试级别，依情况而定
        smtp.set_debuglevel(1)
        smtp.connect(server)
        smtp.login(user, passwd)
        print toAdd
        smtp.sendmail(strFrom, toAdd, msgRoot.as_string())
        smtp.quit()
#             self.render('report.html')

    def sendA(self):
        pass
#         else:
#             SendHtmlReport(version.encode("utf-8") )
#             self.render('report.html')

# if __name__ == '__main__':
#     print sys.argv
#     version = '7.1.4929'
#     adr_send = 'yfwang13@iflytek.com'
#     # version = '6.0.2731.ossptest'
#     # adr_send = 'mingtang@iflytek.com;535807647@qq.com'
#     status = 'a'
#     checkedpannel = 'b'
#     nocheckpannel = 'c'
#     errparsed = 'd'
#     errparsedMes = 'e'
#     notfound = 'f'
#     notfoundMes = 'g'
#     notinit = 'h'
#     notinitMes = 'i'
#     textempty = 'j'
#     textemptyMes = 'k'
#     Report().sendLogCheckResult(version, adr_send, status, checkedpannel, nocheckpannel,
# errparsed, errparsedMes, notfound, notfoundMes, notinit, notinitMes,
# textempty, textemptyMes)
