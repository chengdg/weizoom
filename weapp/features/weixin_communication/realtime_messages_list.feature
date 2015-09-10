# __author__ : "王丽"

Feature:实时消息列表
"""
	公众号与关注此公众号的粉丝直接的消息互动的消息列表展示
	1、在消息列表中对某个粉丝加备注,表示在该粉丝的最后一条消息上（可能是粉丝的发送消息也可能是回复粉丝的消息）加备注
	2、加完备注后消息状态变为已读
	3、自动回复的消息，在以粉丝为列表的选项卡中（"所有信息"、"未读信息"、"未回复"），最后一条不计算自动回复的消息，添加备注时，添加都最后添加消息，
	也不计算自动回复的消息
	备注：为在feature中实现
	4、只有48小时内的消息可以回复，48小时之后的粉丝消息就不能再回复了
	备注：为在feature中实现
"""

Background：

	Given jobs登录系统

	When jobs已添加单图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"ture",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
		}]
		"""

	#bill关注jobs的公众号进行消息互动，发送一条，无回复

	When bill关注jobs的公众号
	When bill在模拟器中给jobs发送消息'bill发送一条文本消息，未回复'

	#bill1关注jobs的公众号进行消息互动，发送两条，无回复

	When bill1关注jobs的公众号
	When bill1在模拟器中给jobs发送消息'bill1发送一条文本消息，未回复'
	When bill1在模拟器中给jobs发送消息'bill1_图片.png'

	#bill2关注jobs的公众号进行消息互动，发送一条，jobs回复一条文本消息

	When bill2关注jobs的公众号
	When bill2在模拟器中给jobs发送消息'bill2发送一条文本消息，回复文本消息'
	When jobs在模拟器中给bill2回复消息'jobs回复bill2消息'

	#bill3关注jobs的公众号进行消息互动，发送一条，jobs回复一条图文消息

	When bill3关注jobs的公众号
	When bill3在模拟器中给jobs发送消息'bill3发送一条文本消息，回复图文'
	When jobs在模拟器中给bill3回复消息'图文1'

Scenario:1 获取"所有消息"选项卡列表

	Given jobs登录系统

	Then jobs获得实时消息"所有信息"列表
		"""
		[{
			"have_read": true,
			"have_replied": true,
			"remark": "",
			"start": false,
			"unread_count": 0,
			"fans_name": "bill3",
			"inf_content": "图文1",
			"last_message_time": "今天",
			"latest_reply_time": "今天",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
			"remark": "",
			"start": false,
			"unread_count": 0,
			"fans_name": "bill2",
			"inf_content": "jobs回复bill2消息",
			"last_message_time": "今天",
			"latest_reply_time": "今天",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 2,
			"fans_name": "bill1",
			"inf_content": "bill1_图片.png，未回复",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 1,
			"fans_name": "bill",
			"inf_content": "bill发送一条文本消息，未回复",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		"""

Scenario:2 获取"未读信息"选项卡列表

	Given jobs登录系统

	Then jobs获得实时消息"未读信息"列表
		"""
		[{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 2,
			"fans_name": "bill1",
			"inf_content": "bill1_图片.png，未回复",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 1,
			"fans_name": "bill",
			"inf_content": "bill发送一条文本消息，未回复",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		"""

Scenario:3 获取"未回复""有备注""星标信息"选项卡列表

	Given jobs登录系统

	Then jobs获得实时消息"所有信息"选项卡列表
		"""
		[{
			"have_read": true,
			"have_replied": true,
			"remark": "",
			"start": false,
			"unread_count": 0,
			"fans_name": "bill3",
			"inf_content": "图文1",
			"last_message_time": "今天",
			"latest_reply_time": "今天",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
			"remark": "",
			"start": false,
			"unread_count": 0,
			"fans_name": "bill2",
			"inf_content": "jobs回复bill2消息",
			"last_message_time": "今天",
			"latest_reply_time": "今天",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 2,
			"fans_name": "bill1",
			"inf_content": "bill1_图片.png，未回复",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 1,
			"fans_name": "bill",
			"inf_content": "bill发送一条文本消息，未回复",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		"""

	When jobs在"所有信息"选项卡下给"bill1 "添加备注信息
		"""
		[{
			"remark": "bill1的备注"
		}]
		"""

	When jobs在"所有信息"选项卡下给"bill2 "添加备注信息
		"""
		[{
			"remark": "bill2的备注"
		}]
		"""

	Then jobs获得实时消息"未回复"选项卡列表
		"""
		[{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 1,
			"fans_name": "bill",
			"inf_content": "bill发送一条文本消息，未回复",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		"""

	Then jobs获得实时消息"有备注"选项卡列表
		"""
		[{
			"have_read": true,
			"have_replied": true,
			"remark": "bill2的备注",
			"start": false,
			"unread_count": 0,
			"fans_name": "bill2",
			"inf_content": "jobs回复bill2消息",
			"last_message_time": "今天",
			"latest_reply_time": "今天",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": false,
			"remark": "bill1的备注",
			"start": false,
			"unread_count": 0,
			"fans_name": "bill1",
			"inf_content": "bill1_图片.png，未回复",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		"""

	When jobs在"所有信息"选项卡下给"bill3 "添加星标
		"""
		[{
			"start": true
		}]
		"""

	Then jobs获得实时消息"星标信息"选项卡列表
		"""
		[{
			"have_read": true,
			"have_replied": true,
			"remark": "",
			"start": true,
			"unread_count": 0,
			"fans_name": "bill3",
			"inf_content": "图文1",
			"last_message_time": "今天",
			"latest_reply_time": "今天",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		"""

Scenario:4 自动回复的消息，在以粉丝为列表的选项卡中（"所有信息"、"未读信息"、"未回复"），最后一条不计算自动回复的消息

Scenario:5 只有48小时内的消息可以回复，48小时之后的粉丝消息就不能再回复
