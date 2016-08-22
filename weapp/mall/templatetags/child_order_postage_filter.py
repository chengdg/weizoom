# -*- coding:utf-8 -*-

import time
from datetime import timedelta, datetime, date

from django import template
from tools.express.util import *

register = template.Library()

@register.filter(name='get_child_order_postage')
def get_child_order_postage(items, key):
  return items.get(key, '')