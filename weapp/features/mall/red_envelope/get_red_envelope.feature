# __author__ : "冯雪静"
#editor 新新 2015.10.19

Feature: 获取分享红包
"""
	Jobs下的会员能通过管理系统获取红包 
	1、会员购买店铺的商品，提交订单后满足分享红包活动规则，在"提交订单付款"后会获得一个红包，领取红包即领取了红包对应的优惠券，
	优惠券的使用和普通的优惠券使用规则相同
		1）奖励条件：订单满（X）元
			（1）设置订单金额条件，只有"提交的订单付款成功"的"商品金额"+"运费"满足订单金额条件，才能得到红包
			（2）订单金额大于等于限额才能领取到红包
			（3）修改价格的订单，按照订单原价判断是否满足分享红包活动限额
			（4）限时抢购商品，按照限时抢购价格判断是否满足分享红包活动限额
			（5）使用积分或优惠券的商品，按照商品金额，即使用积分和优惠券的之前的金额判断是否满足分享红包活动限额
			（6）具有会员价的商品，按照商品会员价判断是否满足分享红包活动限额
		2）奖励条件：未设置
		未设置订单条件，只要"提交订单付款成功"，就能获得红包
	2、将红包分享到朋友圈或者分享给朋友，被分享者也能领取红包
	3、每个会员只能领取一个红包
	4、分享红包活动已经结束，会员再通过分享的链接领取红包，领取失败
	5、通过分享红包活动，领取的优惠券，
		1）分享红包活动结束了，对应的优惠券活动未过期，已经领取的优惠券仍然可以使用
		2）分享红包活动未结束，对应的优惠券活动过期，已经领取的优惠券不可以使用
		3）分享红包活动结束了，对应的优惠券活动过期，已经领取的优惠券不可以使用
	6、分享红包活动未结束，对应的优惠券活动过期，提交满足条件的支付完成的订单，没有领取红包
	7、分享红包活动未结束，对应的优惠券活动优惠券库存为零，提交满足条件的支付完成的订单，没有领取红包
"""
	
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
		},{
			"name": "商品2",
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
	And jobs已添加分享红包
		"""
		[{
			"name": "红包1",
			"prize_info": "全体券1",
			"is_permanant_active": false,
			"start_date": "今天",
			"end_date": "2天后",
			"limit_money": "200",
			"receive_method": "下单领取",
			"detail": "活动说明",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark": "分享有礼"
		}, {
			"name": "红包2",
			"prize_info": "单品券2",
			"is_permanant_active": true,
			"limit_money": "无限制",
			"receive_method": "下单领取",
			"detail": "活动说明",
			"share_pic": "/static/upload/6_20140710/1404981209095_5.jpg",
			"remark": "分享有礼"
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	And jobs登录系统
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

@mall2 @promotion @promotionRedbag
Scenario: 1 会员通过成功创建订单获取红包
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill创建的订单不满足条件，不能获得jobs的分享红包

	#通过成功创建订单能获取此红包，订单必须满足（订单金额满200元、待发货状态）
	Given jobs登录系统
	When jobs'开启'分享红包'红包1'
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
	Then bill'能够'领取分享红包
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
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill'不能'领取分享红包
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
	#没有支付，不能领取
	Then bill'不能'领取分享红包
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""

	Given jobs登录系统
	When jobs'关闭'分享红包'红包1'
	And jobs'开启'分享红包'红包2'

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
	Then bill'能够'领取分享红包
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 100.00,
			"status": "未使用"
		}, {
			"coupon_id": "coupon1_id_1",
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

	And jobs能获得优惠券'单品券2'的码库
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

@mall2 @promotion @promotionRedbag
Scenario: 2 会员B通过会员A成功创建订单分享红包后获取红包
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包后分享红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill把分享红包的链接分享到朋友圈
	3. tom点击bill分享的链接后，能获得jobs的分享红包
	4. tom再次点击bill分享的链接后，不能获得jobs的分享红包

	#通过成功创建订单能获取此红包，订单必须满足（待发货状态）
	Given jobs登录系统
	When jobs'开启'分享红包'红包2'
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
	Then bill'能够'领取分享红包
	And bill能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
	When bill把jobs的分享红包链接分享到朋友圈
	When tom访问jobs的webapp
	When tom点击bill分享红包链接
	
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
	Then bill'能够'领取分享红包
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
	When bill把jobs的分享红包链接分享到朋友圈
	When tom点击bill分享红包链接
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


@mall2 @promotion @promotionRedbag
Scenario: 3 非会员通过会员成功创建订单分享红包后获取红包
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包后分享红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill把分享红包的链接分享到朋友圈
	3. nokia点击bill分享的链接后，关注后能获得jobs的分享红包

	Given jobs登录系统
	When jobs'开启'分享红包'红包2'
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
	Then bill'能够'领取分享红包
	When bill把jobs的分享红包链接分享到朋友圈
	#暂时用先关注再取消关注的方式来模拟非会员的情况，需要改进
	When nokia关注jobs的公众号
	And nokia取消关注jobs的公众号
	And nokia访问jobs的webapp
	And nokia点击bill分享红包链接
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
	When nokia关注jobs的公众号
	When nokia访问jobs的webapp
	Then nokia能获得webapp优惠券列表
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

@mall2 @promotion @promotionRedbag
Scenario: 4 会员通过分享链接领取红包时优惠券库存为零,添加库存后,能获取红包
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包后分享红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill把分享红包的链接分享到朋友圈
	3. 优惠券库存为零时，领取红包失败
	4. 添加优惠券库存后，再次点击链接领取成功


	Given jobs登录系统
	When jobs'开启'分享红包'红包2'
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
	Then bill'能够'领取分享红包
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
	When bill把jobs的分享红包链接分享到朋友圈
	#tom点击bill分享链接页面展示'很遗憾，红包已经领完了'
	When tom访问jobs的webapp
	When tom点击bill分享红包链接
	Then tom能获得webapp优惠券列表
		"""
		[]
		"""
	Given jobs登录系统
	When jobs为优惠券'单品券2'添加库存
		"""
		{
			"count": 1,
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
			}
		}
		"""
	When tom访问jobs的webapp
	When tom点击bill分享红包链接
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon2_id_5",
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
			}
		}
		"""

