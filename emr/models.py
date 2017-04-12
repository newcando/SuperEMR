# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from jsonfield import JSONField#需要导入json字段。pip install jsonfield
import datetime
from SuperEMR import settings
import hashlib
import random
from django.template import Context, loader
from django.contrib import admin
# Create your models here.
###################################################用户信息##########################################################
###采用一对一，拓展了Django默认的User
#####################################################################################################################
class mdlUserExtInfo(models.Model):
    user = models.OneToOneField(User, primary_key = True)
    #username,first_name,last_name,email,password,groups,user_permissions,is_staff,is_active,is_superuser,last_login,date_joined
    #除了username外，邮箱和手机号也具有唯一性，其在经过验证后可以作为登录号
    email_activation_key = models.CharField(verbose_name='邮箱验证码', max_length=40)#邮箱验证码
    uniqEmail = models.EmailField(verbose_name='唯一的email', blank=True, unique=True, max_length=64)
    is_uniqEmailActivated = models.BooleanField(verbose_name='邮箱是否激活过', blank=True, null=False,default=False)
    uniqMobilePhone = models.CharField(verbose_name='手机号码',blank=True, unique=True, default='', max_length=18)
    is_uniqMobilePhoneActivated = models.BooleanField(verbose_name='手机是否激活过', blank=True, null=False, default=False)
    SEX_CHOICES = ((2,u'不告诉你'),(1,u'男'),(0,u'女'),)
    sex = models.SmallIntegerField(verbose_name='性别', choices = SEX_CHOICES, null=False, blank=True, default=2)
    EDUCATION_CHOICES = ((1,u'博士'),(2,u'硕士'),(3,u'本科'),(4,u'高中'),(5,u'初中'),(6,u'小学'),(0,u'其它'),)
    educationbackground = models.SmallIntegerField(verbose_name='学历', choices = EDUCATION_CHOICES, blank=False, null=False, default='0')
    datebirth = models.DateField(verbose_name='出生年月',null=False, blank=True, default='1900-01-01')
    nickname = models.CharField(verbose_name='用户昵称',blank=False, unique=True, max_length=32)
    addressline1 = models.CharField(verbose_name='地址行1',blank=True,default='',max_length=128)
    addressline2 = models.CharField(verbose_name='地址行2',blank=True,default='',max_length=128)
    state = models.CharField(verbose_name='省',blank=True,default='00',max_length=32)
    city = models.CharField(verbose_name='县市',blank=True,default='00',max_length=32)
    district=models.CharField(verbose_name='区',blank=True,default='00',max_length=32)
    zipcode = models.IntegerField(verbose_name='邮编', blank=True, null=True)
    is_locked = models.BooleanField(verbose_name='账号是否被锁定', blank=True, null=False, default=False)
    demo = models.TextField(verbose_name='备注信息', max_length=51200)
    user_type = models.CharField(verbose_name='用户类型', blank=True, null=True, default='A', max_length=4)
    relative_user = models.ManyToManyField('self',verbose_name='关联用户',blank=True, null=True, default=False)
    #
    user_image = models.ImageField(verbose_name='头像',upload_to='MLImage/%Y/%m/%d', blank=True,null=True,default='MLImage/null.jpg')
    name = models.CharField(verbose_name='姓名',blank=True, unique=False, max_length=32)
    home = models.ImageField(verbose_name='我的封面',upload_to='MLImage/%Y/%m/%d', blank=True,null=True)
    height = models.SmallIntegerField(verbose_name='身高', blank=True, null=False, default='0')
    weight = models.SmallIntegerField(verbose_name='体重', blank=True, null=False, default='0')
    blood_type = models.CharField(verbose_name='血型',blank=True, unique=False, max_length=4)
    subject = models.CharField(verbose_name='专业',blank=True, unique=False, max_length=64)
    company = models.CharField(verbose_name='工作单位',blank=True, unique=False, max_length=64)
    jobNumber = models.CharField(verbose_name='工号',blank=True, unique=False, max_length=64)
    achivement = models.CharField(verbose_name='学术成就',blank=True, unique=False, max_length=64)
    personID = models.CharField(verbose_name='身份证',blank=True, unique=False, max_length=64)
    Vocational_qualification_certificate = models.CharField(verbose_name='职业资格证号',blank=True, unique=False, max_length=64)
    VQCID = models.CharField(verbose_name='职业资格证号号',blank=True, unique=False, max_length=64)
    publicGender = models.CharField(verbose_name='是否公开性别',blank=True, unique=False, max_length=1)
    publicHome = models.CharField(verbose_name='是否开放空间',blank=True, unique=False, max_length=1)
    QR = models.ImageField(verbose_name='用户二维码',upload_to='MLImage/%Y/%m/%d', blank=True,null=True)
    roamingtime = models.DateTimeField(verbose_name='漫游时间设置', blank=False, null=False, auto_now_add=True, editable=False)
    workday = models.SmallIntegerField(verbose_name='排班时间', blank=True, null=False, default=1)
    def email_activation_key_expired(self):
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.email_activation_key == "账号已经激活" or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())

    def send_activation_email(self):
        #email=self.user.email
        subject='超级病历-账号激活'
        context = {'username':self.user.username,
                   'email_activation_key':self.email_activation_key}
        t=loader.get_template('email_active_template.txt')
        self.user.email_user(subject=subject,
                             message=t.render(Context(context)))

    def __str__(self):
        return self.user.first_name + self.user.last_name + '(' + self.user.username + ')' + '-' + self.uniqEmail
    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = '个人信息'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        salt = hashlib.sha1((str(random.random())).encode('utf-8')).hexdigest()[:5]
        salted_username = salt + instance.username
        email_activation_key = hashlib.sha1(salted_username.encode('utf-8')).hexdigest()
        profile, created = mdlUserExtInfo.objects.get_or_create(user=instance,
                                                                uniqEmail=instance.email,
                                                                uniqMobilePhone=instance.id,
                                                                nickname=instance.username,
                                                                email_activation_key=email_activation_key)
