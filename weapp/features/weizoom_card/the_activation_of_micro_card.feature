#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
Feature: 激活微众卡确定发放目标
	jobs在微信营销管理系统后台激活微众卡时，显示发放目标
Background:
	Given jobs已添加的微众卡目标账号
		"""
		[{
			"name": "牛仕兰",
			"account_number": "账号1"
		}, {
			"name": "大米",
			"account_number": "账号2"
		}, {
			"name": "红酒",
			"account_number": "账号3"
		}]	
		"""
	Given jobs已有的微众卡
		"""
		[{
			"card_number": "0000001",
			"state":"未激活"
		},{
			"card_number": "0000002",
			"state":"未激活"
		},{
			"card_number": "0000003",
			"state":"未激活"
		}]	
		"""
	And jobs登录系统

@market_tools @market_tools.weizoom_card
Scenario:激活微众卡
	jobs激活微众卡
	1. 单个激活微众卡
	2. 批量激活微众卡

	When jobs激活微众卡
	"""
	[{
		"card_number": "0000001",
		"whether_activation": "是"
	}]
	"""	
	And jobs能获取微众卡激活目标
	"""
	[{	
		"name":"牛仕兰",
		"whether_you_choose":"是"
	},{
		"name":"大米"
	},{
		"name":"红酒"
	}]
	"""
	Then jobs获取微众卡
	"""
	[{
		"card_number": "0000001",
		"state":"未使用"
	}]
	"""

	When jobs激活微众卡
	"""
	[{
		"card_number": "0000002",
		"whether_activation": "是"
	},{
		"card_number": "0000003",
		"whether_activation": "是"
	}]
	"""	
	And jobs能获取微众卡激活目标
	"""
	[{
		"name":"牛仕兰"
	},{
		"name":"大米",
		"whether_you_choose":"是"
	},{
		"name":"红酒"
	}]
	"""
	Then jobs获取微众卡
	"""
	[{
		"card_number": "0000002",
		"state":"未使用"
	},{
		"card_number": "0000003",
		"state":"未使用"
	}]
	"""