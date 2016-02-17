#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

@func:market_tools.tools.test_game.views.list_test_games
Feature: 再次参加趣味测试
	Jobs下的会员能通过管理系统多次参加趣味测试
	
Background:
	Given jobs登录系统
	And jobs已添加趣味测试
		"""
		[{
			"name": "测试1",
			"background_pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"is_non_member": "非会员可参与",
			"prize_info": "积分,10",
			"questions": [{
				"name": "问题1",
				"index": "1",
				"answers": [{
					"index": "A",
					"name": "问题1的答案1",
					"score": "0"
				},{
					"index": "B",
					"name": "问题1的答案2",
					"score": "5"
				}]
			},{
				"name": "问题2",
				"index": "2",
				"answers": [{
					"index": "A",
					"name": "问题2的答案1",
					"score": "2"
				},{
					"index": "B",
					"name": "问题2的答案2",
					"score": "5"
				}]
			}],
			"results": [{
				"index": "1",
				"title": "评价1",
				"range": "0-5",
				"detail": "评价详情"
			},{
				"index": "2",
				"title": "评价2",
				"range": "6-10",
				"detail": "评价详情"
			}]
		}]
		"""
	And bill关注jobs的公众号
	# And bill的积分信息
		# """
		# [{
			# "integral": "20"
		# }]
		# """
 
@weapp.market_tools.test_game.a
Scenario: 可再次参加趣味测试
	Jobs添加"趣味测试"后，微信用户参加完一次后，可再次参加。只是除了第一次参加获取奖励外，其它的都不会有奖励。

	When bill访问jobs的webapp
	When bill参加趣味测试'测试1'
	# Then bill的积分信息
	#	"""
		# [{
			# "integral": "30"
		# }]
		# """
	When bill再次参加营销工具趣味测试'测试1'
	# Then bill的积分信息
	#	"""
		# [{
			# "integral": "30"
		# }]
		# """
