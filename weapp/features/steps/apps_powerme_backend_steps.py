#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

from behave import *
from test import bdd_util

from features.testenv.model_factory import *
import steps_db_util
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from weixin.message.material import models as material_models
import termite.pagestore as pagestore_manager
import json

def __debug_print(content,type_tag=True):
	"""
	debug工具函数
	"""
	if content:
		print '++++++++++++++++++  START ++++++++++++++++++++++++++++++++++++'
		if type_tag:
			print "====== Type ======"
			print type(content)
			print "==================="
		print content
		print '++++++++++++++++++++  END  ++++++++++++++++++++++++++++++++++'
	else:
		pass
