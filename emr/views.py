from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.shortcuts import render_to_response, redirect, render
from captcha.fields import CaptchaField
from django.template import RequestContext
from emr.models import mdlUserExtInfo
import re
from django.contrib.auth.decorators import login_required
from rongcloud import RongCloud
from SuperEMR import settings
from django.http import JsonResponse
# Create your views here.
######################################################################################################################
###################################################注册部分###########################################################
SHA1_RE = re.compile('^[a-f0-9]{40}$')
################################################
###################注册表单#####################
class frmRegister(forms.Form):
    username = forms.CharField(required=True,
                               label='用户名',
                               max_length=12,
                               error_messages={'required':'请输入用户名'},
                               widget=forms.TextInput(attrs={'placeholder':'不少于6个字符','class':'form-control'}))
    password = forms.CharField(required=True,
                               label='密码',
                               max_length=12,
                               min_length=3,
                               error_messages={'required':'请输入密码'},
                               widget=forms.PasswordInput(attrs={'placeholder':'密码', 'class':'form-control'}))
    password1 = forms.CharField(required=True,
                                label='密码确认',
                                max_length=12,
                                min_length=3,
                                error_messages={'required':'再次输入密码'},
                                widget=forms.PasswordInput(attrs={'placeholder':'密码', 'class':'form-control'}))
    email = forms.EmailField(required=True,
                             label='邮箱',
                             error_messages={'required':'请输入邮箱地址'},
                             widget=forms.TextInput(attrs={'placeholder':'电子邮箱','class':'form-control'}))
    is_patient = forms.ChoiceField(required=True,
                                   label='职业',
                                   widget=forms.RadioSelect,choices=(('doctor','医生'),('patient','病人')))
    captcha = CaptchaField(required=True,
                           label='验证码')

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('用户名、密码和邮箱为必填项')
        else:
            cleaned_data = super().clean()

            if cleaned_data['password'] != cleaned_data['password1']:
                self._errors["password"] = self.error_class([u"两个密码字段不一致"])

            if User.objects.filter(username__exact=cleaned_data['username']):
                self._errors["username"] = self.error_class([u"用户名已注册"])

            if User.objects.filter(email__exact=cleaned_data['email']):
                self._errors["email"] = self.error_class([u"邮箱已注册"])

            #return cleaned_data
################################################
###################注册视图#################
def regist(request):
    if request.method == 'POST':
        uf = frmRegister(request.POST)
        if uf.is_valid():
            cd=uf.cleaned_data#获得表单数据 python化
            #添加到数据库
            if cd['is_patient'] == 'patient':
                user_type = 'A' # 病人
            else:
                user_type = 'B' # 医生
            creat_user=User.objects.create_user(username= cd['username'],
                                           password=cd['password'],
                                           email=cd['email'])
            creat_user.mdluserextinfo.is_active=False
            creat_user.mdluserextinfo.user_type=user_type
            creat_user.mdluserextinfo.save()
            creat_user.save()
            if user_type != 'B':
                creat_user.mdluserextinfo.send_activation_email()
            return  HttpResponse('注册成功,请查收邮件激活账号')#HttpResponseRedirect('/emr/login')
    else:
        uf = frmRegister()
    return render_to_response('regist.html',
                              {'form':uf},
                              context_instance=RequestContext(request))
################################################
###################邮箱激活视图#################
def email_activate(request, email_activation_key):
    if SHA1_RE.search(email_activation_key):
        try:
            user_profile = mdlUserExtInfo.objects.get(email_activation_key__exact=email_activation_key)
        except :
            return HttpResponse('验证链接失效')#render_to_response('wrong_url.html', RequestContext(request, locals()))
        if not user_profile.email_activation_key_expired():
            user = user_profile.user
            user.is_active = True
            user.save()
            user_profile.email_activation_key = "账号已经激活"
            user_profile.is_uniqEmailActivated=True
            user_profile.save()
            return HttpResponse('账号' + user.username + '已激活')#render_to_response('activate_complete.html', RequestContext(request, locals()))
        else:
            return HttpResponseRedirect('/emr/login')#HttpResponse('账号已经激活')
    return HttpResponse('验证链接无效')

