#author: 王丽 2015-01-13

Feature: 发优惠券-发优惠券记录查询
	Jobs能通过管理系统发优惠券，对发放优惠券的记录进行查询

Background:
	Given jobs登录系统
	And 开启手动清除cookie模式
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		},{
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 50.00
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
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		}, {
			"name": "全体券3",
			"money": 100.00,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	Given bill关注jobs的公众号
	Given tom关注jobs的公众号
	Given marry关注jobs的公众号

	#为会员发放优惠券
		#为单个会员发优惠券
		When jobs为会员发放优惠券于'2015-10-30'
			"""
			{
				"name": "单品券2",
				"count": 2,
				"members": ["bill"],
				"coupon_ids": ["coupon1_id_1"]
			}
			"""
		#发优惠券给多个会员
		When jobs为会员发放优惠券于'2015-11-03'
			"""
			{
				"name": "单品券2",
				"count": 1,
				"members": ["bill", "tom"],
				"coupon_ids": ["coupon1_id_3", "coupon1_id_2"]
			}
			"""
		#为会员多次发送有领取限制的优惠券
		When jobs为会员发放优惠券于'2015-11-07'
			"""
			{
				"name": "全体券3",
				"count": 1,
				"members": ["marry"]
			}
			"""
		When jobs为会员发放优惠券于'2015-11-08'
			"""
			{
				"name": "全体券3",
				"count": 1,
				"members": ["marry"]
			}
			"""
	#会员使用优惠券购买商品
		When bill访问jobs的webapp
		And bill购买jobs的商品
			"""
			{
				"order_id":"0001",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"products": [{
					"name": "商品1",
					"count": 2
				}],
				"coupon": "coupon1_id_1"
			}
			"""
		Then bill成功创建订单
			"""
			{
				"order_no":"0001",
				"status": "待支付",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"final_price": 90.00,
				"coupon_money": 10.00,
				"products": [{
					"name": "商品1",
					"price": 50.00,
					"count": 2
				}]
			}
			"""

@send_coupon @eugene
Scenario:1 发优惠券-优惠券发送记录按照[优惠券名称]查询
	Given jobs登录系统

	When jobs设置发优惠券记录查询条件
		"""
		{}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 0,
			"send_time":"2015-11-07",
			"send_memeber": 0,
			"used_counts": 0
		},{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 1,
			"send_time":"2015-11-07",
			"send_memeber": 1,
			"used_counts": 0
		},{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-11-03",
			"send_memeber": 2,
			"used_counts": 0
		},{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-10-30",
			"send_memeber": 1,
			"used_counts": 1
		}]
		"""

	#按照名称模糊匹配
	When jobs设置发优惠券记录查询条件
		"""
		{
			"coupon_name":"全体"
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 0,
			"send_time":"2015-11-07",
			"send_memeber": 0,
			"used_counts": 0
		},{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 1,
			"send_time":"2015-11-07",
			"send_memeber": 1,
			"used_counts": 0
		}]
		"""
	#按照名称完全匹配
	When jobs设置发优惠券记录查询条件
		"""
		{
			"coupon_name":"单品券2"
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-11-03",
			"send_memeber": 2,
			"used_counts": 0
		},{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-10-30",
			"send_memeber": 1,
			"used_counts": 1
		}]
		"""
	#查询结果为空
	When jobs设置发优惠券记录查询条件
		"""
		{
			"coupon_name":"5"
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[]
		"""

@send_coupon @eugene
Scenario:2 发优惠券-优惠券发送记录按照[优惠券类型]查询
	Given jobs登录系统

	#类型为"全部"
	When jobs设置发优惠券记录查询条件
		"""
		{
			"type":"全部"
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 0,
			"send_time":"2015-11-07",
			"send_memeber": 0,
			"used_counts": 0
		},{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 1,
			"send_time":"2015-11-07",
			"send_memeber": 1,
			"used_counts": 0
		},{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-11-03",
			"send_memeber": 2,
			"used_counts": 0
		},{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-10-30",
			"send_memeber": 1,
			"used_counts": 1
		}]
		"""
	#类型为"单品券"
	When jobs设置发优惠券记录查询条件
		"""
		{
			"type":"单品券"
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-11-03",
			"send_memeber": 2,
			"used_counts": 0
		},{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-10-30",
			"send_memeber": 1,
			"used_counts": 1
		}]
		"""
	#类型为"全体券"
	When jobs设置发优惠券记录查询条件
		"""
		{
			"type":"全体券"
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 0,
			"send_time":"2015-11-07",
			"send_memeber": 0,
			"used_counts": 0
		},{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 1,
			"send_time":"2015-11-07",
			"send_memeber": 1,
			"used_counts": 0
		}]
		"""

@send_coupon @eugene
Scenario:3 发优惠券-优惠券发送记录按照[发放时间]查询
	Given jobs登录系统

	#发放时间为"空"
	When jobs设置发优惠券记录查询条件
		"""
		{
			"start_send_time":"",
			"end_send_time":""
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 0,
			"send_time":"2015-11-07",
			"send_memeber": 0,
			"used_counts": 0
		},{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 1,
			"send_time":"2015-11-07",
			"send_memeber": 1,
			"used_counts": 0
		},{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-11-03",
			"send_memeber": 2,
			"used_counts": 0
		},{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-10-30",
			"send_memeber": 1,
			"used_counts": 1
		}]
		"""
	#发放时间开始时间等于结束时间
	When jobs设置发优惠券记录查询条件
		"""
		{
			"start_send_time":"2015-11-03",
			"end_send_time":"2015-11-03"
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-11-03",
			"send_memeber": 2,
			"used_counts": 0
		}]
		"""
	#发放时间开始时间不等于结束时间
	When jobs设置发优惠券记录查询条件
		"""
		{
			"start_send_time":"2015-11-03",
			"end_send_time":"2015-11-07"
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 0,
			"send_time":"2015-11-07",
			"send_memeber": 0,
			"used_counts": 0
		},{
			"coupon_name":"全体券3",
			"type":"全体券",
			"money": 100.00,
			"send_counts": 1,
			"send_time":"2015-11-07",
			"send_memeber": 1,
			"used_counts": 0
		},{
			"coupon_name":"单品券2",
			"type":"单品券",
			"money": 10.00,
			"send_counts": 2,
			"send_time":"2015-11-03",
			"send_memeber": 2,
			"used_counts": 0
		}]
		"""
	#查询结果为空
	#发放时间开始时间不等于结束时间
	When jobs设置发优惠券记录查询条件
		"""
		{
			"start_send_time":"2015-12-03",
			"end_send_time":"2015-12-07"
		}
		"""
	Then jobs获得发优惠券记录列表
		"""
		[]
		"""

@send_coupon @eugene
Scenario:4 发优惠券-发优惠券记录详情
	Given jobs登录系统

	Then jobs获得发优惠券'单品券2''2015-10-30'的详情
		"""
		[{
			"coupon_id":"coupon1_id_1",
			"money": 10.00,
			"sart_time":"今天",
			"end_time":"1天后",
			"target":"bill",
			"used_time":"今天",
			"order_no":"0001",
			"status": "已使用"
		}]
		"""

	Then jobs获得发优惠券'单品券2''2015-11-03'的详情
		"""
		[{
			"coupon_id":"coupon1_id_2",
			"money": 10.00,
			"sart_time":"今天",
			"end_time":"1天后",
			"target":"bill",
			"used_time":"",
			"order_no":"",
			"status": "未使用"
		},{
			"coupon_id":"coupon1_id_3",
			"money": 10.00,
			"sart_time":"今天",
			"end_time":"1天后",
			"target":"tom",
			"used_time":"",
			"order_no":"",
			"status": "未使用"
		}]
		"""

	Then jobs获得发优惠券'全体券3''2015-11-07'的详情
		"""
		[{
			"coupon_id":"coupon2_id_1",
			"money": 100.00,
			"sart_time":"今天",
			"end_time":"2天后",
			"target":"marry",
			"used_time":"",
			"order_no":"",
			"status": "未使用"
		}]
		"""

	Then jobs获得发优惠券'全体券3''2015-11-08'的详情
		"""
		[]
		"""

	#取消订单，优惠券退回
	When When bill取消订单'0001'

	Then jobs获得发优惠券'单品券2''2015-10-30'的详情
		"""
		[{
			"coupon_id":"coupon1_id_1",
			"money": 10.00,
			"sart_time":"今天",
			"end_time":"1天后",
			"target":"bill",
			"used_time":"",
			"order_no":"",
			"status": "未使用"
		}]
		"""