#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


def __name2status(name):
    """
    高级投票： 文字 转 状态值
    """
    if name:
        name2status_dic = {u"全部":-1,u"未开始":0,u"进行中":1,u"已结束":2}
        return name2status_dic[name]
    else:
        return -1

# @When(u"{webapp_user_name}在高级投票中为'{target_user_name}'投票")
# def step_impl(context, webapp_user_name, target_user_name):

