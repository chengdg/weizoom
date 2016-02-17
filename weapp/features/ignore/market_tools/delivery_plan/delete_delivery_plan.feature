#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

@func:market_tools.tools.test_game.views.list_test_games

Feature: 修改配送套餐
	Jobs能通过管理系统修改已经添加的"配送套餐"

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1"
		}]
		"""
	And jobs添加配送套餐
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
		},{
			"name": "配送套餐3",
			"product": "商品1",
			"type": "周",
			"frequency": "1",
			"times": "8",
			"price": "800",
			"original_price":"500"
		}]
		"""

@market_tool @market_tool.delivery_plan
Scenario: 删除配送套餐
	jobs添加多个"配送套餐"后
	1. jobs可以删除已添加的配送套餐
	2. 配送套餐列表按添加的顺序倒序排列，不受影响

	When jobs删除配送套餐'配送套餐2'
		
	Then jobs能获得配送套餐列表
		"""
		[{
			"name": "配送套餐3"
		}, {
			"name": "配送套餐1"
		}]
		"""
	
	When jobs删除配送套餐'配送套餐1'
	And jobs删除配送套餐'配送套餐3'
	Then jobs能获得配送套餐列表
		"""
		[]
		"""