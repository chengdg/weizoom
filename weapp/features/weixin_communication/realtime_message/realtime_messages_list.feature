#watcher:wangli@weizoom.com,wangxinrui@weizoom.com,benchi@weizoom.com
# __author__ : "王丽"
#editor 新新 2015.10.16

Feature:实时消息列表
"""
	公众号与关注此公众号的粉丝直接的消息互动的消息列表展示
	1、在消息列表中对某个粉丝加备注,表示在该粉丝的最后一条消息上（可能是粉丝的发送消息也可能是回复粉丝的消息）加备注
	2、加完备注后消息状态变为已读
	3、自动回复的消息，在以粉丝为列表的选项卡中（"所有信息"、"未读信息"、"未回复"），最后一条不计算自动回复的消息，添加备注时，添加到最后添加消息，也不计算自动回复的消息
	备注：为在feature中实现
	4、只有48小时内的消息可以回复，48小时之后的粉丝消息就不能再回复了
	备注：为在feature中实现

	快速回复不能在feature中实现
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

	#nokia关注jobs的公众号进行消息互动，发送一条，jobs回复一条图文消息
	When 清空浏览器
	And nokia关注jobs的公众号
	And nokia在微信中向jobs的公众号发送消息'关键词nokia'


@mall2 @weixin @message @realtimeMessage
Scenario:1 获取"所有消息"选项卡列表

	Given jobs登录系统
	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1
		}]
		"""

@mall2 @weixin @message @realtimeMessage 
Scenario:2 获取"未读信息"选项卡列表

	Given jobs登录系统
	When jobs获得实时消息'未读信息'列表
		"""
		[{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1
		}]
		"""

@mall2 @weixin @message @realtimeMessage 
Scenario:3 获取"未回复"选项卡列表

	Given jobs登录系统
	When jobs获得实时消息'未回复'列表
		"""
		[{
			"member_name": "nokia",
			"inf_content": "关键词nokia",
			"last_message_time": "今天",
			"unread_count": 0
		},{
			"member_name": "tom",
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天",
			"unread_count": 2
		},{
			"member_name": "bill",
			"inf_content": "关键词bill",
			"last_message_time": "今天",
			"unread_count": 1
		}]
		"""

@mall2 @weixin @message @realtimeMessage 
Scenario:4 实时消息列表查询

	Given jobs登录系统
	#添加会员等级
	And jobs添加会员等级
		"""
		[{
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "10"
		},{
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "9"
		}]
		"""
	#添加会员分组
	When jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2",
			"tag_id_3": "分组3"
		}
		"""

	#调整会员分组
	When jobs给"tom"调分组
		"""
		[
			"分组1", "分组3"
		]
		"""
	When jobs给"bill"调分组
		"""
		[
			"分组2", "分组3"
		]
		"""

	#设置会员等级
	When jobs更新'bill'的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "银牌会员"
		}
		"""
	When jobs更新'tom'的会员等级
		"""
		{
			"name": "tom",
			"member_rank": "银牌会员"
		}
		"""

	#按照会员昵称查询
	When jobs设置实时消息查询条件
		"""
		{
			"member_name":"k"
		}
		"""
	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"unread_count": 0,
			"inf_content": "关键词nokia",
			"last_message_time": "今天"
		}]
		"""

	#按照消息内容查询
	When jobs设置实时消息查询条件
		"""
		{
			"inf_content":"文本"
		}
		"""
	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息1，未回复",
			"last_message_time": "今天"
		},{
			"member_name": "bill",
			"unread_count": 0,
			"inf_content": "bill发送一条文本消息，未回复",
			"last_message_time": "今天"
		}]
		"""

	#按消息时间查询
	When jobs设置实时消息查询条件
		"""
		{
			"start_date":"今天",
			"end_date":"1天后"
		}
		"""
	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"unread_count": 0,
			"inf_content": "关键词nokia",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "关键词tom",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息1，未回复",
			"last_message_time": "今天"
		},{
			"member_name": "bill",
			"unread_count": 0,
			"inf_content": "关键词bill",
			"last_message_time": "今天"
		},{
			"member_name": "bill",
			"unread_count": 0,
			"inf_content": "bill发送一条文本消息，未回复",
			"last_message_time": "今天"
		}]
		"""

	#按照会员分组查询
	When jobs设置实时消息查询条件
		"""
		{
			"tags":"分组3"
		}
		"""
	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "关键词tom",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息1，未回复",
			"last_message_time": "今天"
		},{
			"member_name": "bill",
			"unread_count": 0,
			"inf_content": "关键词bill",
			"last_message_time": "今天"
		},{
			"member_name": "bill",
			"unread_count": 0,
			"inf_content": "bill发送一条文本消息，未回复",
			"last_message_time": "今天"
		}]
		"""

	#按照会员等级查询
	When jobs设置实时消息查询条件
		"""
		{
			"member_rank":"银牌会员"
		}
		"""
	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "关键词tom",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息1，未回复",
			"last_message_time": "今天"
		},{
			"member_name": "bill",
			"unread_count": 0,
			"inf_content": "关键词bill",
			"last_message_time": "今天"
		},{
			"member_name": "bill",
			"unread_count": 0,
			"inf_content": "bill发送一条文本消息，未回复",
			"last_message_time": "今天"
		}]
		"""

	#综合查询
	When jobs设置实时消息查询条件
		"""
		{
			"member_name":"tom",
			"inf_content":"关键词tom",
			"start_date":"今天",
			"end_date":"1天后",
			"tags":"分组3",
			"member_rank":"银牌会员"
		}
		"""
	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "关键词tom",
			"last_message_time": "今天"
		}]
		"""


@mall2 @weixin @message @realtimeMessage 
Scenario:5 实时消息"所有消息"列表分页

	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""

	#按消息时间查询
	When jobs设置实时消息查询条件
		"""
		{
			"start_date":"今天",
			"end_date":"1天后"
		}
		"""

	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "nokia",
			"unread_count": 0,
			"inf_content": "关键词nokia",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息2，未回复",
			"last_message_time": "今天"
		}]
		"""

	When jobs浏览列表第2页
	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "关键词tom",
			"last_message_time": "今天"
		},{
			"member_name": "tom",
			"unread_count": 0,
			"inf_content": "tom发送一条文本消息1，未回复",
			"last_message_time": "今天"
		}]
		"""

	When jobs浏览列表第3页
	When jobs获得实时消息'所有信息'列表
		"""
		[{
			"member_name": "bill",
			"unread_count": 0,
			"inf_content": "关键词bill",
			"last_message_time": "今天"
		},{
			"member_name": "bill",
			"unread_count": 0,
			"inf_content": "bill发送一条文本消息，未回复",
			"last_message_time": "今天"
		}]
		"""

