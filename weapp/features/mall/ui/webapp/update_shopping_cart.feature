@func:webapp.modules.mall.views.list_products
Feature: 调整购物车中
	bill能调整购物车

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 3
		}, {
			"name": "商品2",
			"price": 5
		}]	
		"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
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
Scenario: 从购物车中删除商品
	bill在购物车中删除商品后
	1. bill能获得更新后的购物车
	3. tom的购物车不受bill操作的影响

	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 1
		}]
		"""
	When bill从购物车中删除商品'商品1':ui
	Then bill能获得购物车:ui
		"""
		[{
			"name": "商品2",
			"count": 1
		}]
		"""
	When bill从购物车中删除商品'商品2':ui
	Then bill能获得购物车:ui
		"""
		[]
		"""
	When tom访问jobs的webapp:ui
	Then tom能获得购物车:ui
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"count": 1
		}]
		"""