post_save.connect(create_user_profile, sender=User)

####################********************************************************************************###################
###################################################聊天记录##########################################################
###
#####################################################################################################################
class mdlChatRecord(models.Model):
    user1 = models.ForeignKey(mdlUserExtInfo)
    image = models.ImageField(verbose_name='聊天图片',upload_to='MLImage/%Y/%m/%d', blank=True,null=True)
    character = models.CharField(verbose_name='聊天文字', default='', blank=True, null=False, max_length=1024)
    video = models.FileField(verbose_name='聊天视频',upload_to='MLFile/%Y/%m/%d', blank=True,null=True)
    audio = models.FileField(verbose_name='聊天语音',upload_to='MLFile/%Y/%m/%d', blank=True,null=True)
    time = models.DateTimeField(verbose_name='聊天时间', blank=False, null=False, auto_now_add=True, editable=False)
    def __str__(self):
        return self.user1.first_name + self.use2r.first_name
    class Meta:
        verbose_name = '聊天记录'
        verbose_name_plural = '聊天记录'
###############################################体温记录###############################################################
###体温测量是常见的记录，我们专门列一个体温记录表
######################################################################################################################
class mdlbodyTemperature(models.Model):
    user = models.ForeignKey(mdlUserExtInfo)
    #我们假设体温单位都是摄氏度
    temperature = models.FloatField(verbose_name='体温数据', blank=False, null=False)
    measure_datetime = models.DateTimeField(verbose_name='测量时间', blank=False, null=False)
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    demoInfo = models.CharField(verbose_name='其它信息', default='', blank=True, null=False, max_length=128)
    def __str__(self):
        return self.user.nickname + '//' + str(self.temperature)
    class Meta:
        verbose_name = '体温'
        verbose_name_plural = '体温'
        ordering=['-measure_datetime']#查询数据库时按时间降序排列
####################********************************************************************************###################

