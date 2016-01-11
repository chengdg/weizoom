# -*- coding: utf-8 -*-

import json
from core import api_resource
from wapi.decorators import param_required

from account.account_util import get_logined_user_from_token
from market_tools.tools.coupon.util import consume_coupon
from market_tools.tools.coupon.tasks import send_message_to_member
import mall.promotion.models as promotion_models

class IssuingCouponsRecord(api_resource.ApiResource):
	"""
	商品-供应商
	"""
	app = 'promotion'
	resource = 'issuing_coupons_record'

	@param_required(['token', 'member_id', 'coupon_rule_id', 'product_name'])
	def post(args):
		"""
		获取商品和供应商信息

		@param token 调用该接口的账号token，为了保证安全
		@param member_id 要发送优惠券的会员id
		@param coupon_rule_id 优惠券规则id
		"""
		success = False
		coupon_id = ''
		err_msg = ''

		token = args['token']
		member_id = int(args['member_id'])
		coupon_rule_id = int(args['coupon_rule_id'])
		product_name = args['product_name']
		remark_text = u'您对“%s”的反馈已经通过审核，特为您奉上优惠券一张！' % product_name
		# print 'token:',token
		# print 'member_id:',member_id
		# print 'coupon_rule_id:',coupon_rule_id
		
		# return {
		# 	'success': False,
		# 	'coupon_id': coupon_id,
		# 	'errMsg': u'库存不足'
		# }

		user = get_logined_user_from_token(token)
		if not user:
			err_msg = u'获取商家身份信息失败'
			return {
				'success': False,
				'coupon_id': coupon_id,
				'errMsg': err_msg
			}

		# member_ids = request.POST.get('member_id', None)  # 获取会员id 组
		# member_ids = json.loads(member_ids)
		member_ids = [member_id]
		# coupon_rule_id = int(request.POST.get('coupon_rule_id'))  # 优惠券规则
		pre_person_count = 1  # 每人几张
		person_count = 1  # 发放的人数
		send_count = pre_person_count * person_count  # 发放的张数

		# 对应优惠券的库存
		coupon_rule = promotion_models.CouponRule.objects.get(id=coupon_rule_id)
		coupon_count = coupon_rule.remained_count
		if coupon_count < send_count:
			err_msg = u"优惠券库存不足，请先增加库存"
			return {
				'success': False,
				'coupon_id': coupon_id,
				'errMsg': err_msg
			}

		# 创建优惠券记录
		coupon_record = promotion_models.CouponRecord.objects.create(
			owner=request.manager,
			coupon_rule_id=coupon_rule_id,
			pre_person_count=pre_person_count,
			person_count=person_count,
			coupon_count=send_count)
		coupon_record.save()
		if member_ids:  # 会员列表
			# 对每个会员创建优惠券
			real_person_count = 0
			real_coupon_count = 0
			for member_id in member_ids:
				c_index = 0
				c_real_count = 0
				while c_index < pre_person_count:
					coupon, msg = consume_coupon(request.manager.id, coupon_rule_id, member_id,
												 coupon_record_id=coupon_record.id, not_block=True)
					if coupon:
						coupon_id = coupon.coupon_id
						c_real_count += 1
						#给用户发优惠券提示
						#duhao 20160108 加了个remark_text参数
						send_message_to_member(coupon_rule, member_id, remark_text)
					c_index += 1
				if c_real_count:
					real_person_count += 1
					real_coupon_count += c_real_count

			if real_coupon_count < coupon_count:
				# 修正优惠券实际发放数量
				promotion_models.CouponRecord.objects.filter(id=coupon_record.id).update(
					person_count=real_person_count,
					coupon_count=real_coupon_count)

			success = True
		else:
			err_msg = "create_red_enevlop error"

		return {
			'success': success,
			'coupon_id': coupon_id,
			'errMsg': err_msg
		}