###################注册视图#################
@login_required#登录后才可以
def registTeam(request):
    if request.method == 'POST':
        try:
            if request.user.mdluserextinfo.user_type == 'B':
                creat_user=User.objects.create_user(username= request.POST['teamName'],
                                               password=request.POST['password'],
                                               email=request.POST['email'])
                creat_user.save()
                creat_user.mdluserextinfo.is_active=False
                creat_user.mdluserextinfo.nickname = request.POST['teamName']
                creat_user.mdluserextinfo.uniqMobilePhone = request.POST['telephone']
                creat_user.mdluserextinfo.user_type = 'D'
                creat_user.mdluserextinfo.subject = request.POST['majarRange']
                creat_user.mdluserextinfo.company = request.POST['serviceRegion']
                creat_user.mdluserextinfo.achivement = request.POST['serviceGoal']
                creat_user.mdluserextinfo.name = request.POST['Sponser']
                creat_user.mdluserextinfo.relative_user.add(request.user.mdluserextinfo)
                creat_user.mdluserextinfo.save()
                rcloud = RongCloud(settings.app_key, settings.app_secret)
                r = rcloud.Group.create(request.user.mdluserextinfo.user,
                                        creat_user.mdluserextinfo.user,
                                        creat_user.mdluserextinfo.nickname)
                return  HttpResponse(r)
                # return  HttpResponse('Team register is successful.')
            else:
                HttpResponse('support for patient only')
        except:
            return  HttpResponse('errer occur')
    else:
        return  HttpResponse('Method POST only')
###################################################注册部分完#########################################################

######################################################################################################################
###################################################登录部分###########################################################
###################登录表单#################
class frmLogin(forms.Form):
    username = forms.CharField(required=True,
            label='用户名',
            max_length=12,
            error_messages={'required':'请输入用户名'},
            widget=forms.TextInput(attrs={'placeholder':'登录名或昵称','class':'form-control'}))
    password = forms.CharField(required=True,
            label='密码',
            max_length=12,
            min_length=3,
            error_messages={'required':'请输入密码'},
            widget=forms.PasswordInput(attrs={'placeholder':'密码', 'class':'form-control'}))
    captcha = CaptchaField('验证码')

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('用户名和密码为必填项')
        else:
            cleaned_data = super().clean()
            if not User.objects.filter(username__exact=cleaned_data['username']):
                self._errors["username"] = self.error_class([u"用户名不存在"])
            else:
                #获取的表单数据与数据库进行比较
                user = authenticate(username=cleaned_data['username'],
                                    password=cleaned_data['password'])
                if user is None:
                    self._errors["password"] = self.error_class([u"密码不正确"])
            #return cleaned_data
###################登录视图#################
def login(request):
    if request.user.is_authenticated():#已经登录
        user = request.user.mdluserextinfo
        rcloud = RongCloud(settings.app_key, settings.app_secret)
        portraitUri=settings.ROOT_SITE + user.user_image.url
        r = rcloud.User.getToken(userId=user.user.pk, name=user.nickname, portraitUri=portraitUri)
        if r.result['code'] == 200:
            user.demo = r.result['token']
            user.save()
        return  HttpResponseRedirect('/emr/index')
    if request.method == 'POST':
        uf = frmLogin(request.POST)
        if uf.is_valid():
            cleaned_data=uf.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.mdluserextinfo.user_type == 'A':
                    return HttpResponse('用户(%s)是病人，目前仅对医生开放PC客户端!' % user.username)
                if user.is_active:
                    user_login(request, user)
                    response= HttpResponseRedirect('/emr/index')
                    #将username写入浏览器cookie,失效时间为3600
                    response.set_cookie('username',user.username,3600)
                    user = user.mdluserextinfo
                    rcloud = RongCloud(settings.app_key, settings.app_secret)
                    portraitUri=settings.ROOT_SITE + user.user_image.url
                    r = rcloud.User.getToken(userId=user.user.pk, name=user.nickname, portraitUri=portraitUri)
                    if r.result['code'] == 200:
                        user.demo = r.result['token']
                        user.save()
                        response.set_cookie('rongcloudToken',r.result['token'],3600*24)
                    return response
                else:
                    return HttpResponse('用户(%s)没有激活!' % user.username)
    else:
        uf = frmLogin()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))