###############################################血压记录###############################################################
###血压测量是常见的记录，我们专门列一个血压记录表
######################################################################################################################
class mdlbloodpressure(models.Model):
    user = models.ForeignKey(mdlUserExtInfo)
    systolic_pressure = models.SmallIntegerField(verbose_name='收缩压', blank=False, null=False,default=-1)
    diastolic_pressure = models.SmallIntegerField(verbose_name='舒张压', blank=False, null=False,default=-1)
    heart_rate = models.SmallIntegerField(verbose_name='心律',blank=False,null=False,default=-1)
    measure_datetime = models.DateTimeField(verbose_name='测量时间', blank=False, null=False)
    demoInfo = models.CharField(verbose_name='其它信息', default='', blank=True, null=False, max_length=128)
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    def __str__(self):
        return self.user.nickname + '//' + str(self.systolic_pressure) + '/' + str(self.diastolic_pressure)
    class Meta:
        verbose_name = '血压'
        verbose_name_plural = '血压'
        ordering=['-measure_datetime']#查询数据库时按时间降序排列
####################********************************************************************************###################

###############################################血糖记录###############################################################
###血糖测量是常见的记录，我们专门列一个血糖记录表
######################################################################################################################
class mdlbloodglucose(models.Model):
    user =models.ForeignKey(mdlUserExtInfo)
    gluocose = models.FloatField(verbose_name='血糖', blank=False, null=False)
    measure_datetime = models.DateTimeField(verbose_name='测量时间', blank=False, null=False)
    demoInfo = models.CharField(verbose_name='其它信息', default='', blank=True, null=False, max_length=128)
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    def __str__(self):
        return self.user.nickname + '//' + str(self.gluocose)
    class Meta:
        verbose_name = '血糖'
        verbose_name_plural = '血糖'
        ordering=['-measure_datetime']#查询数据库时按时间降序排列
####################********************************************************************************###################

################################################我的常用药品############################################################
###建立每个人自己的药品库，这样我们可以统计，也可以在用户输入时，起到一个提示作用。设计页面时，输入完后弄一个选型询问看是否
###添加定期服用提示
######################################################################################################################
class mdlMedicineLib(models.Model):
    user = models.ForeignKey(mdlUserExtInfo)
    name = models.CharField(verbose_name='药品名称', blank=False, null=False,max_length=254)
    pharmaceutical_factory = models.CharField(verbose_name='生产厂家', blank=True, default='', max_length=128)
    functionDescription = models.CharField(verbose_name='功效描述', blank=True, default='', max_length=254)
    price = models.PositiveIntegerField(verbose_name='价格', blank = True, null=False, default=0)
    seller = models.CharField(verbose_name='销售商', blank=True, null=False, max_length=128, default='')
    sellerPhoneNum = models.CharField(verbose_name='销售商电话', blank='', null=True, max_length=18)
    method=models.CharField(verbose_name='用法',max_length=10)#用法
    how_use=models.CharField(verbose_name='用量',max_length=10)#用量
    resultsEval = models.PositiveSmallIntegerField(verbose_name='效果评价(1-10分)', blank=True, default=-1)
    demoInfo = models.CharField(verbose_name='其它信息', default='', blank=True, null=False, max_length=128)
    mark_image = models.ImageField(verbose_name='药品外观图片',upload_to='MLImage/%Y/%m/%d', blank=True,null=True)
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    def __str__(self):
        return self.name + '//' + self.user.nickname
    class Meta:
        verbose_name = '药品库'
        verbose_name_plural = '药品库'
####################********************************************************************************###################

class mdlMedicineNoteTask(models.Model):
    '''
    吃药提醒任务表，设置一个吃药时间，每次提醒可以同时吃几种药，每一个吃药时间为一条记录
    我们在设计网页时，需要在一个页面设置药品选择，主要从已有药品中选择，也可以让用户自己输入药品，对于用户输入的药品，
    如果数据库中没有记录，则添加到数据库中。
    在网页设计师，我们需要有一个起始日期，提醒天数(一般用户5天，VIP用户最长15天)，间隔天数(默认间隔1天)然后让用户可以添加至少4个时间段(如早上，中午，晚上等)，
    添加完成后，每一个时间段即为一条记录。
    邮件或短信提醒仅能用于已经通过验证了的邮箱和手机，如果用户没有经过验证，则让用户进行验证
    '''
    user = models.ForeignKey(mdlUserExtInfo)
    #在设计网页时，需要设置天数限制，不超过15天，需要设置间隔天数，默认间隔一天
    medicine = JSONField()  #要吃的药品名称,一次可以提醒同时吃几种药,用量用法
    tm = models.DateTimeField(verbose_name='吃药时间', null=False)  #注意，我们这里只有一个字段，但在网页设计时，需要设置至少4个时间段
    noteBeforeMinutes = models.PositiveSmallIntegerField(verbose_name='提前多少分钟提醒', default=10, null=True)
    noteByEmail = models.BooleanField(verbose_name='是否通过邮件提醒', default=True)
    noteByMobileMsg = models.BooleanField(verbose_name='是否通过手机短信提醒', default=True)
    class Meta:
        verbose_name = '用药提醒记录'
        verbose_name_plural = '用药提醒记录'

