Feature: 实时消息中的备注

Scenario: 添加备注信息
	Given jobs登录系统
	And jobs有若干消息
	"""
	[{
		"nickname": "樱桃小丸子",
		"type": 1,
		"text": "网络营销这个词已经被赋予了各种不同的含义",
		"created_at": "2015-03-04 17:21:32",
		"memo": "",
		"is_favourated": false,
		"last_reply_at": "2015-03-24 16:23:21"
	}
	]
	"""
	When jobs在"樱桃小丸子"的消息上添加备注，内容是
	"""
	[
		"text": "有道理，[good]"
	]
	"""
	Then jobs访问消息列表页面，看到"樱桃小丸子"的消息备注是"有道理，[good]"
