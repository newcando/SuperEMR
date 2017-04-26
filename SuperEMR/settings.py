"""
Django settings for SuperEMR project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=d*a+&nkb3ouec$x6uew9im+4uv5kb&akq@tn_f*p=dveyw-3r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',#这是验证码模块
    'emr',
    'rest_framework',
    'rest_framework_docs',
    'crispy_forms',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'SuperEMR.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SuperEMR.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#DATABASES = {
#    'default': {
#         'ENGINE': 'django.db.backends.mysql', #数据库引擎
#         'NAME': 'super_database',                       #数据库名
#         'USER': 'super_emr',                       #用户名
#         'PASSWORD': 'superemr157902',                   #密码
#         'HOST': '',                  #数据库主机，默认为localhost
#         'PORT': '',                 #数据库端口，MySQL默认3306
#         'OPTIONS': {
#             'autocommit': True,
#         },
#     }
#}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh_cn'#'en-us'

TIME_ZONE = 'Asia/Shanghai'#'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
#1.8版本后不推荐使用
#TEMPLATE_DIRS = (
#    os.path.join(BASE_DIR,  'templates'),
#)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,  'static'),
)
STATIC_ROOT=os.path.join(BASE_DIR,  'stat')

AUTH_PROFILE_MODULE = 'emr.mdlUserExtInfo' #User类扩展字段类
LOGIN_URL='/emr/login'#登录地址
MEDIA_ROOT = os.path.join(BASE_DIR, 'Media')
MEDIA_URL  = '/Media/'
ROOT_SITE = 'http://123.57.94.39'
#验证码
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'  #验证码为简单的数学计算算式
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',)  #验证码不加噪声，去掉本行，验证码则为有噪声图像
CAPTCHA_FOREGROUND_COLOR = '#0000FF'

#电子邮件
ACCOUNT_ACTIVATION_DAYS=7
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.sina.cn'                   #SMTP地址
EMAIL_PORT='25'
EMAIL_HOST_USER='18707197564@sina.cn'
EMAIL_HOST_PASSWORD='138750735431'
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL='18707197564@sina.cn'
#管理员站点
SERVER_EMAIL = '18707197564@sina.cn'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend','rest_framework.filters.SearchFilter'),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': False  # Default: False
}

DSA_FIELD_STRATEGY = {
    'list_per_page': 20,
    'list_max_show_all': 50,
}

################################################################################################
### social_auth
# SOCIAL_AUTH_PIPELINE = (
#     'social.pipeline.social_auth.social_details',
#     'social.pipeline.social_auth.social_uid',
#     'social.pipeline.social_auth.auth_allowed',
#     'social_auth.backends.pipeline.social.social_auth_user',
#     # 用户名与邮箱关联，文档说可能出现问题
#     # 'social_auth.backends.pipeline.associate.associate_by_email',
#     'social_auth.backends.pipeline.misc.save_status_to_session',
#     'social_auth.backends.pipeline.user.create_user',
#     'social_auth.backends.pipeline.social.associate_user',
#     'social_auth.backends.pipeline.social.load_extra_data',
#     'social_auth.backends.pipeline.user.update_user_details',
#     'social_auth.backends.pipeline.misc.save_status_to_session',
# )
# AUTHENTICATION_BACKENDS = (
#     'social_auth.backends.contrib.douban.Douban2Backend',
#     # 注意这个比较特殊,因为django-social-auth是依赖python-social-auth的
#     # python-social-auth==0.1.26,已经包含的qq的backend
#     # django-social-auth==0.8.1, 还没包含进来
#     # 你需要在django-social-auth/social_auth/backends/contrib中添加一个文件qq.py
#     # 就一行
#     # from social.backends.qq import QQOAuth2 as QQBackend
#     # 然后setup一下就ok
#     'social_auth.backends.contrib.qq.QQBackend',
#     'social_auth.backends.contrib.weibo.WeiboBackend',
#     # 必须加，否则django默认用户登录不上
#     'django.contrib.auth.backends.ModelBackend',
# )
# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.contrib.auth.context_processors.auth',
#     # login 在template中可以用 "{% url socialauth_begin 'douban-oauth2' %}"
#     'social_auth.context_processors.social_auth_by_type_backends',
#     'social_auth.context_processors.social_auth_login_redirect',
# )

# SOCIAL_AUTH_LOGIN_URL = '/login-url/'
# SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/logged-in/'
# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'
# SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'

# SOCIAL_AUTH_WEIBO_KEY = 'YOUR KEY'
# SOCIAL_AUTH_WEIBO_SECRET = 'YOUR SECRET'
#
# SOCIAL_AUTH_QQ_KEY = 'YOUR KEY'
# SOCIAL_AUTH_QQ_SECRET = 'YOUR SECRET'
#
# SOCIAL_AUTH_DOUBAN_OAUTH2_KEY = 'YOUR KEY'
# SOCIAL_AUTH_DOUBAN_OAUTH2_SECRET = 'YOUR SECRET
#
app_key = 'pwe86ga5ep576'
app_secret = 'i30RzGlwaeyt'