#watcher:wangxinrui@weizoom.com,benchi@weizoom.com
# __author__ : "新新"

Feature: 查看聊天记录
"""
	
	1、【查看聊天记录】：新页面跳转到【微信互动平台】-【消息互动】-【实时消息】下的本会员的消息详情页

	
"""

@ui 
Scenario:1 查看聊天记录

	Given jobs登录系统

	When jobs已添加单图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
		}]
		"""

	#添加关键词自动回复
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "关键词tom",
					"type": "equal"
				}],
			"keyword_reply": [{
					 "reply_content":"关键字回复内容tom",
					 "reply_type":"text"
				}]
		}]
		"""

	#tom关注jobs的公众号进行消息互动，发送三条
	When 清空浏览器
	and tom关注jobs的公众号
	and tom在微信中向jobs的公众号发送消息'tom发送一条文本消息1，未回复'
	and tom在微信中向jobs的公众号发送消息'关键词tom'
	and tom在微信中向jobs的公众号发送消息'tom发送一条文本消息2，未回复'


	#查看有会员消息的会员消息记录
	When jobs查看'tom'聊天记录
		"""
		{
			"name":"tom"
		}
		"""

	Then jobs获得'tom'消息详情消息列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"time": "今天"
		},{
			"member_name": "jobs",
			"inf_content": "【自动回复】 关键字回复内容tom",
			"time": "今天"
		},{
			"member_name": "tom",
			"inf_content": "关键词tom",
			"time": "今天"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息1，未回复",
			"time": "今天"
		}]
		"""
