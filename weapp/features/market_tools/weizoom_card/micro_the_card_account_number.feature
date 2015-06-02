Feature: 添加微众卡账号
	jobs在微信营销管理系统后台创建微众卡账号，以便查询微众卡的发放目标
Background:
	Given jobs已有的账号
		"""
		[{
			"account_number": "账号1"
		}, {
			"account_number": "账号2"
		}, {
			"account_number": "账号3"
		}]	
		"""
	And jobs登录系统

@market_tools @market_tools.weizoom_card
Scenario:添加微众卡账号
	jobs只能添加系统中已有的账号
	1. 添加的账号不可编辑、不可删除
	#添加系统中已有的账号时，账号的名称是做为微众卡的发放目标
	When jobs添加账号
	#名称、账号为必填项.
	"""
	[{
		"name": "微众商城",
		"account_number": "账号1"
	}]
	"""	
	Then jobs能获取账号列表
	"""
	[{
		"name": "微众商城",
		"account_number": "账号1"
	}]
	"""

	When jobs添加账号
	#名称、账号为必填项.
	"""
	[{
		"name": "牛仕兰",
		"account_number": "账号2"
	}]
	"""	
	Then jobs能获取账号列表
	"""
	[{
		"name" : "牛仕兰",
		"account_number": "账号2"
	},{
		"name": "微众商城",
		"account_number": "账号1"
	}]
	"""

	When jobs添加账号
	#名称、账号为必填项.填写的账号系统中没有的会提示"该账号系统里没有请重新添加"
	"""
	[{
		"name": "大米",
		"account_number": "111"
	}]
	"""	
	Then jobs能获取账号列表
	"""
	[{
		"name": "牛仕兰",
		"account_number": "账号2"
	},{
		"name": "微众商城",
		"account_number": "账号1"
	}]
	"""

	