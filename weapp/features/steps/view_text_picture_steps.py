# -*- coding: utf-8 -*-
# __author__='justing'
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from add_multy_text_picture_steps import adict_addNews
@When (u"{user}浏览图文管理列表第{news_page}页")
def step_impl(context, user, news_page):
    try:
        context.url = '/new_weixin/api/materials/?sort_attr=-created_at&page=%s&count_per_page=%s' %(news_page, context.count_per_page)
    except:
        context.url = '/new_weixin/api/materials/?sort_attr=-created_at&page=%s' %news_page

