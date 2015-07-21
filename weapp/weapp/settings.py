# -*- coding: utf-8 -*-
# Django settings for weapp project.

import os

VERSION = 2

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DUMP_DEBUG_MSG = DEBUG
IS_UNDER_BDD = False

IS_UNDER_CODE_GENERATION = False
WEIZOOM_CARD_ADMIN_USERS = ('card_admin',)

MODE = 'develop'

DEBUG_MERGED_JS = True
USE_DEV_JS = True
# whether to use dev resource
USE_DEV_RESOURCE = True

#add by bert at 2015318 to make a distinction between test and event.click flag
IS_MESSAGE_OPTIMIZATION  = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENABLE_SHENGJING_APP = False

# 是否开启TaskQueue(基于Celery)
TASKQUEUE_ENABLED = True

# event dispatcher
#   local: call service directly
#   redis: use redis pub/sub
#   dummy: print event, but not dispatch
EVENT_DISPATCHER = 'redis'

DATETIME_FORMAT = 'Y m d, H:i:s.u'

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        # Or path to database file if using sqlite3.
        'NAME': 'weapp',
        'USER': 'weapp',                      # Not used with sqlite3.
        'PASSWORD': 'weizoom',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': 'db.weapp.com',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
        'CONN_MAX_AGE': 100
    },
    'watchdog': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        # Or path to database file if using sqlite3.
        'NAME': 'operation',
        'USER': 'operation',                      # Not used with sqlite3.
        'PASSWORD': 'weizoom',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': 'db.weapp_operation.com',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
        'CONN_MAX_AGE': 100
    }
}

if MODE == 'develop' or MODE == 'test':
    WATCHDOG_DB = 'default'
else:
    WATCHDOG_DB = 'watchdog'

REDIS_HOST = 'redis.weapp.com'
REDIS_PORT = 6379
REDIS_CACHES_DB = 1
REDIS_SERVICE_DB = 2
IS_ENABLE_REDIS_CACHE = True
if IS_ENABLE_REDIS_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://%s:%s/%s" % (REDIS_HOST, REDIS_PORT, REDIS_CACHES_DB),
            "OPTIONS": {
                "IGNORE_EXCEPTIONS": True,
                #"SOCKET_TIMEOUT": 30,
                # "CONNECTION_POOL_KWARGS": {"max_connections": 100}
                # "COMPRESS_COMPRESSOR": lzma.compress,
                # "COMPRESS_DECOMPRESSOR": lzma.decompress,
                # "COMPRESS_DECOMPRESSOR_ERROR": lzma.LZMAError
            }
        },
        'mem': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache"
        },
        'mem': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }


DJANGO_REDIS_IGNORE_EXCEPTIONS = True

APP_MONGO = {
    "HOST": 'mongo.weapp.com',
    "DB": 'app_data'
}

if ENABLE_SHENGJING_APP:
    DATABASES['shengjing'] = {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.oracle',
        # Or path to database file if using sqlite3.
        'NAME': 'uplookin',
        'USER': 'TURBOCRM5',                      # Not used with sqlite3.
        'PASSWORD': 'TURBOCRM',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': 'db.shengjing.com',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '1521'
    }

# if 'test' in sys.argv or '--database=default' in sys.argv:
    # DATABASES['default'] = {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'test.db'
    # }
    # if str(sys.argv).find('behave') > 0:
    # TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'
    # else:
    #    TEST_RUNNER = 'djnose2.TestRunner'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.s
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'deploy_static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

