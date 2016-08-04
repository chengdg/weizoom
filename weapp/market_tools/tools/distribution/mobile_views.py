# -*- coding: utf-8 -*-

__author__ = 'aix'

import os

from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from weixin2 import models

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

COUNT_PER_PAGE = 15
# def get_page(request):
# 	"""
# 	手机端推广分销页面
# 	"""
# 	webapp_id = request.user_profile.webapp_id
# 	member_id = request.member.id
# 	c = RequestContext(request, {

# 	})


# 	return render_to_response('%s/distribution/webapp/xxx.html' % TEMPLATE_DIR, c)

def get(request):
	"""
	获取提取进度页面
	"""
	webapp_id = request.user_profile.webapp_id
	member_id = request.member.id
	owner_id = "1"
	owner_lists = models.EnchashmentProcess.objects.filter(owner_id=owner_id)
	c = RequestContext(request, {
		"owner_lists": owner_lists
	})
	return render_to_response('%s/distribution/webapp/m_process.html' % TEMPLATE_DIR, c)