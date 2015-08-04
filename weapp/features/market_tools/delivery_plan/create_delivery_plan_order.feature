# __author__ : "崔帅帅"
@func:market_tools.tools.test_game.views.list_test_games

Feature: 用户订购配送套餐
	为新用户可以订购已经添加的"配送套餐"

Background:
	Given jobs登录系统
	And jobs已添加配送套餐
		"""
		[{
			"name": "配送套餐1",
			"product": "商品1",
			"type": "月",
			"frequency": "2",
			"times": "2",
			"price": "400"
		}, {
			"name": "配送套餐1",
			"product": "商品1",
			"type": "周",
			"frequency": "1",
			"times": "4",
			"price": "400"
		}]
		"""
	And 微信用户
	"""
	[{
		"name": "微信用户1"
	}]
	"""

# @weapp.market_tools.delivery_plan @ignore
# Scenario: 订购配送套餐
# 	jobs添加多个"配送套餐"后
# 	1. 微信用户1可以查看添加的配送套餐
# 	2. 微信用户1不可以使用任何折扣、积分、优惠券
# 	3. 微信用户1可以修改首次配送时间，并切其余送货时间会根据首次配送时间发生变化
# 	4. 微信用户1可以订购添加的配送套餐，生成订单
# 	5. 到达每一个配送日期，可以正常配送
# 	6. 微信用户1可以查看订单详情（已发货日期、未发货日期、运单号等信息）

	