import datetime
from jenkinsapi.jenkins import *
import smtplib
from email.mime.text import MIMEText

currenttime = time.localtime(time.time())

currenttime1 = time.strftime('%Y-%m-%d %H:%M:%S', currenttime)

print(type(currenttime1), currenttime1, '-------当前时间----')

date2 = time.mktime(time.strptime(currenttime1, '%Y-%m-%d %H:%M:%S'))

print(type(date2), date2, '---当前时间时间戳--------')

jenkins_server_url = 'http://192.172.2.101:8080'
user_id = 'hucais'
api_token1 = 'hucais'
j = Jenkins(jenkins_server_url, username=user_id, password=api_token1)

jobNames = j.keys()
for jobName in jobNames:
    job = j.get_job(jobName)
    isRunning = job.is_running()
    if isRunning == True:

        job.name = jobName + '----状态：处于构建状态---'

        last_build = job.get_last_buildnumber()

        build = job.get_build(last_build)
        buildtime = build.get_timestamp()

        buildtime1 = buildtime + datetime.timedelta(hours=8)
        buildtime2 = datetime.datetime.strftime(buildtime1, '%Y-%m-%d %H:%M:%S')
        print(job.name, buildtime2, '-----job名 构建时间----------')
        print(type(buildtime2), buildtime2, "------------构建时间----------")

        date1 = time.mktime(time.strptime(buildtime2, '%Y-%m-%d %H:%M:%S'))

        print(type(date1), date1, "------------构建时间时间戳----------")
        delta = date2 - date1
        print(delta)
        if 7200 > delta >= 1800:
            try:
                sender1 = '1357379275@qq.com'
                password1 = 'zmwqvwhxqcglijjg'
                reveivers1 = ['1357379275@qq.com', '981038426@qq.com', '351541764@qq.com', '463689898@qq.com']

                subject1 = '---jenkins邮件当前job已经持续运行30min未结束---'
                content1 = job.name + "执行情况--此job已执行30min尚未完成，请重点关注"
                msg1 = MIMEText(content1, 'plain', 'utf-8')
                msg1['Subject'] = subject1
                msg1['To'] = ','.join(reveivers1)

                server1 = smtplib.SMTP_SSL("smtp.qq.com", 465)
                server1.login(sender1, password1)
                server1.sendmail(sender1, reveivers1, msg1.as_string())
                print(job.name + "执行情况--此job已执行30min尚未完成，请重点关注---邮件已发送")
            except smtplib.SMTPException as e:
                print(e)

        elif delta >= 7200:
            print(job.name + '执行情况--疑似阻塞，请尽快处理')

            Host = 'smtp.qq.com'

            Port = '465'

            From = '1357379275@qq.com'
            TO = '1357379275@qq.com'
            TO1 = '981038426@qq.com'
            TO2 = '351541764@qq.com'
            TO3 = '463689898@qq.com'
            SUBJECT = '来自jenkins的阻塞报警测试邮件@1---'
            CONTENT = job.name + "执行情况--此job构建已经用时3小时，已经自动丢弃这个构建，请注意前往jenkins192.172.2.101服务器进行手动处理"

            smtp_obj = smtplib.SMTP_SSL(host=Host)

            smtp_obj.connect(host=Host, port=Port)

            res = smtp_obj.login(user=From, password='zmwqvwhxqcglijjg')
            print('登陆结果--邮件方式@1已发送:', res)

            msg = '\n'.join(
                ['From:{}'.format(From), 'To:{}'.format(TO, TO1, TO2, TO3), 'Subject:{}'.format(SUBJECT), '', CONTENT])
            smtp_obj.sendmail(from_addr=From, to_addrs=[TO, TO1, TO2, TO3], msg=msg.encode('utf-8'))
    else:
        job.name = jobName + '----当前不在构建中'