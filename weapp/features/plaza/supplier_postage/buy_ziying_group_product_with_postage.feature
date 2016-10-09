# __author__ : "冯雪静"

#自营团购：手机端购买有运费
Feature: 在自营平台手机端购买团购活动（包含商品运费）
	"""
	自营平台的团购活动，根据同步的商品携带的运费收取相应的运费
		1.购买团购活动的商品使用的是运费模板
		2.购买团购活动的商品使用的是统一运费
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
	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""
	When 给供货商选择运费配置
		"""
		{
			"supplier_name": "供货商1",
			"postage_name": "顺丰"
		}
		"""
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
			"postage": 10.00,
			"image": "love.png",
			"stocks": 100,
			"detail": "商品1-2描述信息"
		}
		"""
	#自营平台从商品池上架商品
	Given zy1登录系统
	When zy1上架商品池商品"商品1-1"
	When zy1上架商品池商品"商品2-1"
	When zy1新建团购活动
		"""
		[{
			"group_name":"团购1",
			"start_date":"今天",
			"end_date":"2天后",
			"product_name":"商品1-1",
			"group_dict":{
				"0":{
					"group_type":"5",
					"group_days":"1",
					"group_price":"20.00"
					},
				"1":{
					"group_type":"10",
					"group_days":"2",
					"group_price":"10.00"
				}
			},
			"ship_date":"20",
			"product_counts":"100",
			"material_image":"1.jpg",
			"share_description":"团购分享描述"
		}]
		"""
	When zy1新建团购活动
		"""
		[{
			"group_name":"团购2",
			"start_date":"今天",
			"end_date":"3天后",
			"product_name":"商品2-1",
			"group_dict":{
				"0":{
					"group_type":"5",
					"group_days":"2",
					"group_price":"21.00"
					},
				"1":{
					"group_type":"10",
					"group_days":"2",
					"group_price":"11.00"
				}
			},
			"ship_date":"20",
			"product_counts":"100",
			"material_image":"1.jpg",
			"share_description":"团购分享描述"
		}]
		"""
	When zy1开启团购活动'团购1'
	When zy1开启团购活动'团购2'

	Given bill关注zy1的公众号

@eugeneTMP
Scenario:0

Scenario:1 在自营购买团购商品1，商品1使用的是运费模板

	When bill访问zy1的webapp::apiserver
	When bill参加zy1的团购活动"团购1"进行开团
		"""
		{
			"group_name": "团购1",
			"group_leader": "bill",
			"group_dict":
				{
					"group_type":5,
					"group_days":1,
					"group_price":20.00
				},
			"products": {
				"name": "商品1-1"
			}
		}
		"""
	When bill提交团购订单::apiserver
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"distribution_time":"5天后 10:00-12:30",
			"pay_type":"微信支付"
		}
		"""
	When bill使用支付方式'微信支付'进行支付::apiserver
	#商品1使用运费模板，收取相应的运费
	Then bill成功创建订单::apiserver
		"""
		{
			"is_group_buying": "true",
			"status": "待发货",
			"final_price": 35.00,
			"postage": 15.00,
			"products": [{
				"name": "商品1-1",
				"price": 20.00,
				"count": 1
			}]
		}
		"""


Scenario:2 在自营购买团购商品2，商品1使用的是统一运费

	When bill访问zy1的webapp::apiserver
	When bill参加jobs的团购活动"团购2"进行开团
		"""
		{
			"group_name": "团购2",
			"group_leader": "bill",
			"group_dict":
				{
					"group_type":5,
					"group_days":1,
					"group_price":21.00
				},
			"products": {
				"name": "商品2-1"
			}
		}
		"""
	When bill提交团购订单::apiserver
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type":"微信支付"
		}
		"""
	When bill使用支付方式'微信支付'进行支付::apiserver
	#商品2使用的是统一运费10元，收取相应的运费
	Then bill成功创建订单::apiserver
		"""
		{
			"is_group_buying": "true",
			"status": "待发货",
			"final_price": 31.00,
			"postage": 10.00,
			"products": [{
				"name": "商品2-1",
				"price": 21.00,
				"count": 1
			}]
		}
		"""

