from django.conf.urls import patterns, url
from emr import Ajaxviews
#Ajax
urlpatterns = patterns('',
    url(r'^PersonChange/$', Ajaxviews.PersonChange),#个人信息更改
    url(r'^change_password/$', Ajaxviews.change_password),# 更改密码
     url(r'^find_password/$', Ajaxviews.find_password),# 找回密码
    #url(r'^regist_username_check/$', Ajaxviews.username_check),#注册时用户名是否已被注册检测
    #url(r'^captcha/$', Ajaxviews.refresh_captcha),#验证码
    #url(r'^uploadEMR/$', Ajaxviews.uploadEMR),#上传电子病历-自我描述文本
    url(r'^upload_mark_image/$', Ajaxviews.upload_mark_image),#上传药品库-药品图片
    url(r'^upload_imageRecord/$', Ajaxviews.upload_imageRecord),#上传电子病历图片描述
    #url(r'^uploadVideo/$', Ajaxviews.uploadVideo),#上传电子病历-视频
    #url(r'^deleteEMR/$', Ajaxviews.deleteEMR),#上传电子病历-自我描述文本
    #url(r'^loadEMR/$', Ajaxviews.loadEMR),#上传电子病历-自我描述文本
    url(r'^blood_pressure/$', Ajaxviews.blood_pressure),#上传血压计数据
    url(r'^blood_gluocose/$', Ajaxviews.blood_gluocose),#上传血糖计数据
    url(r'^temperature/$', Ajaxviews.temperature),#上传体温计数据
    url(r'^medication_add/$', Ajaxviews.medication),#增加新药品
    url(r'^medication_table/$', Ajaxviews.medication_table),#药品表格
    url(r'^medicalrecord_add/$', Ajaxviews.medicalrecord_add),#增加电子病历
    url(r'^medicalrecord_table/$', Ajaxviews.medicalrecord_table),#电子病历表格
    url(r'^medicationrecord_add/$', Ajaxviews.Medicine_EatRecord),#增加用药记录
    url(r'^medicationrecord_table/$', Ajaxviews.medicationrecord_table),#用药记录表格
    url(r'^add_device/$', Ajaxviews.add_device),#添加新设备
    url(r'^device_table/$', Ajaxviews.device_table),#设备表格
    url(r'^add_orgnization/$', Ajaxviews.add_orgnization),#添加新医疗机构
    url(r'^orgnization_table/$', Ajaxviews.orgnization_table),#医疗机构表格
    url(r'^add_doctor/$', Ajaxviews.add_doctor),#添加新医生
    url(r'^doctor_table/$', Ajaxviews.doctor_table),#医生表格
    #url(r'^add_new_Record/$', Ajaxviews.add_new_Record),#增加服药记录
    url(r'^searchPatient/$', Ajaxviews.searchPatient),#搜寻病人
    url(r'^addPatient/$', Ajaxviews.addPatient),#添加病人
    url(r'^setworkday/$', Ajaxviews.setWorkday),#设置医生工作值班时间
    url(r'^operate_relative_user/$', Ajaxviews.operate_relative_user),# 操作公众号关联用户
    ##################################################################################
    ###荧光仪器
    url(r'^FluorescenceData/$', Ajaxviews.FluorescenceData),#添加荧光仪器测试数据
    url(r'^FluorescenceInfo/$', Ajaxviews.FluorescenceInfo),#添加荧光仪器设备信息
    url(r'^FluorescenceTester/$', Ajaxviews.FluorescenceTester),#设备操作人员信息
    url(r'^myTestCard/$', Ajaxviews.myTestCard),#添加检测卡信息
    url(r'^myTestPeopleInfo/$', Ajaxviews.myTestPeopleInfo),#添加样品信息
    url(r'^myReport/$', Ajaxviews.myReport),#添加报告信息
    url(r'^myCardUseInfo/$', Ajaxviews.myCardUseInfo),#卡领用记录信息
    url(r'^myStorageTable/$', Ajaxviews.myStorageTable),#库存表

    #荧光仪器 数据呈现
    url(r'^FluorescenceData_table/$', Ajaxviews.FluorescenceData_table),#荧光仪器测试数据表格
    url(r'^FluorescenceInfo_table/$', Ajaxviews.FluorescenceInfo_table),#荧光仪器设备信息表格
    url(r'^FluorescenceTester_table/$', Ajaxviews.FluorescenceTester_table),#设备操作人员信息
    url(r'^TesterCard_table/$', Ajaxviews.TesterCard_table),#检测卡信息
    url(r'^TestPeopleInfo_table/$', Ajaxviews.TestPeopleInfo_table),#样品信息
    url(r'^report_table/$', Ajaxviews.report_table),#报告信息
    url(r'^CardUse_table/$', Ajaxviews.CardUse_table),#卡领用记录
    url(r'^TesterCard_table/$', Ajaxviews.TesterCard_table),#检测卡信息
    url(r'^Storage_table/$', Ajaxviews.Storage_table),#库存表

    url(r'^getTime/$', Ajaxviews.getTime),#获取时间
)