DEFAULT_INDEX_TABLESPACE = ''

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    './static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2m#oe@^8f96q&amp;ezyppacqbh%&amp;p8c15^6^98!5xl4np_ig7v7%e'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
]
MIDDLEWARE_CLASSES = [
    'core.resource_middleware.RestfulUrlMiddleware',
    'django.middleware.common.CommonMiddleware',
    'core.middleware.ExceptionMiddleware',
    'core.debug_middleware.SimulateWeixinMiddleware',

    # Uncomment this middleware for monitor sql querys:
    'core.debug_middleware.SqlMonitorMiddleware',

    # webapp home_page middleware
    'core.termite_middleware.WebappPageHomePageMiddleware',

    # termite middleware
    'core.termite_middleware.WebappPageCacheMiddleware',

    # REST resorce manage
    'core.resource_middleware.ResourceJsMiddleware',

    # Uncomment this middleware to get POST api call's sql sequence
    # 'core.debug_middleware.JsonToHtmlMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'core.middleware.GetRequestInfoMiddleware',
    'core.middleware.RequestUserSourceDetectMiddleware',
    # profiling的中间件
    'core.profiling_middleware.ProfileMiddleware',

    'modules.member.middleware.AddUuidSessionMiddleware',
    'core.middleware.UserManagerMiddleware',
    'core.middleware.UserProfileMiddleware',
    'modules.member.middleware.CleanUpCookieMiddleware',
    'modules.member.middleware.MemberCacheMiddleware',
    'modules.member.middleware.ProcessOpenidMiddleware',
    'modules.member.middleware.OAUTHMiddleware',
    'modules.member.middleware.RedirectBySctMiddleware',
    'modules.member.middleware.RequestSocialAccountMiddleware',
    'modules.member.middleware.MemberMiddleware',
    'modules.member.middleware.WebAppUserMiddleware',
    'modules.member.middleware.RedirectByFmtMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DEFAULT_MSG_HANDLER_CLASSES = (
    'weixin.message.impl_handlers.should_process_checker.ShouldProcessChecker',
    'weixin.message.impl_handlers.recieved_message_log.ReceivedMessageLogger',
    'weixin.statistics.message_statistics.MessageStatistics',
    'weixin.message.impl_handlers.responsed_message_log.ResponseedMessageLogger',
    'weixin.message.impl_handlers.weixin_user_handler.WeixinUserHandler',
    'weixin.message.impl_handlers.member_handler.MemberHandler',
    'market_tools.tools.member_qrcode.ticket_messge_handler.QrcodeHandler',
    'market_tools.tools.channel_qrcode.channel_qrcode_handler.ChannelQrcodeHandler',
    'modules.member.send_mass_msg_result_handler.SendMassMessageResultHandler',
    'weixin.message.impl_handlers.default_event_handler.DefaultEventHandler',
    'weixin.message.qa.auto_qa_message_handler.AutoQaMessageHandler',
    'modules.member.update_member_group_handler.UpdateMemberGroupHandler',
    'weixin.message.qa.auto_qa_default_message_handler.AutoQaDefaultMessageHandler',)

OPTIMIZATION_MSG_HANDLER_CLASSES = (
    'weixin.message.impl_handlers.should_process_checker.ShouldProcessChecker',
    'weixin.message.impl_handlers.recieved_message_log.ReceivedMessageLogger',
    'weixin.statistics.message_statistics.MessageStatistics',
    'weixin.message.impl_handlers.responsed_message_log.ResponseedMessageLogger',
    'weixin.message.message_handler.weixin_user_handler.WeixinUserHandler',
    'weixin.message.message_handler.member_handler.MemberHandler',
    'market_tools.tools.member_qrcode.ticket_messge_handler.QrcodeHandler',
    'market_tools.tools.channel_qrcode.channel_qrcode_handler.ChannelQrcodeHandler',
    'modules.member.send_mass_msg_result_handler.SendMassMessageResultHandler',
    'weixin.message.message_handler.default_event_handler.DefaultEventHandler',
    'weixin.message.message_handler.auto_qa_message_handler.AutoQaMessageHandler',
    'modules.member.update_member_group_handler.UpdateMemberGroupHandler',
    'weixin.message.message_handler.auto_qa_default_message_handler.AutoQaDefaultMessageHandler'
)

ROOT_URLCONF = 'weapp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'weapp.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    'core.context_processors.page_title',
    'core.context_processors.share_page_title',
    'core.context_processors.member_token',
    'core.context_processors.cur_webapp_owner_operation_settings',
    'core.context_processors.get_cur_request_member',
    'core.context_processors.get_cur_request_webapp_user',

    'core.context_processors.cur_request_webapp_id',
    'core.context_processors.mp_user',
    'core.context_processors.system_name',
    'core.context_processors.is_use_dev_resource',
    'core.context_processors.develop_mode',
    #'core.context_processors.webapp_template',

    #'core.context_processors.css_name',
    'core.context_processors.first_navs',
    'core.context_processors.is_operator',
    'core.context_processors.weapp_models',
    'core.context_processors.weapp_views',
    'core.context_processors.weapp_dialogs',
    'core.context_processors.homepage_workspace_info',
    # 'core.context_processors.page_help_document',
    # 'core.context_processors.page_features',
    'core.context_processors.detect_member_operate_capability',
    'core.context_processors.detect_footer_visibility',
    'core.context_processors.get_user_product',
    #'core.context_processors.visit_histroy',

    'core.context_processors.user_token',
    'core.context_processors.request_host',
    'core.context_processors.is_weizoom_mall',
    'core.context_processors.cdn_host',
    'core.context_processors.handlebar_component_templates'

]