@mall2 @promotion @promotionRedbag
Scenario: 5 会员通过分享链接领取红包时红包规则被删除，领取红包失败
	Jobs添加"分享红包"开启后，会员可通过成功创建订单获取红包后分享红包
	1. bill创建的订单满足条件，能获得jobs的分享红包
	2. bill把分享红包的链接分享到朋友圈
	3. 红包规则被删除，领取红包失败

	Given jobs登录系统
	When jobs'开启'分享红包'红包2'
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
	Then bill'能够'领取分享红包
	When bill把jobs的分享红包链接分享到朋友圈
	Given jobs登录系统
	When jobs'关闭'分享红包'红包2'
	#tom点击bill分享链接页面展示'很遗憾，红包已经领完了'
	When tom访问jobs的webapp
	When tom点击bill分享红包链接
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


# _edit_ : "新新" "雪静"
@mall2 @promotionRedbag  @meberGrade
Scenario: 6 不同等级的会员购买有会员价同时有分享红包设置的商品
#分享红包:金额条件取会员价
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品14",
			"price": 100.00,
			"is_member_product": "on",
			"weight": 1,
			"postage": "系统"
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"discount": "10"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}]
		"""
	When jobs更新'bill'的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "铜牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员"
		}, {
			"name": "bill",
			"member_rank": "铜牌会员"
		}]
		"""
	When jobs'开启'分享红包'红包1'
	#tom创建的订单满足条件，能获得jobs的分享红包
	When tom访问jobs的webapp
	And tom购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品14",
				"count": 2
			}]
		}
		"""
	And tom使用支付方式'货到付款'进行支付
	Then tom'能够'领取分享红包
	And tom能获得webapp优惠券列表
		"""
		[{
			"coupon_id": "coupon1_id_1",
			"money": 100.00,
			"status": "未使用"
		}]
		"""
#bill创建的订单不满足条件，不能获得jobs的分享红包
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品14",
				"count": 2
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	Then bill'不能'领取分享红包
	And bill能获得webapp优惠券列表
		"""
		[]
		"""