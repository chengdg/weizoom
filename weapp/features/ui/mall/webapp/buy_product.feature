@func:webapp.modules.mall.views.list_products
Feature: 在webapp中购买商品
	bill能在webapp中购买jobs添加的"商品"

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 9.9
		}, {
			"name": "商品2",
			"price": 8.8
		},{
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 M": {
						"price": 10.0
					}
				}
			}
		}, {
			"name": "商品4",
			"shelve_type": "下架",
			"model": {
				"models": {
					"standard": {
						"price": 5,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品5",
			"model": {
				"models": {
					"standard": {
						"price": 5.0,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "商品6",
			"price": 9.9,
			"pay_interfaces":[{
				"type": "在线支付"
			}]
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用"
		}]
		"""

@ui @ui-mall @ui-mall.webapp
Scenario: 购买单个商品
	jobs添加商品后
	1. bill能在webapp中购买jobs添加的商品
	1. bill的订单中的信息正确
	
	When bill访问jobs的webapp:ui
	And bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"count": 2
			}]
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品1",
				"price": 9.9,
				"count": 2
			}]
		}
		"""


@ui @ui-mall @ui-mall.webapp
Scenario: 购买商品时，使用订单备注
	bill在购买jobs添加的商品时
	1. 添加了"订单备注"，则jobs能在管理系统中看到该"订单备注"
	2. 不添加'订单备注', 则jobs能在管理系统中看到"订单备注"为空字符串
	
	When bill访问jobs的webapp:ui
	And bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"customer_message": "bill的订单备注"
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"customer_message": "bill的订单备注"
		}
		"""
	Given jobs登录系统:ui
	Then jobs能获取最新的订单:ui
		"""
		{
			"customer_message": "bill的订单备注"
		}
		"""

	When bill访问jobs的webapp:ui
	When bill使用'货到付款'购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"customer_message": ""
		}
		"""
	Given jobs登录系统:ui
	Then jobs能获取最新的订单:ui
		"""
		{
			"customer_message": ""
		}
		"""

Scenario: 购买有规格的商品
	jobs添加商品后
	1. bill能在webapp中购买jobs添加的商品
	2. bill的订单中的信息正确

	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
		"""
		{
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品3",
				"model": "黑色 M",
				"price": 10.0,
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 20.0,
			"products": [{
				"name": "商品3",
				"model": "黑色 M",
				"price": 10.0,
				"count": 2
			}]
		}
		"""

Scenario: 购买已经下架的商品
	bill可能会在以下情景下购买已下架的商品A：
	1. bill打开商品A的详情页面
	2. bill点击“购买”，进入商品A的订单编辑页面
	3. jobs在后台将商品A下架
	4. bill点击“支付”，完成订单

	这时，系统应该通知bill：商品已下架

	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1
			}]
		}
		"""
	Then bill获得错误提示'商品已下架<br/>2秒后返回商城首页':ui

Scenario: 购买的商品数量等于库存数量
	jobs添加有限商品后
	1. bill能在webapp中购买jobs添加的商品
	2. bill的订单中的信息正确
	3. jobs查看库存

	When bill访问jobs的webapp:ui
	And bill购买jobs的商品:ui
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单:ui
		"""
		{
			"status": "待支付",
			"final_price": 10.0,
			"products": [{
				"name": "商品5",
				"price": 5.0,
				"count": 2
			}]
		}
		"""
	Given jobs登录系统:ui
	Then jobs能获取商品'商品5':ui
		"""
		{
			"name": "商品5",
			"model": {
				"models": {
					"standard": {
						"price": 5.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""

Scenario:购买库存不足的商品
	bill可能会在以下情景下购买库存不足的商品A：
	1. bill打开商品A的详情页面
	2. bill调整数量为3个点击“购买”，进入商品A的订单编辑页面
	3. jobs在后台将商品A的库存调整为2个
	4. bill点击“支付”，完成订单
	5. jobs查看库存

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 3
			}]
		}
		"""
	Then bill获得错误提示'有商品库存不足<br/>2秒后返回购物车<br/>请重新下单'
	Given jobs登录系统
	Then jobs能获取商品'商品5'
		"""
		{
			"name": "商品5",
			"model": {
				"models": {
					"standard": {
						"price": 5.0,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}
		"""