class mdlMedicineNoteCompletedRecord(models.Model):
    '''
    已经完成的吃药通知,在mdlMedicineNoteTask表中，每完成一条通知后，将其移到本表中
    '''
    user = models.ForeignKey(mdlUserExtInfo)
    #在设计网页时，需要设置天数限制，不超过15天，需要设置间隔天数，默认间隔一天
    medicine = JSONField()  #要吃的药品名称,一次可以提醒同时吃几种药,用量用法
    tm = models.DateTimeField(verbose_name='吃药时间', null=False)
    noteEmail = models.EmailField(verbose_name='通知的邮箱', null=True)
    emailNoteTime = models.DateTimeField(verbose_name='邮箱通知的时间', null=True)
    notePhone = models.CharField(verbose_name='手机号码',blank=True, default='', max_length=18)
    phoneNoteTime = models.DateTimeField(verbose_name='手机号通知的时间', null=True)
    class Meta:
        verbose_name = '用药提醒完成记录'
        verbose_name_plural = '用药提醒完成记录'
################################################我的常用设备############################################################
###建立每个人自己的设备库，这样我们可以统计，也可以在用户输入时，起到一个提示作用
######################################################################################################################
class mdlInstrument(models.Model):
    user = models.ForeignKey(mdlUserExtInfo)
    name = models.CharField(verbose_name='设备名称', blank=False,max_length=64)
    instrumentType = models.CharField(verbose_name='设备型号', blank=True, null=False, max_length=64, default='')
    instrumentSN = models.CharField(verbose_name='设备机身号', blank=True, null=False, max_length=64, default='')
    manufacture = models.CharField(verbose_name='生产商', blank=True, null=False, max_length=128, default='')
    seller = models.CharField(verbose_name='销售商', blank=True, null=False, max_length=128, default='')
    price = models.PositiveIntegerField(verbose_name='价格', blank = True, null=False, default=0)
    sellerPhoneNum = models.CharField(verbose_name='销售商电话', blank = True,default='', null=False, max_length=18)
    servicePhoneNum = models.CharField(verbose_name='服务商电话',blank = True, default='', null=False, max_length=18)
    buyDateTime = models.DateTimeField(verbose_name='购买时间', blank=True, null=False, default = '1900-01-01')
    demoInfo = models.CharField(verbose_name='其它信息', default='', blank=True, null=False, max_length=128)
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    class Meta:
        verbose_name = '常用设备'
        verbose_name_plural = '常用设备'
####################********************************************************************************###################

###############################################我的常用医疗机构#######################################################
###设置常用医疗机构信息字段，这样在用户输入医疗机构时，我们可以给他提示信息，他只需从列表中选择即可
######################################################################################################################
class mdlmyMedicalOrgnization(models.Model):
    user = models.ForeignKey(mdlUserExtInfo)
    name = models.CharField(verbose_name='医院名称', blank=False, null=False, max_length=256)
    addressline1 = models.CharField(verbose_name='地址行1',blank=True,default='',max_length=128)
    addressline2 = models.CharField(verbose_name='地址行2',blank=True,default='',max_length=128)
    city = models.CharField(verbose_name='县市',blank=True,default='',max_length=32)
    state = models.CharField(verbose_name='省',blank=True,default='',max_length=32)
    zipcode = models.IntegerField(verbose_name='邮编', blank=True)
    phoneNum1 = models.CharField(verbose_name='服务电话1', default='', blank=True, max_length=18)
    phoneNum2 = models.CharField(verbose_name='服务电话2', default='', blank=True, max_length=18)
    phoneNum3 = models.CharField(verbose_name='服务电话3', default='', blank=True, max_length=18)
    demoInfo = models.CharField(verbose_name='其它信息', default='', blank=True, null=False, max_length=128)
    def __str__(self):
        return self.user.first_name + self.user.last_name + '//' + self.name
    class Meta:
        verbose_name = '我的常用医疗机构表'
        verbose_name_plural = '我的常用医疗机构表'
