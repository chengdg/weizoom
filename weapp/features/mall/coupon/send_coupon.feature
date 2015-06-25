# __author__ : "冯雪静"
Feature: 发放优惠券
	Jobs能通过管理系统将生成的"优惠券"发放给会员

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "单品券2",
			"money": 10.00,
			"each_limit": "不限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}, {
<<<<<<< .working
			"name": "全体券3",
			"money": 100.00,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
=======
			"name": "全体券3",
			"money": 100.00,
			"each_limit": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
>>>>>>> .merge-right.r15430
		}]
		"""
<<<<<<< .working
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	Then jobs能获得优惠券'全体券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	Given bill关注jobs的公众号
	Given tom关注jobs的公众号
=======
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	Then jobs能获得优惠券'全体券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号
>>>>>>> .merge-right.r15430


<<<<<<< .working
@mall2 @send_coupon @eugene
Scenario: 1 发送优惠券给一个会员
	jobs添加"优惠券规则"后，将优惠券"单品券2"发放给一个会员(bill)
=======
 
Scenario: 1 发送优惠券给一个会员
	jobs添加"优惠券规则"后，将优惠券"单品券2"发放给一个会员(bill)
>>>>>>> .merge-right.r15430
	1. bill访问jobs的webapp时能看到获得的优惠券
<<<<<<< .working
	2. tom访问jobs的webapp不能看到bill获得的优惠券
	3. jobs能获得包含发放的优惠券的的优惠券码库

=======
	2. tom访问jobs的webapp不能看到bill获得的优惠券
	3. jobs能获得包含发放的优惠券的的优惠券码库
	
>>>>>>> .merge-right.r15430
	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 2,
<<<<<<< .working
			"members": ["bill"]
=======
			"members": ["bill"],
			"coupon_ids": ["coupon2_id_2", "coupon2_id_1"]
>>>>>>> .merge-right.r15430
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[]
<<<<<<< .working
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @send_coupon @eugene
Scenario: 2 发送优惠券给多个会员
	jobs添加"优惠券规则"后，将优惠券"单品券2"发放给多个会员(bill，tom)
	1. bill访问jobs的webapp时能看到获得的优惠券
	2. tom访问jobs的webapp时能看到获得的优惠券
	3. jobs能获得包含发放的优惠券的优惠券码库

	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 1,
			"members": ["bill", "tom"],
			"coupon_ids": ["coupon2_id_2", "coupon2_id_1"]
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @send_coupon @eugene
Scenario: 3 多次发送有领取限制的优惠券给一个会员
	jobs添加"优惠券规则"后，将优惠券"全体券3"发放给1个会员(bill)
	1. bill访问jobs的webapp时只能看到一张优惠券
	2. jobs能获得包含发放的优惠券的优惠券码库

	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"name": "全体券3",
			"count": 1,
			"members": ["bill"]
		}
		"""
	When jobs为会员发放优惠券
		"""
		{
			"name": "全体券3",
			"count": 1,
			"members": ["bill"]
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon3_id_1",
				"money": 100.00,
				"status": "未使用"
			}
		]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'全体券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon3_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

@mall2 @send_coupon @eugene
Scenario: 4 发送优惠券总数超出优惠券库存
	jobs添加"优惠券规则"后，将优惠券发放给1个会员或多个会员
	1. jobs发放优惠券总数超出库存，jobs能够看到提示信息
	2. bill访问jobs的webapp时不能看到优惠券
	3. jobs能获得发放的优惠券的优惠券码库

	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 5,
			"members": ["bill"],
			"coupon_ids": []
		}
		"""
	Then jobs能获得发放优惠券失败的信息
		"""
		{
			"error_message": "发放数量大于优惠券库存,请先增加库存"
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
=======
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""


Scenario: 2 发送优惠券给多个会员
	jobs添加"优惠券规则"后，将优惠券"单品券2"发放给多个会员(bill，tom)
	1. bill访问jobs的webapp时能看到获得的优惠券
	2. tom访问jobs的webapp时能看到获得的优惠券
	3. jobs能获得包含发放的优惠券的优惠券码库

	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 1,
			"members": ["bill", "tom"],
			"coupon_ids": ["coupon2_id_2", "coupon2_id_1"]
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "tom"
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""


Scenario: 3 多次发送有领取限制的优惠券给一个会员
	jobs添加"优惠券规则"后，将优惠券"全体券3"发放给1个会员(bill)
	1. bill访问jobs的webapp时只能看到一张优惠券
	2. jobs能获得包含发放的优惠券的优惠券码库

	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"name": "全体券3",
			"count": 1,
			"members": ["bill"],
			"coupon_ids": ["coupon3_id_1"]
		}
		"""
	When jobs为会员发放优惠券
		"""
		{
			"name": "全体券3",
			"count": 1,
			"members": ["bill"],
			"coupon_ids": ["coupon3_id_2"]
		}
		"""
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon3_id_1",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'全体券3'的码库
		"""
		{
			"coupon3_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon3_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_3": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon3_id_4": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""


Scenario: 4 发送优惠券总数超出优惠券库存
	jobs添加"优惠券规则"后，将优惠券发放给1个会员或多个会员
	1. jobs发放优惠券总数超出库存，jobs能够看到提示信息
	2. bill访问jobs的webapp时不能看到优惠券
	3. jobs能获得发放的优惠券的优惠券码库

	Given jobs登录系统
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 5,
			"members": ["bill"],
			"coupon_ids": []
		}
		"""
	Then jobs能获得发放优惠券失败的信息'发放数量大于优惠券库存,请先增加库存'
	When bill访问jobs的webapp
	Then bill能获得webapp优惠券列表
		"""
>>>>>>> .merge-right.r15430
		[]
<<<<<<< .working
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 3,
			"members": ["bill", "tom"],
			"coupon_ids": []
		}
		"""
	Then jobs能获得发放优惠券失败的信息
		"""
		{
			"error_message": "发放数量大于优惠券库存,请先增加库存"
		}
		"""
	When bill访问jobs的webapp
=======
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 3,
			"members": ["bill", "tom"],
			"coupon_ids": []
		}
		"""
	Then jobs能获得发放优惠券失败的信息'发放数量大于优惠券库存,请先增加库存'
	When bill访问jobs的webapp
>>>>>>> .merge-right.r15430
	Then bill能获得webapp优惠券列表
		"""
		[]
		"""
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
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""