#_author_:张三香 2016.08.31

Feature:自营平台财务审核订单列表查询
	"""
		1、财务审核订单列表查询条件包含
			订单编号:精确匹配，按母订单进行查询
			下单时间:开始时间必须小于等于结束时间
			收货人姓名：精确匹配
			支付方式：默认显示全部
			供货商类型：默认为全部（全部、同步供货商、自建供货商）
			收货人电话:精确匹配
			物流单号:精确匹配
			订单状态:默认显示全部（全部、团购退款、退款中、退款成功）
			商品名称：模糊匹配
			订单类型：默认为全部（全部、团购订单）
		2、查询时是按照子订单进行筛选结果
	"""

Background:
	Given 重置'weizoom_card'的bdd环境
	Given 重置'apiserver'的bdd环境
	Given zy1登录系统
	And zy1设定会员积分策略
		"""
		{
			"integral_each_yuan":2
		}
		"""
	And zy1已有微众卡支付权限
	And zy1已添加支付方式
		"""
		[{
			"type":"货到付款"
		},{
			"type":"微信支付"
		},{
			"type":"支付宝"
		},{
			"type":"微众卡支付"
		}]
		"""
	#创建微众卡
		Given test登录管理系统::weizoom_card
		When test新建通用卡::weizoom_card
			"""
			[{
				"name":"100元微众卡",
				"prefix_value":"100",
				"type":"virtual",
				"money":"100.00",
				"num":"2",
				"comments":"微众卡"
			}]
			"""
		#微众卡审批出库
		When test下订单::weizoom_card
			"""
			[{
				"card_info":[{
					"name":"100元微众卡",
					"order_num":"2",
					"start_date":"2016-04-07 00:00",
					"end_date":"2019-10-07 00:00"
				}],
				"order_info":{
					"order_id":"0001"
					}
			}]
			"""
		#激活微众
		When test激活卡号'100000001'的卡::weizoom_card
	#创建供货商、设置商家运费、同步商品到自营平台
		#创建供货商
			Given 创建一个特殊的供货商，就是专门针对商品池供货商
				"""
				{
					"supplier_name":"商家1"
				}
				"""
			Given 创建一个特殊的供货商，就是专门针对商品池供货商
				"""
				{
					"supplier_name":"商家2"
				}
				"""
			Given 创建一个特殊的供货商，就是专门针对商品池供货商
				"""
				{
					"supplier_name":"商家3"
				}
				"""
		#设置商家运费
			#商家1设置运费-满10包邮，否则收取统一运费1元
			Then 给供货商添加运费配置
				"""
				{
					"supplier_name": "商家1",
					"postage":1,
					"condition_money": "10"
				}
				"""
		#同步商品到自营平台
			Given 给自营平台同步商品
				"""
				{
					"accounts":["zy1"],
					"supplier_name":"商家1",
					"name": "商品1a",
					"promotion_title": "商品1a促销",
					"purchase_price": 9.00,
					"price": 10.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品1a描述信息"
				}
				"""
			Given 给自营平台同步商品
				"""
				{
					"accounts":["zy1"],
					"supplier_name":"商家1",
					"name": "商品1b",
					"promotion_title": "商品1b促销",
					"purchase_price": 8.00,
					"price": 9.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品1b描述信息"
				}
				"""
			Given 给自营平台同步商品
				"""
				{
					"accounts":["zy1"],
					"supplier_name":"商家2",
					"name": "商品2a",
					"promotion_title": "商品2a促销",
					"purchase_price": 9.00,
					"price": 10.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品2a描述信息"
				}
				"""
			Given 给自营平台同步商品
				"""
				{
					"accounts":["zy1"],
					"supplier_name":"商家2",
					"name": "商品2b",
					"promotion_title": "商品2b促销",
					"purchase_price": 19.00,
					"price": 20.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品2b描述信息"
				}
				"""
			Given 给自营平台同步商品
				"""
				{
					"accounts":["zy1"],
					"supplier_name":"商家3",
					"name": "商品3a",
					"promotion_title": "商品3a促销",
					"purchase_price": 9.00,
					"price": 10.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品3a描述信息"
				}
				"""
			Given 给自营平台同步商品
				"""
				{
					"accounts":["zy1"],
					"supplier_name":"商家3",
					"name": "商品3b",
					"promotion_title": "商品3b促销",
					"purchase_price": 19.00,
					"price": 20.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品3b描述信息"
				}
				"""
	#自营平台从商品池上架商品
		Given zy1登录系统
		When zy1上架商品池商品"商品1a"
		When zy1上架商品池商品"商品1b"
		When zy1上架商品池商品"商品2a"
		When zy1上架商品池商品"商品2b"
		When zy1上架商品池商品"商品3a"
		When zy1上架商品池商品"商品3b"
	When bill关注zy1的公众号
	When tom关注zy1的公众号
	When lily关注zy1的公众号
	#订单数据
		#单个子订单-10101-退款中-商品1a
			When bill访问zy1的webapp::apiserver
			When bill绑定微众卡::apiserver
				"""
				{
					"binding_date":"2016-06-16",
					"binding_shop":"zy1",
					"weizoom_card_info":
						{
							"id":"100000001",
							"password":"1234567"
						}
				}
				"""
			When bill购买zy1的商品::apiserver
				"""
				{
					"order_id": "10101",
					"date":"2016-08-29",
					"products": [{
						"name": "商品1a",
						"count": 1
					}],
					"pay_type":"微信支付",
					"ship_name":"张大大",
					"ship_tel":"18511223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "海淀科技大厦"
				}
				"""
			And bill使用支付方式'微信支付'进行支付::apiserver
			Given zy1登录系统
			When zy1'申请退款'自营订单'10101-商家1'
				"""
				{
					"cash":0.00,
					"weizoom_card":0.00,
					"coupon_money":5.00,
					"integral":10,
					"integral_money":5.00
				}
				"""
		#单个子订单-10201-退款成功-商品1a,1+商品1b,b
			When bill购买zy1的商品::apiserver
				"""
				{
					"order_id": "10201",
					"date":"2016-08-30",
					"products": [{
						"name": "商品1a",
						"count": 1
					},{
						"name": "商品1b",
						"count": 1
					}],
					"weizoom_card":[{
						"card_name":"100000001",
						"card_pass":"1234567"
						}],
					"pay_type":"支付宝",
					"ship_name":"赵二喜",
					"ship_tel":"18511223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "海淀科技大厦"
				}
				"""
			Given zy1登录系统
			When zy1'申请退款'自营订单'10201-商家1'
				"""
				{
					"cash":0.00,
					"weizoom_card":9.00,
					"coupon_money":5.00,
					"integral":10,
					"integral_money":5.00
				}
				"""
			When zy1通过财务审核'退款成功'自营订单'10201-商家1'
		#多个子订单
			#商品1a,商品2a,商品3a-bill
			#201-待发货（待发货/待发货/退款中（退款成功））
				When bill购买zy1的商品::apiserver
					"""
					{
						"order_id": "20101",
						"date":"2016-09-01",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3a",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"赵二喜",
						"ship_tel":"18211223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And bill使用支付方式'微信支付'进行支付::apiserver
				When bill购买zy1的商品::apiserver
					"""
					{
						"order_id": "20102",
						"date":"2016-09-01",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3a",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"赵二喜",
						"ship_tel":"18211223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And bill使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1'申请退款'自营订单'20101-商家3'
					"""
					{
						"cash":0.00,
						"weizoom_card":0.00,
						"coupon_money":5.00,
						"integral":10,
						"integral_money":5.00
					}
					"""
				When zy1'申请退款'自营订单'20102-商家3'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'20102-商家3'
			#202-待发货（待发货/已发货/退款中（退款成功））
				When bill购买zy1的商品::apiserver
					"""
					{
						"order_id": "20201",
						"date":"2016-09-02",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3a",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"赵二喜",
						"ship_tel":"18221223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And bill使用支付方式'微信支付'进行支付::apiserver
				When bill购买zy1的商品::apiserver
					"""
					{
						"order_id": "20202",
						"date":"2016-09-02",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3a",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"赵二喜",
						"ship_tel":"18221223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And bill使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1对订单进行发货
					"""
					{
						"order_no": "20201-商家2",
						"logistics": "申通快递",
						"number": "2020102",
						"shipper": "zy1"
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "20202-商家2",
						"logistics": "申通快递",
						"number": "2020202",
						"shipper": "zy1"
					}
					"""
				When zy1'申请退款'自营订单'20201-商家3'
					"""
					{
						"cash":0.00,
						"weizoom_card":0.00,
						"coupon_money":5.00,
						"integral":10,
						"integral_money":5.00
					}
					"""
				When zy1'申请退款'自营订单'20202-商家3'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'20202-商家3'
			#203-待发货（待发货/退款中/退款中（退款成功））
				When bill购买zy1的商品::apiserver
					"""
					{
						"order_id": "20301",
						"date":"2016-09-03",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3a",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"赵二喜",
						"ship_tel":"18231223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And bill使用支付方式'微信支付'进行支付::apiserver
				When bill购买zy1的商品::apiserver
					"""
					{
						"order_id": "20302",
						"date":"2016-09-03",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3a",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"赵二喜",
						"ship_tel":"18231223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And bill使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1'申请退款'自营订单'20301-商家2'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'20301-商家3'
					"""
					{
						"cash":0.00,
						"weizoom_card":0.00,
						"coupon_money":5.00,
						"integral":10,
						"integral_money":5.00
					}
					"""
				When zy1'申请退款'自营订单'20302-商家2'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'20302-商家3'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'20302-商家3'
			#204-待发货（待发货/已完成/退款中（退款成功））
				When bill购买zy1的商品::apiserver
					"""
					{
						"order_id": "20401",
						"date":"2016-09-04",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3a",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"赵二喜",
						"ship_tel":"18241223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And bill使用支付方式'微信支付'进行支付::apiserver
				When bill购买zy1的商品::apiserver
					"""
					{
						"order_id": "20402",
						"date":"2016-09-04",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3a",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"赵二喜",
						"ship_tel":"18241223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And bill使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1对订单进行发货
					"""
					{
						"order_no": "20401-商家2",
						"logistics": "申通快递",
						"number": "2040102",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'20401-商家2'
				When zy1'申请退款'自营订单'20401-商家3'
					"""
					{
						"cash":0.00,
						"weizoom_card":0.00,
						"coupon_money":5.00,
						"integral":10,
						"integral_money":5.00
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "20402-商家2",
						"logistics": "申通快递",
						"number": "2040202",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'20402-商家2'
				When zy1'申请退款'自营订单'20402-商家3'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'20402-商家3'
			#205-待发货（待发货/退款成功/退款成功）
				When bill购买zy1的商品::apiserver
					"""
					{
						"order_id": "20501",
						"date":"2016-09-05",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3a",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"赵二喜",
						"ship_tel":"18251223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And bill使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1'申请退款'自营订单'20501-商家2'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'20501-商家2'
				When zy1'申请退款'自营订单'20501-商家3'
					"""
					{
						"cash":0.00,
						"weizoom_card":0.00,
						"coupon_money":5.00,
						"integral":10,
						"integral_money":5.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'20501-商家3'

			#商品1a,商品2b,商品3b-tom
			#301-已发货（已发货/已发货/退款中（退款成功））
				When tom购买zy1的商品::apiserver
					"""
					{
						"order_id": "30101",
						"date":"2016-09-13",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2b",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张山山",
						"ship_tel":"18311223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And tom使用支付方式'微信支付'进行支付::apiserver
				When tom购买zy1的商品::apiserver
					"""
					{
						"order_id": "30102",
						"date":"2016-09-13",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2b",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"支付宝",
						"ship_name":"张山山",
						"ship_tel":"18311223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And tom使用支付方式'支付宝'进行支付::apiserver
				Given zy1登录系统
				When zy1对订单进行发货
					"""
					{
						"order_no": "30101-商家1",
						"logistics": "申通快递",
						"number": "3010101",
						"shipper": "zy1"
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "30101-商家2",
						"logistics": "申通快递",
						"number": "3010102",
						"shipper": "zy1"
					}
					"""
				When zy1'申请退款'自营订单'30101-商家3'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":5.00,
						"integral":10,
						"integral_money":5.00
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "30102-商家1",
						"logistics": "申通快递",
						"number": "3010201",
						"shipper": "zy1"
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "30102-商家2",
						"logistics": "申通快递",
						"number": "3010202",
						"shipper": "zy1"
					}
					"""
				When zy1'申请退款'自营订单'30102-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'30102-商家3'
			#302-已发货（已发货/退款中/退款中（已完成）（退款成功））
				When tom购买zy1的商品::apiserver
					"""
					{
						"order_id": "30201",
						"date":"2016-09-13",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2b",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张山山",
						"ship_tel":"18321223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And tom使用支付方式'微信支付'进行支付::apiserver
				When tom购买zy1的商品::apiserver
					"""
					{
						"order_id": "30202",
						"date":"2016-09-13",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2b",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张山山",
						"ship_tel":"18321223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And tom使用支付方式'微信支付'进行支付::apiserver
				When tom购买zy1的商品::apiserver
					"""
					{
						"order_id": "30203",
						"date":"2016-09-12",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2b",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张山山",
						"ship_tel":"18321223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And tom使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1对订单进行发货
					"""
					{
						"order_no": "30201-商家1",
						"logistics": "申通快递",
						"number": "3020101",
						"shipper": "zy1"
					}
					"""
				When zy1'申请退款'自营订单'30201-商家2'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'30201-商家3'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":5.00,
						"integral":10,
						"integral_money":5.00
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "30202-商家1",
						"logistics": "申通快递",
						"number": "3020201",
						"shipper": "zy1"
					}
					"""
				When zy1'申请退款'自营订单'30202-商家2'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "30202-商家3",
						"logistics": "申通快递",
						"number": "3020203",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'30202-商家3'
				When zy1对订单进行发货
					"""
					{
						"order_no": "30203-商家1",
						"logistics": "申通快递",
						"number": "3020301",
						"shipper": "zy1"
					}
					"""
				When zy1'申请退款'自营订单'30203-商家2'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'30203-商家3'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":5.00,
						"integral":10,
						"integral_money":5.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'30203-商家3'
			#303-已发货（已发货/已完成/退款成功）
				When tom购买zy1的商品::apiserver
					"""
					{
						"order_id": "30301",
						"date":"2016-09-13",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2b",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张山山",
						"ship_tel":"18331223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And tom使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1对订单进行发货
					"""
					{
						"order_no": "30301-商家1",
						"logistics": "申通快递",
						"number": "3030101",
						"shipper": "zy1"
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "30301-商家2",
						"logistics": "申通快递",
						"number": "3030102",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'30301-商家2'
				When zy1'申请退款'自营订单'30301-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'30301-商家3'
			#304-已发货（已发货/退款成功/退款成功）
				When tom购买zy1的商品::apiserver
					"""
					{
						"order_id": "30401",
						"date":"2016-09-13",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2b",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张山山",
						"ship_tel":"18341223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And tom使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1对订单进行发货
					"""
					{
						"order_no": "30401-商家1",
						"logistics": "申通快递",
						"number": "3040101",
						"shipper": "zy1"
					}
					"""
				When zy1'申请退款'自营订单'30401-商家2'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'30401-商家2'
				When zy1'申请退款'自营订单'30401-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'30401-商家3'

			#商品1a,商品2a,商品3b-lily
			#401-退款中（退款中/退款中/退款中（已完成）（退款成功））
				When lily购买zy1的商品::apiserver
					"""
					{
						"order_id": "40101",
						"date":"2016-09-14",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张小四",
						"ship_tel":"18411223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And lily使用支付方式'微信支付'进行支付::apiserver
				When lily购买zy1的商品::apiserver
					"""
					{
						"order_id": "40102",
						"date":"2016-09-14",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张小四",
						"ship_tel":"18421223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And lily使用支付方式'微信支付'进行支付::apiserver
				When lily购买zy1的商品::apiserver
					"""
					{
						"order_id": "40103",
						"date":"2016-09-14",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张小四",
						"ship_tel":"18431223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And lily使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1'申请退款'自营订单'40101-商家1'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'40101-商家2'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'40101-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'40102-商家1'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'40102-商家2'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "40102-商家3",
						"logistics": "申通快递",
						"number": "4010203",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'40102-商家3'
				When zy1'申请退款'自营订单'40103-商家1'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'40103-商家2'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'40103-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'40103-商家3'
			#402-退款中（退款中/已完成/已完成（退款成功））
				When lily购买zy1的商品::apiserver
					"""
					{
						"order_id": "40201",
						"date":"2016-09-14",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张小四",
						"ship_tel":"18411223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And lily使用支付方式'微信支付'进行支付::apiserver
				When lily购买zy1的商品::apiserver
					"""
					{
						"order_id": "40202",
						"date":"2016-09-14",
						"products": [{
							"name": "商品1a",
							"count": 1
						},{
							"name": "商品2a",
							"count": 1
						},{
							"name": "商品3b",
							"count": 1
						}],
						"pay_type":"微信支付",
						"ship_name":"张小四",
						"ship_tel":"18421223344",
						"ship_area": "北京市 北京市 海淀区",
						"ship_address": "海淀科技大厦"
					}
					"""
				And lily使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1'申请退款'自营订单'40201-商家1'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "40201-商家2",
						"logistics": "申通快递",
						"number": "4020102",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'40201-商家2'
				When zy1对订单进行发货
					"""
					{
						"order_no": "40201-商家3",
						"logistics": "申通快递",
						"number": "4020103",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'40201-商家3'
				When zy1'申请退款'自营订单'40202-商家1'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1对订单进行发货
					"""
					{
						"order_no": "40202-商家2",
						"logistics": "申通快递",
						"number": "4020202",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'40202-商家2'
				When zy1'申请退款'自营订单'40202-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'40202-商家3'
			#403-退款中（退款中/退款成功/退款成功）
				When lily购买zy1的商品::apiserver
						"""
						{
							"order_id": "40301",
							"date":"2016-09-14",
							"products": [{
								"name": "商品1a",
								"count": 1
							},{
								"name": "商品2a",
								"count": 1
							},{
								"name": "商品3b",
								"count": 1
							}],
							"pay_type":"微信支付",
							"ship_name":"张小四",
							"ship_tel":"18431223344",
							"ship_area": "北京市 北京市 海淀区",
							"ship_address": "海淀科技大厦"
						}
						"""
				And lily使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1'申请退款'自营订单'40301-商家1'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1'申请退款'自营订单'40301-商家2'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'40301-商家2'
				When zy1'申请退款'自营订单'40301-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'40301-商家3'

			#501-已完成（已完成/已完成/退款成功）
				When lily购买zy1的商品::apiserver
						"""
						{
							"order_id": "50101",
							"date":"2016-09-15",
							"products": [{
								"name": "商品1a",
								"count": 1
							},{
								"name": "商品2a",
								"count": 1
							},{
								"name": "商品3b",
								"count": 1
							}],
							"pay_type":"微信支付",
							"ship_name":"张小五",
							"ship_tel":"18511223344",
							"ship_area": "北京市 北京市 海淀区",
							"ship_address": "海淀科技大厦"
						}
						"""
				And lily使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1对订单进行发货
					"""
					{
						"order_no": "50101-商家1",
						"logistics": "申通快递",
						"number": "5010101",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'50101-商家1'
				When zy1对订单进行发货
					"""
					{
						"order_no": "50101-商家2",
						"logistics": "申通快递",
						"number": "5010102",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'50101-商家2'
				When zy1'申请退款'自营订单'50101-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'50101-商家3'
			#502-已完成（已完成/退款成功/退款成功）
				When lily购买zy1的商品::apiserver
						"""
						{
							"order_id": "50201",
							"date":"2016-09-15",
							"products": [{
								"name": "商品1a",
								"count": 1
							},{
								"name": "商品2a",
								"count": 1
							},{
								"name": "商品3b",
								"count": 1
							}],
							"pay_type":"微信支付",
							"ship_name":"张小五",
							"ship_tel":"18521223344",
							"ship_area": "北京市 北京市 海淀区",
							"ship_address": "海淀科技大厦"
						}
						"""
				And lily使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1对订单进行发货
					"""
					{
						"order_no": "50201-商家1",
						"logistics": "申通快递",
						"number": "5020101",
						"shipper": "zy1"
					}
					"""
				When zy1完成订单'50201-商家1'
				When zy1'申请退款'自营订单'50201-商家2'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'50201-商家2'
				When zy1'申请退款'自营订单'50201-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'50201-商家3'

			#601-退款成功（退款成功/退款成功/退款成功）
				When lily购买zy1的商品::apiserver
						"""
						{
							"order_id": "60101",
							"date":"2016-09-16",
							"products": [{
								"name": "商品1a",
								"count": 1
							},{
								"name": "商品2a",
								"count": 1
							},{
								"name": "商品3b",
								"count": 1
							}],
							"pay_type":"微信支付",
							"ship_name":"张大大",
							"ship_tel":"18411223344",
							"ship_area": "北京市 北京市 海淀区",
							"ship_address": "海淀科技大厦"
						}
						"""
				And lily使用支付方式'微信支付'进行支付::apiserver
				Given zy1登录系统
				When zy1'申请退款'自营订单'60101-商家1'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'60101-商家1'
				When zy1'申请退款'自营订单'60101-商家2'
					"""
					{
						"cash":10.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'60101-商家2'
				When zy1'申请退款'自营订单'60101-商家3'
					"""
					{
						"cash":20.00,
						"weizoom_card":0.00,
						"coupon_money":0.00,
						"integral":0,
						"integral_money":0.00
					}
					"""
				When zy1通过财务审核'退款成功'自营订单'60101-商家3'

			#701-待支付
					When lily购买zy1的商品::apiserver
						"""
						{
							"order_id": "70101",
							"date":"2016-09-17",
							"products": [{
								"name": "商品1a",
								"count": 1
							},{
								"name": "商品2a",
								"count": 1
							},{
								"name": "商品3b",
								"count": 1
							}],
							"pay_type":"微信支付",
							"ship_name":"张大大",
							"ship_tel":"18711223344",
							"ship_area": "北京市 北京市 海淀区",
							"ship_address": "海淀科技大厦"
						}
						"""

	#方便校验数据（已注释，请勿删除）
		# | order_no | status   |       group               | final_price | buyer | order_date |ship_name|  ship_tel   |pay_type |
		# | 70101    | 待支付   | [商品1a,10.00,1] 待支付   | 0.00        | lily  | 2016-09-17 | 张小七  | 18711223344 |微信支付 |
		# | 60101    | 退款成功 | [商品1a,10.00,1] 退款成功 | 0.00        | lily  | 2016-09-16 | 张小六  | 18611223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 退款成功 |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 50201    | 已完成   | [商品1a,10.00,1] 已完成   | 10.00       | lily  | 2016-09-15 | 张小五  | 18521223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 退款成功 |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 50101    | 已完成   | [商品1a,10.00,1] 已完成   | 20.00       | lily  | 2016-09-15 | 张小五  | 18511223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 已完成   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 40301    | 退款中   | [商品1a,10.00,1] 退款中   | 10.00       | lily  | 2016-09-14 | 张小四  | 18431223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 退款成功 |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 40202    | 退款中   | [商品1a,10.00,1] 退款中   | 20.00       | lily  | 2016-09-14 | 张小四  | 18421223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 已完成   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 40202    | 退款中   | [商品1a,10.00,1] 退款中   | 40.00       | lily  | 2016-09-14 | 张小四  | 18411223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 已完成   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 已完成   |             |       |            |         |             |         |
		# | 40103    | 退款中   | [商品1a,10.00,1] 退款中   | 20.00       | lily  | 2016-09-14 | 张小四  | 18431223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 退款中   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 40102    | 退款中   | [商品1a,10.00,1] 退款中   | 40.00       | lily  | 2016-09-14 | 张小四  | 18421223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 退款中   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 40101    | 退款中   | [商品1a,10.00,1] 退款中   | 40.00       | lily  | 2016-09-14 | 张小四  | 18411223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 退款中   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款中   |             |       |            |         |             |         |
		# | 30401    | 已发货   | [商品1a,10.00,1] 已发货   | 10.00       | tom   | 2016-09-13 | 张山山  | 18341223344 |微信支付 |
		# |          |          | [商品2b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 30301    | 已发货   | [商品1a,10.00,1] 已发货   | 30.00       | tom   | 2016-09-13 | 张山山  | 18331223344 |微信支付 |
		# |          |          | [商品2b,20.00,1] 已完成   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 30203    | 已发货   | [商品1a,10.00,1] 已发货   | 40.00       | tom   | 2016-09-13 | 张山山  | 18321223344 |微信支付 |
		# |          |          | [商品2b,20.00,1] 退款中   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 30202    | 已发货   | [商品1a,10.00,1] 已发货   | 30.00       | tom   | 2016-09-13 | 张山山  | 18321223344 |微信支付 |
		# |          |          | [商品2b,20.00,1] 退款中   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 已完成   |             |       |            |         |             |         |
		# | 30201    | 已发货   | [商品1a,10.00,1] 已发货   | 50.00       | tom   | 2016-09-13 | 张山山  | 18321223344 |微信支付 |
		# |          |          | [商品2b,20.00,1] 退款中   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款中   |             |       |            |         |             |         |
		# | 30102    | 已发货   | [商品1a,10.00,1] 已发货   | 30.00       | tom   | 2016-09-13 | 张山山  | 18311223344 |支付宝   |
		# |          |          | [商品2b,20.00,1] 已发货   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款成功 |             |       |            |         |             |         |
		# | 30101    | 已发货   | [商品1a,10.00,1] 已发货   | 40.00       | tom   | 2016-09-13 | 张山山  | 18311223344 |微信支付 |
		# |          |          | [商品2b,20.00,1] 已发货   |             |       |            |         |             |         |
		# |          |          | [商品3b,20.00,1] 退款中   |             |       |            |         |             |         |
		# | 20501    | 待发货   | [商品1a,10.00,1] 待发货   | 20.00       | bill  | 2016-09-05 | 赵二喜  | 18251223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 退款成功 |             |       |            |         |             |         |
		# |          |          | [商品3a,10.00,1] 退款成功 |             |       |            |         |             |         |
		# | 20402    | 待发货   | [商品1a,10.00,1] 待发货   | 20.00       | bill  | 2016-09-04 | 赵二喜  | 18241223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 已完成   |             |       |            |         |             |         |
		# |          |          | [商品3a,10.00,1] 退款成功 |             |       |            |         |             |         |
		# | 20401    | 待发货   | [商品1a,10.00,1] 待发货   | 30.00       | bill  | 2016-09-04 | 赵二喜  | 18241223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 已完成   |             |       |            |         |             |         |
		# |          |          | [商品3a,10.00,1] 退款中   |             |       |            |         |             |         |
		# | 20302    | 待发货   | [商品1a,10.00,1] 待发货   | 20.00       | bill  | 2016-09-03 | 赵二喜  | 18231223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 退款中   |             |       |            |         |             |         |
		# |          |          | [商品3a,10.00,1] 退款成功 |             |       |            |         |             |         |
		# | 20301    | 待发货   | [商品1a,10.00,1] 待发货   | 30.00       | bill  | 2016-09-03 | 赵二喜  | 18231223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 退款中   |             |       |            |         |             |         |
		# |          |          | [商品3a,10.00,1] 退款中   |             |       |            |         |             |         |
		# | 20202    | 待发货   | [商品1a,10.00,1] 待发货   | 20.00       | bill  | 2016-09-02 | 赵二喜  | 18221223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 已发货   |             |       |            |         |             |         |
		# |          |          | [商品3a,10.00,1] 退款成功 |             |       |            |         |             |         |
		# | 20201    | 待发货   | [商品1a,10.00,1] 待发货   | 30.00       | bill  | 2016-09-02 | 赵二喜  | 18221223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 已发货   |             |       |            |         |             |         |
		# |          |          | [商品3a,10.00,1] 退款中   |             |       |            |         |             |         |
		# | 20102    | 待发货   | [商品1a,10.00,1] 待发货   | 20.00       | bill  | 2016-09-01 | 赵二喜  | 18211223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 待发货   |             |       |            |         |             |         |
		# |          |          | [商品3a,10.00,1] 退款成功 |             |       |            |         |             |         |
		# | 20101    | 待发货   | [商品1a,10.00,1] 待发货   | 30.00       | bill  | 2016-09-01 | 赵二喜  | 18211223344 |微信支付 |
		# |          |          | [商品2a,10.00,1] 待发货   |             |       |            |         |             |         |
		# |          |          | [商品3a,10.00,1] 退款中   |             |       |            |         |             |         |

		# | 10201    | 退款成功  | [商品1a,10.00,1] 退款成功 | 10.00       | bill  | 2016-08-30 | 张大大  | 18121223344 |优惠抵扣 |
		# |          |           | [商品1b,9.00,1]  运费1   |             |       |            |         |             |         |
		# | 10101    | 退款中    | [商品1a,10.00,1] 退款中   | 30.00       | bill  | 2016-08-29 | 张大大  | 18111223344 |微信支付 |

@order @finance @refund
Scenario:1 ziying自营平台财务审核订单列表查询
	Given zy1登录系统
	#按照'订单编号'查询
		#默认查询
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"60101"
			},{
				"order_no":"50201"
			},{
				"order_no":"50101"
			},{
				"order_no":"40301"
			},{
				"order_no":"40202"
			},{
				"order_no":"40201"
			},{
				"order_no":"40103"
			},{
				"order_no":"40102"
			},{
				"order_no":"40101"
			},{
				"order_no":"30401"
			},{
				"order_no":"30301"
			},{
				"order_no":"30203"
			},{
				"order_no":"30202"
			},{
				"order_no":"30201"
			},{
				"order_no":"30102"
			},{
				"order_no":"30101"
			},{
				"order_no":"20501"
			},{
				"order_no":"20402"
			},{
				"order_no":"20401"
			},{
				"order_no":"20302"
			},{
				"order_no":"20301"
			},{
				"order_no":"20202"
			},{
				"order_no":"20201"
			},{
				"order_no":"20102"
			},{
				"order_no":"20101"
			},{
				"order_no":"10201"
			},{
				"order_no":"10101"
			}]
			"""
		#完全匹配查询
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"60101",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"60101"
			}]
			"""
		#查询结果为空
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"123",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[]
			"""
	#按照'下单时间'查询
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"2016-08-28 00:00-2016-08-31 00:00",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"10201"
			},{
				"order_no":"10101"
			}]
			"""
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"2016-08-27 00:00-2016-08-28 00:00",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[]
			"""
	#按照'收货人姓名'查询
		#完全匹配
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"张大大",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"10201"
			},{
				"order_no":"10101"
			}]
			"""
		#查询结果为空
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"aa",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[]
			"""
	#按照'支付方式'查询
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"优惠抵扣",
				"supplier_type":"全部",
				"ship_tel":"张大大",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"10201"
			}]
			"""
	#按照'收货人电话'查询
		#完全匹配
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"18111223344",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"10201"
			},{
				"order_no":"10101"
			}]
			"""
		#查询结果为空
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"181",
				"number":"",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[]
			"""
	#按照'物流单号'查询
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"3010102",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"30101"
			}]
			"""
		#查询结果为空
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"1122",
				"status":"全部",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[]
			"""
	#按照'订单状态'查询
		#查询'退款中'状态的订单
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"退款中",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'退款中'订单列表
			"""
			[{
				"order_no":"40301"
			},{
				"order_no":"40202"
			},{
				"order_no":"40201"
			},{
				"order_no":"40103"
			},{
				"order_no":"40102"
			},{
				"order_no":"40101"
			},{
				"order_no":"30203"
			},{
				"order_no":"30202"
			},{
				"order_no":"30201"
			},{
				"order_no":"30101"
			},{
				"order_no":"20401"
			},{
				"order_no":"20302"
			},{
				"order_no":"20301"
			},{
				"order_no":"20201"
			},{
				"order_no":"20101"
			},{
				"order_no":"10201"
			},{
				"order_no":"10101"
			}]
			"""
		#查询'退款成功'状态的订单
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"退款成功",
				"product_name":"",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"60101"
			},{
				"order_no":"50201"
			},{
				"order_no":"50101"
			},{
				"order_no":"40301"
			},{
				"order_no":"40202"
			},{
				"order_no":"40103"
			},{
				"order_no":"30401"
			},{
				"order_no":"30301"
			},{
				"order_no":"30203"
			},{
				"order_no":"30102"
			},{
				"order_no":"20501"
			},{
				"order_no":"20402"
			},{
				"order_no":"20302"
			},{
				"order_no":"20202"
			},{
				"order_no":"20102"
			},{
				"order_no":"10201"
			}]
			"""
	#按照'商品名称'查询
		#模糊匹配
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"全部",
				"product_name":"商品",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"60101"
			},{
				"order_no":"50201"
			},{
				"order_no":"50101"
			},{
				"order_no":"40301"
			},{
				"order_no":"40202"
			},{
				"order_no":"40201"
			},{
				"order_no":"40103"
			},{
				"order_no":"40102"
			},{
				"order_no":"40101"
			},{
				"order_no":"30401"
			},{
				"order_no":"30301"
			},{
				"order_no":"30203"
			},{
				"order_no":"30202"
			},{
				"order_no":"30201"
			},{
				"order_no":"30102"
			},{
				"order_no":"30101"
			},{
				"order_no":"20501"
			},{
				"order_no":"20402"
			},{
				"order_no":"20401"
			},{
				"order_no":"20302"
			},{
				"order_no":"20301"
			},{
				"order_no":"20202"
			},{
				"order_no":"20201"
			},{
				"order_no":"20102"
			},{
				"order_no":"20101"
			},{
				"order_no":"10201"
			},{
				"order_no":"10101"
			}]
			"""
		#完全匹配
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"全部",
				"product_name":"商品1b",
				"order_type":"全部"
			}
			"""
		Then zy1获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"10201"
			}]
			"""
	#按照'订单类型'查询
		When zy1设置自营财务审核订单列表查询条件
			"""
			{
				"order_no":"",
				"order_time":"",
				"ship_name":"",
				"pay_type":"全部",
				"supplier_type":"全部",
				"ship_tel":"",
				"number":"",
				"status":"全部",
				"product_name":"商品",
				"order_type":"团购退款"
			}
			"""
		Then zy1获得自营财务审核'团购退款'订单列表
			"""
			[]
			"""
	#组合查询
		When zy1设置自营财务审核订单列表查询条件
				"""
				{
					"order_no":"30102",
					"order_time":"2016-08-28 00:00-2016-09-30 00:00",
					"ship_name":"张山山",
					"pay_type":"支付宝",
					"supplier_type":"全部",
					"ship_tel":"18311223344",
					"number":"3010201",
					"status":"退款成功",
					"product_name":"商品2b",
					"order_type":"全部"
				}
				"""
		Then zy1获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"30102"
			}]
			"""