CUSTOMERIZED_TEMPLATES_DIR = '%s/../templates/custom' % PROJECT_HOME
CUSTOMIZED_APP_TEMPLATES_DIR = '%s/../apps/customerized_apps' % PROJECT_HOME
PAY_TEMPLATES_DIR = '%s/../pay' % PROJECT_HOME
TERMITE2_TEMPLATES_DIR = '%s/../termite2/templates' % PROJECT_HOME


TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/../mall/templates' % PROJECT_HOME,
    '%s/../webapp/modules' % PROJECT_HOME,
    '%s/../market_tools/tools' % PROJECT_HOME,
    '%s/templates' % PROJECT_HOME,
    './templates',
    '../templates',
    CUSTOMERIZED_TEMPLATES_DIR,
    CUSTOMIZED_APP_TEMPLATES_DIR,
    PAY_TEMPLATES_DIR,
    TERMITE2_TEMPLATES_DIR,
]


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'captcha',

    'apps.customerized_apps.shengjing',
    'apps.customerized_apps.weshop',

    'account',
    'account.social_account',
    'simulator',
    'watchdog',
    'operation',

    'modules',
    'modules.member',

    'weixin',
    'weixin.user',
    'weixin2',
    'termite2',
    'stats',
    'wapi',

    'weixin.message.material',
    'weixin.message.message',
    'weixin.message.qa',

    'weixin.manage',
    'weixin.manage.customerized_menu',

    'weixin.statistics',

    'wxpay',

    'market_tools',
    'market_tools.question',
    'market_tools.prize',

    'tools',
    'tools.map',
    'tools.weather',
    'tools.regional',
    'tools.express',

    'webapp',
    'webapp.modules.cms',
    'webapp.modules.user_center',
    # 'webapp.modules.shop',
    'termite.workbench',

    'manage_tools',
    'help_system',

    'product',

    'mockapi',
    'example',

    'order',

    'apps',

    'deploy',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 'django_behave',
    'mobile_app',
    'erp',
    # 'momus',
    'pay',
    'card',
    'mall',
    'mall.promotion',
    'auth',
    'member',
    'weixin.message.message_handler',
    'notice',
    'svsmon',

    # Third-party apps
    # 'django_extensions',

    # 'new_mall', # for exercises
]


# Celery任务
INSTALLED_TASKS = [
    # Celery for Django
    'watchdog',
    'example.example_echo',
    'modules.member',
    'weixin.message.qa',
    'weixin.statistics',
    'weixin.message.message_handler',
    'market_tools.tools.shake',

    # for services
    'services.example_service',
    'services.page_visit_service',
    'services.post_save_order_service',
    'services.shared_url_page_visit_service',
    'services.post_pay_order_service',
    'services.oauth_shared_url_service',
    'services.start_promotion_service',
    'services.finish_promotion_service',

    'services.daily_page_visit_statistic_service',
    'services.update_mp_token_service',
    'services.cancel_not_pay_order_service',
    # 'services.update_component_mp_token_service',
    'services.analysis_message_service',
    'services.count_keyword_service',
]


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

MALL_CSS_FILE_PATH = os.path.join(PROJECT_HOME, '../static', 'css', 'webapp')
SESSION_COOKIE_AGE = 5 * 24 * 3600  # one week
AUTH_PROFILE_MODULE = "account.UserProfile"
LOGIN_URL = '/login/'
UPLOAD_DIR = os.path.join(PROJECT_HOME, '../static', 'upload')
HEADIMG_UPLOAD_DIR = os.path.join(PROJECT_HOME, '../static', 'head_images')
LOTTERY_HEADIMG_UPLOAD_DIR = os.path.join(
    PROJECT_HOME,
    '../static',
    'lottery_head_images')
MIXUP_FACTOR = 3179
WATCH_DOG_DEVICE = 'mysql'

WATCHDOG_WEIXIN_MESSAGE = False
ENABLE_WEPAGE_CACHE = True

