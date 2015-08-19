@func:webapp.modules.mall.views.list_products
Feature: Sort Product
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

@mall.product
Scenario Outline: 调整商品顺序
	Jobs调整商品顺序后，会得到顺序调整顺序后的商品列表

	When jobs\'<direction>'调整'<product>'
	Then jobs能获取商品列表'<product_list>'

	Examples: 
		| direction | product | product_list |
		| up        | 商品1   | [{"name": "商品3"}, {"name": "商品1"}, {"name": "商品2"}] |
		| down      | 商品3   | [{"name": "商品2"}, {"name": "商品3"}, {"name": "商品1"}] |


@mall.product
Scenario: 置顶商品
	When jobs置顶商品'商品1'
	Then jobs能获取商品列表
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品3"
		}, {
			"name": "商品2"
		}]
		"""