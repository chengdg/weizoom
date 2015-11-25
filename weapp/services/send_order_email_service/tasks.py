#coding:utf8
"""@package services.cancel_order_service.tasks
发送邮件的service

"""
from django.conf import settings
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info
import time
from core.alipay.alipay_submit import *
from account.models import UserProfile
from modules.member.models import *
from mall.models import *
from modules.member.models import WebAppUser
from account.models import *
from mall.models import *
from tools.regional.views import get_str_value_by_string_ids
from celery import task
from utils import cache_util
from account.util import _send_email

########################################################################
# email_order: 订单状态改变发送邮件
########################################################################
@task
def send_order_email(request,args):


	from mall.promotion.models import Coupon
	order = Order.from_dict(json.loads(args['order']))
	print "send_order_email-----------------------------------"
	order_has_products = OrderHasProduct.objects.filter(order=order)
	buy_count = ''
	product_name = ''
	product_pic_list = []
	for order_has_product in order_has_products:
		buy_count = buy_count+str(order_has_product.number)+','
		product_name = product_name+order_has_product.product.name+','
		product_pic_list.append(order_has_product.product.thumbnails_url)
	buy_count = buy_count[:-1]
	product_name = product_name[:-1]

	user = UserProfile.objects.get(webapp_id=order.webapp_id).user

	if order.coupon_id == 0:
		coupon = ''
	else:
		coupon = str(Coupon.objects.get(id=int(order.coupon_id)).coupon_id)+u',￥'+str(order.coupon_money)

	try:
		area = get_str_value_by_string_ids(order.area)
	except:
		area = order.area
	else:
		area = u''

	buyer_address = area+u" "+order.ship_address

	if order.status == 0:
		status = 0
		order_status = u"待支付"
	elif order.status == 3:
		status = 1
		order_status = u"待发货"
	elif order.status == 4:
		status = 2
		order_status = u"已发货"
	elif order.status == 5:
		status = 3
		order_status = u"已完成"
	elif order.status == 1:
		status = 4
		order_status = u"已取消"
	elif order.status == 6:
		status = 5
		order_status = u"退款中"
	elif order.status == 7:
		status = 6
		order_status = u"退款完成"
	else:
		status = -1
		order_status = ''

	try:
		member= WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
		if member is not None:
			member_id = member.id
		else:
			member_id = -1
	except :
		member_id = -1

	if order.express_company_name:
		from tools.express.util import  get_name_by_value
		express_company_name = get_name_by_value(order.express_company_name)
	else:
		express_company_name = ""
	if order.express_number:
		express_number = order.express_number
	else:
		express_number = ''

	notify_order(
			user=user,
			member_id=member_id,
			status=status,
			order_id=order.order_id,
			buyed_time=time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
			order_status=order_status,
			buy_count=buy_count,
			total_price=order.final_price,
			bill=order.bill,
			coupon=coupon,
			product_name=product_name,
			integral=order.integral,
			buyer_name=order.ship_name,
			buyer_address=buyer_address,
			buyer_tel=order.ship_tel,
			remark=order.customer_message,
			product_pic_list=product_pic_list,
			postage=order.postage,
			express_company_name=express_company_name,
			express_number=express_number
			)


#===============================================================================
# notify_order : 发送邮件
#===============================================================================
def notify_order(user, member_id, status, order_id, buyed_time, order_status, buy_count,
				 total_price, bill, coupon, product_name, integral, buyer_name, buyer_address,
				 buyer_tel, remark, product_pic_list, postage='0', express_company_name=None, express_number=None):
	notify_setting_key = "notify_settings_{wo:%s}_{status:%s}" % (user.id,status)
	settings_dict = cache_util.get_mhash_from_redis(notify_setting_key)
	order_notify = UserOrderNotifySettings.from_dict(settings_dict)
	# zhaolei  肯定拥有id
	if not order_notify.id:
		order_notify = UserOrderNotifySettings.objects.filter(user=user, status=status, is_active=True)
		if order_notify.count():
			order_notify = order_notify[0]
			cache_util.add_mhash_to_redis(notify_setting_key,order_notify.to_dict())
	# 获得要发送的邮件列表
	if order_notify and str(member_id) not in str(order_notify.black_member_ids).split('|') and order_notify.emails != '':
		content_list = []
		content_described = u'微商城-%s-订单' % order_status
		if order_id:
			if product_name:
				content_list.append(u'商品名称：%s' % product_name)
			if product_pic_list:
				pic_address = ''
				for pic in product_pic_list:
					pic_address = pic_address+"<img src='http://%s%s' width='170px' height='200px'></img>" % (settings.DOMAIN, pic)
				if pic_address != '':
					content_list.append(pic_address)
			content_list.append(u'订单号：%s' % order_id)
			if buyed_time:
				content_list.append(u'下单时间：%s' % buyed_time)
			if order_status:
				content_list.append(u'订单状态：<font color="red">%s</font>' % order_status)
			if express_company_name:
				content_list.append(u'<font color="red">物流公司：%s</font>' % express_company_name)
			if express_number:
				content_list.append(u'<font color="red">物流单号：%s</font>' % express_number)
			if buy_count:
				content_list.append(u'订购数量：%s' % buy_count)
			if total_price:
				content_list.append(u'支付金额：%s' % total_price)
			if integral:
				content_list.append(u'使用积分：%s' % integral)
			if coupon:
				content_list.append(u'优惠券：%s' % coupon)
			if bill:
				content_list.append(u'发票：%s' % bill)
			if postage:
				content_list.append(u'邮费：%s' % postage)
			if buyer_name:
				content_list.append(u'收货人：%s' % buyer_name)
			if buyer_tel:
				content_list.append(u'收货人电话：%s' % buyer_tel)
			if buyer_address:
				content_list.append(u'收货人地址：%s' % buyer_address)
			if remark:
				content_list.append(u'顾客留言：%s' % remark)

		content = u'<br> '.join(content_list)
		try:
			_send_email(user, order_notify.emails, content_described, content)
		except:
			if status == 0:
				notify_message = u"订单状态为已付款时发邮件失败，order_id={}, webapp_id={}, cause:\n{}".format(order_id, user.id, unicode_full_stack())
			elif status == 3:
				notify_message = u"订单状态为已发货时发邮件失败，order_id:{}，cause:\n{}".format(order_id, unicode_full_stack())
			# elif status == 4:
			# 	status = 2
			# 	order_status = u"已发货"
			# elif status == 5:
			# 	status = 3
			# 	order_status = u"已完成"
			# elif status == 1:
			# 	status = 4
			# 	order_status = u"已取消"
			# elif status == 6:
			# 	status = 5
			# 	order_status = u"退款中"
			# elif status == 7:
			# 	status = 6
			# 	order_status = u"退款完成"
			else:
				notify_message = u"订单状态改变时发邮件失败，cause:\n{}".format(unicode_full_stack())

			watchdog_alert(notify_message)
