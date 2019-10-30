import datetime
from jenkinsapi.jenkins import *
import smtplib
from email.mime.text import MIMEText
# for key, job1 in j.iteritems():
# jobName 是Strin类型 job是obj
currenttime = time.localtime(time.time())
# %Y-%m-%d %H:%M:%S 格式化当前时间
currenttime1 = time.strftime('%Y-%m-%d %H:%M:%S', currenttime)
# 获得String类型
print(type(currenttime1), currenttime1, '-------当前时间----')
##时间戳转换
date2 = time.mktime(time.strptime(currenttime1, '%Y-%m-%d %H:%M:%S'))

print(type(date2), date2, '---当前时间时间戳--------')

jenkins_server_url = 'http://192.172.2.101:8080'
user_id = 'hucais'
api_token1 = 'hucais'
j = Jenkins(jenkins_server_url, username=user_id, password=api_token1)
# 获得作业的名字 数组jobnames
jobNames = j.keys()
for jobName in jobNames:
    # 通过get_job获得job对象
    job = j.get_job(jobName)
    # print(job)
    # run = jobname.get_last_buildnumber()
    # print(jobname2,run)
    isRunning = job.is_running()
    if isRunning == True:
        # print(jobname)
        job.name = jobName + '----状态：处于构建状态---'
        # 获得最后一次构建编号
        last_build = job.get_last_buildnumber()
        # 获得最后一次的构建时间
        build = job.get_build(last_build)
        buildtime = build.get_timestamp()
        # 获得构建时间改变时区
        buildtime1 = buildtime + datetime.timedelta(hours=8)
        buildtime2 = datetime.datetime.strftime(buildtime1, '%Y-%m-%d %H:%M:%S')
        print(job.name, buildtime2, '-----job名 构建时间----------')
        print(type(buildtime2), buildtime2, "------------构建时间----------")
        ##时间戳转换
        date1 = time.mktime(time.strptime(buildtime2, '%Y-%m-%d %H:%M:%S'))
        # 获得String类型
        print(type(date1), date1, "------------构建时间时间戳----------")
        delta = date2 - date1
        print(delta)
        if 7200 > delta >= 1800:
            try:
                sender1 = '1357379275@qq.com'
                password1 = 'zmwqvwhxqcglijjg'
                reveivers1 = ['1357379275@qq.com', '981038426@qq.com', '351541764@qq.com','463689898@qq.com']
                #30min预警
                subject1='---jenkins邮件当前job已经持续运行30min未结束---'
                content1=job.name+"执行情况--此job已执行30min尚未完成，请重点关注"
                msg1=MIMEText(content1,'plain','utf-8')
                msg1['Subject']=subject1
                msg1['To']=','.join(reveivers1)
                #####用join()多个邮箱按照逗号拼接成字符串
                server1 = smtplib.SMTP_SSL("smtp.qq.com", 465)
                server1.login(sender1, password1)
                server1.sendmail(sender1,reveivers1,msg1.as_string())
                print(job.name + "执行情况--此job已执行30min尚未完成，请重点关注---邮件已发送")
            except smtplib.SMTPException as e:
                print(e)

        elif delta >= 7200:
            print(job.name + '执行情况--疑似阻塞，请尽快处理')
            ####发送邮件第一种方式#######
            # 配置邮件的服务器地址
            Host = 'smtp.qq.com'
            # 邮件的发送端口
            Port = '465'
            # 指定发件人和收件人
            From ='1357379275@qq.com'
            TO = '1357379275@qq.com'
            TO1 = '981038426@qq.com'
            TO2 = '351541764@qq.com'
            TO3='463689898@qq.com'
            SUBJECT = '来自jenkins的阻塞报警测试邮件@1---'
            CONTENT = job.name + "执行情况--此job构建已经用时3小时，已经自动丢弃这个构建，请注意前往jenkins192.172.2.101服务器进行手动处理"
            # 创建邮件发送对象
            # 普通的邮件发送形式
            # smtp_obj=smtplib.SMTP()
            # 数据在传输过程中会被加密
            # python3语法中有改变
            smtp_obj = smtplib.SMTP_SSL(host=Host)
            # 需要进行发件人的认证，授权
            # smtp_obj就是一个第三方客户端对象
            smtp_obj.connect(host=Host, port=Port)

            # 如果使用第三方客户端登陆，要求使用授权码，防止真实密码泄露
            res = smtp_obj.login(user=From, password='zmwqvwhxqcglijjg')
            print('登陆结果--邮件方式@1已发送:', res)
            # 发送邮件
            msg = '\n'.join(
                ['From:{}'.format(From), 'To:{}'.format(TO, TO1, TO2,TO3), 'Subject:{}'.format(SUBJECT), '', CONTENT])
            smtp_obj.sendmail(from_addr=From, to_addrs=[TO, TO1, TO2,TO3], msg=msg.encode('utf-8'))
###发送邮件第二种方式#########################################################################################
            # try:
            #     sender = '1357379275@qq.com'
            #     password = 'zmwqvwhxqcglijjg'
            #     reveivers = ['1357379275@qq.com', '981038426@qq.com', '351541764@qq.com','463689898@qq.com']
            #     subject = 'jenkins邮件测试报警@2'
            #     content = job.name + "执行情况--此job构建已经用时3小时，已经自动丢弃这个构建，请注意前往jenkins192.172.2.101服务器进行查看触发器重新构建情况"
            #     #30min预警
            #     msg = MIMEText(content, 'plain', 'utf-8')
            #     msg['Subject'] = subject
            #     msg['From'] = sender
            #     #####用join()多个邮箱按照逗号拼接成字符串
            #     msg['To'] = ','.join(reveivers)
            #     server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            #     server.login(sender, password)
            #     server.sendmail(sender, reveivers, msg.as_string())
            #     print("邮件@2已成功发送")
            # except smtplib.SMTPException as e:
            #     print(e)
    else:
        job.name = jobName + '----当前不在构建中'




    # 初始化零时区
    # tz = pytz.timezone('GMT')
    # 获取当前系统
    #toTimes = datetime.datetime.fromtimestamp(int(buildtime1), tz).strftime('%Y-%m-%d %H:%M:%S')
    #print(job.name,toTimes)
#     print(currenttime1)
#     print(job.name,buildtime1)
print('--------------------------------')
for jobName in jobNames:
    job = j.get_job(jobName)
    print(job.name)

# print(jobname2)
# print(jobname2,jjj)
# print(jobname2)