if 'develop' == MODE:
    DOMAIN = 'dev.weapp.com'
    BATMAN_API_IMPL = 'memory'
    BATMAN_API_HOST = 'dev.batman.com:8080'
    MOM_HOST = '192.168.1.11'
    MOM_PORT = 61613
    IS_IN_TESTING = True
    WATCH_DOG_LEVEL = 0
    RECORD_SIMULATOR_MESSAGE = True
    VISIT_RECORD_MIN_TIME_SPAN_SECONDS = 3 * 60
    # USE_MOCK_PAY_API = True
    USE_MOCK_PAY_API = False
    CDN_HOST = ''
    EVENT_DISPATCHER = 'local'
    ENABLE_WEPAGE_CACHE = True

    import logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

elif 'test' == MODE:
    DOMAIN = 'testweapp.weizoom.com'
    BATMAN_API_IMPL = 'server'
    BATMAN_API_HOST = 'batman.weizoom.com'
    MOM_HOST = 'amq.wintim.com'
    MOM_PORT = 61613
    IS_IN_TESTING = True
    WATCH_DOG_LEVEL = 0
    RECORD_SIMULATOR_MESSAGE = True
    VISIT_RECORD_MIN_TIME_SPAN_SECONDS = 3 * 60
    USE_MOCK_PAY_API = False
    CDN_HOST = ''
else:
    DEBUG = False
    BATMAN_API_IMPL = 'memory'
    BATMAN_API_HOST = 'batman.weizoom.com'
    MOM_HOST = 'amq.wintim.com'
    MOM_PORT = 61613
    DOMAIN = 'weapp.weizoom.com'
    DUMP_DEBUG_MSG = False
    WATCHDOG_WEIXIN_MESSAGE = True
    IS_IN_TESTING = False
    WATCH_DOG_LEVEL = 200
    RECORD_SIMULATOR_MESSAGE = False
    VISIT_RECORD_MIN_TIME_SPAN_SECONDS = 24 * 60 * 60
    USE_MOCK_PAY_API = False
    CDN_HOST = 'http://weappstatic.b0.upaiyun.com'
    DEBUG_MERGED_JS = False
    USE_DEV_JS = False

IN_DEVELOP_MODE = (MODE == 'develop')
ALLOWED_HOSTS = ['*', ]

# added by chuter
# mail config for auto sending notify mail
MAIL_NOTIFY_USERNAME = u'noreply@weizoom.com'
MAIL_NOTIFY_PASSWORD = u'weizoom2013'
MAIL_NOTIFY_ACCOUNT_SMTP = u'smtp.biz.mail.qq.com'

IS_UPDATE_PV_UV_REALTIME = True

# config for notify server
#NOTIFY_SERVER_SECRET = 'http://211.100.52.42/'
NOTIFY_SERVER_SECRET = ')*notify,lion@('
IS_WRITE_EXCEPTION_BY_WATCHDOG = True
IS_WRITE_NOTIFY_BY_WATCHDOG = True
UNCATCHED_EXCEPTION_ACTION_URL = ''


WEAPP_WEB_DIALOG_DIRS = [
    ('static', '%s/../static/' %
     PROJECT_HOME), ('markettools_static', '%s/../market_tools/tools/*' %
                     PROJECT_HOME), ('customerized_apps_static', '%s/../apps/customerized_apps/*' %
                                     PROJECT_HOME), ]
WEAPP_WEB_VIEW_DIRS = [
    ('static', '%s/../static/' % PROJECT_HOME),
]
WEAPP_WEB_MODEL_DIRS = [
    ('static', '%s/../static/' % PROJECT_HOME),
]

WEAPP_WEB_DIALOG_DIRS_V2 = [
    ('static_v2', '%s/../static_v2/' % PROJECT_HOME),
]
WEAPP_WEB_VIEW_DIRS_V2 = [
    ('static_v2', '%s/../static_v2/' % PROJECT_HOME),
]
WEAPP_WEB_MODEL_DIRS_V2 = [
    ('static_v2', '%s/../static_v2/' % PROJECT_HOME),
]


#####################################################################
# import termite content
#####################################################################
from termite import embed_settings as termite_settings
 
TEMPLATE_LOADERS.extend(termite_settings.TEMPLATE_LOADERS)
MIDDLEWARE_CLASSES.extend(termite_settings.MIDDLEWARE_CLASSES)
TEMPLATE_CONTEXT_PROCESSORS.extend(termite_settings.TEMPLATE_CONTEXT_PROCESSORS)
TEMPLATE_DIRS.extend(termite_settings.TEMPLATE_DIRS)
INSTALLED_APPS.extend(termite_settings.INSTALLED_APPS)
locals().update(termite_settings.exports)

