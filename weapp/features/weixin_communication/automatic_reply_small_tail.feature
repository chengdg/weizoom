# __author__ : "王丽"

Feature:  微信互动平台-自动回复-小尾巴
"""
	开启后，自动回复给粉丝的文本消息末尾都会自动加上“小尾巴”里的内容

	小尾巴内容只能是文本或者链接

"""

Background:
	
	Given jobs登录系统

	When jobs已添加多条图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
			"sub": [{
				"title":"sub图文1",,
				"cover": [{
					"url": "/standard_static/test_resource_img/hangzhou2.jpg"
					}],
				"cover_in_the_text":"ture",
				"summary":"sub单条图文1文本摘要",
				"content":"sub单条图文1文本内容"
		}]
		"""

Scenario:1 关注后自动回复,文本类型，带文本小尾巴

	When jobs已添加关注后自动回复
		"""
		[{
			"reply_content":"关注后自动回复内容",
			"reply_type":"text"
		}]
		"""

	When jobs已添加小尾巴
		"""
		[{
			"is_open":"true",
			"reply":[{
			"reply_content":"+小尾巴"
			"reply_type":"text"
			}]
		}]
		"""
	When bill关注jobs的公众号
	Then bill获得jobs的回复
		"""
		[{
			"reply_content":"关注后自动回复内容+小尾巴"
		}]
		"""

Scenario:2 关注后自动回复,外链接类型，带外链接小尾巴

	When jobs已添加关注后自动回复
		"""
		[{
			"reply_content":"关注后自动回复外链接",
			"URL":"链接网址1",
			"reply_type":"text"
		}]
		"""

	When jobs已添加小尾巴
		"""
		[{
			"is_open":"true",
			"reply":[{
			"reply_content":"+小尾巴链接"
			"URL":"链接网址2",
			"reply_type":"text"
			}]
		}]
		"""
	When bill关注jobs的公众号
	Then bill获得jobs的回复
		"""
		[{
			"reply_content":"关注后自动回复外链接+小尾巴链接"
		}]
		"""

Scenario:3 关键词自动回复,文本类型，带文本小尾巴；没有自动回复，没有小尾巴

	When jobs已添加关键词自动回复规则
		"""
		[{
			"patterns": {"keyword1"},
			"reply":[{
			"reply_content":"关键词自动回复"
			"reply_type":"text"
			}]
		}]
		"""
	When jobs已添加小尾巴
		"""
		[{
			"is_open":"true",
			"reply":[{
			"reply_content":"+小尾巴"
			"reply_type":"text"
			}]
		}]
		"""
	When bill关注jobs的公众号
	When bill在模拟器中给jobs发送消息'keyword1'
	Then bill获得jobs的回复
		"""
		[{
			"reply_content":"关键词自动回复+小尾巴"
		}]
		"""

	#没有自动回复没有小尾巴
	When bill在模拟器中给jobs发送消息'bill消息'
	Then bill获得jobs的回复
		"""
		[{}]
		"""

Scenario:4 消息托管，图文自动回复没有小尾巴

	When jobs已添加消息托管
		"""
		{
			"is_open":"true",
			"time_start":"23:00",
			"time_end":"8:00",
			"Weeks":{"一"},
			"reply":[{
					"reply_content":"消息托管，自动回复文本"
					"reply_type":"text"
					},{
					"reply_content":"图文1"
					"reply_type":"text_picture"
					}]
		}
		"""
	When jobs已添加小尾巴
		"""
		{
			"is_open":"true",
			"reply":[{
			"reply_content":"+小尾巴"
			"reply_type":"text"
			}]
		}
		"""

	#bill获得消息托管的文本回复，有小尾巴
		When jobs获取当前时间为
			"""
			{
				"time":"2015-08-24 7:00:00"
			}
			"""
		When bill在模拟器中给jobs发送消息'消息托管'
		Then bill获得jobs的回复
			"""
			{
				"reply_content":"消息托管，自动回复文本+小尾巴"
			}
			"""

	#bill获得消息托管的图文回复，无小尾巴
		When jobs获取当前时间为
			"""
			{
				"time":"2015-08-24 6:00:00"
			}
			"""
		When bill在模拟器中给jobs发送消息'消息托管'
		Then bill获得jobs的回复
			"""
			{
				"reply_content":"图文1"
			}
			"""


Scenario:5 小尾巴未开启，关注后自动回复,文本类型，无文本小尾巴

	When jobs已添加关注后自动回复
		"""
		[{
			"reply_content":"关注后自动回复内容",
			"reply_type":"text"
		}]
		"""

	When jobs已添加小尾巴
		"""
		[{
			"is_open":"false",
			"reply":[{
			"reply_content":"+小尾巴"
			"reply_type":"text"
			}]
		}]
		"""
	When bill关注jobs的公众号
	Then bill获得jobs的回复
		"""
		[{
			"reply_content":"关注后自动回复内容"
		}]
		"""

		