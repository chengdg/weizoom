#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.shvote.models import Shvote, ShvoteParticipance, ShvoteControl
from weixin.message.material import models as material_models
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

import time
from django.core.management.base import BaseCommand, CommandError
from utils.cache_util import SET_CACHE
from modules.member.models import Member

def __CreatePlayer(context,webapp_user_name,webapp_owner_id,shvote_name,shvote_id,openid):
	'''
	后台创建选手报名
	'''
	design_mode = 0
	version = 1

	text = json.loads(context.text)
	headImg = text.get('headImg')
	name = text.get('name','')
	group = text.get('group',[""])[0]
	number = text.get('number')
	details = text.get('details','')
	detail_pic = json.dumps(text.get('detail_pic'))

	termite_post_args = {
		'webapp_owner_id':webapp_owner_id,
		'head_img_src':headImg,
		'player_name':name,
		'group':group,
		'serial_number':number,
		'details':details,
		'img_des_srcs':detail_pic,
	}

	post_url = '/apps/shvote/api/shvote_create_player/?_method=post&id={}&opid={}'.format(shvote_id,openid)
	post_termite_response = context.client.post(post_url,termite_post_args)
	while post_termite_response.status_code==302:
		redirect_url = post_termite_response['Location']
		post_termite_response = context.client.post(redirect_url,termite_post_args)



@When(u'{webapp_user_name}于"{shvote_name}"高级投票活动后台创建选手')
def step_impl(context, webapp_user_name,shvote_name):
	webapp_owner_id = str(context.webapp_owner_id)
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	shvote = Shvote.objects.get(owner_id=context.webapp_owner_id)
	shvote_id = str(shvote.id)

	create_respone = __CreatePlayer(context,webapp_user_name,webapp_owner_id,shvote_name,shvote_id,openid)
	context.openid = openid
	context.shvote_id = shvote_id
