#_author_:邓成龙 2016.04.13

Feature: 查看三维数据
	"""
		微信用户进入高级投票主页
	"""
Background:
	Given jobs登录系统
	When jobs新建高级微信投票活动
		"""
		[{
			"title":"微信高级投票-进行中",
			"groups":["初中组","高中组"],
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
#	When bill参加高级投票报名活动
#	"""
#		{
#			"name":"bill",
#			"group":"初中组",
#			"number":"003"
#		}
#	"""
#	When dill关注jobs的公众号
#	When dill访问jobs的webapp
#	When dill参加高级投票报名活动
#	"""
#		{
#			"name":"dill",
#			"group":"高中组",
#			"number":"002"
#		}
#	"""

@mall2 @apps @shvote @shvote_top
Scenario:1 微信用户浏览高级投票活动主页
	Given jobs登录系统
#	When jobs审核通过'bill'
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票'
	Then bill收到自动回复'高级投票活动1单图文'
	When bill点击图文'高级投票活动1单图文'进入高级投票活动首页面
	Then bill获得微信高级投票活动内容
		"""
		{
			"participant_count":2,
			"vote_count":0,
			"visit_num":2,
			"end_date":"2天后"
		}
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级投票活动1单图文'
	When tom点击图文'高级投票活动1单图文'进入高级投票活动页面
	When tom在高级投票中为'bill'投票
	Then tom获得微信高级投票活动内容
		"""
		{
			"participant_count":2,
			"vote_count":1,
			"visit_num":3,
			"end_date":"2天后"
		}
		"""
	When jobs删除'dill'
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级投票活动1单图文'
	When tom点击图文'高级投票活动1单图文'进入高级投票活动页面
	When tom在高级投票中为'bill'投票
	Then tom获得微信高级投票活动内容
		"""
		{
			"participant_count":1,
			"vote_count":1,
			"visit_num":4,
			"end_date":"2天后"
		}
		"""