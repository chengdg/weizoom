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


@When(u'{webapp_user_name}于"{shvote_name}"高级投票活动后台创建选手')
def step_impl(context, webapp_user_name,shvote_name):
	record_id = context.record_id
	webapp_owner_id = context.webapp_owner_id
	shvote_id = context.shvote_id
	openid = context.openid
	print ">>>> Shvote Mobile Page --- Sign Up ----[start]>>>>"
	print "webapp_owner_id:"+webapp_owner_id
	print "shvote_id:"+shvote_id
	print "record_id:"+record_id
	print "<<<< Shvote Mobile Page --- Sign Up ----[ end ] <<<<"
	response = __get_into_shvote_signup_pages(context,webapp_owner_id,shvote_id,openid)#resp.context=> data ; resp.content => Http Text
