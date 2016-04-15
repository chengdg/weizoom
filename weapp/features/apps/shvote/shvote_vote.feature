#_author_:张雪 2016.04.12

Feature: 微信用户给参与者投票
	"""
		1.微信用户提交报名申请；
		2.报名详情中管理员通过该用户提交的报名申请；
		3.参与者可以被投票；
	"""
Background:
	Given jobs登录系统
	When jobs新建微信高级投票活动
		"""
		[{
			"title":"微信高级投票-进行中",
			"group":["初中组"],
			"desc":"高级投票活动介绍",
			"start_date":"2天前",
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
			"summary":"微信高级投票",
			"content":"微信高级投票",
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
					"reply_content":"微信高级投票",
					"reply_type":"text_picture"
				}]
		
		}]
		"""
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill参加高级投票报名活动
	"""
		[{
			"name":"bill",
			"group":["初中组"],
			"number":"001"
			"detail":"123456789"
		}]
	"""
	When dill关注jobs的公众号
	When dill访问jobs的webapp
	When dill参加高级投票报名活动
	"""
		[{
			"name":"dill",
			"group":["初中组"],
			"number":"002"
			"detail":"我好美"
		}]
	"""


@mall2 @apps @shvote @shvote_vote @we
Scenario:1 管理员查看选手详情
	Given jobs登录系统
	When jobs审核通过"bill"
	Then jobs获得'bill'的详情
		"""
		[{
			"player":"bill",
			"number":"001",
			"votes":0,
			"detail":"123456789"
		}]
		"""
@mall2 @apps @shvote @shvote_vote
Scenario:2 微信用户可以给参与者投票
	Given jobs登录系统
	When jobs审核通过'bill'
	When jobs审核通过'dill'
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级投票活动1单图文'
	When tom点击图文'高级投票活动1单图文'进入高级投票活动页面
	When tom在高级投票中为'bill'投票
	Then jobs获得微信高级投票活动排行榜列表
	"""
		[{
			"number":"001",
			"name":"bill",
			"votes":1
		},{
			"number":"002",
			"name":"dill",
			"votes":0
		}]
	"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"vote_count":1,
			"participant_count":2,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["删除","链接","预览","报名详情","查看结果"]
		}]
		"""
	When tom在高级投票中再次为'bill'投票
	Then jobs获得微信高级投票活动排行榜列表
	"""
		[{
			"number":"001",
			"name":"bill",
			"votes":1
		},{
			"number":"002",
			"name":"dill",
			"votes":0
		}]
	"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"vote_count":1,
			"participant_count":2,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""

	When guo访问jobs的webapp
	When guo在微信中向jobs的公众号发送消息'微信高级投票'
	Then guo收到自动回复'高级投票活动1单图文'
	When guo点击图文'高级投票活动1单图文'进入高级投票活动页面
	When guo在高级投票中为'bill'投票
	Then jobs获得微信高级投票活动排行榜列表
	"""
		[{
			"number":"001",
			"name":"bill",
			"votes":2
		},{
			"number":"002",
			"name":"dill",
			"votes":0
		}]
	"""
	Then jobs获得微信高级投票活动列表
		"""
		[{
			"name":"微信高级投票-进行中",
			"vote_count":2,
			"participant_count":2,
			"start_date":"2天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","报名详情","查看结果"]
		}]
		"""
	







