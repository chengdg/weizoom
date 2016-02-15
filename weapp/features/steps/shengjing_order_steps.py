# -*- coding: utf-8 -*-

import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from webapp.modules.cms.models import *

@Given(u"{webapp_user}所属公司")
def step_impl(context, webapp_user):
	print('')

@Given(u"{webapp_user}拥有人次卡")
def step_impl(context, webapp_user):
	print('')

@Given(u"{webapp_user}拥有时间卡")
def step_impl(context, webapp_user):
	print('')

@When(u"{bill}访问{status}的账单明细")
def step_impl(context, webapp_user, status):
	print('')

@Then(u"{bill}可以看到账单明细")
def step_impl(context, webapp_user):
	print('')


