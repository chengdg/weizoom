#_author_:张雪 2016.04.12

Feature: 后台操作
	"""
	管理员删除用户提交的报名申请，列表中消失
		1.微信用户提交报名申请；
		2.报名详情中该微信用户提交高级投票申请状态为“待审核”；
		3.管理员删除该用户提交的申请；
		4.活动详情中的报名申请记录消失；


	"""
Background:
	Given jobs登录系统
	When jobs新建高级微信投票活动
		"""
		[{
			"title":"微信高级投票-进行中",
			"groups":["初中组","高中组"],
			"rule": "高级投票规则",
			"desc":"高级投票活动介绍",
			"start_date":"今天",
			"end_date":"2天后",
			"pic":"3.jpg"
		}]
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"高级投票活动1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"微信高级投票摘要",
			"content":"微信高级投票内容",
			"jump_url":"微信高级投票"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword":
				[{
					"keyword": "微信高级投票",
					"type": "equal"
				}],
			"keyword_reply":
				[{
					"reply_content":"高级投票活动1单图文",
					"reply_type":"text_picture"
				}]

		}]
		"""
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级投票活动1单图文'
	When bill点击图文"高级投票活动1单图文"进入高级微信投票活动页面
	When bill参加高级投票报名活动
	"""
		{
			"headImg":"bill_head.jpg",
			"name":"bill",
			"group":["初中组"],
			"number":"001",
			"details":"bill的产品好",
			"detail_pic":["pic1.jpg","pic2.jpg"]
		}
	"""
	When dill关注jobs的公众号
	When dill访问jobs的webapp
	When dill在微信中向jobs的公众号发送消息'微信高级投票'
	Then dill收到自动回复'高级投票活动1单图文'
	When dill点击图文"高级投票活动1单图文"进入高级微信投票活动页面
	When dill参加高级投票报名活动
	"""
		{
			"headImg":"dill_head.jpg",
			"name":"dill",
			"group":["高中组"],
			"number":"002",
			"details":"dill的产品好",
			"detail_pic":["pic3.jpg","pic4.jpg"]
		}
	"""

@mall2 @apps @shvote @shvote_delete @yang2
Scenario:1 管理员删除微信用户提交高级投票申请，列表中消失
	Given jobs登录系统
	When jobs于高级微信投票活动审核通过'bill'
	When jobs于高级微信投票活动删除'dill'
	Then jobs获得报名详情列表
		"""
		[{
			"headImg":"bill_head.jpg",
			"player":"bill",
			"votes":0,
			"number":"001",
			"start_date":"今天",
			"status":"审核通过",
			"actions":["查看"]
		}]
		"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"vote_count":1,
			"participant_count":1,
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""

