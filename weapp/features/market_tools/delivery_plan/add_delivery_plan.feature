Feature: 添加配送套餐
	Jobs能通过管理系统添加"配送套餐"

Background:
	Given jobs已添加商品
		"""
		[{
			"name": "商品1"
		}]
		"""

@market_tool @market_tool.delivery_plan
Scenario: 添加配送套餐
	jobs添加多个"配送套餐"后
	1. jobs能获得添加的配送套餐
	2. 配送套餐列表按添加的顺序倒序排列
	3. bill不能获得jobs添加的配送套餐

	Given jobs登录系统
	When jobs添加配送套餐
		"""
		[{
			"name": "配送套餐1",
			"product": "商品1",
			"type": "月",
			"frequency": "2",
			"times": "2",
			"price": "400",
			"original_price":"500"
		}, {
			"name": "配送套餐2",
			"product": "商品1",
			"type": "周",
			"frequency": "1",
			"times": "4",
			"price": "400",
			"original_price":"500"
		}]
		"""
	Then jobs能获得配送套餐'配送套餐1'
		'''
		{
			"name": "配送套餐1",
			"product": "商品1",
			"type": "月",
			"frequency": "2",
			"times": "2",
			"price": "400"
		}
		'''
	Then jobs能获得配送套餐'配送套餐2'
		'''
		{
			"name": "配送套餐2",
			"product": "商品1",
			"type": "周",
			"frequency": "1",
			"times": "4",
			"price": "400"
		}
		'''
	Then jobs能获得配送套餐列表
		'''
		[{
			"name": "配送套餐2"
		}, {
			"name": "配送套餐1"
		}]
		'''
	Given bill登录系统
	Then bill能获得配送套餐列表
		'''
		[]
		'''
