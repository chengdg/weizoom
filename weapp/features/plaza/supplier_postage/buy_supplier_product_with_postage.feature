# __author__ : "冯雪静"

Feature: 自营平台按照供货商配置的运费计算
	"""
	供货商设置运费模板和统一运费：
		1.购买一个供货商的商品，使用运费模板，如有续重商品重量累加计算，如没有续重直接取首重费用
		2.购买一个供货商的商品，使用运费模板，满足件数包邮/满足金额包邮
		3.购买一个供货商的商品，使用运费模板和统一运费，运费是累加的，互不影响
		4.购买多家供货商的商品，使用运费模板和统一运费，运费是累加的，互不影响
		5.购买一个供货商的商品，使用统一运费，同一个商品不会随数量而累加
	"""

Background:
	Given 重置'apiserver'的bdd环境
	Given zy1登录系统
	When zy1已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	#所有商品开通所有支付方式
	#创建供货商、设置供货商运费、同步商品到自营平台
	#创建供货商
	Given 创建一个特殊的供货商，就是专门针对商品池供货商
		"""
		{
			"supplier_name":"供货商1"
		}
		"""
	Given 创建一个特殊的供货商，就是专门针对商品池供货商
		"""
		{
			"supplier_name":"供货商2"
		}
		"""
	#设置供货商运费
	#给供货商1配置两个运费模板-顺丰-只有首重，中通-包含续重，特殊地区包邮条件
	When 给供货商'供货商1'添加运费配置
		"""
		[{
			"name": "顺丰",
			"first_weight": 0.1,
			"first_weight_price": 10.00
		},{
			"name":"中通",
			"first_weight": 1,
			"first_weight_price": 13.00,
			"added_weight": 1,
			"added_weight_price": 5.00,
			"special_area": [{
				"to_the":"北京市,江苏省",
				"first_weight": 1,
				"first_weight_price": 20.00,
				"added_weight": 1,
				"added_weight_price": 10.00
			}],
			"free_postages": [{
				"to_the":"北京市",
				"condition": "count",
				"value": 3
			}, {
				"to_the":"北京市",
				"condition": "money",
				"value": 100.00
			}]
		}]
		"""

	#给供货商2配置两个运费模板-顺丰-只有首重，圆通-包含续重
	When 给供货商'供货商2'添加运费配置
		"""
		[{
			"name": "圆通",
			"first_weight": 5,
			"first_weight_price": 10.00,
			"added_weight": 1,
			"added_weight_price": 5.00
		},{
			"name": "顺丰",
			"first_weight": 2.1,
			"first_weight_price": 5.00
		}]
		"""

	#商品1和商品2选系统运费，商品3统一运费
	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"供货商1",
			"name": "商品1-1",
			"promotion_title": "商品1-2促销",
			"purchase_price": 40.00,
			"price": 50.00,
			"weight": 1,
			"postage": "系统",
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1-1描述信息"
		}
		"""
	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"供货商1",
			"name": "商品2-1",
			"promotion_title": "商品1-2促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"postage": "系统",
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1-2描述信息"
		}
		"""
	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"供货商1",
			"name": "商品3-1",
			"promotion_title": "商品1-2促销",
			"purchase_price": 9.00,
			"price": 10.00,
			"weight": 1,
			"postage": 10.00,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1-2描述信息"
		}
		"""
	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"供货商2",
			"name": "商品1-2",
			"promotion_title": "商品2-1促销",
			"purchase_price": 20.00,
			"price": 30.00,
			"weight": 1,
			"postage": "系统",
			"image": "love.png",
			"stocks": 100,
			"detail": "商品2-1描述信息"
		}
		"""
	Given 给自营平台同步商品
		"""
		{
			"accounts":["zy1"],
			"supplier_name":"供货商2",
			"name": "商品2-2",
			"promotion_title": "商品2-2促销",
			"purchase_price": 19.00,
			"price": 20.00,
			"weight": 1,
			"postage": 0.00,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品2-2描述信息"
		}
		"""
    When 给供货商选择运费配置
		"""
		{
			"supplier_name": "供货商1",
			"postage_name": "中通"
		}
		"""
    When 给供货商选择运费配置
		"""
		{
			"supplier_name": "供货商2",
			"postage_name": "圆通"
		}
		"""
	#自营平台从商品池上架商品
	Given zy1登录系统
	When zy1上架商品池商品"商品1-1"
	When zy1上架商品池商品"商品2-1"
	When zy1上架商品池商品"商品3-1"
	When zy1上架商品池商品"商品1-2"
	When zy1上架商品池商品"商品2-2"

	Given bill关注zy1的公众号

