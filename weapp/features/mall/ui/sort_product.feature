@func:webapp.modules.mall.views.list_products
Feature: 调整商品的顺序
	Jobs能调整商品的顺序

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}, {
			"name": "商品3"
		}]	
		"""

@ui @ui-mall @ui-mall.product
Scenario Outline: 调整商品顺序
	Jobs调整商品顺序后，会得到顺序调整顺序后的商品列表

	Given jobs登录系统:ui
	When jobs\'<direction>'调整'<product>':ui
	Then jobs能获取商品列表'<product_list>':ui

	Examples: 
		| direction | product | product_list |
		| up        | 商品1   | [{"name": "商品3"}, {"name": "商品1"}, {"name": "商品2"}] |
		| down      | 商品3   | [{"name": "商品2"}, {"name": "商品3"}, {"name": "商品1"}] |


@ui @ui-mall @ui-mall.product
Scenario: 置顶商品
	Given jobs登录系统:ui
	When jobs置顶商品'商品1':ui
	Then jobs能获取商品列表:ui
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品3"
		}, {
			"name": "商品2"
		}]
		"""