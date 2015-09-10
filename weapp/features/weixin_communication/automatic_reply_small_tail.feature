# __author__ : "王丽"

Feature:  微信互动平台-自动回复-小尾巴
"""
	开启后，自动回复给粉丝的文本消息末尾都会自动加上“小尾巴”里的内容

	小尾巴内容只能是文本或者链接

"""

Background:
	
	Given jobs登录系统

	When jobs已添加多图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
		},{
			"title":"sub图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
				}],
			"cover_in_the_text":"true",
			"summary":"sub单条图文1文本摘要",
			"content":"sub单条图文1文本内容"
		},{
			"title":"sub图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
				}],
			"cover_in_the_text":"false",
			"summary":"sub单条图文2文本摘要",
			"content":"sub单条图文2文本内容"
		},{
			"title":"sub图文3",
			"cover": [{
				"url": "/standard_static/test_resource_img/wufan1.jpg"
				}],
			"cover_in_the_text":"false",
			"summary":"sub单条图文3文本摘要",
			"jump_url":"www.baidu.com",
			"content":"sub单条图文3文本内容"
		}]
		"""

@mall2 @message @automaticReply
Scenario:1 关注后自动回复,文本类型，带文本小尾巴

	When jobs添加关注自动回复规则
		"""
		[{
			"reply_content":"关注后自动回复内容",
			"reply_type":"text"
		}]
		"""

	When jobs添加小尾巴
		"""
		[{
			"is_open":"true",
			"reply_content":"+小尾巴"
		}]
		"""
	When bill关注jobs的公众号
	Then bill收到自动回复'关注后自动回复内容+小尾巴'

@mall2 @message @automaticReply
Scenario:2 关键词自动回复,文本类型，带文本小尾巴；没有自动回复，没有小尾巴

	When jobs已添加关键词自动回复规则
		"""
		[{
			"patterns": "keyword1",
			"answer": "关键词自动回复"
		}]	
		"""
	When jobs添加小尾巴
		"""
		[{
			"is_open":"true",
			"reply_content":"+小尾巴"
		}]
		"""
	When bill关注jobs的公众号
	When bill在微信中向jobs的公众号发送消息'keyword1'
	Then bill收到自动回复'关键词自动回复+小尾巴'

	#没有自动回复没有小尾巴
	When bill在微信中向jobs的公众号发送消息'bill消息'
	Then bill收到自动回复' '

@mall2 @message @automaticReply
Scenario:3 小尾巴未开启，关注后自动回复,文本类型，无文本小尾巴
	
	When jobs添加关注自动回复规则
		"""
		[{
			"reply_content":"关注后自动回复内容",
			"reply_type":"text"
		}]
		"""

	When jobs添加小尾巴
		"""
		[{
			"is_open":"false",
			"reply_content":"+小尾巴"
		}]
		"""
	When bill关注jobs的公众号
	Then bill收到自动回复'关注后自动回复内容'

		