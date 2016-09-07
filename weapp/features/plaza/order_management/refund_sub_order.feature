#_author_:张三香 20160.09.02

Feature:自营平台退款子订单
	"""
	1、对某个子订单点击【申请退款】，弹出退款录入的界面
	2、退款录入界面显示信息:
		a.弹框上方显示：退款录入，当前订单应退￥x.xx（x.xx=商品总金额（商品售价x商品数量）+运费）
		b.展示母订单支付金额详情，格式'母订单支付金额：现金￥x.xx+微众卡￥x.xx+优惠券￥x.xx+积分抵扣￥x.xx=￥x.xx'
		c.当母订单中已经有子订单退款录入时，再对其他子订单操作退款时，添加【已录入退款金额】详情）；录入时，现金、微众卡可退金额需要扣除“已退款金额”的相应部分；
		d.运营人员需要输入当前子订单退款的各个方式对应的金额；其中，现金、微众卡支付金额不得大于母订单支付时的对应金额；
		e.录入的'现金+微众卡+优惠券+积分抵扣'的总和应等于'商品总金额+运费'
		f.积分比例按照系统当前的抵扣比例展示；输入积分数后即按照该比例展示抵扣的金额；
		g.现金、微众卡输入的金额大于最多可退金额时，系统提示“最多可退x元”；
		h.'共计'需要根据已填写的金额实时计算变化;当共计金额与应退金额一致时,才可以提交退款申请;否则点击提交后提示"退款金额不等于x"

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
				"name":"50元微众卡",
				"prefix_value":"100",
				"type":"virtual",
				"money":"50.00",
				"num":"2",
				"comments":"微众卡"
			}]
			"""
		#微众卡审批出库
		When test下订单::weizoom_card
			"""
			[{
				"card_info":[{
					"name":"50元微众卡",
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
			Given 创建一个特殊的供货商
				"""
				{
					"supplier_name":"商家1"
				}
				"""
			Given 创建一个特殊的供货商
				"""
				{
					"supplier_name":"商家2"
				}
				"""
			Given 创建一个特殊的供货商
				"""
				{
					"supplier_name":"商家3"
				}
				"""
		#设置商家运费
			#商家1设置运费-满20包邮，否则收取统一运费1元
			Then 给供货商添加运费配置
				"""
				{
					"supplier_name": "商家1",
					"postage":1,
					"condition_money": "20"
				}
				"""
		#同步商品到自营平台
			Given 给自营平台同步商品
				"""
				{
					"account":["zy1"],
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
					"account":["zy1"],
					"supplier_name":"商家1",
					"name": "商品1b",
					"promotion_title": "商品1b促销",
					"purchase_price": 19.00,
					"price": 20.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品1b描述信息"
				}
				"""
			Given 给自营平台同步商品
				"""
				{
					"account":["zy1"],
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
					"account":["zy1"],
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
	#自营平台从商品池上架商品
		Given jobs登录系统
		When jobs上架商品池商品"商品1a"
		When jobs上架商品池商品"商品1b"
		When jobs上架商品池商品"商品2a"
		When jobs上架商品池商品"商品3a"
	Given zy1登录系统
	When zy1创建限时抢购活动
		"""
		[{
			"name": "商品1b限时抢购",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name":"商品1b",
			"member_grade": "全部会员",
			"count_per_purchase": 2,
			"promotion_price": 15.00,
			"limit_period": 1
		}]
		"""
	#bill购买多个供货商的商品
		When bill关注zy1的公众号
		When bill访问zy1的webapp::apiserver
		#10101-微信支付（商品1b(限时抢购、运费)+商品2a+商品3a）
			When bill购买jobs的商品::apiserver
				"""
				{
					"order_id": "10101",
					"products": [{
						"name": "商品1b",
						"count": 1
					},{
						"name": "商品2a",
						"count": 1
					},{
						"name": "商品3a",
						"count": 1
					}],
					"pay_type":"微信支付",
					"ship_name":"bill",
					"ship_tel":"13811223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "海淀科技大厦"
				}
				"""
			And bill使用支付方式'微信支付'进行支付::apiserver
			When bill访问jobs的webapp::apiserver
			When bill绑定微众卡
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
		#10102-优惠抵扣（微众卡全额支付,满额包邮）-商品1a,2+商品2a,1+商品3a,1
			When bill购买jobs的商品::apiserver
				"""
				{
					"order_id": "10102",
					"products": [{
						"name": "商品1a",
						"count": 2
					},{
						"name": "商品2a",
						"count": 1
					},{
						"name": "商品3a",
						"count": 1
					}],
					"weizoom_card":[{
						"card_name":"100000001",
						"card_pass":"1234567"
						}],
					"pay_type":"微信支付",
					"ship_name":"bill",
					"ship_tel":"13811223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "海淀科技大厦"
				}
				"""
		#10103-微信支付（现金+微众卡，不满足满额包邮）-商品1a,1+商品2a,1+商品3a,1
			When bill购买jobs的商品::apiserver
				"""
				{
					"order_id": "10103",
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
					"weizoom_card":[{
						"card_name":"100000001",
						"card_pass":"1234567"
						}],
					"pay_type":"微信支付",
					"ship_name":"bill",
					"ship_tel":"13811223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "海淀科技大厦"
				}
				"""
			And bill使用支付方式'微信支付'进行支付::apiserver

Scenario:1 ziying自营平台子订单退款（全退现金）
	Given zy1登录系统
	When zy1'申请退款'自营订单'10101-商家1'
		"""
		{
			"cash":16.00,
			"weizoom_card":0.00,
			"coupon_money":0.00,
			"intergal":0,
			"intergal_money":0.00
		}
		"""
	Then zy1获得自营订单'10101'
			"""
			{
				"order_no":"10101",
				"status":"待发货",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "海淀科技大厦"
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"微信支付",
				"group":[{
					"商家1":{
						"order_no":"10101-商家1",
						"products":[{
							"name":"商品1b",
							"price":20.00,
							"count":1,
							"single_save":"直降5.00元"
						}],
						"postage": 1.00,
						"status":"退款中"
						},
					"商家2":{
							"order_no":"10101-商家2",
							"products":[{
								"name":"商品2a",
								"price":10.00,
								"count":1,
								"single_save":""
							}],
							"postage": 0.00,
							"status":"待发货"
						},
					"商家3":{
							"order_no":"10101-商家3",
							"products":[{
								"name":"商品3a",
								"price":10.00,
								"count":1,
								"single_save":""
							}],
							"postage": 0.00,
							"status":"待发货"
						}
				}],
				"total_save":"",
				"weizoom_card":"",
				"products_count":3,
				"product_price": 40.00,
				"postage": 1.00,
				"save_money": -5.00,
				"cash":36.00,
				"final_price": 36.00
			}
			"""

Scenario:2 ziying自营平台子订单退款（全退微众卡）
	Given zy1登录系统
	When zy1'申请退款'自营订单'10102-商家1'
		"""
		{
			"cash":0.00,
			"weizoom_card":20.00,
			"coupon_money":0.00,
			"intergal":0,
			"intergal_money":0.00
		}
		"""
	Then zy1获得自营订单'10102'
			"""
			{
				"order_no":"10102",
				"status":"待发货",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "海淀科技大厦"
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"优惠抵扣",
				"group":[{
					"商家1":{
						"order_no":"10102-商家1",
						"products":[{
							"name":"商品1a",
							"price":10.00,
							"count":2,
							"single_save":""
						}],
						"postage": 0.00,
						"status":"退款中"
						},
					"商家2":{
							"order_no":"10102-商家2",
							"products":[{
								"name":"商品2a",
								"price":10.00,
								"count":1,
								"single_save":""
							}],
							"postage": 0.00,
							"status":"待发货"
							},
					"商家3":{
							"order_no":"10102-商家3",
							"products":[{
								"name":"商品3a",
								"price":10.00,
								"count":1,
								"single_save":""
							}],
							"postage": 0.00,
							"status":"待发货"
							}
				}],
				"total_save":"",
				"weizoom_card":40.00,
				"products_count":4,
				"product_price": 40.00,
				"postage": 0.00,
				"cash":0.00,
				"final_price": 40.00
			}
			"""

Scenario:3 ziying自营平台子订单退款（全退优惠券、全退积分、退优惠券+积分）
	Given zy1登录系统
	When zy1'申请退款'自营订单'10101-商家1'
		"""
		{
			"cash":0.00,
			"weizoom_card":0.00,
			"coupon_money":21.00,
			"intergal":0,
			"intergal_money":0.00
		}
		"""
	When zy1'申请退款'自营订单'10101-商家2'
		"""
		{
			"cash":0.00,
			"weizoom_card":0.00,
			"coupon_money":0.00,
			"intergal":20,
			"intergal_money":10.00
		}
		"""
	When zy1'申请退款'自营订单'10101-商家3'
		"""
		{
			"cash":0.00,
			"weizoom_card":0.00,
			"coupon_money":5.00,
			"intergal":10,
			"intergal_money":5.00
		}
		"""
	Then zy1获得自营订单'10101'
			"""
			{
				"order_no":"10101",
				"status":"退款中",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "海淀科技大厦"
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"微信支付",
				"group":[{
					"商家1":{
						"order_no":"10101-商家1",
						"products":[{
							"name":"商品1b",
							"price":20.00,
							"count":1,
							"single_save":"直降5.00元"
						}],
						"postage": 1.00,
						"status":"退款中"
						},
					"商家2":{
							"order_no":"10101-商家2",
							"products":[{
								"name":"商品2a",
								"price":10.00,
								"count":1,
								"single_save":""
							}],
							"postage": 0.00,
							"status":"退款中"
						},
					"商家3":{
							"order_no":"10101-商家3",
							"products":[{
								"name":"商品3a",
								"price":10.00,
								"count":1,
								"single_save":""
							}],
							"postage": 0.00,
							"status":"退款中"
						}
				}],
				"total_save":"",
				"weizoom_card":"",
				"products_count":3,
				"product_price": 40.00,
				"postage": 1.00,
				"save_money": -5.00,
				"cash":36.00,
				"final_price": 36.00
			}
			"""

Scenario:4 ziying自营平台子订单退款（退现金+微众卡+优惠券+积分）
	Given zy1登录系统
	#10103-现金21.00+微众卡10+优惠券0.00+积分0.00=31.00
	When zy1'申请退款'自营订单'10103-商家1'
		"""
		{
			"cash":6.00,
			"weizoom_card":5.00,
			"coupon_money":0.00,
			"intergal":0,
			"intergal_money":0.00
		}
		"""
	When zy1'申请退款'自营订单'10103-商家2'
		"""
		{
			"cash":0.00,
			"weizoom_card":5.00,
			"coupon_money":2.00,
			"intergal":6,
			"intergal_money":3.00
		}
		"""
	When zy1'申请退款'自营订单'10103-商家3'
		"""
		{
			"cash":5.00,
			"weizoom_card":0.00,
			"coupon_money":2.00,
			"intergal":6,
			"intergal_money":3.00
		}
		"""
	When zy1通过财务审核'退款成功'自营订单'10103-商家1'
	When zy1通过财务审核'退款成功'自营订单'10103-商家2'
	When zy1通过财务审核'退款成功'自营订单'10103-商家3'
	Then zy1获得自营订单'10103'
			"""
			{
				"order_no":"10101",
				"status":"退款成功",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "海淀科技大厦"
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"微信支付",
				"group":[{
					"商家1":{
						"order_no":"10103-商家1",
						"products":[{
							"name":"商品1a",
							"price":10.00,
							"count":1,
							"single_save":""
						}],
						"postage": 1.00,
						"status":"退款成功"
						},
					"商家2":{
							"order_no":"10103-商家2",
							"products":[{
								"name":"商品2a",
								"price":10.00,
								"count":1,
								"single_save":""
							}],
							"postage": 0.00,
							"status":"退款成功"
						},
					"商家3":{
							"order_no":"10103-商家3",
							"products":[{
								"name":"商品3a",
								"price":10.00,
								"count":1,
								"single_save":""
							}],
							"postage": 0.00,
							"status":"退款成功"
						}
				}],
				"total_save":"",
				"weizoom_card":10.00,
				"products_count":3,
				"product_price": 30.00,
				"postage": 1.00,
				"cash":21.00,
				"final_price": 31.00,
				"refund_details":{
					"cash": 11.00,
					"weizoom_card": 10.00,
					"coupon_money": 4.00,
					"integral_money": 6.00
				}
			}
			"""