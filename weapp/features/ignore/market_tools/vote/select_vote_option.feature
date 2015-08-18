@func:market_tools.tools.vote.views.list_votes
Feature: Select Vote Option
	Jobs能通过管理系统查看"微信投票"的投票票项统计，并按投票项的投票数量倒序排序

Background:
	Given jobs登录系统
	And jobs已添加'微信投票'
		"""
		[{
			"name": "娃娃笑",
			"detail": "娃娃笑内容详情",
			"is_non_member": "可参与",
			"show_style": "带图片",
			"prize_info": "积分,10",
			"vote_options": [{
				"name": "票项a",
				"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
				"name": "票项b",
				"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}]
		"""
	And jobs已添加会员
		"""
		[{
			"name": "樱桃小丸子"
		}]
		"""

@weapp.market_tools.vote @vote.option
Scenario: 查询"微信投票"的投票票项统计
	会员"樱桃小丸子"在"娃娃笑"中的"票项b"项投票后，能按照票项投票数量倒序排序

	Given jobs登录系统
	Then jobs查询微信投票'娃娃笑'的票项统计
		"""
		[{
			"name": "票项a",
			"count": 0
		},{
            "name": "票项b",
            "count": 0
        }]
		"""

	When 会员'樱桃小丸子'在'娃娃笑'中的'票项b'项投票
	Then jobs查询微信投票'娃娃笑'的票项统计
		"""
		[{
			"name": "票项b",
			"count": 1
		},{
            "name": "票项a",
            "count": 0
        }]
		"""
