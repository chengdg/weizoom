# __author__ : "benchi"
Feature: jobs能根据 搜索条件，搜索到实时消息列表信息，搜索条件包括，'消息内容'， 开始时间，结束时间
						  消息内容的搜索为，部分匹配，例如abc，搜ac，结果为空，搜ab，结果为abc
						  搜索功能与选项卡无关，例如，当前选项卡是'有备注'但搜索的信息是针对所有消息进行搜索的
	
@new_weixin.message
Scenario: 1 jobs根据'消息内容'搜索实时消息列表内容，搜索结果与所在的选项卡无关,搜索结果按内容，全部列到 所有信息列表中
			注意：列表展现时，是按粉丝展现的，但搜索结果是按内容展现
	Given jobs登录系统
	And jobs已获取粉丝信息列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标----2",
	    	"last_message_time": "2015-04-20 14:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start":true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝55555",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，有星标",
	    	"last_message_time": "2015-04-20 13:45:07",
	    	"latest_reply_time": "2015-04-21 12:32:45",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""

	When jobs在"所有信息"选项卡下搜索消息内容
	"""
		{
			"inf_content": "星标"
		}
	"""
	Then jobs成功获取"搜索结果"列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标----2",
	    	"last_message_time": "2015-04-20 14:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start":true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝55555",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，有星标",
	    	"last_message_time": "2015-04-20 15:45:07",
	    	"latest_reply_time": "2015-04-21 12:32:45",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""
	When jobs在"星标信息"选项卡下搜索消息内容
	"""
		{
			"inf_content": "星标"
		}
	"""
	Then jobs成功获取"搜索结果"列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标----2",
	    	"last_message_time": "2015-04-20 14:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start":true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝55555",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，有星标",
	    	"last_message_time": "2015-04-20 15:45:07",
	    	"latest_reply_time": "2015-04-21 12:32:45",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""
	When jobs在"星标信息"选项卡下搜索消息内容
	"""
		{
			"inf_content": "信息内容未读未回复没有备注没有星标----2"
		}
	"""
	Then jobs成功获取"搜索结果"列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标----2",
	    	"last_message_time": "2015-04-20 14:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}
	]
	"""
	When jobs在"星标信息"选项卡下搜索消息内容
	"""
		{
			"inf_content": "信息星标"
		}
	"""
	Then jobs成功获取"搜索结果"列表
	"""
		[]
	"""
@new_weixin.message
Scenario: 2 jobs根据粉丝发消息的时间范围搜索，搜索结果与所在的选项卡无关
	Given jobs登录系统
	And jobs已获取粉丝信息列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标",
	    	"last_message_time": "2015-04-20 00:00:00",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标",
	    	"last_message_time": "2015-04-19 23:00:00",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start":true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝55555",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，有星标",
	    	"last_message_time": "2015-03-19 15:45:07",
	    	"latest_reply_time": "2015-04-20 12:32:45",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start":true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝55555",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，有星标",
	    	"last_message_time": "2015-03-19 00:00:00",
	    	"latest_reply_time": "2015-04-20 12:32:45",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""

	
	When jobs在"星标信息"选项卡下按时间搜索
	"""
		{
			"start_time": "2015-03-19 00:00:00",
			"end_time": "2015-04-20 00:00:00"
		}
	"""
	Then jobs成功获取"搜索结果"列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容未读未回复没有备注没有星标",
	    	"last_message_time": "2015-04-20 00:00:00",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start":true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝55555",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，有星标",
	    	"last_message_time": "2015-03-19 00:00:00",
	    	"latest_reply_time": "2015-04-20 12:32:45",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""
	When jobs在"星标信息"选项卡下按时间搜索
	"""
		{
			"start_time": "2015-03-18 00:00:00",
			"end_time": "2015-03-17 00:00:00"
		}
	"""
	Then jobs成功获取"搜索结果"列表
	"""
		[]
	"""
	
@new_weixin.message
Scenario: 3 jobs根据 消息内容和粉丝发消息的时间范围搜索，搜索结果与所在的选项卡无关
	Given jobs登录系统
	And jobs已获取粉丝信息列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "粉丝1消息内容1",
	    	"last_message_time": "2015-04-20 00:00:00",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "粉丝1消息内容2",
	    	"last_message_time": "2015-04-19 23:00:00",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "粉丝1消息内容12",
	    	"last_message_time": "2015-04-18 23:00:00",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""

	
	When jobs在"星标信息"选项卡下按时间搜索
	"""
		{
			"inf_content": "粉丝1消息内容1",
			"start_time": "2015-04-19 00:00:00",
			"end_time": "2015-04-20 00:00:00"
		}
	"""
	Then jobs成功获取"搜索结果"列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "粉丝1消息内容1",
	    	"last_message_time": "2015-04-20 00:00:00",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""
	When jobs在"星标信息"选项卡下按时间搜索
	"""
		{
			"inf_content": "粉丝1消息内容2",
			"start_time": "2015-03-18 00:00:00",
			"end_time": "2015-04-18 00:00:00"
		}
	"""
	Then jobs成功获取"搜索结果"列表
	"""
		[]
	"""