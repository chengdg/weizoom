@func:webapp.modules.mall.views.list_products
Feature: 在webapp中从购物车中购买商品
	bill能在webapp中从购物车中购买商品

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 3.3
		}, {
			"name": "商品2",
			"price": 5.3
		}]	
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
	Given tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom加入jobs的商品到购物车
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 从购物车购买商品，不勾选商品时，获得错误提示
	bill将jobs的一个商品加入购物车后
	1. 不勾选商品时点击下单，获得错误提示
	
	Given bill关注jobs的公众号
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}]
		"""
	When bill从购物车发起购买操作:ui
	Then bill获得出错提示'请选择结算的商品':ui


@ui @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 从购物车购买单个商品
	bill将jobs的一个商品加入购物车后
	1. bill能从购物车中下单
	2. bill的订单中的信息正确
	3. bill的购物车被清空
	4. tom的购物车不受影响
	
	Given bill关注jobs的公众号
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}]
		"""
	When bill从购物车发起购买操作:ui
		"""
		{
			"products":"all",
			"ship_info": {
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦"
			}
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1,
				"price": 3.3
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
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
				"price": 3.3,
				"count": 1
			}]
		}
		"""
	And bill能获得购物车:ui
		"""
		[]
		"""
	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}]
		"""


@ui @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 从购物车购买多个商品
	bill将jobs的多个商品加入购物车后
	1. bill能从购物车中下单
	2. bill能调整购物车中的商品数量
	2. bill的订单中的信息正确
	3. bill的购物车被清空
	4. tom的购物车不受影响
	
	Given bill关注jobs的公众号
	When bill访问jobs的webapp:ui
	And bill加入jobs的商品到购物车:ui
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}]
		"""
	When bill从购物车发起购买操作:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}, {
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	Then bill获得待编辑订单:ui
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 2
			}, {
				"name": "商品2",
				"count": 1
			}]
		}
		"""
	When bill使用'货到付款'购买订单中的商品:ui
	Then bill获得支付结果:ui
		"""
		{
			"status": "待发货",
			"products": [{
				"name": "商品1",
				"price": 3.3,
				"count": 2
			}, {
				"name": "商品2",
				"price": 5.3,
				"count": 1
			}]
		}
		"""
	And bill能获得购物车:ui
		"""
		[]
		"""
	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}]
		"""