# -*- coding: utf-8 -*-
from datetime import datetime
import random

from django.dispatch import Signal
from django.dispatch.dispatcher import receiver

from webapp.modules.mall import signals as mall_signals
from models import *
from core.common_util import ignore_exception


#############################################################################################
# 检查积分
#############################################################################################
def check_order_related_resource_handler(order, args, request, **kwargs):
	3/0