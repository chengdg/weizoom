# __author__ : "benchi"
Feature: jobs给实时消息加备注
			1在消息列表中对某个粉丝消息加备注1)表示在最后一条加备注，那么备注信息显示在该粉丝备注信息中，2)加完备注后消息状态变为已读
			2在消息详情中加备注，针对的是某个粉丝的某一条消息的备注
			3在已有备注下，加备注，相当于替换原有的备注信息
			4备注图标不变，只有加星标后图标才变化
	
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
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "粉丝1之前的信息------信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 11:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 1,
	   		"fans_name": "粉丝2",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:48:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容",
	    	"last_message_time": "2015-04-20 15:48:06",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""
	
	

@new_weixin.message
Scenario: 1在消息列表中对某个粉丝消息加备注 1)表示在最后一条加备注，那么备注信息显示在该粉丝备注信息中，2)加完备注后消息状态变为已读 3）对已有备注进行修改

	When jobs在"所有信息"选项卡下给"粉丝1"添加备注信息
		"""
		[{
			"remark": "粉丝1的备注"
			
		}]
		"""
	
	Then jobs成功获取'有备注'列表
	"""
		[{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝1的备注",
	   		"start": false,
	   		"unread_count": 0 ,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容",
	    	"last_message_time": "2015-04-20 15:48:06",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""

#把粉丝1的备注去掉，'有备注选项卡'下不显示粉丝1的消息
	When jobs在"有备注"选项卡下给"粉丝1"修改备注信息
		"""
		[{
			"remark": ""
			
		}]
		"""
	
	Then jobs成功获取'有备注'列表
	"""
		[{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容",
	    	"last_message_time": "2015-04-20 15:48:06",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""

	When jobs在"所有信息"选项卡下给"粉丝3"修改备注信息
		"""
		[{
			"remark": "粉丝3的备注修改"
			
		}]
		"""
	Then jobs成功获取'所有信息'列表
	"""
		[{
			"have_read": true,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 0 ,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": false,
	   		"unread_count": 1,
	   		"fans_name": "粉丝2",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:48:07",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注修改",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容",
	    	"last_message_time": "2015-04-20 15:48:06",
	    	"latest_reply_time": "",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""

@new_weixin.message
Scenario: 2在消息详情中加备注，针对的是某个粉丝的某一条消息的备注
	Given jobs登录系统
	And jobs已获取"粉丝1"粉丝信息列表
	"""
		[{
			"remark": "",
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07"
		},{
			"remark": "",
	   		"fans_name": "粉丝1",
	   		"inf_content": "粉丝1之前的信息------信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 11:50:07"
		}]
	"""
	When jobs给"粉丝1"添加备注信息
		"""
		[{
			"last_message_time": "2015-04-20 11:50:07",
			"remark": "粉丝1的备注"
			
		}]
		"""
	
	Then jobs成功获取"粉丝1"消息详情列表
	"""
		{
			"messages": [{
			"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"remark": ""
	    },{
			"fans_name": "粉丝1",
	   		"inf_content": "粉丝1之前的信息------信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 11:50:07",
	    	"remark": "粉丝1的备注"
	    }]
		}
	"""

	When jobs获取"粉丝1"原有备注信息
		"""
		[{
			"last_message_time": "2015-04-20 11:50:07",
			"remark": "粉丝1的备注"
			
		}]
		"""
	Then jobs给"粉丝1"修改备注信息
		"""
		[{
			"last_message_time": "2015-04-20 11:50:07",
			"remark": "粉丝1的-------备注修改"
			
		}]
		"""

	Then jobs成功获取"粉丝1"消息详情列表
	"""
		{
			"messages": [{
			"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"remark": ""
	    },{
			"fans_name": "粉丝1",
	   		"inf_content": "粉丝1之前的信息------信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 11:50:07",
	    	"remark": "粉丝1的-------备注修改"
	    }]
		}
	"""