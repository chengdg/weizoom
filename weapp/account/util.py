# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.conf import settings
from django.contrib.auth.models import Group, User
from core.exceptionutil import full_stack, unicode_full_stack
from core.sendmail import sendmail
from watchdog.utils import watchdog_warning, watchdog_error
from weixin.user.models import WeixinMpUser, WeixinMpUserAccessToken
from models import *

def get_binding_weixin_mpuser(user):
	if isinstance(user, User):
		mpusers = WeixinMpUser.objects.filter(owner=user)
	else:
		mpusers = WeixinMpUser.objects.filter(owner_id=user)
	if mpusers.count() > 0:
		return mpusers[0]
	else:
		return None

def get_mpuser_accesstoken(mpuser):
	access_tokens = WeixinMpUserAccessToken.objects.filter(mpuser=mpuser)
	if access_tokens.count() > 0:
		return access_tokens[0]
	else:
		return None
#===============================================================================
# notify_order : 发送邮件
#===============================================================================
def notify_order(user, member_id, status, order_id, buyed_time, order_status, buy_count, total_price, bill, coupon, product_name, integral, buyer_name, buyer_address, buyer_tel, remark, product_pic_list, postage='0', express_company_name=None, express_number=None):
	order_notifys = UserOrderNotifySettings.objects.filter(user=user, status=status, is_active=True)
	if order_notifys.count() > 0 and str(member_id) not in order_notifys[0].black_member_ids.split('|') and order_notifys[0].emails != '':
		order_notify = order_notifys[0]
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
			
			# if member_id:
			# 	try:
			# 		member = Member.objects.get(id=member_id)
			# 		content_list.append(u'会员昵称：%s' % member.username_for_html)
			# 	except:
			# 		pass
				
		content = u'<br> '.join(content_list) 
		_send_email(user, order_notify.emails, content_described, content)

def _send_email(user, emails, content_described, content):
	try:
		for email in emails.split('|'):
			if email.find('@') > -1:
				sendmail(email, content_described, content)
	except:
		notify_message = u"发送邮件失败user_id（{}）, cause:\n{}".format(user.id,unicode_full_stack())
		watchdog_warning(notify_message)
