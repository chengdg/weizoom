# __author__ : "崔帅帅"
@func:weapp.product
Feature: 添加修改产品
	manager可以通过后台管理系统添加修改产品

Background:
	Given manager登录系统

@weapp.product @ignore
Scenario: manager添加修改产品
	When manager添加产品
		"""
		{
			"name": "手机",
			"price": "599",
			"footer": "0",
			"market_tools": ["趣味测试", "感恩贺卡", "用户反馈"],
			"remark": "sell phone"
		}	
		"""
	Then manager可以获取产品手机
		"""
			{
				"name": "手机",
				"price": 599.0,
				"footer": 0,
				"market_tools": ["趣味测试", "感恩贺卡", "用户反馈"],
				"remark":"sell phone"
			}
		"""
	When manager编辑产品手机
		"""
			{
				"name": "平板",
				"price": "1599",
				"footer": "0",
				"market_tools": ["微信抽奖", "微信红包"],
				"remark": "sell pad"
			}
		"""
	Then manager可以获取产品平板
		"""
			{
				"name": "平板",
				"price": 1599.0,
				"footer": 0,
				"market_tools": ["微信抽奖", "微信红包"],
				"remark": "sell pad"
			}
		"""