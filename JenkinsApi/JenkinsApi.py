import datetime
from jenkinsapi.jenkins import *
import smtplib
from email.mime.text import MIMEText
# for key, job1 in j.iteritems():
# jobName ��Strin���� job��obj
currenttime = time.localtime(time.time())
# %Y-%m-%d %H:%M:%S ��ʽ����ǰʱ��
currenttime1 = time.strftime('%Y-%m-%d %H:%M:%S', currenttime)
# ���String����
print(type(currenttime1), currenttime1, '-------��ǰʱ��----')
##ʱ���ת��
date2 = time.mktime(time.strptime(currenttime1, '%Y-%m-%d %H:%M:%S'))

print(type(date2), date2, '---��ǰʱ��ʱ���--------')

jenkins_server_url = 'http://192.172.2.101:8080'
user_id = 'hucais'
api_token1 = 'hucais'
j = Jenkins(jenkins_server_url, username=user_id, password=api_token1)
# �����ҵ������ ����jobnames
jobNames = j.keys()
for jobName in jobNames:
    # ͨ��get_job���job����
    job = j.get_job(jobName)
    # print(job)
    # run = jobname.get_last_buildnumber()
    # print(jobname2,run)
    isRunning = job.is_running()
    if isRunning == True:
        # print(jobname)
        job.name = jobName + '----״̬�����ڹ���״̬---'
        # ������һ�ι������
        last_build = job.get_last_buildnumber()
        # ������һ�εĹ���ʱ��
        build = job.get_build(last_build)
        buildtime = build.get_timestamp()
        # ��ù���ʱ��ı�ʱ��
        buildtime1 = buildtime + datetime.timedelta(hours=8)
        buildtime2 = datetime.datetime.strftime(buildtime1, '%Y-%m-%d %H:%M:%S')
        print(job.name, buildtime2, '-----job�� ����ʱ��----------')
        print(type(buildtime2), buildtime2, "------------����ʱ��----------")
        ##ʱ���ת��
        date1 = time.mktime(time.strptime(buildtime2, '%Y-%m-%d %H:%M:%S'))
        # ���String����
        print(type(date1), date1, "------------����ʱ��ʱ���----------")
        delta = date2 - date1
        print(delta)
        if 7200 > delta >= 1800:
            try:
                sender1 = '1357379275@qq.com'
                password1 = 'zmwqvwhxqcglijjg'
                reveivers1 = ['1357379275@qq.com', '981038426@qq.com', '351541764@qq.com','463689898@qq.com']
                #30minԤ��
                subject1='---jenkins�ʼ���ǰjob�Ѿ���������30minδ����---'
                content1=job.name+"ִ�����--��job��ִ��30min��δ��ɣ����ص��ע"
                msg1=MIMEText(content1,'plain','utf-8')
                msg1['Subject']=subject1
                msg1['To']=','.join(reveivers1)
                #####��join()������䰴�ն���ƴ�ӳ��ַ���
                server1 = smtplib.SMTP_SSL("smtp.qq.com", 465)
                server1.login(sender1, password1)
                server1.sendmail(sender1,reveivers1,msg1.as_string())
                print(job.name + "ִ�����--��job��ִ��30min��δ��ɣ����ص��ע---�ʼ��ѷ���")
            except smtplib.SMTPException as e:
                print(e)

        elif delta >= 7200:
            print(job.name + 'ִ�����--�����������뾡�촦��')
            ####�����ʼ���һ�ַ�ʽ#######
            # �����ʼ��ķ�������ַ
            Host = 'smtp.qq.com'
            # �ʼ��ķ��Ͷ˿�
            Port = '465'
            # ָ�������˺��ռ���
            From ='1357379275@qq.com'
            TO = '1357379275@qq.com'
            TO1 = '981038426@qq.com'
            TO2 = '351541764@qq.com'
            TO3='463689898@qq.com'
            SUBJECT = '����jenkins���������������ʼ�@1---'
            CONTENT = job.name + "ִ�����--��job�����Ѿ���ʱ3Сʱ���Ѿ��Զ����������������ע��ǰ��jenkins192.172.2.101�����������ֶ�����"
            # �����ʼ����Ͷ���
            # ��ͨ���ʼ�������ʽ
            # smtp_obj=smtplib.SMTP()
            # �����ڴ�������лᱻ����
            # python3�﷨���иı�
            smtp_obj = smtplib.SMTP_SSL(host=Host)
            # ��Ҫ���з����˵���֤����Ȩ
            # smtp_obj����һ���������ͻ��˶���
            smtp_obj.connect(host=Host, port=Port)

            # ���ʹ�õ������ͻ��˵�½��Ҫ��ʹ����Ȩ�룬��ֹ��ʵ����й¶
            res = smtp_obj.login(user=From, password='zmwqvwhxqcglijjg')
            print('��½���--�ʼ���ʽ@1�ѷ���:', res)
            # �����ʼ�
            msg = '\n'.join(
                ['From:{}'.format(From), 'To:{}'.format(TO, TO1, TO2,TO3), 'Subject:{}'.format(SUBJECT), '', CONTENT])
            smtp_obj.sendmail(from_addr=From, to_addrs=[TO, TO1, TO2,TO3], msg=msg.encode('utf-8'))
###�����ʼ��ڶ��ַ�ʽ#########################################################################################
            # try:
            #     sender = '1357379275@qq.com'
            #     password = 'zmwqvwhxqcglijjg'
            #     reveivers = ['1357379275@qq.com', '981038426@qq.com', '351541764@qq.com','463689898@qq.com']
            #     subject = 'jenkins�ʼ����Ա���@2'
            #     content = job.name + "ִ�����--��job�����Ѿ���ʱ3Сʱ���Ѿ��Զ����������������ע��ǰ��jenkins192.172.2.101���������в鿴���������¹������"
            #     #30minԤ��
            #     msg = MIMEText(content, 'plain', 'utf-8')
            #     msg['Subject'] = subject
            #     msg['From'] = sender
            #     #####��join()������䰴�ն���ƴ�ӳ��ַ���
            #     msg['To'] = ','.join(reveivers)
            #     server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            #     server.login(sender, password)
            #     server.sendmail(sender, reveivers, msg.as_string())
            #     print("�ʼ�@2�ѳɹ�����")
            # except smtplib.SMTPException as e:
            #     print(e)
    else:
        job.name = jobName + '----��ǰ���ڹ�����'




    # ��ʼ����ʱ��
    # tz = pytz.timezone('GMT')
    # ��ȡ��ǰϵͳ
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
