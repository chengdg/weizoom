# -*- coding: utf-8 -*-
import qrcode
import os

from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from core.restful_url_route import *

from mall.models import Order
from mall import export
from models import *
from modules.member import models as member_models

from modules.member.models import WebAppUser
from modules.member.module_api import get_member_by_id_list

from excel_response import ExcelResponse

COUNT_PER_PAGE = 20
PROMOTION_TYPE_COUPON = 4
FIRST_NAV_NAME = export.MALL_PROMOTION_FIRST_NAV

@view(app='mall_promotion', resource='coupon_rules', action='get')
@login_required
def list_coupon_rules(request):
	"""
	优惠券规则列表
	"""
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_promotion_second_navs(request),
		'second_nav_name': export.MALL_PROMOTION_COUPON_NAV,
	})
	return render_to_response('mall/editor/promotion/coupon_rules.html', c)


@view(app='mall_promotion', resource='coupons', action='get')
@login_required
def list_coupons(request):
	"""
	优惠券列表
	"""
	rule_id = request.GET.get('id', '0')

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_promotion_second_navs(request),
		'second_nav_name': export.MALL_PROMOTION_COUPON_NAV,
		'rule_id': rule_id,
	})
	return render_to_response('mall/editor/promotion/coupons.html', c)


@view(app='mall_promotion', resource='coupon', action='create')
@login_required
def create_coupon(request):
	"""
	添加库码
	"""
	rule_id = request.GET.get('rule_id', '0')
	rules = CouponRule.objects.filter(id=rule_id)
	if request.method == 'GET':
		ungot_count = Coupon.objects.filter(coupon_rule__id=rule_id, status=COUPON_STATUS_UNGOT).count()
		# if rules
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_promotion_second_navs(request),
			'second_nav_name': export.MALL_PROMOTION_COUPON_NAV,
			'rule': rules[0]
		})
		return render_to_response('mall/editor/promotion/create_coupon.html', c)
	else:
		count = int(request.POST.get('count', '0'))
		__create_coupons(rules[0], count)
		CouponRule.objects.filter(id=rule_id).update(
				count=(rules[0].count+count)
			)
		return HttpResponseRedirect('/mall_promotion/coupons/get/?id=%s' % rule_id)
		# pass

@view(app='mall_promotion', resource='coupon_rules', action='create')
@login_required
def create_coupon_rule(request):
	"""
	创建优惠券规则
	"""
	member_grades = member_models.MemberGrade.get_all_grades_list(request.user_profile.webapp_id)

	c = RequestContext(request, {
		'member_grades': member_grades,
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_promotion_second_navs(request),
		'second_nav_name': export.MALL_PROMOTION_COUPON_NAV,
	})
	return render_to_response('mall/editor/promotion/create_coupon_rule.html', c)


########################################################################
# update_coupon_rule: 对优惠券规则进行更新操作
########################################################################
@view(app='mall_promotion', resource='coupon_rules', action='update')
@login_required
def update_coupon_rule(request):
	promotion_id = request.GET['id']
	# if request.method == 'GET':
	promotion = Promotion.objects.get(id=promotion_id)
	Promotion.fill_details(request.manager, [promotion], {
		'with_product': True,
		'with_concrete_promotion': True
	})

	coupon_rule = CouponRule.objects.get(id=promotion.detail_id)

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_promotion_second_navs(request),
		'second_nav_name': export.MALL_PROMOTION_COUPON_NAV,
		'coupon_rule': coupon_rule,
		'start_date': promotion.start_date.strftime("%Y-%m-%d %H:%M"),
		'end_date': promotion.end_date.strftime("%Y-%m-%d %H:%M"),
		'promotion': promotion
	})
	return render_to_response('mall/editor/promotion/create_coupon_rule.html', c)
	# else:
	# 	rule_id = request.POST.get('rule_id', None)
	# 	# rule = CouponRule.objects.get(id=rule_id)
	# 	CouponRule.objects.filter(id=rule_id).update(
	# 		name = request.POST.get('name', ''),
	# 		remark = request.POST.get('remark', '')
	# 	)

	# 	return HttpResponseRedirect('/mall_promotion/coupon_rules/get/')