#####################################################################
# import order content
#####################################################################
from order import embed_settings as order_settings

MIDDLEWARE_CLASSES.extend(order_settings.MIDDLEWARE_CLASSES)
TEMPLATE_DIRS.extend(order_settings.TEMPLATE_DIRS)
INSTALLED_APPS.extend(order_settings.INSTALLED_APPS)


MIDDLEWARE_CLASSES.extend([
    'core.middleware.ModuleNameMiddleware',
    'core.middleware.MarketToolsMiddleware',
    'core.middleware.UserAgentMiddleware',
    'core.middleware.DisablePostInPcBrowserUnderDeployMiddleware',
    'core.middleware.BrowserSourceDetectMiddleware',
    'core.middleware.AuthorizedUserMiddleware',
    'core.middleware.ForceLogoutMiddleware',
    'core.middleware.RequestWebAppMiddleware',

    'core.middleware.WeizoomCardUseAuthKeyMiddleware',
    'core.middleware.SubUserMiddleware',

    #'modules.member.middleware.AddSocialAccountInfoForPcBrowserMiddleware',

    #'modules.member.middleware.RequestSocialAccountMiddleware',
    #'modules.member.middleware.MemberSessionMiddleware',
    #'modules.member.middleware.WebAppUserMiddleware',
    #'modules.member.middleware.SharedUrlRequestProcessMiddleWare',
    # 'modules.member.middleware.MemberRelationMiddleware', #DONE: move to page_visit service
    # 'modules.member.middleware.MemberSouceMiddleware', #DONE: move to page_visit service
    #'modules.member.middleware.SharedPageVisitSessionMiddleWare',
    'modules.member.middleware.RemoveSharedInfoMiddleware',
    'core.debug_middleware.DisplayImportantObjectMiddleware',
    'core.debug_middleware.DumpContextMiddleware',
    'core.middleware.PageIdMiddleware',
    'core.middleware.ManagerDetectMiddleware',
    'core.middleware.PermissionMiddleware',
    # 'modules.member.middleware.MemberBrowseRecordMiddleware', #TODO: change to service
    'core.middleware.WeizoomMallMiddleware',
    'core.middleware.WebAppPageVisitMiddleware',
    'core.middleware.LocalCacheMiddleware',
])


# settings for profiling middleware
# True即开启profiling
ENABLE_PROFILE = False
PROFILE_MIDDLEWARE_SORT = ('time', 'calls')
#PROFILE_MIDDLEWARE_STRIP_DIRS = True
PROFILE_MIDDLEWARE_RESTRICTIONS = ('template', 0.5)  # 只看有template的、前50%的记录

from market_tools import embed_settings as market_tools_settings
INSTALLED_APPS.extend(market_tools_settings.INSTALLED_APPS)

# add customized apps
CUSTOMERIZED_APP_DIR = os.path.join(PROJECT_HOME, '../apps/customerized_apps')
for app_dir in os.listdir(CUSTOMERIZED_APP_DIR):
    mysql_model_path = os.path.join(
        CUSTOMERIZED_APP_DIR,
        app_dir,
        'mysql_models.py')
    if os.path.exists(mysql_model_path):
        INSTALLED_APPS.append('apps.customerized_apps.%s' % app_dir)

#     NOSE_ARGS = [
#         '--with-coverage',
# '--cover-package=myapp1, myapp2',
#         '--cover-inclusive',
#     ]

PROFILE_MIDDLEWARE_JSON = False
DUMP_TEST_REQUEST = False
if DUMP_TEST_REQUEST:
    MIDDLEWARE_CLASSES.insert(4, 'core.debug_middleware.DumpCookieMiddleware')


# enable RECORD_SQL_STACKTRACE to record stack trace when record sql in ORM
DJANGO_HACK_PARAMS = {
    'enable_record_sql_stacktrace': True
}

RESOURCE_LOADED = False
RESOURCES = ['stats', 'termite2', 'weixin2']

#WAPI_SECRET_ACCESS_TOKEN = '!@#$1asDkl;fffo!&^OumsG#$RvZzhHQ!piuqwe;laasdf@'
WAPI_SECRET_ACCESS_TOKEN = 'simple_wapi_key'


from weapp import hack_django
hack_django.hack(DJANGO_HACK_PARAMS)
