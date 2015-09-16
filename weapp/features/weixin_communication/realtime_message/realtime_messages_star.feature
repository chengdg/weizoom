# __author__ : "benchi"
# __author__ : "王丽"
Feature: jobs给实时消息加星标
			1在消息列表中，在所有信息，未读信息，未回复，三个选项卡下对某个粉丝消息加星标1)表示在最后一条加星标2)加完星标后，消息状态还是以前的状态，例如未读，还是未读状态
			2在消息详情中加星标，针对的是某个粉丝的某一条消息的星标
			3星标图变化，未加是空心星标，已加，是实心，并且可以相互切换
	
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
	
@weixin @message @realtimeMessage @wll
Scenario: 1 在消息列表的"所有信息"、"未读信息"、"未回复"加星标
	1)三个选项卡下对某个粉丝消息加星标，去掉星标,表示在最后一条加星标
	2)加完星标后，消息状态还是以前的状态，例如未读，还是未读状态

	#在"所有信息"选项卡加星标
	When jobs访问实时消息'所有信息'

	#添加星标
	When jobs修改实时消息星标
		"""
		[{
			"member_name":"bill",
			"inf_content":"关键词bill",
			"start": "true"
		}]
		"""
	When jobs修改实时消息星标
		"""
		[{
			"member_name":"nokia",
			"inf_content":"关键词nokia",
			"start": "true"
		}]
		"""
	Then jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "true"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2,
			"start": "false"
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1,
			"start": "true"
		}]
		"""

	#去掉星标
	When jobs修改实时消息星标
		"""
		[{
			"member_name":"bill",
			"inf_content":"关键词bill",
			"start": "false"
		}]
		"""
	Then jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "true"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2,
			"start": "false"
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1,
			"start": "false"
		}]
		"""

	#在"未读信息"选项卡加星标
	When jobs访问实时消息'未读信息'
	When jobs修改实时消息星标
		"""
		[{
			"member_name":"tom",
			"inf_content":"tom发送一条文本消息2，未回复",
			"start": "true"
		}]
		"""
	Then jobs获得实时消息'未读信息'列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2,
			"start": "true"
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1,
			"start": "false"
		}]
		"""

	#在"未回复"选项卡加星标
	When jobs访问实时消息'未回复'
	When jobs修改实时消息星标
		"""
		[{
			"member_name":"tom",
			"inf_content":"tom发送一条文本消息2，未回复",
			"start": "flase"
		}]
		"""
	Then jobs获得实时消息'未回复'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "true"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2,
			"start": "false"
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1,
			"start": "false"
		}]
		"""

@weixin @message @realtimeMessage
Scenario: 2 在消息详情中加星标
	#针对的是某个粉丝的某一条消息的星标或去掉星标

	Given jobs登录系统

	When jobs查看'tom'的消息详情
	Then jobs获得'tom'消息详情消息列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"time": "今天",
			"start": "false"
		},{
			"member_name": "jobs",
			"inf_content": "【自动回复】 关键字回复内容tom",
			"time": "今天",
			"start": "false"
		},{
			"member_name": "tom",
			"inf_content": "关键词tom",
			"time": "今天",
			"start": "false"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息1，未回复",
			"time": "今天",
			"start": "false"
		}]
		"""

	#给tom在消息详情中的最后一条消息上添加星标
	When jobs修改实时消息星标
		"""
		[{
			"member_name":"tom",
			"inf_content":"tom发送一条文本消息2，未回复",
			"start": "true"
		}]
		"""
	Then jobs获得'tom'消息详情消息列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"time": "今天",
			"start": "true"
		},{
			"member_name": "jobs",
			"inf_content": "【自动回复】 关键字回复内容tom",
			"time": "今天",
			"start": "false"
		},{
			"member_name": "tom",
			"inf_content": "关键词tom",
			"time": "今天",
			"start": "false"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息1，未回复",
			"time": "今天",
			"start": "false"
		}]
		"""
	Then jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "false"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "true"
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1,
			"start": "false"
		}]
		"""
	Then jobs获得实时消息'星标信息'列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "true"
		}]
		"""

	#给tom在消息详情中的非最后一条消息上添加星标
	When jobs修改实时消息星标
		"""
		[{
			"member_name":"tom",
			"inf_content":"tom发送一条文本消息2，未回复",
			"start": "false"
		}]
		"""
	When jobs修改实时消息星标
		"""
		[{
			"member_name":"tom",
			"inf_content":"关键词tom",
			"start": "true"
		}]
		"""
	When jobs修改实时消息星标
		"""
		[{
			"member_name":"jobs",
			"inf_content":"【自动回复】 关键字回复内容tom",
			"start": "true"
		}]
		"""
	Then jobs获得'tom'消息详情消息列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"time": "今天",
			"start": "false"
		},{
			"member_name": "jobs",
			"inf_content": "【自动回复】 关键字回复内容tom",
			"time": "今天",
			"start": "true"
		},{
			"member_name": "tom",
			"inf_content": "关键词tom",
			"time": "今天",
			"start": "true"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息1，未回复",
			"time": "今天",
			"start": "false"
		}]
		"""
	Then jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "false"
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "false"
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1,
			"start": "false"
		}]
		"""
	Then jobs获得实时消息'星标信息'列表
		"""
		[{
			"member_name": "jobs",
			"inf_content": "【自动回复】 关键字回复内容tom",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "true"
		},{
			"member_name": "tom",
			"inf_content": "关键词tom",
			"last_message_time": "今天",
			"unread_count": 0,
			"start": "true"
		}]
		"""

