# -*- coding: utf-8 -*-

import json
from core import api_resource
from wapi.decorators import param_required

from account.account_util import get_logined_user_from_token
from market_tools.tools.coupon.util import consume_coupon
from market_tools.tools.coupon.tasks import send_message_to_member, send_message_to_member_for_weizoom
import mall.promotion.models as promotion_models

#微众自营账号发送反馈未通过审核通知的模板id以及跳转的url
OWNER2TEMPLATE = {
	481: {  #wzjx001
		'template_id': 'ktCjZFwXIrEVEpwPC-Ocv0KklGPcjNL6qa_yoaTdrxY',
		'template_url': 'http://mp.weixin.qq.com/s?__biz=MzA4ODE3MTE5Mw==&mid=401901456&idx=1&sn=90f0301cd6c0f104bf7d1fa897ee4b28'
	},
	677: {  #weizoomxs
		'template_id': 'vpjtAB0vtio1Nr9ejzBkOmNIeT2LhraopdHzJph1tkY',
		'template_url': 'http://mp.weixin.qq.com/s?__biz=MzI4NTA0MzEyMg==&mid=403188126&idx=1&sn=7217a4291527313c520d935f9926ff99'
	},
	676: {  #weizoommm
		'template_id': 'ChQGrx21U7_a1pY_lO2JrbGO2vzTM2sxGcjMqJGx6P4',
		'template_url': 'http://mp.weixin.qq.com/s?__biz=MzIxNTA1NDE0MQ==&mid=401545855&idx=2&sn=e038d3f83f9ca72bc2007f92780392ef'
	}
}

class IssuingCouponsRecord(api_resource.ApiResource):
	"""
	商品-供应商
	"""
	app = 'promotion'
	resource = 'issuing_coupons_record'

	@param_required(['owner_id', 'token', 'member_id', 'coupon_rule_id', 'product_name', 'has_reward'])
	def post(args):
		"""
		获取商品和供应商信息

		@param token 调用该接口的账号token，为了保证安全
		@param member_id 要发送优惠券的会员id
		@param coupon_rule_id 优惠券规则id
		@param has_reward 是否有奖励
		"""
		has_reward = bool(args['has_reward'])
		owner_id = int(args['owner_id'])
		token = args['token']
		member_id = int(args['member_id'])
		coupon_rule_id = int(args['coupon_rule_id'])
		product_name = args['product_name']

		user = get_logined_user_from_token(token)
		if not user:
			err_msg = u'获取商家身份信息失败'
			return {
				'success': False,
				'coupon_id': coupon_id,
				'errMsg': err_msg
			}

		#发送未采纳通知
		if not has_reward:
			template_id = OWNER2TEMPLATE[owner_id]['template_id']
			template_url = OWNER2TEMPLATE[owner_id]['template_url']
			first_text = u'很遗憾，您对“%s”的反馈建议未被采纳呢~' % product_name
			remark_text = u'想知道怎样的反馈才能被采纳么？赶快点击详情了解吧！'
			try:
				send_message_to_member_for_weizoom(owner_id, member_id, template_id, template_url, first_text, remark_text)
				return {
					'success': True,
					'coupon_id': '',
					'errMsg': ''
				}
			except Exception, e:
				print 'send no reward message error:',e
				return {
					'success': False,
					'coupon_id': '',
					'errMsg': e
				}


		#发送优惠券和通知
		success = False
		coupon_id = ''
		err_msg = ''
		first_text = u'恭喜您，您对“%s”的反馈已经被采纳，特为您奉上反馈奖励券一张！' % product_name
		print 'token:',token
		print 'member_id:',member_id
		print 'coupon_rule_id:',coupon_rule_id
		print 'product_name:',product_name
		print 'first_text:',first_text
		print 'owner_id:',owner_id
		
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
			owner_id=owner_id,
			coupon_rule_id=coupon_rule_id,
			pre_person_count=pre_person_count,
			person_count=person_count,
			coupon_count=send_count)
		coupon_record.save()

		print 'coupon_record:',coupon_record.id
		if member_ids:  # 会员列表
			# 对每个会员创建优惠券
			real_person_count = 0
			real_coupon_count = 0
			for member_id in member_ids:
				print 'processing:', member_id
				c_index = 0
				c_real_count = 0
				while c_index < pre_person_count:
					coupon, msg = consume_coupon(owner_id, coupon_rule_id, member_id,
												 coupon_record_id=coupon_record.id, not_block=True)
					# print 'coupon:', coupon.id
					print 'msg:',msg
					if coupon:
						coupon_id = coupon.coupon_id
						c_real_count += 1
						#给用户发优惠券提示
						#duhao 20160108 加了个first_text参数
						send_message_to_member(coupon_rule, member_id, first_text)
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
