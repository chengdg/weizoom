#_author_:邓成龙 2016.04.12

Feature: 微信用户查看排行信息
	"""
		微信用户进入高级投票主页
		微信用户点击“排行”链接进入排行页面
		查看排行榜列表
	"""
Background:
	Given jobs登录系统
	When jobs新建微信高级投票活动
		"""
		[{
			"title":"微信高级投票-非会员参与",
			"rule":[{
				"content":"微信高级投票活动",
				"cycle":"daily",
				"vote_times":"1"
			}],
			"group":"初中组",
			"player_num":"报名输入",
			"desc":"高级投票活动介绍",
			"start_date":"今天",
			"end_date":"2天后",
			"pic":"1.jpg"
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
			"summary":"微信高级投票-非会员参与",
			"content":"微信高级投票-非会员参与",
			"jump_url":"微信高级投票-非会员参与"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": 
				[{
					"keyword": "微信高级投票-非会员参与",
					"type": "equal"
				}],
			"keyword_reply": 
				[{
					"reply_content":"微信高级投票-非会员参与",
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


@mall2 @apps @shvote @shvote_rank
Scenario:1 没有有微信用户报名参与活动和有微信用户报名参与活动，但是均未通过审核
	#选手分组-无分组
	Given jobs登录系统
	When jobs审核不通过'bill'
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'微信高级投票-非会员参与'
	Then bill收到自动回复'微信高级投票-非会员参与'
	When bill点击图文"微信高级投票-非会员参与"进入高级投票活动页面
	When bill参加高级投票报名活动
	Then bill获得微信高级投票活动排行榜列表
		"""
		[]
		"""

#@mall2 @apps @shvote @shvote_rank
#Scenario:2 有微信用户报名参与活动并通过审核
#	#选手分组-无分组
#	Given jobs登录系统
#	When jobs审核通过'bill'
#	When jobs审核通过'dill'
#	When bill关注jobs的公众号
#	When bill访问jobs的webapp
#	When bill在微信中向jobs的公众号发送消息'微信高级投票-非会员参与'
#	Then bill收到自动回复'微信高级投票-非会员参与'
#	When bill点击图文"微信高级投票-非会员参与"进入高级投票活动页面
#	When bill参加高级投票报名活动
#	Then bill获得微信高级投票活动排行榜列表
#		"""
#		[{
#			"group":"初中组",
#			"ranking":"1",
#			"player":"bill",
#			"num_vote":"10",
#			"num":"003"
#		},{
#			"group":"初中组",
#			"ranking":"2",
#			"player":"dill",
#			"num_vote":"9",
#			"num":"002"
#		}]
#		"""