def login2(request):
    if request.user.is_authenticated():#已经登录
        user = request.user.mdluserextinfo
        rcloud = RongCloud(settings.app_key, settings.app_secret)
        portraitUri=settings.ROOT_SITE + user.user_image.url
        r = rcloud.User.getToken(userId=user.user.pk, name=user.nickname, portraitUri=portraitUri)
        if r.result['code'] == 200:
            user.demo = r.result['token']
            user.save()
        res = {'type':user.user_type,
               'rongcloud':r.result}
        return JsonResponse(res)
        # return  HttpResponse(user.user_type)
    if request.method == 'POST':
        uf = frmLogin(request.POST)
        if uf.is_valid():
            cleaned_data=uf.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                # if user.mdluserextinfo.user_type == 'B':
                #     return HttpResponse('用户(%s) 不是是病人，目前仅对病人开放改接口!' % user.username)
                if user.is_active:
                    user_login(request, user)
                    user = request.user.mdluserextinfo
                    rcloud = RongCloud(settings.app_key, settings.app_secret)
                    portraitUri=settings.ROOT_SITE + user.user_image.url
                    r = rcloud.User.getToken(userId=user.user.pk, name=user.nickname, portraitUri=portraitUri)
                    if r.result['code'] == 200:
                        user.demo = r.result['token']
                        user.save()
                    res = {'type':user.user_type,
                           'rongcloud':r.result}
                    response=  JsonResponse(res)#登录成功
                    #将username写入浏览器cookie,失效时间为3600
                    response.set_cookie('username',user.nickname,3600)
                    return response
                else:
                    return HttpResponse('用户(%s)没有激活!' % user.username)
    else:
        uf = frmLogin()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))
###################登出视图#################
def logout(request):
    user_logout(request)
    response = HttpResponseRedirect('/emr/login')
    response.delete_cookie('username')#清理cookie里保存username
    return response
###################################################登录部分完#########################################################

######################################################################################################################
###################################################个人中心首页#######################################################
###################个人中心首页视图#################
@login_required#登录后才可以
def index(request):
    user=request.user.mdluserextinfo
    return render_to_response('index.html',{'user':user},context_instance=RequestContext(request))

###################################################个人中心首页完#####################################################

######################################################################################################################
###################################################设置###############################################################
###################设置视图#################
@login_required#登录后才可以
def setup(request):
    user=request.user.mdluserextinfo
    return render_to_response('setup.html',{'user':user},context_instance=RequestContext(request))

###################################################设置完#############################################################

######################################################################################################################
###################################################加载模板###########################################################
###################设置视图#################
@login_required#登录后才可以
def templates(request):
    user=request.user.mdluserextinfo
    html_name=request.GET['html_name']
    return render_to_response(html_name,{'user':user},context_instance=RequestContext(request))

###################################################加载模板完#########################################################

######################################################################################################################
###################################################设备模板###########################################################
###################设备视图#################
@login_required#登录后才可以
def device(request):
    user=request.user.mdluserextinfo
    return render_to_response('device.html',{'user':user},context_instance=RequestContext(request))

###################################################加载模板完#########################################################

######################################################################################################################
###################################################药物模板###########################################################
###################药物视图#################
@login_required#登录后才可以
def medication(request):
    user=request.user.mdluserextinfo
    return render_to_response('medication.html',{'user':user},context_instance=RequestContext(request))

###################################################加载模板完#########################################################

######################################################################################################################
#################################################医疗机构模板#########################################################
###################医疗机构视图#################
@login_required#登录后才可以
def orgnization(request):
    user=request.user.mdluserextinfo
    return render_to_response('orgnization.html',{'user':user},context_instance=RequestContext(request))

###################################################加载模板完#########################################################

######################################################################################################################
#################################################电子病历模板#########################################################
###################医疗记录视图#################
@login_required#登录后才可以
def medicaalrecord(request):
    user=request.user.mdluserextinfo
    return render_to_response('medicalrecord.html',{'user':user},context_instance=RequestContext(request))

###################################################加载模板完#########################################################