@view(app='mall', resource='coupons', action='export')
@login_required
def export_coupons(request):
    """
    导出优惠券
    """
    rule_id = request.GET.get('rule_id')
    coupons = [
        [u'优惠码', u'金额', u'创建时间', u'领取时间', u'领取人', u'使用时间', u'使用人', u'订单号', u'状态']
    ]

    coupon_list = Coupon.objects.filter(owner=request.manager, coupon_rule_id=rule_id)

    member_ids = [c.member_id for c in coupon_list]
    members = get_member_by_id_list(member_ids)
    member_id2member = dict([(m.id, m) for m in members])

    #获取被使用的优惠券使用者信息
    coupon_ids = [c.id for c in coupon_list if c.status==COUPON_STATUS_USED]
    orders = Order.get_orders_by_coupon_ids(coupon_ids)
    user_ids = []
    if orders:
        coupon_id2webapp_user_id = dict([(o.coupon_id, \
            {'id': o.id, 'user':o.webapp_user_id, 'order_id':o.order_id, 'created_at': o.created_at})\
            for o in orders])
        user_ids.append(o.webapp_user_id)
    else:
        coupon_id2webapp_user_id = {}

    #获取使用优惠券会员的信息
    webapp_user_id2member_id = dict([(user.id, user.member_id ) for user in WebAppUser.objects.filter(id__in=user_ids) if (user.member_id != 0 and user.member_id != -1)])
    member_ids = webapp_user_id2member_id.values()
    members = get_member_by_id_list(member_ids)
    for member in members:
    	if not member_id2member.has_key(member.id):
    		member_id2member[member.id] = member

    now = datetime.today()
    for coupon in coupon_list:
        coupon.consumer_name = ''
        coupon.use_time = ''
        coupon.order_fullid = ''

        member_id = int(coupon.member_id)
        if member_id in member_id2member:
            member = member_id2member[member_id]
            coupon.member_name = member.username_for_html
        else:
            coupon.member_name = ''

        if coupon.status == COUPON_STATUS_USED:
            if coupon.id in coupon_id2webapp_user_id:
                order = coupon_id2webapp_user_id[coupon.id]
                coupon.order_id = order['id']
                coupon.order_fullid = order['order_id']
                coupon.use_time = order['created_at'].strftime("%Y-%m-%d %H:%M")
                webapp_user_id = order['user']
                if webapp_user_id2member_id.has_key(webapp_user_id) and member_id2member.has_key(webapp_user_id2member_id[webapp_user_id]):
                    member = member_id2member[webapp_user_id2member_id[webapp_user_id]]
                else:
                    member = None
                if member:
                    coupon.consumer_name = member.username_for_html
                else:
                    consumer.consumer_name = '未知'
            else:
                consumer.consumer_name = '未知'

            coupon.status = COUPONSTATUS.get(coupon.status)['name']
        elif coupon.expired_time <= now:
            coupon.status = COUPONSTATUS.get(COUPON_STATUS_EXPIRED)['name']
        else:
            coupon.status = COUPONSTATUS.get(coupon.status)['name']


        coupons.append([
            coupon.coupon_id,
            coupon.money,
            coupon.created_at,
            coupon.provided_time if coupon.member_name else '' ,
            coupon.member_name,
            coupon.use_time,
            coupon.consumer_name,
            coupon.order_fullid,
            coupon.status
        ])

    return ExcelResponse(coupons,output_name=u'优惠券详情'.encode('utf8'),force_csv=False)

@view(app='mall_promotion', resource='coupon_rules', action='select')
@login_required
def select_coupon_rule(request):
    """
    查看优惠券信息
    """
    promotion_id = request.GET['id']
    promotion = Promotion.objects.get(id=promotion_id)
    Promotion.fill_details(request.manager, [promotion], {
        'with_product': True,
        'with_concrete_promotion': True
    })

    coupon_rule = CouponRule.objects.get(id=promotion.detail_id)

    url = "http://"+request.META['HTTP_HOST']+"/termite/workbench/jqm/preview/?module=market_tool:coupon&model=coupon&action=get&workspace_id=market_tool:coupon&webapp_owner_id="+str(coupon_rule.owner_id)+"&project_id=0&rule_id="+str(coupon_rule.id)

    coupon_img_url = _create_coupon_qrcode(url, coupon_rule.id)

    coupon_rule.get_url = url
    coupon_rule.qrcode_url = coupon_img_url

    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV_NAME,
        'second_navs': export.get_promotion_second_navs(request),
        'second_nav_name': export.MALL_PROMOTION_COUPON_NAV,
        'coupon_rule': coupon_rule,
    })
    return render_to_response('mall/editor/promotion/select_coupon_rule.html', c)

@view(app='mall_promotion', resource='coupon_qrcode', action='download')
@login_required
def download_coupon_qrcode(request):
    """
    下载优惠券二维码
    """
    coupon_id = request.GET["id"]
    dir_path = os.path.join(settings.UPLOAD_DIR, '../coupon_qrcode/')
    filename = dir_path + coupon_id +'.png'
    try:
        response = HttpResponse(open(filename,"rb").read(), mimetype='application/x-msdownload')
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
    except:
        response = HttpResponse('')
    return response

def _create_coupon_qrcode(coupon_url, coupon_id):
    """
    创建优惠券二维码
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(coupon_url)
    img = qr.make_image()

    file_name = '%d.png' % coupon_id
    dir_path = os.path.join(settings.UPLOAD_DIR, '../coupon_qrcode')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_path = os.path.join(dir_path, file_name)
    img.save(file_path)

    return '/static/coupon_qrcode/%s' % file_name
