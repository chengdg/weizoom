#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
@func:market_tools.tools.vote.views.list_votes
Feature: update Vote
	Jobs能通过管理系统更新"微信投票"

Background:
	Given jobs登录系统
	And jobs已添加'微信投票'
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

@weapp.market_tools.vote @ignore
Scenario: 更新"微信投票"
	Jobs更新"微信投票"后，能获取更新的投票，并且更改后列表排序不变

	Given jobs登录系统
	When jobs更新微信投票'投票1'
		"""
		{
			"name": "投票3",
			"detail": "投票3内容详情",
			"is_non_member": "不可参与",
			"show_style": "带图片",
			"prize_info": "积分,10",
			"vote_options": [{
				"old_name": "票项1a",
				"name": "票项3a",
				"pic_url": "/standard_static/test_resource_img/hangzhou3.jpg"
			},{
				"old_name": "票项1b",
				"name": "票项3b",
				"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg"
			},{
				"name": "票项3c",
				"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}]
		}
		"""
	And jobs更新微信投票'投票2'
		"""
		{
			"name": "投票4",
			"detail": "投票4内容详情",
			"is_non_member": "可参与",
			"show_style": "不带图片",
			"prize_info": "无奖励",
			"vote_options": [{
				"name": "票项4a"
			},{
	            "name": "票项4c"
	        }]
		}
		"""
	Then jobs能获取投票'投票3'
		"""
		{
			"name": "投票3",
			"detail": "投票3内容详情",
			"is_non_member": "不可参与",
			"show_style": "带图片",
			"prize_info": "积分,10",
			"vote_options": [{
				"name": "票项3a",
				"pic_url": "/standard_static/test_resource_img/hangzhou3.jpg"
			},{
				"name": "票项3b",
				"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg"
			},{
				"name": "票项3c",
				"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}]
		}
		"""
	And jobs能获取投票'投票4'
		"""
		{
			"name": "投票4",
			"detail": "投票4内容详情",
			"is_non_member": "可参与",
			"show_style": "不带图片",
			"prize_info": "无奖励",
			"vote_options": [{
				"name": "票项4a"
			},{
	            "name": "票项4c"
	        }]
		}
		"""
	And jobs能获取投票列表
		"""
		[{
			"name": "投票4"
		}, {
			"name": "投票3"
		}]
		"""
	And bill能获取投票列表
		"""
		[]
		"""


