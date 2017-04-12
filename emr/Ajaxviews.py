from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.shortcuts import render_to_response, redirect, render
from captcha.fields import CaptchaField
from django.template import RequestContext
from emr.models import mdlUserExtInfo,mdlbloodpressure,mdlbloodglucose,mdlbodyTemperature,mdlMedicineLib,mdlInstrument,mdlmyMedicalOrgnization,mdlmyDoctorList,mdlmyMedicineEatRecord,mdlmyMedicalRecords
from emr import models
import re
from django.contrib.auth.decorators import login_required
import os,uuid
import datetime
from PIL import ImageFile
from SuperEMR import settings
import random
import string
from django.core.mail import send_mail
from rongcloud import RongCloud
# Create your views here.
######################################################################################################################
##################################################个人信息更改########################################################
@login_required#登录后才可以上传
def PersonChange(request):
    UserExtInfo=request.user.mdluserextinfo
    ChangeInfo=request.GET
    error='0'
    try:#sex 字段存在
        if UserExtInfo.sex==2 and int(ChangeInfo['sex']) != UserExtInfo.sex:
            UserExtInfo.sex = int(ChangeInfo['sex'])
    except:
        error='1'
    try:#datebirth 字段存在
        if ChangeInfo['datebirth'] != UserExtInfo.datebirth.strftime('%Y-%m-%d'):
            UserExtInfo.datebirth = ChangeInfo['datebirth']
    except:
        error='1'
    try:#educationbackground 字段存在
        if int(ChangeInfo['educationbackground']) != UserExtInfo.educationbackground:
            UserExtInfo.educationbackground = int(ChangeInfo['educationbackground'])
    except:
        error='1'
    try:#state 字段存在
        if ChangeInfo['state'] == '0':
            UserExtInfo.state = '00'
        else:
            if int(ChangeInfo['state']) != int(UserExtInfo.state[0:2]):
                UserExtInfo.state = ChangeInfo['state']+ChangeInfo['_state']
    except:
        error='1'
    try:#city 字段存在
        if ChangeInfo['city'] == '0':
            UserExtInfo.city = '00'
        else:
            if int(ChangeInfo['city'][2:4]) != int(UserExtInfo.city[0:2]):
                UserExtInfo.city = ChangeInfo['city'][2:4]+ChangeInfo['_city']
    except:
        error='1'
    try:#district 字段存在
        if ChangeInfo['district'] == '0':
            UserExtInfo.district = '00'
        else:
            if int(ChangeInfo['district'][4:6]) != int(UserExtInfo.district[0:2]):
                UserExtInfo.district = ChangeInfo['district'][4:6]+ChangeInfo['_district']
    except:
        error='1'
    try:#addressline1 字段存在
        if ChangeInfo['addressline1'] != UserExtInfo.addressline1:
            UserExtInfo.addressline1 = ChangeInfo['addressline1']
    except:
        error='1'
    try:#addressline2 字段存在
        if ChangeInfo['addressline2'] != UserExtInfo.addressline2:
            UserExtInfo.addressline2 = ChangeInfo['addressline2']
    except:
        error='1'
    try:#uniqEmail 字段存在
        if UserExtInfo.is_uniqEmailActivated == False and ChangeInfo['uniqEmail'] != UserExtInfo.uniqEmail:
            UserExtInfo.uniqEmail = ChangeInfo['uniqEmail']
    except:
        error='1'
    try:#uniqMobilePhone 字段存在
        if UserExtInfo.is_uniqMobilePhoneActivated == False and ChangeInfo['uniqMobilePhone'] != UserExtInfo.uniqMobilePhone:
            UserExtInfo.uniqMobilePhone = ChangeInfo['uniqMobilePhone']
    except:
        error='1'
    try:
        UserExtInfo.save()
    except:
        error='1'
    return JsonResponse({"error":error})
######################################################################################################################

######################################################################################################################
##################################################个人密码更改########################################################
@login_required#登录后才可以上传
def change_password(request):
    username=request.user.username
    ChangeInfo=request.GET
    old_password=ChangeInfo['old_password']
    new_password=ChangeInfo['new_password']
    new_password1=ChangeInfo['new_password1']
    error='0'
    if new_password == new_password1 and new_password != '':
        user = authenticate(username=username,password=old_password)
        if user is not None:
          newuser = User.objects.get(username__exact=username)
          newuser.set_password(new_password)
          newuser.save()
        else:
            error='1'
    else:
        error='2'
    return JsonResponse({"error":error})

##################################################个人密码更改########################################################
#@login_required#登录后才可以上传
def find_password(request):
    ChangeInfo=request.GET
    username=ChangeInfo['username']
    email = ChangeInfo['email']
    try:
        #user = mdlUserExtInfo.objects.get(nickname__exact=username)
        user = User.objects.get(username__exact=username)
        if user.email != email:
            error = "username doesn't match email address."
            return JsonResponse({"error":error})
        e=1
    except:
        e=0
    if e  ==0 :
        error='username not exist'
    else:
        new_password=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        user.set_password(new_password)
        user.save()
        subject='超级病历-账号激活'
        context = "用户(" + user.username + ") 新密码: "+ new_password + " 请及时修改您的密码."
        send_mail(subject, context,settings.EMAIL_HOST_USER,[user.email,],fail_silently=False)
        error="new password has been send into your email"
    return JsonResponse({"error":error})
######################################################################################################################

######################################################################################################################
##################################################血压数据上传########################################################

