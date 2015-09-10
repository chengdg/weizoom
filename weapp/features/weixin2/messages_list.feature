# __author__ : "benchi"
Feature: jobs能看到消息列表信息，包括，分页显示，所有信息，未读信息，未回复，有备注 ，星标信息
	
Background:
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
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝2",
	   		"inf_content": "信息内容aaaaaaaaa已读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:48:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3333",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:47:07",
	    	"latest_reply_time": "2015-04-21 13:31:45",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝44444",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:46:07",
	    	"latest_reply_time": "2015-04-21 11:32:45",
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
		}
	]
	"""
	
	Given bill关注jobs的公众号

@new_weixin.message @va
Scenario: 1 bill给jobs发微信后，jobs登录系统后 能看到 消息信息列表 (分页，每页两条)

	When bill发信息给jobs
	"""
		{
			"fans_name": "bill",
	   		"inf_content": "信息内容aaaaaaaaa",
	    	"last_message_time": "2015-04-21 15:45:07"
		}
	"""
	Then jobs成功获取'所有信息'列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count":1 ,
	   		"fans_name": "bill",
	   		"inf_content": "信息内容aaaaaaaaa",
	    	"last_message_time": "2015-04-21 15:45:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}
	]
	"""
	When jobs浏览'下一页'
	Then jobs成功获取"所有信息"列表
	"""
		[{
			"have_read": true,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝2",
	   		"inf_content": "信息内容aaaaaaaaa已读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:48:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3333",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:47:07",
	    	"latest_reply_time": "2015-04-21 13:31:45",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}
	]
	"""
	When jobs浏览'上一页'
	Then jobs成功获取"所有信息"列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": ,
	   		"fans_name": "bill",
	   		"inf_content": "信息内容aaaaaaaaa",
	    	"last_message_time": "2015-04-21 15:45:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}
	]
	"""
	When jobs浏览'第3页'
	Then jobs成功获取"所有信息"列表
	"""
		[{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝44444",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:46:07",
	    	"latest_reply_time": "2015-04-21 11:32:45",
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
		}
	]
	"""

@new_weixin.message
Scenario: 2 bill给jobs发微信后，jobs登录系统后 能看到 消息信息列表 (不分页)，包括，所有信息，未读信息，未回复，有备注 ，星标信息

	When bill发信息给jobs
	"""
		{
			"fans_name": "bill",
	   		"inf_content": "信息内容aaaaaaaaa",
	    	"last_message_time": "2015-04-21 15:45:07"
		}
	"""

	Then jobs成功获取"所有信息"列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 1,
	   		"fans_name": "bill",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-21 15:45:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝2",
	   		"inf_content": "信息内容aaaaaaaaa已读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:48:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3333",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:47:07",
	    	"latest_reply_time": "2015-04-21 13:31:45",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝44444",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:46:07",
	    	"latest_reply_time": "2015-04-21 11:32:45",
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
		}
	]
	"""

	Then jobs成功获取"未读信息"列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 1,
	   		"fans_name": "bill",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-21 15:45:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}
	]
	"""
	Then jobs成功获取"未回复"列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 1,
	   		"fans_name": "bill",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-21 15:45:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝2",
	   		"inf_content": "信息内容aaaaaaaaa已读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:48:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}
	]
	"""

	Then jobs成功获取"有备注"列表
	"""
		[{
			"have_read": true,
			"have_replied": true,
	   		"remark": "我的备注信息111",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝44444",
	   		"inf_content": "信息内容aaaaaaaaa已读，已回复，有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:46:07",
	    	"latest_reply_time": "2015-04-21 11:32:45",
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
		}
	]
	"""
	Then jobs成功获取"星标信息"列表
	"""
		[{
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
		}
	]
	"""