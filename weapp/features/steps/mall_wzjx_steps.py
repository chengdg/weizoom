# -*- coding: utf-8 -*-
import urllib
import urllib2

from behave import *

from test import bdd_util
from mall.models import (ORDER_TYPE2TEXT, STATUS2TEXT, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED, express_util,
                         ORDERSTATUS2TEXT, Order, Supplier)
from mall.models import Supplier
from features.testenv.model_factory import timedelta, json, ORDER_STATUS_NOT
from mall.promotion.models import datetime
import steps_db_util
import mall.models as mall_models

@given(u"{user}成为自营帐号")
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)

	mall_models.UserProfile.objects.filter(user_id=context.webapp_owner_id).update(webapp_type=1)
