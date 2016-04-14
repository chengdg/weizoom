#_author_:邓成龙 2016.04.13

Feature: 微信用户搜索选手
	"""
		微信用户进入投票活动主页
		微信用户输入关键词搜索选手
		选手列表中展示名字包含关键词与编号包含关键词的选手信息，按照得票数由高到底排列
	"""
Background:
	Given jobs登录系统
	When jobs新建微信高级投票活动
		When jobs新建微信高级投票活动
		"""
		[{
			"title":"微信高级投票-进行中",
			"group":["初中组","高中组"],
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
		{
			"name":"bill",
			"group":"初中组",
			"number":"003"	
		}
	"""
	When dill关注jobs的公众号
	When dill访问jobs的webapp
	When dill参加高级投票报名活动
	"""
		{
			"name":"dill",
			"group":"初中组",
			"number":"002"	
		}
	"""


@mall2 @apps @shvote @shvote_top
Scenario:1 微信用户搜索选手
		#模糊查询
	Given jobs登录系统
	When jobs审核通过'bill'
	When jobs审核通过'dill'
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom在微信中向jobs的公众号发送消息'微信高级投票'
	Then tom收到自动回复'高级投票活动1单图文'
	When tom点击图文'高级投票活动1单图文'进入高级投票活动页面
	When tom在高级投票中为'bill'投票
	Then tom获得微信高级投票活动内容
	When tom搜索选手'dill'
	Then tom获得微信高级投票活动排行榜列表
		"""
		[{
			"group":"初中组",
			"ranking":2,
			"number":"002",
			"player":"dill",
			"votes":0
		}]
		"""
	When tom搜索选手'ill'
	Then tom获得微信高级投票活动排行榜列表
		"""
		[{
			"group":"初中组",
			"ranking":1,
			"number":"003",
			"player":"bill",
			"votes":1
		},{
			"group":"初中组",
			"ranking":2,
			"number":"002",
			"player":"dill",
			"votes":0
		}]
		"""
	When tom搜索选手'tom'
	Then tom获得微信高级投票活动排行榜列表
		"""
		[]
		"""
	
