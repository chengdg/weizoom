# __author__ : "benchi"
# __author__ : "王丽"

Feature: jobs给实时消息加备注
"""
	1在消息列表中对某个粉丝消息加备注1)表示在最后一条加备注，那么备注信息显示在该粉丝备注信息中，2)加完备注后消息状态变为已读
	2在消息详情中加备注，针对的是某个粉丝的某一条消息的备注
	3在已有备注下，加备注，相当于替换原有的备注信息
	4备注图标不变，只有加备注后图标才变化
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
			"rules_name":"规则2",
			"keyword": [{
					 "keyword": "关键词nokia",
					 "type": "like"
				}],
			"keyword_reply": [{
					 "reply_content":"图文1",
					 "reply_type":"text_picture"
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
	and bill关注jobs的公众号
	and bill访问jobs的webapp
	and bill在微信中向jobs的公众号发送消息'bill发送一条文本消息，未回复'
	and bill在微信中向jobs的公众号发送消息'关键词bill'

	#tom关注jobs的公众号进行消息互动，发送两条，第一条回复文本消息，第二条无回复
	When 清空浏览器
	and tom关注jobs的公众号
	and tom在微信中向jobs的公众号发送消息'tom发送一条文本消息1，未回复'
	and tom在微信中向jobs的公众号发送消息'关键词tom'
	and tom在微信中向jobs的公众号发送消息'tom发送一条文本消息2，未回复'

	#nokia关注jobs的公众号进行消息互动，发送一条，jobs回复一条图文消息
	When 清空浏览器
	and nokia关注jobs的公众号
	and nokia在微信中向jobs的公众号发送消息'关键词nokia'

@weixin @message @realtimeMessage @eugeneA
Scenario:1 在消息列表的"所有信息"、"未读信息"、"未回复"加备注
	#1)表示在最后一条加备注，那么备注信息显示在该粉丝备注信息中，
	#2)加完备注后消息状态变为已读
	#3)对已有备注进行修改

	#在"所有信息"选项卡加备注
	Given jobs登录系统
	When jobs访问实时消息'所有信息'

	#添加备注
	When jobs修改实时消息备注
		"""
		[{
			"member_name":"bill",
			"inf_content":"关键词bill",
			"remark": "bill消息“关键词bill”的消息备注"
		}]
		"""
	When jobs修改实时消息备注
		"""
		[{
			"member_name":"nokia",
			"inf_content":"关键词nokia",
			"remark": "nokia消息“关键词nokia”的消息备注"
		}]
		"""
	Then jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "nokia消息“关键词nokia”的消息备注"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2,
			"remark": ""
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "bill消息“关键词bill”的消息备注"
		}]
		"""

	#去掉备注
	When jobs修改实时消息备注
		"""
		[{
			"member_name":"bill",
			"inf_content":"关键词bill",
			"remark": ""
		}]
		"""
	Then jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "nokia消息“关键词nokia”的消息备注"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2,
			"remark": ""
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": ""
		}]
		"""

	#在"未读信息"选项卡加备注
	When jobs访问实时消息'未读信息'
	Then jobs获得实时消息'未读信息'列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2,
			"remark": ""
		}]
		"""
	When jobs修改实时消息备注
		"""
		[{
			"member_name":"tom",
			"inf_content":"tom发送一条文本消息2，未回复",
			"remark": "tom消息“文本消息2”的消息备注"
		}]
		"""
	Then jobs获得实时消息'未读信息'列表
		"""
		[]
		"""
	When jobs访问实时消息'所有信息'
	Then jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "nokia消息“关键词nokia”的消息备注"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "tom消息“文本消息2”的消息备注"
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": ""
		}]
		"""

	#在"未回复"选项卡加备注
	When jobs访问实时消息'未回复'
	When jobs修改实时消息备注
		"""
		[{
			"member_name":"tom",
			"inf_content":"tom发送一条文本消息2，未回复",
			"remark": ""
		}]
		"""
	When jobs访问实时消息'未回复'
	Then jobs获得实时消息'未回复'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "nokia消息“关键词nokia”的消息备注"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": ""
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": ""
		}]
		"""


@weixin @message @realtimeMessage
Scenario:2 在消息详情中加备注
	#针对的是某个粉丝的某一条消息的备注

	Given jobs登录系统

	When jobs查看'tom'的消息详情
	Then jobs获得'tom'消息详情消息列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"time": "今天",
			"remark": ""
		},{
			"member_name": "jobs",
			"inf_content": "【自动回复】 关键字回复内容tom",
			"time": "今天",
			"remark": ""
		},{
			"member_name": "tom",
			"inf_content": "关键词tom",
			"time": "今天",
			"remark": ""
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息1，未回复",
			"time": "今天",
			"remark": ""
		}]
		"""

	#给tom在消息详情中的最后一条消息上添加备注
	When jobs修改实时消息备注
		"""
		[{
			"member_name":"tom",
			"inf_content":"tom发送一条文本消息2，未回复",
			"remark": "tom消息“文本消息2”的消息备注"
		}]
		"""
	Then jobs获得'tom'消息详情消息列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"time": "今天",
			"remark": "tom消息“文本消息2”的消息备注"
		},{
			"member_name": "jobs",
			"inf_content": "【自动回复】 关键字回复内容tom",
			"time": "今天",
			"remark": ""
		},{
			"member_name": "tom",
			"inf_content": "关键词tom",
			"time": "今天",
			"remark": ""
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息1，未回复",
			"time": "今天",
			"remark": ""
		}]
		"""
	When jobs访问实时消息'所有信息'
	Then jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": ""
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "tom消息“文本消息2”的消息备注"
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1,
			"remark": ""
		}]
		"""
	When jobs访问实时消息'有备注'
	Then jobs获得实时消息'有备注'列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "tom消息“文本消息2”的消息备注"
		}]
		"""

	#给tom在消息详情中的非最后一条消息上添加备注
	When jobs修改实时消息备注
		"""
		[{
			"member_name":"tom",
			"inf_content":"tom发送一条文本消息2，未回复",
			"remark": ""
		}]
		"""
	When jobs修改实时消息备注
		"""
		[{
			"member_name":"tom",
			"inf_content":"关键词tom",
			"remark": "tom消息“关键词tom”的消息备注"
		}]
		"""
	When jobs修改实时消息备注
		"""
		[{
			"member_name":"jobs",
			"inf_content":"【自动回复】 关键字回复内容tom",
			"remark": "tom消息“【自动回复】XXX”的消息备注"
		}]
		"""
	Then jobs获得'tom'消息详情消息列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"time": "今天",
			"remark": ""
		},{
			"member_name": "jobs",
			"inf_content": "【自动回复】 关键字回复内容tom",
			"time": "今天",
			"remark": "tom消息“【自动回复】XXX”的消息备注"
		},{
			"member_name": "tom",
			"inf_content": "关键词tom",
			"time": "今天",
			"remark": "tom消息“关键词tom”的消息备注"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息1，未回复",
			"time": "今天",
			"remark": ""
		}]
		"""
	When jobs访问实时消息'所有信息'
	Then jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": ""
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": ""
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1,
			"remark": ""
		}]
		"""
	When jobs访问实时消息'有备注'
	Then jobs获得实时消息'有备注'列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "关键词tom",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "tom消息“关键词tom”的消息备注"
		},{
			"member_name": "jobs",
			"inf_content": "【自动回复】 关键字回复内容tom",
			"last_message_time": "今天",
			"unread_count": 0,
			"remark": "tom消息“【自动回复】XXX”的消息备注"
		}]
		"""
