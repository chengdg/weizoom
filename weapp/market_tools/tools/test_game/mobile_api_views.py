# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import shutil
import random

from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import full_stack, unicode_full_stack
from core import dateutil
from core import paginator
from market_tools.prize.module_api import *
from watchdog.utils import watchdog_fatal, watchdog_error
from models import *


########################################################################
# play_test_game:
########################################################################
def play_test_game(request):
    member = request.member
    webapp_user = request.webapp_user
    game_id = request.POST['game_id']
    score = request.POST['score']

    try:
        game = TestGame.objects.get(id=game_id)
    except:
        response = create_response(500)
        response.errMsg = u'该趣味测试不存在'
        response.innerErrMsg = full_stack()
        return response.get_response()    

    if request.POST:
        try:
            is_participated = False #是否已经参加
            #判断是否参与过
            records = TestGameRecord.objects.filter(webapp_user_id=webapp_user.id, test_game=game.id)
            if records:
                is_participated = True
                
            TestGameRecord.objects.create(test_game=game, webapp_user_id=webapp_user.id, score=score)
            
            if member and (not is_participated):
                prize_info = PrizeInfo.from_json(game.award_prize_info)
                award(prize_info, member, u'趣味测试获得积分')
            response = create_response(200)
        except:
            response = create_response(500)
            response.errMsg = u'提交错误'
            response.innerErrMsg = full_stack()
            return response.get_response()
    else:
        response = create_response(500)
        response.errMsg = u'is not POST method'

    return response.get_response()