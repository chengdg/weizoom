
#_author_:张三香

Feature:发放优惠券时,优惠券总价值的校验
	#说明：
		#针对线上"bug3900"补充feature
		#bug3900:功能问题【促销管理-发优惠券】选择发送会员后，先选择每人限领张数，在选择优惠券，显示金额错误
		#发优惠券时,先选择限领张数,再选择其他'领取限制'的优惠券,验证优惠券金额显示是否正确

Background:
	Given jobs登录系统
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "全体券3",
			"money": 100.00,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""
	And bill关注jobs的公众号

@promotion @promotionSendCoupon 
Scenario: 发放优惠券时,优惠券总价值的校验
	#jobs选择发放对象
	#jobs先选择限领张数:每人2张
	#jobs再添加'领取限制'为'每人1张'的优惠券,
	#验证每人领取张数是否自动变为1,总价值是否显示正确（显示1张优惠券的价值不显示2张的价值）

	Given jobs登录系统
	When jobs设置发放优惠券条件
		"""
		{
			"members": ["bill"],
			"name": "",
			"count": 2
		}
		"""
	Then jobs能获得发放优惠券条件
		"""
		{
			"members": ["bill"],
			"name": "",
			"count": 2,
			"total_values":0.00
		}
		"""
	When jobs添加优惠券'全体券3'
	Then jobs能获得发放优惠券条件
		"""
		{
			"members": ["bill"],
			"name": "全体券3",
			"count": 1,
			"total_values":100.00
		}
		"""