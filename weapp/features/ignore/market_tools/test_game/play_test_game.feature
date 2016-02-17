#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

@func:market_tools.tools.test_game.views.list_test_games
Feature: 参与趣味测试
	微信用户能通过微信参与"趣味测试"

@weapp.market_tools.test_game.d @ignore
Scenario: 参与"趣味测试"
	jobs添加"趣味测试"后，微信用户可以参与"趣味测试"

	Given jobs已添加趣味测试
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
	And jobs已有会员
		"""
		[{
			"name": "会员"
		}]
		"""
	And 微信用户
		"""
		[{
			"name": "非会员"
		}]
		"""
	
	When "非会员"参与趣味测试"测试1"
		"""
		{
			"answers": [{
				"answer": "A"
			},{
				"answer": "B"
			}]
		}
		"""
	Then "非会员"得到评价"评价1"
		"""
		{
			"result": "评价1",
			"prize_info": "没有奖励"
		}
		"""
		
	When "会员"参与趣味测试"测试2"
		"""
		{
			"answers": [{
				"answer": "B"
			},{
				"answer": "B"
			}]
		}
		"""
	Then "会员"得到评价"评价2"
		"""
		{
			"result": "评价2",
			"prize_info": "优惠券,10元"
		}
		"""
	
