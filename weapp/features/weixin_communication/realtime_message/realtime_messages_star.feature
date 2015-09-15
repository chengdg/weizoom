# __author__ : "benchi"
Feature: jobs给实时消息加星标
			1在消息列表中，在所有信息，未读信息，未回复，三个选项卡下对某个粉丝消息加星标1)表示在最后一条加星标2)加完星标后，消息状态还是以前的状态，例如未读，还是未读状态
			2在消息详情中加星标，针对的是某个粉丝的某一条消息的星标
			3星标图变化，未加是空心星标，已加，是实心，并且可以相互切换
	
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
	    	"star_icon": "空心星图"
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
	    	"star_icon": "空心星图"
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
	    	"star_icon": "空心星图"
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
	    	"star_icon": "空心星图"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注",
	   		"start": true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容----2",
	    	"last_message_time": "2015-04-20 14:48:06",
	    	"latest_reply_time": "",
	    	"star_icon": "实心星图"
		}]
	"""
	
	

@new_weixin.message
Scenario: 1在消息列表中，在所有信息，未读信息，未回复，三个选项卡下对某个粉丝消息加星标，去掉星标
			1)表示在最后一条加星标2)加完星标后，消息状态还是以前的状态，例如未读，还是未读状态

	When jobs在"所有信息"选项卡下给"粉丝1"添加星标
		"""
		[{
			"start": true
		}]
		"""
	
	Then jobs成功获取'所有信息'列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": true,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"star_icon": "实心星图"
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
	    	"star_icon": "空心星图"
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
	    	"star_icon": "空心星图"
		}]
	"""

	Then jobs成功获取'星标信息'列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": true,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"star_icon": "实心星图"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注",
	   		"start": true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容----2",
	    	"last_message_time": "2015-04-20 14:48:06",
	    	"latest_reply_time": "",
	    	"star_icon": "实心星图"
		}]
	"""

	When jobs在"所有信息"选项卡下给"粉丝3"添加星标
		"""
		[{
			"start": true
		}]
		"""
	Then jobs成功获取'星标信息'列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": true,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"star_icon": "实心星图"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注",
	   		"start": true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容",
	    	"last_message_time": "2015-04-20 15:48:06",
	    	"latest_reply_time": "",
	    	"star_icon": "实心星图"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注",
	   		"start": true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容----2",
	    	"last_message_time": "2015-04-20 14:48:06",
	    	"latest_reply_time": "",
	    	"star_icon": "实心星图"
		}]
	"""

#取消的是粉丝3的第二条星标信息，在所有信息选项卡下，看到粉丝3，还是有星标的，因为，该处显示的是最后一条信息情况
	When jobs在"星标信息"选项卡下给"粉丝3"取消星标
		"""
		[{
			"last_message_time": "2015-04-20 14:48:06",
			"start": false
		}]
		"""
	Then jobs成功获取'所有信息'列表
	"""
		[{
			"have_read": false,
			"have_replied": false,
	   		"remark": "",
	   		"start": true,
	   		"unread_count": 2,
	   		"fans_name": "粉丝1",
	   		"inf_content": "信息内容aaaaaaaaa未读，未回复，没有备注，没有星标",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"latest_reply_time": "",
	    	"star_icon": "实心星图"
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
	    	"star_icon": "空心星图"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注",
	   		"start": true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容",
	    	"last_message_time": "2015-04-20 15:48:06",
	    	"latest_reply_time": "",
	    	"star_icon": "实心心星图"
		}]
	"""
@new_weixin.message @wl
Scenario: 2在消息详情中加星标，针对的是某个粉丝的某一条消息的星标或去掉星标
	Given jobs登录系统
	And jobs已获取"粉丝3"粉丝信息列表
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
	    	"star_icon": "空心星图"
		},{
			"have_read": true,
			"have_replied": false,
	   		"remark": "粉丝3的备注",
	   		"start": true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容----2",
	    	"last_message_time": "2015-04-20 14:48:06",
	    	"latest_reply_time": "",
	    	"star_icon": "实心星图"
		}]
	"""
	When jobs给"粉丝3"添加星标
		"""
		[{
			"last_message_time": "2015-04-20 15:48:06",
			"start": true
			
		}]
		"""
	When jobs给"粉丝3"取消星标
		"""
		[{
			"last_message_time": "2015-04-20 14:48:06",
			"start": false
			
		}]
		"""
	
	Then jobs成功获取"粉丝3"消息详情列表
	"""
		{
			"messages": [{
			"remark": "粉丝3的备注",
	   		"start": true,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容",
	    	"last_message_time": "2015-04-20 15:48:06",
	    	"star_icon": "实心星图"
		},{
			"remark": "粉丝3的备注",
	   		"start": false,
	   		"unread_count": 0,
	   		"fans_name": "粉丝3",
	   		"inf_content": "粉丝3信息内容----2",
	    	"last_message_time": "2015-04-20 14:48:06",
	    	"star_icon": "空心星图"
		}]
		}
	"""