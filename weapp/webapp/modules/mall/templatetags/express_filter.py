# -*- coding:utf-8 -*-

import time
from datetime import timedelta, datetime, date

from django import template
from tools.express.util import *

register = template.Library()

########################################################################
# get_company_name_by_value: 根据快递公司value，获取快递公司名称
########################################################################
@register.filter(name='get_company_name_by_value')
def get_company_name_by_value(value):
	return get_name_by_value(value)
