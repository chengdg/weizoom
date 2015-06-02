# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil

from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core import chartutil

from core.alipay.alipay_submit import *
from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from core import paginator
from core.exceptionutil import full_stack
from core.alipay.alipay_notify import AlipayNotify
from core.alipay.alipay_submit import AlipaySubmit
from account.models import UserProfile
from modules.member.models import *
from modules.member.util import *
import httplib
from webapp.modules.cms.models import *
from account.models import *


########################################################################
# get_category_articles: 获得category下的文章列表
########################################################################
def get_category_articles(category_id):
	article_ids = [r.article_id for r in CategoryHasArticle.objects.filter(category_id=category_id)]
	return list(Article.objects.filter(id__in=article_ids))