@eugene @postage
Scenario:1 在ziying购买单个供货商的商品，使用系统运费模板不满足续重

	When bill访问zy1的webapp::apiserver
	When bill购买zy1的商品::apiserver
		"""
		{
			"order_id":"001",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "河北省 秦皇岛 昌黎县",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":1
			}],
			"postage": 13.00
		}
		"""
	Then bill手机端获取订单'001'::apiserver
		"""
		{
			"order_no": "001",
			"status":"待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "河北省 秦皇岛 昌黎县",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1-1",
				"price": 50.00,
				"count": 1
			}],
			"methods_of_payment":"微信支付",
			"product_price": 50.00,
			"postage": 13.00,
			"final_price": 63.00
		}
		"""

@eugene @postage
Scenario:2 在ziying购买单个供货商的商品，使用系统运费模板满足续重

	When bill访问zy1的webapp::apiserver
	When bill购买zy1的商品::apiserver
		"""
		{
			"order_id":"001",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "河北省 秦皇岛 昌黎县",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":2
			}],
			"postage": 18.00
		}
		"""
	Then bill手机端获取订单'001'::apiserver
		"""
		{
			"order_no": "001",
			"status":"待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "河北省 秦皇岛 昌黎县",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1-1",
				"price": 50.00,
				"count": 2
			}],
			"methods_of_payment":"微信支付",
			"product_price": 100.00,
			"postage": 18.00,
			"final_price": 118.00
		}
		"""

@eugene @postage
Scenario:3 在ziying购买单个供货商的商品，使用系统运费模板特殊地区

	When bill访问zy1的webapp::apiserver
	When bill购买zy1的商品::apiserver
		"""
		{
			"order_id":"001",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":1
			}],
			"postage": 20.00
		}
		"""
	Then bill手机端获取订单'001'::apiserver
		"""
		{
			"order_no": "001",
			"status":"待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1-1",
				"price": 50.00,
				"count": 1
			}],
			"methods_of_payment":"微信支付",
			"product_price": 50.00,
			"postage": 20.00,
			"final_price": 70.00
		}
		"""

@eugene @postage
Scenario:4 在ziying购买单个供货商的商品，使用系统运费模板满足金额包邮条件

	When bill访问zy1的webapp::apiserver
	When bill购买zy1的商品::apiserver
		"""
		{
			"order_id":"001",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":2
			}],
			"postage": 0.00
		}
		"""
	Then bill手机端获取订单'001'::apiserver
		"""
		{
			"order_no": "001",
			"status":"待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1-1",
				"price": 50.00,
				"count": 2
			}],
			"methods_of_payment":"微信支付",
			"product_price": 100.00,
			"postage": 0.00,
			"final_price": 100.00
		}
		"""

@eugene @postage
Scenario:5 在ziying购买单个供货商的商品，使用系统运费模板满足件数包邮条件

	When bill访问zy1的webapp::apiserver
	When bill购买zy1的商品::apiserver
		"""
		{
			"order_id":"001",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":1
			}, {
				"name":"商品2-1",
				"price":10.00,
				"count":2
			}],
			"postage": 0.00
		}
		"""
	Then bill手机端获取订单'001'::apiserver
		"""
		{
			"order_no": "001",
			"status":"待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1-1",
				"price": 50.00,
				"count": 1
			}, {
				"name":"商品2-1",
				"price":10.00,
				"count":2
			}],
			"methods_of_payment":"微信支付",
			"product_price": 70.00,
			"postage": 0.00,
			"final_price": 70.00
		}
		"""

@eugene @postage
Scenario:6 在ziying购买单个供货商的商品，使用系统运费模板和统一运费
	1.使用运费模板的商品满足件数包邮条件
	2.只收取使用统一运费的商品运费

	#商品3-1收取统一运费10元
	When bill访问zy1的webapp::apiserver
	When bill购买zy1的商品::apiserver
		"""
		{
			"order_id":"001",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":1
			}, {
				"name":"商品2-1",
				"price":10.00,
				"count":2
			}, {
				"name":"商品3-1",
				"price":10.00,
				"count":2
			}],
			"postage": 10.00
		}
		"""
	Then bill手机端获取订单'001'::apiserver
		"""
		{
			"order_no": "001",
			"status":"待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1-1",
				"price": 50.00,
				"count": 1
			}, {
				"name":"商品2-1",
				"price":10.00,
				"count":2
			}, {
				"name":"商品3-1",
				"price":10.00,
				"count":2
			}],
			"methods_of_payment":"微信支付",
			"product_price": 90.00,
			"postage": 10.00,
			"final_price": 100.00
		}
		"""

