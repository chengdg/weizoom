# __author__ : "崔帅帅"
@func:market_tools.tools.red_envelope.views.list_red_envelope
Feature: 添加红包
	Jobs能通过管理系统添加"添加红包"

@weapp.market_tools.red_envelope
Scenario: 添加微信红包
	Jobs添加"微信红包"后，能获取他的红包，"红包"列表会按照添加的倒序排列

	Given jobs登录系统
	When jobs添加微信红包
		""" 
		[{
			"name": "微信红包",
			"total_award_value": "522",
			"desc": "红包",	
			"expected_participation_count": "85",
			"is_non_member": "非会员可参与",
			"prize_odds|1": "100",
			"prize_count|1": "3",
			"prize_type|1": "3",
			"prize_source|1": "3",
			"prize_name|1": "一等奖",	
			"logo_url": "/static/upload/6_20140710/1404981209095_5.jpg"
		}]
		"""
	Then jobs能获取红包列表
		"""
		[{
			"name": "微信红包"
		}]
		"""
	And bill能获取红包列表
		"""
		[]
		"""
		
		
