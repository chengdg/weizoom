# __author__ : "崔帅帅"
@func:market_tools.tools.test_game.views.list_test_games
Feature: 删除趣味测试
	Jobs能通过管理系统删除"趣味测试"

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

@weapp.market_tools.test_game @ignore
Scenario: 删除趣味测试
	jobs能删除单个趣味测试, 删除后, 排序不会被破坏

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
	When jobs删除趣味测试'测试2'
	Then jobs能获取趣味测试列表
		"""
		[{
			"name": "测试3"
		}, {
			"name": "测试1"
		}]
		"""
	When jobs删除趣味测试'测试3'
	When jobs删除趣味测试'测试1'
	Then jobs能获取趣味测试列表
		"""
		[]
		"""