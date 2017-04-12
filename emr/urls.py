from django.conf.urls import patterns, url
from emr import views
from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),#登录
    # url(r'^auth/$', include('social_auth.urls')),
    url(r'^login/$',views.login,name = 'login'),#登录
    url(r'^login2/$',views.login2,name = 'login2'),#登录
    url(r'^logout/$',views.logout,name = 'logout'),#登出
    url(r'^regist/$',views.regist,name = 'regist'),#用户注册
    url(r'^registTeam/$',views.registTeam,name = 'registTeam'),#用户注册
    url(r'^regist/activate/(?P<email_activation_key>\w+)/$', views.email_activate,name = 'email_regist_active'),#用户注册激活
    url(r'^index/$',views.index,name = 'index'),#主页
    url(r'^setup/$',views.setup,name = 'setup'),#设置
    url(r'^templates/$',views.templates,name = 'templates'),#加载模板
    #url(r'^uploademr/$',views.emrUpLoad,name = 'uploadEMR'),#上传病历
    #url(r'^manageemr/$',views.manageemr,name = 'manageemr'),#病历管理
    url(r'^device/$',views.device,name = 'device'),#设备
    url(r'^medication/$',views.medication,name = 'medication'),#常用药品
    url(r'^orgnization/$',views.orgnization,name = 'orgnization'),#常用医疗机构
    url(r'^medicalrecord/$',views.medicaalrecord,name = 'medicaalrecord'),#电子病历
)
