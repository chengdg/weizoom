# __author__ : "崔帅帅"
@func:market_tools.tools.test_game.views.list_test_games
Feature: 添加趣味测试
	jobs能通过管理系统添加"趣味测试"

@weapp.market_tools.test_game
Scenario: 添加"趣味测试"
	jobs添加"趣味测试"后，能获取添加的测试配置，"趣味测试"列表会按照添加的倒序排列

	Given jobs登录系统
	When jobs添加趣味测试
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
		}, {
			"name": "测试2",
			"background_pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"is_non_member": "非会员可参与",
			"prize_info": "优惠券,10元",
			"questions": [{
				"name": "问题1",
				"index": "1",
				"answers": [{
					"index": "A",
					"name": "问题1的答案1",
					"score": "1"
				},{
					"index": "B",
					"name": "问题1的答案2",
					"score": "3"
				}]
			},{
				"name": "问题2",
				"index": "2",
				"answers": [{
					"index": "A",
					"name": "问题2的答案1",
					"score": "0"
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
	Then jobs能获取趣味测试'测试1'
		"""
		{
			"name": "测试1"
		}
		"""
	And jobs能获取趣味测试'测试2'
		"""
		{
			"name": "测试2"
		}
		"""
	And jobs能获取趣味测试列表
		"""
		[{
			"name": "测试2"
		}, {
			"name": "测试1"
		}]
		"""
	And bill能获取趣味测试列表
		"""
		[]
		"""
