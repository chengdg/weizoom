@func:market_tools.tools.vote.views.list_votes
Feature: Add Vote
	Jobs能通过管理系统添加"微信投票"

@weapp.market_tools.vote @ignore
Scenario: 添加"微信投票"
	Jobs添加"微信投票"后，能获取添加的投票，"微信投票"列表会按照添加的倒序排列

	Given jobs登录系统
	When jobs添加微信投票
		""" 
		[{
			"name": "投票1",
			"detail": "投票1内容详情",
			"is_non_member": "可参与",
			"show_style": "带图片",
			"prize_info": "积分,10",
			"vote_options": [{
				"name": "票项1a",
				"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
				"name": "票项1b",
				"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]		
		}, {
			"name": "投票2",
			"detail": "投票2内容详情",
			"is_non_member": "不可参与",
			"show_style": "不带图片",
			"prize_info": "实物奖励,小熊",
			"vote_options": [{
				"name": "票项2a"
			}]
		}]
		"""
	Then jobs能获取投票'投票1'
		"""
		{
			"name": "投票1",
			"detail": "投票1内容详情",
			"is_non_member": "可参与",
			"show_style": "带图片",
			"prize_info": "积分,10",
			"vote_options": [{
				"name": "票项1a",
				"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
				"name": "票项1b",
				"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""
	And jobs能获取投票'投票2'
		"""
		{
			"name": "投票2",
			"detail": "投票2内容详情",
			"is_non_member": "不可参与",
			"show_style": "不带图片",
			"prize_info": "实物奖励,小熊",
			"vote_options": [{
				"name": "票项2a"
			}]
		}
		"""
	And jobs能获取投票列表
		"""
		[{
			"name": "投票2"
		}, {
			"name": "投票1"
		}]
		"""
	And bill能获取投票列表
		"""
		[]
		"""


