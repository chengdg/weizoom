#!/usr/bin/env python
# -*- coding: utf-8 -*-
from features.steps.apps_shvote_index_steps import get_dynamic_data

__author__ = 'aix'

from behave import *
from test import bdd_util
import apps_step_utils as app_utils
from collections import OrderedDict

from django.contrib.auth.models import User
from features.testenv.model_factory import *
import steps_db_util
from mall.promotion import models as  promotion_models
from mall.models import WxCertSettings
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings
from weixin.message.material import models as material_models
from apps.customerized_apps.shvote import models as shvote_models
import termite.pagestore as pagestore_manager
import json
import copy

@When(u"{webapp_user_name}在高级投票中为'{target_user_name}'投票")
def step_impl(context, webapp_user_name, target_user_name):
    #获取动态数据
    get_dynamic_data(context)
    record_id = context.shvote_id
    shp = shvote_models.ShvoteParticipance.objects.get(belong_to=record_id, name=target_user_name)
    response = app_utils.get_response(context, {
        "app": "m/apps/shvote",
        "resource": "shvote_participance",
        "method": "post",
        "type": "api",
        "args": {
            "webapp_owner_id": context.webapp_owner_id,
            "recordId": record_id,
            "vote_to": shp.id,
            "voted_group": shp.group
        }
    })
    bdd_util.assert_api_call_success(response)
