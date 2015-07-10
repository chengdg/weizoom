# __author__ : "冯雪静"

Feature: 获取分享红包
	Jobs下的会员能通过管理系统获取红包
	
Background:
	Given jobs登录系统
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"pay_interfaces":[{
				"type": "在线支付"
			}, {
				"type": "货到付款"
			}]
		}]
		"""
	
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "全体券1",
			"money": 100.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "单品券2",
			"money": 100.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}]
		"""
	Then jobs能获得优惠券'全体券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	And jobs已添加分享红包
		"""
		[{
			"name": "红包1",
			"prize_info": ["全体券1"],
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "订单满200元可以领取",
			"desc": "下订单领红包",	
			"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
		}, {
			"name": "红包2",
			"prize_info": ["单品券2"],
			"is_permanant_active": true,
			"using_limit": "无限制",
			"desc": "下订单领红包",	
			"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号

 

Scenario: 1 会员通过成功创建订单获取红包
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill创建的订单不满足条件，不能获得jobs的分享红包

	#通过成功创建订单能获取此红包，订单必须满足（订单金额满200元、待发货状态）
	Given jobs登录系统
	When jobs开启分享红包'分享红包1'
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 200.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 2
			}]
		}
		"""
	#bill创建的订单满足条件，能获得jobs的分享红包
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	#bill创建的订单不满足条件，不能获得jobs的分享红包
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""

	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 200.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 2
			}]
		}
		"""
	#bill创建的订单不满足条件，不能获得jobs的分享红包
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 200.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 2
			}]
		}
		"""
	#bill创建的订单满足条件，能获得jobs的分享红包
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}, {
			"coupon_id": "coupon1_id_2",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'全体券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""


Scenario: 2 会员B通过会员A成功创建订单分享红包后获取红包
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包后分享红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill把分享红包的链接分享到朋友圈
	3. tom点击bill分享的链接后，能获得jobs的分享红包
	4. tom再次点击bill分享的链接后，不能获得jobs的分享红包

	#通过成功创建订单能获取此红包，订单必须满足（待发货状态）
	Given jobs登录系统
	When jobs开启分享红包'分享红包2'
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	#When bill把jobs的微站链接分享到朋友圈
	When bill把jobs的分享红包'红包2'的链接分享到朋友圈
	When tom点击bill分享链接
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_2",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 100.00,
			"status": "未使用"
		}, {
			"coupon_id": "coupon2_id_3",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	#When bill把jobs的微站链接分享到朋友圈
	When bill把jobs的分享红包'红包2'的链接分享到朋友圈
	When tom点击bill分享链接
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_2",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon2_id_3": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""


Scenario: 3 非会员通过会员成功创建订单分享红包后获取红包
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包后分享红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill把分享红包的链接分享到朋友圈
	3. nokia点击bill分享的链接后，关注后能获得jobs的分享红包

	Given jobs登录系统
	When jobs开启分享红包'分享红包2'
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	#When bill把jobs的微站链接分享到朋友圈，非会员进行点击
	When bill把jobs的分享红包'红包2'的链接分享到朋友圈
	When nokia点击bill分享链接
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "未知"
			},
			"coupon2_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When nokia关注jobs的公众号
	When nokia访问jobs的webapp
	And nokia能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_2",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "nokia"
			},
			"coupon2_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""


Scenario: 4 会员通过分享链接领取红包时优惠券库存为零,添加库存后,能获取红包
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包后分享红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill把分享红包的链接分享到朋友圈
	3. 优惠券库存为零时，领取红包失败
	4. 添加优惠券库存后，再次点击链接领取成功


	Given jobs登录系统
	When jobs开启分享红包'分享红包2'
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 3,
			"members": ["bill"],
			"coupon_ids": ["coupon2_id_3", "coupon2_id_2", "coupon2_id_1"]
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 100.00,
			"status": "未使用"
		}, {
			"coupon_id": "coupon2_id_2",
			"money": 100.00,
			"status": "未使用"
		}, {
			"coupon_id": "coupon2_id_3",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 100.00,
			"status": "未使用"
		}, {
			"coupon_id": "coupon2_id_2",
			"money": 100.00,
			"status": "未使用"
		}, {
			"coupon_id": "coupon2_id_3",
			"money": 100.00,
			"status": "未使用"
		}, {
			"coupon_id": "coupon2_id_4",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	When bill把jobs的分享红包'红包2'的链接分享到朋友圈
	#tom点击bill分享链接页面展示'很遗憾，红包已经领完了'
	When tom点击bill分享链接
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[]
		"""
	Given jobs登录系统
	When jobs为优惠券'单品券2'添加库存
		"""
		{
			"count": 2,
			"coupon_id_prefix": "coupon2_id_"
		}
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_3": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_4": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_5": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_6": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When tom点击bill分享链接
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_5",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_3": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_4": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_5": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon2_id_6": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""


Scenario: 4 会员通过分享链接领取红包时红包规则被删除，领取红包失败
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包后分享红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill把分享红包的链接分享到朋友圈
	3. 红包规则被删除，领取红包失败

	Given jobs登录系统
	When jobs开启分享红包'分享红包2'
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill成功创建订单
		"""
		{
			"status": "待发货",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	#When bill把jobs的微站链接分享到朋友圈，非会员进行点击
	When bill把jobs的分享红包'红包2'的链接分享到朋友圈
	Given jobs登录系统
	When jobs关闭分享红包'红包2'
	#tom点击bill分享链接页面展示'很遗憾，红包已经领完了'
	When tom点击bill分享链接
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