#血压计数据录入表单
class BloodPressure(forms.Form):
    systolic_pressure=forms.IntegerField(label='收缩压',
                                         required=True,)#收缩压
    diastolic_pressure=forms.IntegerField(label='舒张压',
                                          required=True,)#舒张压
    heart_rate=forms.IntegerField(label='心率',
                                  required=True,)#心率
    measure_datetime=forms.DateTimeField(label='测量时间',
                                         required=True,)#测量时间
    demoInfo=forms.CharField(label='其他信息',
                             required=False,)

@login_required#登录后才可以上传血压计数据
def blood_pressure(request):
    bp=BloodPressure(request.GET)
    error='0'
    #user=request.user.mdluserextinfo
    user=request.user.mdluserextinfo
    if bp.is_valid():
        bp_data=bp.cleaned_data
        BP=mdlbloodpressure(user=user,
                            systolic_pressure=bp_data['systolic_pressure'],
                            diastolic_pressure=bp_data['diastolic_pressure'],
                            heart_rate=bp_data['heart_rate'],
                            measure_datetime=bp_data['measure_datetime'],
                            demoInfo=bp_data['demoInfo'])
        BP.save()
    else:
        error='1'
        #return JsonResponse({"error":error })
    #######################################################################
    #血压数据查询
    try:
        all_bp=user.mdlbloodpressure_set.all()[0:10]
    except:
        all_bp=[]
    measure_datetime=[]
    systolic_pressure=[]
    diastolic_pressure=[]
    heart_rate=[]
    for a_bp in all_bp:
        systolic_pressure.insert(0,a_bp.systolic_pressure)
        diastolic_pressure.insert(0,a_bp.diastolic_pressure)
        heart_rate.insert(0,a_bp.heart_rate)
        measure_datetime.insert(0,a_bp.measure_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        return JsonResponse({"systolic_pressure":systolic_pressure,
                             "diastolic_pressure":diastolic_pressure,
                             "heart_rate":heart_rate,
                             "measure_datetime":measure_datetime,
                             "error":error
                             })
    except:
        pass
######################################################################################################################

######################################################################################################################
##################################################血糖数据上传########################################################

#血糖计数据录入表单
class BloodGlucose(forms.Form):
    glucose=forms.FloatField(label='血糖',
                              required=True,)#收缩压
    measure_datetime=forms.DateTimeField(label='测量时间',
                                         required=True,)#测量时间
    demoInfo=forms.CharField(label='其他信息',
                             required=False,)

@login_required#登录后才可以上传血糖计数据
def blood_gluocose(request):
    bp=BloodGlucose(request.GET)
    error='0'
    user=request.user.mdluserextinfo
    if bp.is_valid():
        bp_data=bp.cleaned_data
        BP=mdlbloodglucose(user=user,
                           gluocose=bp_data['glucose'],
                           measure_datetime=bp_data['measure_datetime'],
                           demoInfo=bp_data['demoInfo'])
        BP.save()
    else:
        error='1'
        #return JsonResponse({"error":error })
    #######################################################################
    #血糖数据查询
    try:
        all_bp=user.mdlbloodglucose_set.all()[0:10]
    except:
        all_bp=[]
    measure_datetime=[]
    gluocose=[]
    for a_bp in all_bp:
        gluocose.insert(0,a_bp.gluocose)
        measure_datetime.insert(0,a_bp.measure_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        return JsonResponse({"gluocose":gluocose,
                             "measure_datetime":measure_datetime,
                             "error":error
                             })
    except:
        pass
######################################################################################################################

######################################################################################################################
##################################################体温数据上传########################################################

#血糖计数据录入表单
class Temperature(forms.Form):
    temperature=forms.FloatField(label='体温',
                              required=True,)#体温
    measure_datetime=forms.DateTimeField(label='测量时间',
                                         required=True,)#测量时间
    demoInfo=forms.CharField(label='其他信息',
                             required=False,)

@login_required#登录后才可以上传血糖计数据
def temperature(request):
    bp=Temperature(request.GET)
    error='0'
    user=request.user.mdluserextinfo
    if bp.is_valid():
        bp_data=bp.cleaned_data
        BP=mdlbodyTemperature(user=user,
                              temperature=bp_data['temperature'],
                              measure_datetime=bp_data['measure_datetime'],
                              demoInfo=bp_data['demoInfo'])
        BP.save()
    else:
        error='1'
        #return JsonResponse({"error":error })
    #######################################################################
    #体温数据查询
    try:
        all_bp=user.mdlbodytemperature_set.all()[0:10]
    except:
        all_bp=[]
    measure_datetime=[]
    temperature=[]
    for a_bp in all_bp:
        temperature.insert(0,a_bp.temperature)
        measure_datetime.insert(0,a_bp.measure_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        return JsonResponse({"temperature":temperature,
                             "measure_datetime":measure_datetime,
                             "error":error
                             })
    except:
        pass
######################################################################################################################

######################################################################################################################
##################################################药物数据上传########################################################

#药物数据录入表单-后期可更改必选之段 required=True
class Medication(forms.Form):
    name=forms.CharField(label='药品名称',
                          required=True,)
    pharmaceutical_factory=forms.CharField(label='生产厂家',
                                           required=False,)
    functionDescription=forms.CharField(label='功效描述',
                                        required=False,)
    price=forms.IntegerField(label='价格',
                             required=False,)
    seller=forms.CharField(label='销售商',
                           required=False,)
    sellerPhoneNum=forms.CharField(label='销售商电话',
                                   required=True,)
    method=forms.CharField(label='用法',
                           required=True,)
    how_use=forms.CharField(label='用量',
                            required=True,)
    resultsEval=forms.IntegerField(label='效果评价(1-10分)',
                                   required=False,)
    mark_image=forms.CharField(label='药品外观图片',#ImageField
                                required=False,)
    demoInfo=forms.CharField(label='其他信息',
                             required=False,)

@login_required#登录后才可以上传药物数据
def medication(request):
    bp=Medication(request.GET,request.FILES)
    error='0'
    user=request.user.mdluserextinfo
    if bp.is_valid():
        bp_data=bp.cleaned_data
        BP=mdlMedicineLib(user=user,
                          name=bp_data['name'],
                          pharmaceutical_factory=bp_data['pharmaceutical_factory'],
                          functionDescription=bp_data['functionDescription'],
                          price=bp_data['price'],
                          seller=bp_data['seller'],
                          sellerPhoneNum=bp_data['sellerPhoneNum'],
                          method=bp_data['method'],
                          how_use=bp_data['how_use'],
                          resultsEval=bp_data['resultsEval'],
                          mark_image=bp_data['mark_image'],
                          demoInfo=bp_data['demoInfo'])
        BP.save()
    else:
        error='1'
        #return JsonResponse({"error":error })
    #######################################################################
    try:
        a=[]
        if error=='0':
            a.append(BP.name)
            a.append(BP.pharmaceutical_factory)
            a.append(BP.functionDescription)
            a.append(BP.price)
            a.append(BP.seller)
            a.append(BP.sellerPhoneNum)
            a.append(BP.method)
            a.append(BP.how_use)
            a.append(BP.resultsEval)
            a.append(BP.demoInfo)
            a.append(BP.mark_image.url)
        return JsonResponse({"error":error,
                             "new_medication":a
                             })
    except:
        pass

@login_required#登录后才可以获取药品数据
def medication_table(request):
    user=request.user.mdluserextinfo
    try:
        medications=user.mdlmedicinelib_set.all()
        data=[]
        for medication in medications:
            a=[]
            a.append(medication.name)
            a.append(medication.pharmaceutical_factory)
            a.append(medication.functionDescription)
            a.append(medication.price)
            a.append(medication.seller)
            a.append(medication.sellerPhoneNum)
            a.append(medication.method)
            a.append(medication.how_use)
            a.append(medication.resultsEval)
            a.append(medication.demoInfo)
            a.append(medication.mark_image.url)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass

#上传图片函数
def upload_picture(file,dirpath):
    '''''图片上传函数'''
    if file:
        path=os.path.join(settings.MEDIA_ROOT,dirpath+datetime.datetime.now().strftime('%Y/%m/%d'))
        if(not (os.path.exists((path)))):
            os.makedirs(path)
        file_name=str(uuid.uuid1())+'-'+file.name
        path_file=os.path.join(path,file_name)
        parser = ImageFile.Parser()
        for chunk in file.chunks():
            parser.feed(chunk)
        img = parser.close()
        try:
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(path_file)
        except:
            return False
        return dirpath+datetime.datetime.now().strftime('%Y/%m/%d')+'/'+file_name
    return False

#上传药品图片
@login_required#登录后才可以上传
def upload_mark_image(request):
    response=HttpResponse()
    response['Content-Type']="text/javascript"
    error="1"
    url=[]
    path=[]
    file = request.FILES.get("Filedata",None)
    if file:
        path=upload_picture(file,'MLImage/')
        if path:
            url=settings.MEDIA_URL+path
            error="0"
    response.write({'err':error,'img_url':url,'image_path':path})
    return response
######################################################################################################################

######################################################################################################################
####################################################设备添加##########################################################

#设备数据录入表单-后期可更改必选之段 required=True
class Device(forms.Form):
    name=forms.CharField(label='设备名称',
                          required=True,)
    instrumentType=forms.CharField(label='设备型号',
                                   required=False,)
    instrumentSN=forms.CharField(label='设备机身号',
                                 required=False,)
    price=forms.IntegerField(label='价格',
                             required=False,)
    seller=forms.CharField(label='销售商',
                           required=False,)
    sellerPhoneNum=forms.CharField(label='销售商电话',
                                   required=False,)
    manufacture=forms.CharField(label='生产商',
                                required=False,)
    servicePhoneNum=forms.CharField(label='服务商电话',
                                    required=False,)
    buyDateTime=forms.DateTimeField(label='购买时间',
                                    required=False,)
    demoInfo=forms.CharField(label='其他信息',
                             required=False,)

@login_required#登录后才可以添加设备
def add_device(request):
    bp=Device(request.GET,request.FILES)
    error='0'
    user=request.user.mdluserextinfo
    if bp.is_valid():
        bp_data=bp.cleaned_data
        BP= mdlInstrument(user=user,
                          name=bp_data['name'],
                          instrumentType=bp_data['instrumentType'],
                          instrumentSN=bp_data['instrumentSN'],
                          price=bp_data['price'],
                          seller=bp_data['seller'],
                          sellerPhoneNum=bp_data['sellerPhoneNum'],
                          manufacture=bp_data['manufacture'],
                          servicePhoneNum=bp_data['servicePhoneNum'],
                          buyDateTime=bp_data['buyDateTime'],
                          demoInfo=bp_data['demoInfo'])
        BP.save()
    else:
        error='1'
        #return JsonResponse({"error":error })
    #######################################################################
    try:
        a=[]
        if error=='0':
            a.append(BP.name)
            a.append(BP.instrumentType)
            a.append(BP.instrumentSN)
            a.append(BP.manufacture)
            a.append(BP.seller)
            a.append(BP.price)
            a.append(BP.sellerPhoneNum)
            a.append(BP.servicePhoneNum)
            a.append(BP.buyDateTime.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(BP.demoInfo)
            a.append(BP.upload_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        return JsonResponse({"error":error,
                             "new_device":a
                             })
    except:
        pass

@login_required#登录后才可以获取设备数据
def device_table(request):
    user=request.user.mdluserextinfo
    try:
        Instrument=user.mdlinstrument_set.all()
        data=[]
        for instrument in Instrument:
            a=[]
            a.append(instrument.name)
            a.append(instrument.instrumentType)
            a.append(instrument.instrumentSN)
            a.append(instrument.manufacture)
            a.append(instrument.seller)
            a.append(instrument.price)
            a.append(instrument.sellerPhoneNum)
            a.append(instrument.servicePhoneNum)
            a.append(instrument.buyDateTime.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(instrument.demoInfo)
            a.append(instrument.upload_datetime.strftime("%Y-%m-%d %H:%M:%S"))
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################

######################################################################################################################
##################################################医疗机构添加########################################################

#医疗机构数据录入表单-后期可更改必选之段 required=True
class Orgnization(forms.Form):
    name=forms.CharField(label='医院名称',
                          required=True,)
    addressline1=forms.CharField(label='地址行1',
                                   required=False,)
    addressline2=forms.CharField(label='地址行2',
                                 required=False,)
    city=forms.CharField(label='县市',
                             required=False,)
    state=forms.CharField(label='省',
                           required=False,)
    zipcode=forms.IntegerField(label='邮编',
                                   required=False,)
    phoneNum1=forms.CharField(label='服务电话1',
                                required=False,)
    phoneNum2=forms.CharField(label='服务电话2',
                                    required=False,)
    phoneNum3=forms.CharField(label='服务电话3',
                                    required=False,)
    demoInfo=forms.CharField(label='其他信息',
                             required=False,)

@login_required#登录后才可以添加设备
def add_orgnization(request):
    bp=Orgnization(request.GET)
    error='0'
    user=request.user.mdluserextinfo
    if bp.is_valid():
        bp_data=bp.cleaned_data
        if bp_data['zipcode']:
            zipcode=bp_data['zipcode']
        else:
            zipcode=0
        BP= mdlmyMedicalOrgnization(user=user,
                          name=bp_data['name'],
                          addressline1=bp_data['addressline1'],
                          addressline2=bp_data['addressline2'],
                          city=request.GET['_city'][2:4]+bp_data['city'],
                          state=request.GET['_state']+bp_data['state'],
                          zipcode=zipcode,
                          phoneNum1=bp_data['phoneNum1'],
                          phoneNum2=bp_data['phoneNum2'],
                          phoneNum3=bp_data['phoneNum3'],
                          demoInfo=bp_data['demoInfo'])
        BP.save()
    else:
        error='1'
        #return JsonResponse({"error":error })
    #######################################################################
    try:
        a=[]
        if error=='0':
            a.append(BP.name)
            a.append(BP.state)
            a.append(BP.city)
            a.append(BP.addressline1)
            a.append(BP.addressline2)
            a.append(BP.zipcode)
            a.append(BP.phoneNum1)
            a.append(BP.phoneNum2)
            a.append(BP.phoneNum3)
            a.append(BP.demoInfo)
        return JsonResponse({"error":error,
                             "new_orgnization":a
                             })
    except:
        pass

@login_required#登录后才可以获取数据
def orgnization_table(request):
    user=request.user.mdluserextinfo
    try:
        Orgnization=user.mdlmymedicalorgnization_set.all()
        data=[]
        for org in Orgnization:
            a=[]
            a.append(org.name)
            a.append(org.state)
            a.append(org.city)
            a.append(org.addressline1)
            a.append(org.addressline2)
            a.append(org.zipcode)
            a.append(org.phoneNum1)
            a.append(org.phoneNum2)
            a.append(org.phoneNum3)
            a.append(org.demoInfo)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################

######################################################################################################################
####################################################医生添加##########################################################

#医疗机构数据录入表单-后期可更改必选之段 required=True
class Doctor(forms.Form):
    doctorname=forms.CharField(label='医生姓名',
                          required=True,)
    department=forms.CharField(label='科室',
                                   required=False,)
    orgnization=forms.CharField(label='医疗机构',
                                 required=False,)
    specialTech=forms.CharField(label='专长',
                             required=False,)
    phoneNum=forms.CharField(label='联系电话',
                           required=False,)
    demoInfo=forms.CharField(label='其他信息',
                             required=False,)

@login_required#登录后才可以添加设备
def add_doctor(request):
    bp=Doctor(request.GET)
    error='0'
    user=request.user.mdluserextinfo
    if bp.is_valid():
        bp_data=bp.cleaned_data
        orgnization=mdlmyMedicalOrgnization.objects.get(name__exact=bp_data['orgnization'])
        BP= mdlmyDoctorList(user=user,
                          doctorname=bp_data['doctorname'],
                          department=bp_data['department'],
                          orgnization=orgnization,
                          specialTech=bp_data['specialTech'],
                          phoneNum=bp_data['phoneNum'],
                          demoInfo=bp_data['demoInfo'])
        BP.save()
    else:
        error='1'
        #return JsonResponse({"error":error })
    #######################################################################
    try:
        a=[]
        if error=='0':
            a.append(BP.doctorname)
            a.append(BP.department)
            a.append(BP.orgnization.name)
            a.append(BP.specialTech)
            a.append(BP.phoneNum)
            a.append(BP.demoInfo)
        return JsonResponse({"error":error,
                             "new_doctor":a
                             })
    except:
        pass

@login_required#登录后才可以获取数据
def doctor_table(request):
    user=request.user.mdluserextinfo
    try:
        doctor=user.mdlmydoctorlist_set.all()
        data=[]
        for doc in doctor:
            a=[]
            a.append(doc.doctorname)
            a.append(doc.department)
            a.append(doc.orgnization.name)
            a.append(doc.specialTech)
            a.append(doc.phoneNum)
            a.append(doc.demoInfo)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################

######################################################################################################################
##################################################用药记录上传########################################################

#用药记录录入表单-后期可更改必选之段 required=True
class MedicineEatRecord(forms.Form):
    medicine=forms.CharField(label='药品名称',
                             required=True,)
    method=forms.CharField(label='用法',
                           required=False,)
    how_use=forms.CharField(label='用量',
                            required=False,)
    eatTime=forms.CharField(label='吃药时间',
                            required=False,)
    resultDescription=forms.CharField(label='效果记录',
                                      required=False,)

@login_required#登录后才可以上传药物数据
def Medicine_EatRecord(request):
    bp=MedicineEatRecord(request.GET,request.FILES)
    error='0'
    user=request.user.mdluserextinfo
    if bp.is_valid():
        bp_data=bp.cleaned_data
        medicine=mdlMedicineLib.objects.get(name__exact=bp_data['medicine'])
        BP=mdlmyMedicineEatRecord(user=user,
                                  medicine=medicine,
                                  method=bp_data['method'],
                                  how_use=bp_data['how_use'],
                                  eatTime=bp_data['eatTime'],
                                  resultDescription=bp_data['resultDescription'])
        BP.save()
    else:
        error='1'
        #return JsonResponse({"error":error })
    #######################################################################
    try:
        a=[]
        if error=='0':
            a.append(BP.medicine.name)
            a.append(BP.method)
            a.append(BP.how_use)
            a.append(BP.eatTime)
            a.append(BP.resultDescription)
        return JsonResponse({"error":error,
                             "new_medicationrecord":a
                             })
    except:
        pass

@login_required#登录后才可以获取用药记录数据
def medicationrecord_table(request):
    user=request.user.mdluserextinfo
    try:
        medicationrecord=user.mdlmymedicineeatrecord_set.all()
        data=[]
        for record in medicationrecord:
            a=[]
            a.append(record.medicine.name)
            a.append(record.method)
            a.append(record.how_use)
            a.append(record.eatTime)
            a.append(record.resultDescription)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################

######################################################################################################################
##################################################电子病历上传########################################################

#电子病历录入表单-后期可更改必选之段 required=True
class MedicalRecord(forms.Form):
    title=forms.CharField(label='标题',
                          required=True,)
    recordType=forms.IntegerField(label='病历类型',
                               required=True,)
    hospital=forms.CharField(label='检查医院',
                             required=True,)
    doctor=forms.CharField(label='医生',
                           required=True,)
    RecordOccurTime=forms.CharField(label='病历产生时间',
                                    required=True,)
    symptomDescription=forms.CharField(label='症状文字描述',
                                       required=True,)
    diagnosis=forms.CharField(label='诊断结论文字描述',
                              required=True,)
    voiceDescription0=forms.CharField(label='语音描述症状0',
                                      required=False,)
    imageRecord0=forms.CharField(label='图像记录',
                                 required=False,)

@login_required#登录后才可以上传药物数据
def medicalrecord_add(request):
    bp=MedicalRecord(request.GET,request.FILES)
    error='0'
    user=request.user.mdluserextinfo
    if bp.is_valid():
        bp_data=bp.cleaned_data
        BP = mdlmyMedicalRecords(user=user,
                                  title=bp_data['title'],
                                  recordType=bp_data['recordType'],
                                  hospital=bp_data['hospital'],
                                  doctor=bp_data['doctor'],
                                  RecordOccurTime=bp_data['RecordOccurTime'],
                                  symptomDescription=bp_data['symptomDescription'],
                                  diagnosis=bp_data['diagnosis'],
                                  imageRecord0=bp_data['imageRecord0'])
                                  #imageRecord0=bp_data['imageRecord0'])
        BP.save()
    else:
        error='1'
        #return JsonResponse({"error":error })
    #######################################################################
    try:
        a=[]
        if error=='0':
            a.append(BP.title)
            a.append(BP.recordType)
            a.append(BP.hospital)
            a.append(BP.doctor)
            a.append(BP.RecordOccurTime.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(BP.symptomDescription)
            a.append(BP.diagnosis)
            a.append(BP.imageRecord0.url)
        return JsonResponse({"error":error,
                             "new_medicalrecord":a
                             })
    except:
        pass

#上传电子病历图片描述
@login_required#登录后才可以上传
def upload_imageRecord(request):
    response=HttpResponse()
    response['Content-Type']="text/javascript"
    error="1"
    url=[]
    path=[]
    file = request.FILES.get("Filedata",None)
    if file:
        path=upload_picture(file,'MRVoice/')
        if path:
            url=settings.MEDIA_URL+path
            error="0"
    response.write({'err':error,'img_url':url,'image_path':path})
    return response

@login_required#登录后才可以获取用药记录数据
def medicalrecord_table(request):
    #user=request.user.mdluserextinfo
    try:
        #medicalrecord=user.mdlmymedicalrecords_set.all()
        patientName = request.GET['patientName']
        user = mdlUserExtInfo.objects.get(nickname__exact=patientName)
        medicalrecord=user.mdlmymedicalrecords_set.all()
        #medicalrecord = mdlmyMedicalRecords.objects.filter(user__exact=patientName)
        data=[]
        for record in medicalrecord:
            a=[]
            a.append(record.title)
            a.append(record.recordType)
            a.append(record.hospital)
            a.append(record.doctor)
            a.append(record.RecordOccurTime.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(record.symptomDescription)
            a.append(record.diagnosis)
            a.append(record.imageRecord0.url)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################

@login_required#登录后才可以获取用药记录数据
def searchPatient(request):
    #user=request.user.mdluserextinfo
    user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['patientID'])
    if not user:
        error="1"
        username=''
        uniqEmail=''
    else:
        error="0"
        username=user[0].nickname
        uniqEmail=user[0].uniqEmail
    return JsonResponse({'error':error,'username':username,'uniqEmail':uniqEmail})
######################################################################################################################

@login_required#登录后才可以获取用药记录数据
def addPatient(request):
    doctor_user=request.user.mdluserextinfo
    user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['username'])
    if not user:
        error="用户不存在"
    else:
        if user[0].user_type != 'A':
            error='该用户不是病人'
        else:
            doctor_user.relative_user.add(user[0])
            doctor_user.save()
            error="用户添加成功"
    return JsonResponse({'error':error})

#@login_required#
def operate_relative_user(request):
    error = ''
    try:
        publicName = mdlUserExtInfo.objects.filter(nickname__exact=request.POST['publicName'])
        doctorName = mdlUserExtInfo.objects.filter(nickname__exact=request.POST['doctorName'])
        if not publicName or not doctorName:
            error="doctorName or publicName not exist"
        else:
            if publicName[0].user_type != 'D' or  (doctorName[0].user_type != 'B'and doctorName[0].user_type != 'A'):
                error='user type doen not match '
            else:
                rcloud = RongCloud(settings.app_key, settings.app_secret)
                if request.POST['optation'] == 'add':
                    publicName[0].relative_user.add(doctorName[0])
                    publicName[0].save()
                    r = rcloud.Group.join(doctorName[0].user,publicName[0].user,publicName[0].nickname)
                    # error=r#"adding member successful"
                    HttpResponse(r)
                elif request.POST['optation'] == 'delete':
                    publicName[0].relative_user.remove(doctorName[0])
                    publicName[0].save()
                    r = rcloud.Group.quit(doctorName[0].user,publicName[0].user)
                    # error=r#"deleting member successful"
                    HttpResponse(r)
    except:
        error = 'error occur'
    return JsonResponse({'error':error})
######################################################################################################################

######################################################################################################################
#添加荧光仪器测试数据
#@login_required#登录后才可以添加荧光仪器测试数据
def FluorescenceData(request):
    #doctor_user=request.user.mdluserextinfo
    #user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['user'])
    myid = ""
    if not request.GET:
        error="1"
    else:
        error="0"
        try:
            FD = models.mdlmyFluorescenceData(item=request.GET['item'],
                                          testtime=request.GET['testtime'],
                                          result=request.GET['result'],
                                          test_reaction_time=request.GET['test_reaction_time'],
                                          temperature=request.GET['temperature'],
                                          fluorescence_data=request.GET['fluorescence_data'],
                                          Cposition=request.GET['Cposition'],
                                          Baseposition=request.GET['Baseposition'],
                                          T1position=request.GET['T1position'],
                                          T2position=request.GET['T2position'],
                                          T3position=request.GET['T3position'],
                                          T4position=request.GET['T4position'],
                                          upload_datetime=request.GET['upload_datetime']
                                        )
            FD.save()
            myid = FD.id
        except:
            error="1"
    return JsonResponse({'error':error,"id":myid})
######################################################################################################################
######################################################################################################################
#添加荧光设备信息
#@login_required#登录后才可以添加荧光仪器测试数据
def FluorescenceInfo(request):
    #doctor_user=request.user.mdluserextinfo
    #user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['user'])
    myid = ""
    if not request.GET:
        error="1"
    else:
        error="0"
        try:
            FI = models.mdlmyFluorescenceInfo(id1=request.GET['id1'],
                                          units=request.GET['units'],
                                          result=request.GET['result'],
                                          install_time=request.GET['install_time'],
                                          responsibel_man=request.GET['responsibel_man'],
                                          use_state=request.GET['use_state'],
                                          maintain=request.GET['maintain']
                                        )
            FI.save()
            myid = FI.id
        except:
            error="1"
    return JsonResponse({'error':error,"id":myid})
######################################################################################################################
######################################################################################################################
#设备操作人员信息
#@login_required#登录后才可以添加荧光仪器测试数据
def FluorescenceTester(request):
    #doctor_user=request.user.mdluserextinfo
    #user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['user'])
    deviceInfo =models.mdlmyFluorescenceInfo.objects.filter(id__exact=request.GET['tester'])
    myid = ""
    if not request.GET:
        error="1"
    else:
        error="0"
        try:
            FT = models.mdlmyFluorescenceTester(tester=deviceInfo,
                                          name=request.GET['name'],
                                          sex=request.GET['sex'],
                                          age=request.GET['age'],
                                          fluorescence_data=request.GET['fluorescence_data'],
                                          head_portrait=request.GET['head_portrait'],
                                          contact_information=request.GET['contact_information'],
                                          position=request.GET['position']
                                        )
            FT.save()
            myid = FT.id
        except:
            error="1"
    return JsonResponse({'error':error,"id":myid})
######################################################################################################################
######################################################################################################################
#检测卡信息
#@login_required#登录后才可以添加
def myTestCard(request):
    #doctor_user=request.user.mdluserextinfo
    #user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['user'])
    myid = ""
    if not request.GET:
        error="1"
    else:
        error="0"
        try:
            FT = models.mdlmyTestCard(id1=request.GET['id1'],
                                          units=request.GET['units'],
                                          reaction_time=request.GET['reaction_time'],
                                          batch_number=request.GET['batch_number'],
                                          valid_time=request.GET['valid_time'],
                                          normal_range=request.GET['normal_range'],
                                          normal_parameter=request.GET['normal_parameter'],
                                          storage_conditions=request.GET['storage_conditions']
                                        )
            FT.save()
            myid = FT.id
        except:
            error="1"
    return JsonResponse({'error':error,"id":myid})
######################################################################################################################
######################################################################################################################
#样品信息
#@login_required#登录后才可以添加
def myTestPeopleInfo(request):
    #doctor_user=request.user.mdluserextinfo
    #user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['user'])
    myid = ""
    if not request.GET:
        error="1"
    else:
        error="0"
        try:
            FPI = models.mdlmyTestPeopleInfo(id1=request.GET['id1'],
                                          name=request.GET['name'],
                                          sex=request.GET['sex'],
                                          age=request.GET['age'],
                                          remark=request.GET['remark'],
                                          departments=request.GET['departments']
                                        )
            FPI.save()
            myid = FPI.id
        except:
            error="1"
    return JsonResponse({'error':error,"id":myid})
######################################################################################################################

######################################################################################################################
#我的报告信息
#@login_required#登录后才可以添加
def myReport(request):
    #doctor_user=request.user.mdluserextinfo
    user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['user'])
    test_data=models.mdlmyFluorescenceData.objects.filter(id__exact=request.GET['test_data'])
    tester =models.mdlmyFluorescenceTester.objects.filter(id__exact=request.GET['tester'])
    deviceInfo =models.mdlmyFluorescenceInfo.objects.filter(id__exact=request.GET['deviceInfo'])
    test_card =models.mdlmyTestCard.objects.filter(id__exact=request.GET['test_card'])
    sample =models.mdlmyTestPeopleInfo.objects.filter(id__exact=request.GET['sample'])
    myid = ""
    if not request.GET:
        error="1"
    else:
        error="0"
        try:
            FPI = models.mdlmyReport(user=user,
                                     test_data=test_data,
                                     tester=tester,
                                     deviceInfo=deviceInfo,
                                     test_card=test_card,
                                     sample =sample,
                                     state=request.GET['state'],
                                     result=request.GET['result'],
                                     upload_datetime=request.GET['upload_datetime']
                                        )
            FPI.save()
            myid = FPI.id
        except:
            error="1"
    return JsonResponse({'error':error,"id":myid})

######################################################################################################################
######################################################################################################################
#卡领用记录信息
#@login_required#登录后才可以添加
def myCardUseInfo(request):
    #doctor_user=request.user.mdluserextinfo
    user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['user'])
    myid = ""
    if not request.GET:
        error="1"
    else:
        error="0"
        try:
            CUI = models.mdlmyCardUseInfo(name=request.GET['name'],
                                          number=request.GET['number'],
                                          whouse=request.GET['whouse'],
                                          use_datetime=request.GET['use_datetime'],
                                          valid_time=request.GET['valid_time'],
                                          storage_conditions=request.GET['storage_conditions'],
                                          batch_number=request.GET['batch_number'],
                                          deviceid=request.GET['deviceid']
                                        )
            CUI.save()
            myid = CUI.id
        except:
            error="1"
    return JsonResponse({'error':error,"id":myid})
######################################################################################################################
######################################################################################################################
#库存表
#@login_required#登录后才可以添加
def myStorageTable(request):
    #doctor_user=request.user.mdluserextinfo
    user = mdlUserExtInfo.objects.filter(nickname__exact=request.GET['user'])
    myid = ""
    if not request.GET:
        error="1"
    else:
        error="0"
        try:
            CUI = models.mdlmyStorageTable(name=request.GET['name'],
                                          number=request.GET['number'],
                                          deviceid=request.GET['deviceid']
                                        )
            CUI.save()
            myid = CUI.id
        except:
            error="1"
    return JsonResponse({'error':error,"id":myid})
######################################################################################################################

@login_required#登录后才可以获取
def FluorescenceData_table(request):
    #user=request.user.mdluserextinfo
    try:
        #medicalrecord=user.mdlmymedicalrecords_set.all()
        patientName = request.GET['patientName']
        user = mdlUserExtInfo.objects.get(nickname__exact=patientName)
        myReport=user.mdlmyReport_set.all()
        #medicalrecord = mdlmyMedicalRecords.objects.filter(user__exact=patientName)
        data=[]
        for record in myReport:
            a=[]
            a.append(record.test_data.item)
            a.append(record.test_data.testtime.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(record.test_data.test_reaction_time.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(record.test_data.temperature)
            a.append(record.test_data.fluorescence_data)
            a.append(record.test_data.Cposition)
            a.append(record.test_data.Baseposition)
            a.append(record.test_data.T1position)
            a.append(record.test_data.T2position)
            a.append(record.test_data.T3position)
            a.append(record.test_data.T4position)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################
@login_required#登录后才可以获取
def FluorescenceInfo_table(request):
    #user=request.user.mdluserextinfo
    try:
        #medicalrecord=user.mdlmymedicalrecords_set.all()
        patientName = request.GET['patientName']
        user = mdlUserExtInfo.objects.get(nickname__exact=patientName)
        myReport=user.mdlmyReport_set.all()
        # myReport = models.mdlmyFluorescenceTester.objects.all()
        data=[]
        for record in myReport:
            a=[]
            a.append(record.deviceInfo.id1)
            a.append(record.deviceInfo.units)
            a.append(record.deviceInfo.install_time.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(record.deviceInfo.responsibel_man)
            a.append(record.deviceInfo.use_state)
            a.append(record.deviceInfo.maintain)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################
@login_required#登录后才可以获取
def FluorescenceTester_table(request):
    #user=request.user.mdluserextinfo
    try:
        #medicalrecord=user.mdlmymedicalrecords_set.all()
        patientName = request.GET['patientName']
        user = mdlUserExtInfo.objects.get(nickname__exact=patientName)
        myReport=user.mdlmyReport_set.all()
        # myReport = models.mdlmyFluorescenceTester.objects.all()
        data=[]
        for record in myReport:
            a=[]
            a.append(record.tester.tester)
            a.append(record.tester.name)
            a.append(record.tester.sex)
            a.append(record.tester.age)
            a.append(record.tester.fluorescence_data)
            a.append(record.tester.head_portrait)
            a.append(record.tester.contact_information)
            a.append(record.tester.position)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################
@login_required#登录后才可以获取
def TesterCard_table(request):
    #user=request.user.mdluserextinfo
    try:
        #medicalrecord=user.mdlmymedicalrecords_set.all()
        patientName = request.GET['patientName']
        user = mdlUserExtInfo.objects.get(nickname__exact=patientName)
        myReport=user.mdlmyReport_set.all()
        # myReport = models.mdlmyFluorescenceTester.objects.all()
        data=[]
        for record in myReport:
            a=[]
            a.append(record.test_card.id1)
            a.append(record.test_card.units)
            a.append(record.test_card.reaction_time.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(record.test_card.batch_number)
            a.append(record.test_card.valid_time.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(record.test_card.normal_range)
            a.append(record.test_card.normal_parameter)
            a.append(record.test_card.storage_conditions)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################
@login_required#登录后才可以获取
def TestPeopleInfo_table(request):
    #user=request.user.mdluserextinfo
    try:
        #medicalrecord=user.mdlmymedicalrecords_set.all()
        patientName = request.GET['patientName']
        user = mdlUserExtInfo.objects.get(nickname__exact=patientName)
        myReport=user.mdlmyReport_set.all()
        # myReport = models.mdlmyFluorescenceTester.objects.all()
        data=[]
        for record in myReport:
            a=[]
            a.append(record.sample.id1)
            a.append(record.sample.name)
            a.append(record.sample.sex)
            a.append(record.sample.age)
            a.append(record.sample.remark)
            a.append(record.sample.departments)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################
@login_required#登录后才可以获取
def report_table(request):
    #user=request.user.mdluserextinfo
    data=[]
    try:
        #medicalrecord=user.mdlmymedicalrecords_set.all()
        patientName = request.GET['patientName']
        user = mdlUserExtInfo.objects.get(nickname__exact=patientName)
        myReport=user.mdlmyReport_set.all()
        # myReport = models.mdlmyFluorescenceTester.objects.all()
        for record in myReport:
            a=[]
            a.append(record.user)
            a.append(record.test_data)
            a.append(record.tester)
            a.append(record.deviceInfo)
            a.append(record.test_card)
            a.append(record.sample)
            a.append(record.state)
            a.append(record.result)
            a.append(record.upload_datetime.strftime("%Y-%m-%d %H:%M:%S"))
            data.append(a)
        return JsonResponse({'data':data})
    except:
        JsonResponse({'data':data})
        pass
######################################################################################################################
@login_required#登录后才可以获取
def CardUse_table(request):
    #user=request.user.mdluserextinfo
    try:
        myReport = models.mdlmyCardUseInfo.objects.all()
        data=[]
        for record in myReport:
            a=[]
            a.append(record.name)
            a.append(record.number)
            a.append(record.whouse)
            a.append(record.use_datetime.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(record.valid_time.strftime("%Y-%m-%d %H:%M:%S"))
            a.append(record.storage_conditions)
            a.append(record.batch_number)
            a.append(record.deviceid)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass

######################################################################################################################
@login_required#登录后才可以获取
def Storage_table(request):
    #user=request.user.mdluserextinfo
    try:
        myReport = models.mdlmyStorageTable.objects.all()
        data=[]
        for record in myReport:
            a=[]
            a.append(record.name)
            a.append(record.number)
            a.append(record.deviceid)
            data.append(a)
        return JsonResponse({'data':data})
    except:
        pass
######################################################################################################################
######################################################################################################################
#@login_required#登录后才可以获取
def getTime(request):
    time = datetime.datetime.now()
    return JsonResponse({'time':time.strftime("%Y%m%d%H%M%S")})

@login_required#登录后才可以获取用药记录数据
def setWorkday(request):
    doctor_user=request.user.mdluserextinfo
    user = mdlUserExtInfo.objects.filter(nickname__exact=request.POST['username'])
    if not user:
        error="医生不存在"
    else:
        if user[0].user_type != 'B':
            error='该用户不是医生'
        else:
            workday = int(request.POST['workday'])
            user[0].workday = workday
            user[0].save()
            error="设置成功"
    return JsonResponse({'error':error})