@eugene @postage
Scenario:7 在ziying购买多个供货商的商品，使用系统运费模板和统一运费
	1.使用运费模板供货商1的商品满足件数包邮条件，有统一运费
	2.使用运费模板供货商1的商品没有续重，有统一运费

	#供货商1的商品运费和33，供货商2的商品运费和10
	When bill访问zy1的webapp::apiserver
	When bill购买zy1的商品::apiserver
		"""
		{
			"order_id":"001",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":1
			}, {
				"name":"商品2-1",
				"price":10.00,
				"count":2
			}, {
				"name":"商品3-1",
				"price":10.00,
				"count":1
			}, {
				"name":"商品1-2",
				"price":30.00,
				"count":1
			}, {
				"name":"商品2-2",
				"price":20.00,
				"count":1
			}],
			"postage": 20.00
		}
		"""
	Then bill手机端获取订单'001'::apiserver
		"""
		{
			"order_no": "001",
			"status":"待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name":"商品1-1",
				"price":50.00,
				"count":1
			}, {
				"name":"商品2-1",
				"price":10.00,
				"count":2
			}, {
				"name":"商品3-1",
				"price":10.00,
				"count":1
			}, {
				"name":"商品1-2",
				"price":30.00,
				"count":1
			}, {
				"name":"商品2-2",
				"price":20.00,
				"count":1
			}],
			"methods_of_payment":"微信支付",
			"product_price": 130.00,
			"postage": 20.00,
			"final_price": 150.00
		}
		"""

@eugene @postage
Scenario:8 供货商换运费模板配置在ziying购买多个供货商的商品，使用系统运费模板和统一运费
	1.供货商变更运费模板后，在自营平台下单，是按照新的运费模板收取运费

	When 给供货商选择运费配置
		"""
		{
			"supplier_name": "供货商1",
			"postage_name": "顺丰"
		}
		"""
	When 给供货商选择运费配置
		"""
		{
			"supplier_name": "供货商2",
			"postage_name": "顺丰"
		}
		"""
	When bill访问zy1的webapp::apiserver
	When bill购买zy1的商品::apiserver
		"""
		{
			"order_id":"001",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "河北省 秦皇岛 昌黎县",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":1
			}, {
				"name":"商品2-1",
				"price":10.00,
				"count":2
			}, {
				"name":"商品3-1",
				"price":10.00,
				"count":1
			}, {
				"name":"商品1-2",
				"price":30.00,
				"count":3
			}, {
				"name":"商品2-2",
				"price":20.00,
				"count":1
			}],
			"postage": 25.00
		}
		"""
	Then bill手机端获取订单'001'::apiserver
		"""
		{
			"order_no": "001",
			"status":"待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "河北省 秦皇岛 昌黎县",
			"ship_address": "泰兴大厦",
			"products": [{
				"name":"商品1-1",
				"price":50.00,
				"count":1
			}, {
				"name":"商品2-1",
				"price":10.00,
				"count":2
			}, {
				"name":"商品3-1",
				"price":10.00,
				"count":1
			}, {
				"name":"商品1-2",
				"price":30.00,
				"count":3
			}, {
				"name":"商品2-2",
				"price":20.00,
				"count":1
			}],
			"methods_of_payment":"微信支付",
			"product_price": 190.00,
			"postage": 25.00,
			"final_price": 215.00
		}
		"""

	#后台订单列表
	Given zy1登录系统
	Then zy1获得自营订单列表
		"""
		[{
			"order_no":"001",
			"methods_of_payment":"微信支付",
			"buyer":"bill",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"ship_address": "河北省 秦皇岛 昌黎县 泰兴大厦",
			"final_price": 215.00,
			"postage": 25.00,
			"status":"待支付",
			"actions": ["支付","取消订单"],
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":1
			}, {
				"name":"商品2-1",
				"price":10.00,
				"count":2
			}, {
				"name":"商品3-1",
				"price":10.00,
				"count":1
			}, {
				"name":"商品1-2",
				"price":30.00,
				"count":3
			}, {
				"name":"商品2-2",
				"price":20.00,
				"count":1
			}]
		}]
		"""
	Then zy1获得自营订单'001'
		"""
		{
			"order_no":"001",
			"status":"待支付",
			"actions": ["支付","取消订单"],
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"ship_area": "河北省 秦皇岛 昌黎县",
			"ship_address": "泰兴大厦",
			"methods_of_payment":"微信支付",
			"group":[{
				"order_no":"001-供货商1",
				"products":[{
					"name":"商品1-1",
					"supplier":"供货商1",
					"price":50.00,
					"count":1
				}, {
					"name":"商品2-1",
					"supplier":"供货商1",
					"price":10.00,
					"count":2
				}, {
					"name":"商品3-1",
					"supplier":"供货商1",
					"price":10.00,
					"count":1
				}],
				"postage": 20.00,
				"status":"待支付"
			},{
				"order_no":"002-供货商2",
				"products":[{
					"name":"商品1-2",
					"supplier":"供货商2",
					"price":30.00,
					"count":3
				}, {
					"name":"商品2-2",
					"supplier":"供货商2",
					"price":20.00,
					"count":1
				}],
				"postage": 5.00,
				"status":"待支付"
			}],
			"products_count":8,
			"total_price": 190.00,
			"postage": 25.00,
			"final_price": 215.00
		}
		"""