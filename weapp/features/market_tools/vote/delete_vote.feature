@func:market_tools.tools.vote.views.list_votes
Feature: Delete Vote
	Jobs能通过管理系统删除"微信投票"

Background:
	Given jobs登录系统
	And jobs已添加'微信投票'
		"""
		[{
			"name": "投票1"
		}, {
			"name": "投票2"
		}, {
			"name": "投票3"
		}]
		"""

@weapp.market_tools.vote @ignore
Scenario: 删除投票
	Jobs添加一组投票后, 能删除单个投票, 删除后, 排序不会被破坏

	Given jobs登录系统
	Then jobs能获取投票列表
		"""
		[{
			"name": "投票3"
		}, {
			"name": "投票2"
		}, {
			"name": "投票1"
		}]
		"""
	When jobs删除投票'投票2'
	Then jobs能获取投票列表
		"""
		[{
			"name": "投票3"
		}, {
			"name": "投票1"
		}]
		"""
	When jobs删除投票'投票3'
	When jobs删除投票'投票1'
	Then jobs能获取投票列表
		"""
		[]
		"""