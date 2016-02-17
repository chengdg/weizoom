#watcher:benchi@weizoom.com
# __author__ : "benchi"
Feature: 实时消息-消息详情
"""
	1）jobs能看到其会员的实时消息的详情，分为能回复，与不能回复（消息仅在48小时内回复有效）
	2）消息仅在48小时内回复有效，不能在feature中实现
"""

Background:
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
		},{
			"rules_name":"规则3",
			"keyword": [{
					 "keyword": "关键词bill",
					 "type": "like"
				}],
			"keyword_reply": [{
					 "reply_content":"图文1",
					 "reply_type":"text_picture"
				}]
		}]
		"""

	#bill关注jobs的公众号进行消息互动，发送一条，无回复
	When 清空浏览器
	And bill关注jobs的公众号
	And bill访问jobs的webapp
	And bill在微信中向jobs的公众号发送消息'bill发送一条文本消息，未回复'
	And bill在微信中向jobs的公众号发送消息'关键词bill'

	#tom关注jobs的公众号进行消息互动，发送两条，第一条回复文本消息，第二条无回复
	When 清空浏览器
	And tom关注jobs的公众号
	And tom在微信中向jobs的公众号发送消息'tom发送一条文本消息1，未回复'
	And tom在微信中向jobs的公众号发送消息'关键词tom'
	And tom在微信中向jobs的公众号发送消息'tom发送一条文本消息2，未回复'

@mall2 @weixin @message @realtimeMessage 
Scenario: 1 jobs浏览会员的消息详情

	Given jobs登录系统

	When jobs查看'tom'的消息详情
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

	When jobs查看'bill'的消息详情
	Then jobs获得'bill'消息详情消息列表
		"""
		[{
			"member_name": "jobs",
			"inf_content": "图文1",
			"time": "今天"
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"time": "今天"
		},{
			"member_name": "bill",
			"inf_content": "bill发送一条文本消息，未回复",
			"time": "今天"
		}]
		"""

