# __author__ : "崔帅帅"
@func:market_tools.tools.test_game.views.list_test_games
Feature: 修改趣味测试
	Jobs能通过管理系统修改"趣味测试"

Background:
	Given jobs登录系统
	And jobs已添加趣味测试
		"""
		[{
			"name": "测试1"
		}, {
			"name": "测试2"
		}, {
			"name": "测试3"
		}]
		"""

@weapp.market_tools.test_game
Scenario: 更新趣味测试
	jobs能更新单个趣味测试, 更新后, 排序不会被破坏

	Given jobs登录系统
	Then jobs能获取趣味测试列表
		"""
		[{
			"name": "测试3"
		}, {
			"name": "测试2"
		}, {
			"name": "测试1"
		}]
		"""
	When jobs更新趣味测试'测试2'
		"""
		{
			"name": "测试4",
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
		}
		"""
	Then jobs能获取趣味测试'测试4'
		"""
		{
			"name": "测试4"
		}
		"""
	And jobs能获取趣味测试列表
		"""
		[{
			"name": "测试3"
		}, {
			"name": "测试4"
		}, {
			"name": "测试1"
		}]
		"""