####################********************************************************************************###################

################################################我的常用医生############################################################
###建立每个人自己的医生库，这样我们可以统计，也可以在用户输入时，起到一个提示作用
######################################################################################################################
class mdlmyDoctorList(models.Model):
    user = models.ForeignKey(mdlUserExtInfo)
    doctorname = models.CharField(verbose_name='医生姓名', blank=False,max_length=32)
    department = models.CharField(verbose_name='科室', blank=True,max_length=32)
    orgnization = models.ForeignKey(mdlmyMedicalOrgnization)  #可以从我的医疗机构中选择，如果没有，则添加进去
    specialTech = models.CharField(verbose_name='专长', blank=True, max_length=256)
    phoneNum = models.CharField(verbose_name='联系电话', blank=True, max_length=18)
    demoInfo = models.CharField(verbose_name='其它信息', default='', blank=True, null=False, max_length=128)
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    class Meta:
        verbose_name = '常用医生'
        verbose_name_plural = '常用医生'
####################********************************************************************************###################

class mdlmyMedicineEatRecord(models.Model):
    '''
    吃药记录
    可以从我的药品库中提示药品名称，用法，用量
    '''
    user = models.ForeignKey(mdlUserExtInfo)
    #medicine = models.ForeignKey(mdlMedicineLib)
    medicine = models.CharField(verbose_name='药物',max_length=64)#药物名称
    method=models.CharField(verbose_name='用法',max_length=10)#用法
    how_use=models.CharField(verbose_name='用量',max_length=10)#用量
    eatTime = models.DateTimeField(verbose_name='吃药时间', blank=False, null=False)
    resultDescription = models.CharField(verbose_name='效果记录',default='', max_length=256)
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    class Meta:
        verbose_name = '吃药记录'
        verbose_name_plural = '吃药记录'

class mdlmyMedicalRecords(models.Model):
    '''
    我的病历记录，在这个网页设计时，我们可以添加一个提醒下次进行医疗的时间
    '''
    user = models.ForeignKey(mdlUserExtInfo)
    title = models.CharField(verbose_name='标题', default='无标题', max_length=64)
    #门诊病历、住院病历、检查数据、自我描叙
    RECORD_TYPE_OPTION = ((1,u'门诊病历'),(2,u'住院病历'),(3,u'检查数据'),(4,u'自我描叙'),)
    recordType = models.SmallIntegerField(verbose_name='病历类型', choices = RECORD_TYPE_OPTION, blank=False, null=False, default='4')
    hospital = models.CharField(verbose_name='检查医院',default='', max_length=64) #这里我们从前面的医疗机构中提示，存入医院名字
    doctor = models.CharField(verbose_name='医生',default='', max_length=64) #这里我们从前面的医生中提示，存入医生名字
    RecordOccurTime = models.DateTimeField(verbose_name='病历产生时间', blank=False, null=False, auto_now_add=True)
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    symptomDescription = models.CharField(verbose_name='症状文字描述',default='', max_length=1024)
    diagnosis = models.CharField(verbose_name='诊断结论文字描述',default='', max_length=1024)
    #最多一次上传5段录音文件,普通用户一次只能上传1段语音描述,时长10秒，VIP用户一次30秒
    voiceDescription0 = models.FileField(verbose_name='语音描述症状0',upload_to='MRVoice/%Y/%m/%d', blank=True,null=True)
    voiceDescription1 = models.FileField(verbose_name='语音描述症状1',upload_to='MRVoice/%Y/%m/%d', blank=True,null=True)
    voiceDescription2 = models.FileField(verbose_name='语音描述症状2',upload_to='MRVoice/%Y/%m/%d', blank=True,null=True)
    voiceDescription3 = models.FileField(verbose_name='语音描述症状3',upload_to='MRVoice/%Y/%m/%d', blank=True,null=True)
    voiceDescription4 = models.FileField(verbose_name='语音描述症状4',upload_to='MRVoice/%Y/%m/%d', blank=True,null=True)
    #图片记录，普通用户一次只能上传2张图片，VIP可以上传8张图片
    imageRecord0 = models.FileField(verbose_name='图像记录',upload_to='MRImage/%Y/%m/%d', blank=True,null=True)
    imageRecord1 = models.FileField(verbose_name='图像记录',upload_to='MRImage/%Y/%m/%d', blank=True,null=True)
    imageRecord2 = models.FileField(verbose_name='图像记录',upload_to='MRImage/%Y/%m/%d', blank=True,null=True)
    imageRecord3 = models.FileField(verbose_name='图像记录',upload_to='MRImage/%Y/%m/%d', blank=True,null=True)
    imageRecord4 = models.FileField(verbose_name='图像记录',upload_to='MRImage/%Y/%m/%d', blank=True,null=True)
    imageRecord5 = models.FileField(verbose_name='图像记录',upload_to='MRImage/%Y/%m/%d', blank=True,null=True)
    imageRecord6 = models.FileField(verbose_name='图像记录',upload_to='MRImage/%Y/%m/%d', blank=True,null=True)
    imageRecord7 = models.FileField(verbose_name='图像记录',upload_to='MRImage/%Y/%m/%d', blank=True,null=True)

    class Meta:
        verbose_name = '病历记录'
        verbose_name_plural = '病历记录'
        ordering=['-upload_datetime']#查询数据库时按时间降序排列
