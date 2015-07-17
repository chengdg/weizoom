# -*- coding: utf-8 -*-
from datetime import datetime
import urllib2
import urllib
import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from modules.member import util as member_util
from modules.member.models import Member
from mall.promotion.models import CouponRule, Coupon, RedEnvelopeRule, RedEnvelopeToOrder, GetRedEnvelopeRecord
from mall.models import Order
from market_tools.tools.coupon.util import consume_coupon
from modules.member.models import Member
from weixin.user.util import get_component_info_from
import weixin.user.models as weixin_models

def get_share_red_envelope(request):
    """
    领取分享红包
    """
    red_envelope_rule_id = request.GET.get('red_envelope_rule_id', 0)
    order_id = request.GET.get('order_id', 0)
    user_id = request.GET.get('webapp_owner_id', 0)
    #订单
    order = Order.objects.get(id=order_id)

    #会员
    member_id = request.member.id
    member = Member.objects.get(id=request.member.id)

    #用户商城信息
    try:
        component_info = get_component_info_from(request)
    except:
        component_info = None
    qcode_img_url = ''
    shop_name = ''
    if component_info:
        if weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=user_id).count() == 0:
            weixin_models.ComponentAuthedAppid.objects.create(component_info=component_info, user_id=user_id)
        auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=user_id)[0]
        if weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid).count() > 0:
            auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
            qcode_img_url = auth_appid_info.qrcode_url
            shop_name = auth_appid_info.nick_name

    red_envelope_rule = RedEnvelopeRule.objects.get(id=red_envelope_rule_id)
    coupon_rule_id = red_envelope_rule.coupon_rule_id
    coupon_rule = CouponRule.objects.get(id=coupon_rule_id)
    if coupon_rule.limit_product:
        from cache.webapp_cache import get_webapp_product_detail
        product = get_webapp_product_detail(request.webapp_owner_id, coupon_rule.limit_product_id)
        coupon_rule.limit_product_name = product.name

    relation = RedEnvelopeToOrder.objects.filter(order_id=order_id, red_envelope_rule_id=red_envelope_rule_id)

    return_data = {
        'red_envelope_rule': red_envelope_rule,
        'shop_name': shop_name,
        'page_title': "微购送优惠",
        'share_page_desc': red_envelope_rule.share_title,
        'share_img_url': red_envelope_rule.share_pic
    }

    if relation.count() > 0:
        #分享获取红包
        record = GetRedEnvelopeRecord.objects.filter(member_id=member_id, red_envelope_rule_id=red_envelope_rule_id)
        friends = GetRedEnvelopeRecord.objects.filter(red_envelope_relation_id=relation[0].id).order_by("-id")
        if friends.count()>4:
            friends = friends[:4]
        if record.count() > 0:
            #会员已经领了
            return_data['has_red_envelope'] = True
            return_data['coupon_rule'] = coupon_rule
            return_data['member'] = member if member.is_subscribed else ""
            return_data['qcode_img_url'] = qcode_img_url
            return_data['friends'] = friends
        else:
            if member.is_subscribed:
                if not(coupon_rule.is_active
                    and coupon_rule.remained_count
                    and coupon_rule.end_date > datetime.now()
                    and (red_envelope_rule.end_time > datetime.now() or red_envelope_rule.limit_time)):
                    pass
                else:
                    coupon, msg = consume_coupon(request.webapp_owner_id, coupon_rule_id, member_id)
                    if coupon:
                        GetRedEnvelopeRecord.objects.create(
                                    owner_id=request.webapp_owner_id,
                                    coupon_id=coupon.id,
                                    red_envelope_rule_id=red_envelope_rule_id,
                                    red_envelope_relation_id=relation[0].id,
                                    member_id=member.id,
                                    member_name=member.username_for_html,
                                    member_header_img=member.user_icon
                            )
                        return_data['has_red_envelope'] = False
                        return_data['coupon_rule'] = coupon_rule
                        return_data['member'] = member
                        return_data['friends'] = friends
                    else:
                        pass
            else:
                #不是会员
                coupon, msg = consume_coupon(request.webapp_owner_id, coupon_rule_id, member_id)
                if coupon:
                    GetRedEnvelopeRecord.objects.create(
                                owner_id=request.webapp_owner_id,
                                coupon_id=coupon.id,
                                red_envelope_rule_id=red_envelope_rule_id,
                                red_envelope_relation_id=relation[0].id,
                                member_id=member.id,
                                member_name=member.username_for_html,
                                member_header_img=member.user_icon
                        )

                    return_data['has_red_envelope'] = False
                    return_data['coupon_rule'] = coupon_rule
                    return_data['qcode_img_url'] = qcode_img_url
                    return_data['friends'] = friends
                else:
                    pass
    else:
        #用户订单获取
        # if not order.webapp_user_id == member_id:
        #     return HttpResponseRedirect("/workbench/jqm/preview/?module=mall&model=products&action=list&workspace_id=mall&project_id=0&webapp_owner_id=%s" % user_id)
        member.member_name = member.username_for_html
        if not(coupon_rule.is_active
            and coupon_rule.remained_count
            and coupon_rule.end_date > datetime.now()
            and (red_envelope_rule.end_time > datetime.now() or red_envelope_rule.limit_time)):
            pass
        else:
            coupon, msg = consume_coupon(request.webapp_owner_id, coupon_rule_id, member_id)
            if coupon:
                relation = RedEnvelopeToOrder.objects.create(
                            owner_id=request.webapp_owner_id,
                            member_id=member_id,
                            order_id=order_id,
                            red_envelope_rule_id=red_envelope_rule_id,
                            count = 1
                    )
                GetRedEnvelopeRecord.objects.create(
                            owner_id=request.webapp_owner_id,
                            coupon_id=coupon.id,
                            red_envelope_rule_id=red_envelope_rule_id,
                            red_envelope_relation_id=relation.id,
                            member_id=member.id,
                            member_name=member.username_for_html,
                            member_header_img=member.user_icon
                    )

                return_data['has_red_envelope'] = False
                return_data['coupon_rule'] = coupon_rule
                return_data['member'] = member if member.is_subscribed else ""
                return_data['qcode_img_url'] = qcode_img_url
            else:
                pass

    c = RequestContext(request, return_data)
    return render_to_response('shareRedEnvelope/webapp/share_red_envelope.html', c)