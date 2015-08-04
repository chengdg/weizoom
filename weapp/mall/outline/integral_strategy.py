# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from core import resource
from mall import export
from mall.promotion import models as promotion_models  # 注意：不要覆盖此module
from modules.member import models as member_models


class IntegralStrategy(resource.Resource):
    app = 'mall2'
    resource = 'integral_strategy'

    @login_required
    def get(request):
        """
        """
        webapp_id = request.user_profile.webapp_id
        integral_strategy = member_models.IntegralStrategySttings.objects.get(
            webapp_id=webapp_id)
        has_a_integral_strategy = promotion_models.Promotion.objects.filter(
            owner=request.manager,
            status=promotion_models.
            PROMOTION_STATUS_STARTED,
            type=promotion_models.PROMOTION_TYPE_INTEGRAL_SALE
        ).exists()
        show_guide = False
        if integral_strategy.use_ceiling == -1:
            # 需要进入积分引导页
            show_guide = True
            integral_strategy.use_ceiling = 0
            member_models.IntegralStrategySttings.objects.filter(
                webapp_id=webapp_id).update(use_ceiling=0)
        c = RequestContext(request, {
            'first_nav_name': export.MALL_HOME_FIRST_NAV,
            'second_navs': export.get_home_second_navs(request),
            'second_nav_name': export.MALL_HOME_INTEGRAL_NAV,
            'integral_strategy': integral_strategy,
            'has_a_integral_strategy':  has_a_integral_strategy,
            'show_guide': show_guide
        })
        return render_to_response('mall/editor/integral_strategy.html', c)

    def post(request):
        """
        """

        webapp_id = request.user_profile.webapp_id
        member_models.IntegralStrategySttings.objects.filter(
            webapp_id=webapp_id
        ).update(
            integral_each_yuan=request.POST['integral_each_yuan'],
            be_member_increase_count=request.POST['be_member_increase_count'],
            click_shared_url_increase_count=request.POST[
                'click_shared_url_increase_count'],
            buy_award_count_for_buyer=request.POST[
                'buy_award_count_for_buyer'],
            order_money_percentage_for_each_buy=request.POST[
                'order_money_percentage_for_each_buy'],
            buy_via_shared_url_increase_count_for_author=request.POST[
                'buy_via_shared_url_increase_count_for_author'],
            buy_via_offline_increase_count_for_author=request.POST[
                'buy_via_offline_increase_count_for_author'],
            buy_via_offline_increase_count_percentage_for_author=request.POST[
                'buy_via_offline_increase_count_percentage_for_author'],
            use_ceiling=request.POST['use_ceiling'] if request.POST[
                'use_ceiling'] else 0,
            review_increase=request.POST['review_increase']
        )

        return HttpResponseRedirect('/mall2/integral_strategy/')