#########################################################################################################################################
#########################################################################################################################################
###########################################################荧光仪器数据模################################################################
class mdlmyFluorescenceData(models.Model):
    '''
    我的荧光仪器测试数据
    '''
    #item = models.CharField(verbose_name='测试项目', default='无', max_length=64)
    testtime = models.DateTimeField(verbose_name='测试时间', blank=False, null=False, auto_now_add=True, editable=False)
    #result = models.CharField(verbose_name='', default='无', max_length=256)
    test_reaction_time = models.PositiveIntegerField(verbose_name='测试超时时间', blank=False, null=False)
    temperature = models.FloatField(verbose_name='测试环境温度', blank=False, null=False)
    temperature2 = models.FloatField(verbose_name='测试检测卡温度', blank=False, null=False)
    fluorescence_data = models.CharField(verbose_name='测试曲线', default='无', max_length=2000)
    Cposition = models.PositiveIntegerField(verbose_name='C线位置', default='无')
    Baseposition = models.PositiveIntegerField(verbose_name='基线线位置', default='无')
    Tposition = models.PositiveIntegerField(verbose_name='T线位置', default='无')
    resultratio = models.FloatField(verbose_name='测试峰高比', default='无')
    resultprimitive = models.FloatField(verbose_name='测试原始结果', default='无')
    resultcalibration = models.FloatField(verbose_name='测试校准结果', default='无')
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    testSampleID = models.CharField(verbose_name='测试样品ID', default='无', max_length=20)
    DeviceID = models.CharField(verbose_name='设备ID', default='无', max_length=20)
    testCardID = models.CharField(verbose_name='测试卡ID', default='无', max_length=20)
    class Meta:
        verbose_name = '荧光仪器测试数据'
        verbose_name_plural = '荧光仪器测试数据'
        ordering=['-upload_datetime']#查询数据库时按时间降序排列

class mdlmyFluorescenceInfo(models.Model):
    '''
    荧光设备信息
    '''
    id1 = models.CharField(verbose_name='设备ID', default='无', max_length=16)
    name  = models.CharField(verbose_name='设备名称', default='无', max_length=32)
    manufacture = models.CharField(verbose_name='设备制造商', default='无', null=True, max_length=32)
    tel = models.CharField(verbose_name='设备制造商电话', default='无',  null=True, max_length=32)
    status = models.CharField(verbose_name='在线状态', default='无',  null=True, max_length=32)
    statustime = models.DateTimeField(verbose_name='状态提交时间', blank=False,  null=True, auto_now=True)
    address = models.CharField(verbose_name='设备使用地址', default='无', max_length=16)
    needmainten = models.CharField(verbose_name='是否需要维修', default='无', max_length=32)
    class Meta:
        verbose_name = '荧光设备信息'
        verbose_name_plural = '荧光设备信息'

