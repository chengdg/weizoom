# -*- coding:utf-8 -*-

import time
from datetime import timedelta, datetime, date

from django import template
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from datetime import datetime

register = template.Library()


@register.filter(name='to_nav_name')
def transfer_to_nav_name(name):
	return '%s_NAV' % name.replace('-', '_').upper()


@register.filter(name='to_data_type')
def to_data_type(property):
	if property['type'] == 'checkbox':
		return 'bool'
	elif property['type'] == 'swipe_images_input':
		return 'none'
	else:
		return 'text'