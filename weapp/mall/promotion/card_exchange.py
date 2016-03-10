# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from mall import export
from core.jsonresponse import JsonResponse, create_response
from core import paginator
from models import (CouponRule, Coupon, CouponRecord, COUPON_STATUS_USED,
                    COUPONSTATUS, COUPON_STATUS_EXPIRED)
from . import models as promotion_models
from mall import models as mall_models
from modules.member.module_api import get_member_by_id_list
from modules.member.models import (MemberGrade, MemberTag, WebAppUser)
from core import search_util
from market_tools.tools.coupon.tasks import send_message_to_member


FIRST_NAV_NAME = export.MALL_PROMOTION_AND_APPS_FIRST_NAV


class CardExchange(resource.Resource):
    app = "mall2"
    resource = "card_exchange"

    @login_required
    def get(request):
        """
        卡兑换配置页
        """
        print(export.MALL_PROMOTION_ISSUING_COUPONS_NAV)
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV_NAME,
            'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
            'third_nav_name': export.MALL_PROMOTION_CARD_EXCHANGE_NAV,
        })
        return render_to_response('mall/editor/promotion/card_exchange.html', c)

    @login_required
    def api_get(request):
        """
        卡兑换
        """
        response = create_response(200)
        return response.get_response()

    def api_post(request):
        """
        卡兑换
        """
        is_bind = request.POST.get('isBind',0)
        prize = request.POST.get('prize','')
        reward_type = request.POST.get('reward',0)

        webapp_id = request.user_profile.webapp_id
        
        prize_list = json.loads(prize)
        card_exchange_rule_list = []
        
        card_exchange = promotion_models.CardExchange.objects.create(
            webapp_id = webapp_id,
            require = is_bind,
            reward_type = reward_type
        )
        for prize in prize_list:
            card_number = prize['snum'] + '-' + prize['endnum']
            card_exchange_rule_list.append(promotion_models.CardExchangeRule(
                integral = prize['integral'],
                money = prize['money'],
                card_number = card_number,
                exchange = card_exchange
            ))
        promotion_models.CardExchangeRule.objects.bulk_create(card_exchange_rule_list)    

        response = create_response(200)
        return response.get_response()