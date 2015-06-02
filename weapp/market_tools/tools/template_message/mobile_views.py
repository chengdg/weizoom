# -*- coding: utf-8 -*-

__author__ = 'bert'

import os
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response

from core.exceptionutil import unicode_full_stack
from core import core_setting
from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info

from models import *

from modules.member.models import IntegralStrategySttings

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]