class mdlmyFluorescenceTester(models.Model):
    '''
    设备操作人员信息
    '''
    tester = models.ForeignKey(mdlmyFluorescenceInfo) #设备
    name = models.CharField(verbose_name='姓名', default='无', max_length=16)
    sex  = models.CharField(verbose_name='性别', default='无', max_length=8)
    age = models.SmallIntegerField(verbose_name='年龄', blank=False, null=False)
    deviceID = models.CharField(verbose_name='设备ID', default='无', max_length=500)
    contact_information = models.CharField(verbose_name='电话', default='无', max_length=128)
    position = models.CharField(verbose_name='职务', default='无', max_length=64)
    demo = models.CharField(verbose_name='备注', default='无', max_length=64)
    class Meta:
        verbose_name = '测试人员信息'
        verbose_name_plural = '测试人员信息'

class mdlmyTestCard(models.Model):
    '''
    检测卡信息
    '''
    id1 = models.CharField(verbose_name='检测卡编号', default='无', max_length=16)
    units  = models.CharField(verbose_name='检测卡项目', default='无', max_length=32)
    normal_value = models.FloatField(verbose_name='正常值',null=True)
    lowest_value = models.FloatField(verbose_name='最低检测线',null=True)
    highest_value = models.FloatField(verbose_name='最高检测线',null=True)
    result_unit = models.CharField(verbose_name='测试结果单位', default='无', max_length=16,null=True)
    T = models.IntegerField(verbose_name='T线位置',null=True)
    StandardCurveNumber = models.IntegerField(verbose_name='标准曲线数目',null=True)
    a1 = models.FloatField(verbose_name='曲线1-a',null=True)
    b1 = models.FloatField(verbose_name='曲线1-b',null=True)
    c1 = models.FloatField(verbose_name='曲线1-c',null=True)
    a2 = models.FloatField(verbose_name='曲线2-a',null=True)
    b2 = models.FloatField(verbose_name='曲线2-b',null=True)
    c2 = models.FloatField(verbose_name='曲线2-c',null=True)
    C = models.IntegerField(verbose_name='C线位置',null=True)
    reaction_time = models.IntegerField(verbose_name='试剂反应时间',null=True)
    made_time = models.DateTimeField(verbose_name='生产日期', blank=False, null=True)
    valid_time = models.DateTimeField(verbose_name='过期时间', blank=False, null=False)
    class Meta:
        verbose_name = '检测卡信息'
        verbose_name_plural = '检测卡信息'

class mdlmyTestPeopleInfo(models.Model):
    '''
    样品信息
    '''
    id1 = models.CharField(verbose_name='样品', default='无', max_length=16)
    name = models.CharField(verbose_name='姓名', default='无', max_length=16)
    sex  = models.CharField(verbose_name='性别', default='无', max_length=8)
    age = models.SmallIntegerField(verbose_name='年龄', blank=False, null=False)
    remark  = models.CharField(verbose_name='备注', default='无', max_length=32)
    departments = models.CharField(verbose_name='科室', default='无', max_length=32)
    class Meta:
        verbose_name = '样品信息'
        verbose_name_plural = '样品信息'

class mdlmyReport(models.Model):
    '''
    我的报告信息
    '''
    user = models.ForeignKey(mdlUserExtInfo)
    test_data = models.OneToOneField(mdlmyFluorescenceData) #测试数据
    tester = models.ForeignKey(mdlmyFluorescenceTester)# 测试人
    deviceInfo = models.ForeignKey(mdlmyFluorescenceInfo) #测试设备
    test_card = models.OneToOneField(mdlmyTestCard) #测试卡
    sample = models.OneToOneField(mdlmyTestPeopleInfo) #测试样品

    state = models.CharField(verbose_name='报告状态', default='无', max_length=64)
    result = models.CharField(verbose_name='报告结果', default='无', max_length=256)
    upload_datetime = models.DateTimeField(verbose_name='上传时间', blank=False, null=False, auto_now_add=True, editable=False)
    class Meta:
        verbose_name = '报告记录'
        verbose_name_plural = '报告记录'
        ordering=['-upload_datetime']#查询数据库时按时间降序排列

