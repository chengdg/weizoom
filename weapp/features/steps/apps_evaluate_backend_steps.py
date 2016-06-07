#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'aix'

import json
from behave import *
from test import bdd_util


@when(u'{user}配置商品评论自定义模板')
def step_impl(context, user):
	given_data = json.loads(context.text)
	#访问页面，获得分配的project_id
	get_response = context.client.get("/apps/evaluate/evaluate/")
	project_id = get_response.context['project_id']
	design_mode = 0
	version = 1
	#编辑页面获得右边的page_json
	dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	context.client.get(dynamic_url)