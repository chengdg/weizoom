@func:webapp.modules.mall.views.list_products
Feature: 在webapp中购买商品
	bill能在webapp中购买jobs添加的"商品"

Background:
	Given jobs登录系统
	Given jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	And jobs已有微众卡支付权限
	And jobs已添加支付方式
		"""
		[{
			"type": "微众卡支付"
		}, {
			"type": "货到付款"
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
	And bill关注jobs的公众号

@mall2 @mall.webapp @zy_bp01
Scenario: 购买单个商品
	jobs添加商品后
	1. bill能在webapp中购买jobs添加的商品
	1. bill的订单中的信息正确

	When bill访问jobs的webapp
	And bill购买jobs的商品
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
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"final_price": 19.8,
			"products": [{
				"name": "商品1",
				"price": 9.9,
				"count": 2
			}]
		}
		"""


@mall.webapp @mall2 @zy_bp02
Scenario: 购买商品时，使用订单备注
	bill在购买jobs添加的商品时
	1. 添加了"订单备注"，则jobs能在管理系统中看到该"订单备注"
	2. 不添加'订单备注', 则jobs能在管理系统中看到"订单备注"为空字符串

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"ship_area": "北京市 北京市 海淀区",
			"customer_message": "bill的订单备注"
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付"
		}
		"""
	Given jobs登录系统
	Then jobs能获取订单
		"""
		{
			"customer_message": "bill的订单备注"
		}
		"""

	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}],
			"ship_area": "北京市 北京市 海淀区"
		}
		"""
	Given jobs登录系统
	Then jobs能获取订单
		"""
		{
			"customer_message": ""
		}
		"""

@mall.webapp @mall2 @zy_bp03
Scenario: 购买有规格的商品
	jobs添加商品后
	1. bill能在webapp中购买jobs添加的商品
	2. bill的订单中的信息正确

	When bill访问jobs的webapp
	And bill购买jobs的商品
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
	Then bill成功创建订单
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


@mall.webapp @mall2 @zy_bp04
Scenario: 购买已经下架的商品
	bill可能会在以下情景下购买已下架的商品A：
	1. bill打开商品A的详情页面
	2. bill点击“购买”，进入商品A的订单编辑页面
	3. jobs在后台将商品A下架
	4. bill点击“支付”，完成订单

	这时，系统应该通知bill：商品已下架

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品4",
				"count": 1
			}]
		}
		"""
	Then bill获得错误提示'商品已下架<br/>2秒后返回商城首页'

@mall.webapp @mall2 @zy_bp05
Scenario: 购买的商品数量等于库存数量
	jobs添加有限商品后
	1. bill能在webapp中购买jobs添加的商品
	2. bill的订单中的信息正确
	3. jobs查看库存

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
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
						"stocks": 0
					}
				}
			}
		}
		"""

@mall.webapp @mall2 @zy_bp06
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

@mall.webapp @mall2 @zy_bp07
Scenario:货到付款的商品有两种支付方式
	bill购买jobs配有'货到付款'的商品时
	1.bill可以使用'在线支付'进行支付
	2.bill可以使用'货到付款'进行支付

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
	Then bill'能'使用支付方式'微众卡支付'进行支付
	Then bill'能'使用支付方式'货到付款'进行支付

@mall.webapp @mall2 @zy_bp08
Scenario:没有货到付款的商品只有一种支付方式
	bill购买jobs没有配'货到付款'的商品时
	1.bill可以使用'在线支付'进行支付
	2.bill不可以使用'货到付款'进行支付

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品6",
				"count": 2
			}]
		}
		"""
	Then bill'能'使用支付方式'微众卡支付'进行支付
	Then bill'不能'使用支付方式'货到付款'进行支付



#后续补充.雪静
@mall.webapp @mall2 @zy_bp09
Scenario: 购买库存为零的商品
	bill可能会在以下情景下购买库存不足的商品A：
	1. bill打开商品A的详情页面
	2. bill调整数量为2个点击“购买”，进入商品A的订单编辑页面
	3. bill点击“支付”，完成订单
	4. bill再次购买商品A
	5. jobs查看库存

	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 2
			}]
		}
		"""
	Then bill成功创建订单
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
	#bill从新进入商品详情页
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品5",
				"count": 1
			}]
		}
		"""
	Then bill获得错误提示'有商品库存不足<br/>2秒后返回购物车<br/>请重新下单'