class mdlmyCardUseInfo(models.Model):
    '''
    卡领用记录信息
    '''
    name = models.CharField(verbose_name='项目名称', default='无', max_length=64)
    number = models.PositiveIntegerField(verbose_name='数量', blank=False, null=False)
    whouse = models.CharField(verbose_name='领用人', default='无', max_length=256)
    use_datetime = models.DateTimeField(verbose_name='领用时间', blank=False, null=False, auto_now_add=True, editable=False)
    valid_time = models.DateTimeField(verbose_name='有效期', blank=False, null=False, auto_now_add=True, editable=False)
    storage_conditions = models.CharField(verbose_name='储存条件', default='无', max_length=32)
    batch_number = models.CharField(verbose_name='卡批号', default='无', max_length=256)
    deviceid = models.CharField(verbose_name='机器ID', default='无', max_length=256)
    class Meta:
        verbose_name = '卡领用记录信息'
        verbose_name_plural = '卡领用记录信息'
        ordering=['-use_datetime']#查询数据库时按时间降序排列

class mdlmyStorageTable(models.Model):
    '''
    库存表
    '''
    name = models.CharField(verbose_name='项目名称', default='无', max_length=64)
    number = models.PositiveIntegerField(verbose_name='数量', blank=False, null=False)
    deviceid = models.CharField(verbose_name='机器ID', default='无', max_length=256)
    class Meta:
        verbose_name = '库存表'
        verbose_name_plural = '库存表'

########################################################荧光仪器数据模型完###############################################################
#########################################################################################################################################
###################################################用户动态##########################################################
###
#####################################################################################################################
class scContent(models.Model):
    uid = models.ForeignKey(mdlUserExtInfo)
    text = models.CharField(verbose_name='文字内容', default='', max_length=1000)
    img1 = models.FileField(verbose_name='图片1',upload_to='SC/%Y/%m/%d', blank=True,null=True)
    img2 = models.FileField(verbose_name='图片2',upload_to='SC/%Y/%m/%d', blank=True,null=True)
    img3 = models.FileField(verbose_name='图片3',upload_to='SC/%Y/%m/%d', blank=True,null=True)
    time = models.DateTimeField(verbose_name='发表时间', blank=False, null=False, auto_now_add=True, editable=False)
    comment_counts=models.PositiveIntegerField(verbose_name='评论数',default=0)
    def __str__(self):
        return str(self.uid) + ": " +self.text
    class Meta:
        verbose_name = '用户动态'
        verbose_name_plural = '用户动态'
        ordering=['-time']#查询数据库时按时间降序排列
###################################################用户评论##########################################################
###
#####################################################################################################################
class scComment(models.Model):
    uid = models.ForeignKey(mdlUserExtInfo,related_name='scCommentuid_set')
    wid = models.ForeignKey(scContent,related_name='scComment_set')
    ctext = models.CharField(verbose_name='文字内容', default='', max_length=1000)
    time = models.DateTimeField(verbose_name='发表时间', blank=False, null=False, auto_now_add=True, editable=False)
    class Meta:
        verbose_name = '用户动态'
        verbose_name_plural = '用户动态'
        ordering=['-time']#查询数据库时按时间降序排列
    def __str__(self):
        return str(self.uid) + "to" + str(self.wid)

class scMessage(models.Model):
    uid = models.ForeignKey(mdlUserExtInfo,related_name='mdlUserExtInfo_uid_set')
    uid2 = models.ForeignKey(mdlUserExtInfo,related_name='mdlUserExtInfo_uid2_set')
    text = models.CharField(verbose_name='文字内容', default='', max_length=1000)
    time = models.DateTimeField(verbose_name='发表时间', blank=False, null=False, auto_now_add=True, editable=False)
    def __str__(self):
        return str(self.uid) + "to" + str(self.uid2)
    class Meta:
        verbose_name = '用户动态'
        verbose_name_plural = '用户动态'
        ordering=['-time']#查询数据库时按时间降序排列
