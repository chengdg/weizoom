#coding:utf8
"""@package services.start_promotion_service.tasks
start_promotion_service 的Celery task实现

"""
import json
import urllib2

from django.conf import settings
from core.exceptionutil import unicode_full_stack
from datetime import datetime

from mall.promotion import models as promotion_models
from mall import models as mall_models

from celery import task
# from utils import cache_util

from datetime import datetime, timedelta

from core.exceptionutil import unicode_full_stack

# from settings import *

from weixin.user.models import WeixinMpUserAccessToken

from watchdog.utils import watchdog_fatal, watchdog_notice, watchdog_warning
