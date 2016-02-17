#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

@func:market_tools.tools.activity.views.list_activities
Feature: Add Activity
	Jobs能通过管理系统添加"活动报名"

@weapp.market_tools.activity
Scenario: 添加活动报名
	Jobs添加"活动报名"后，能获取他参加的活动，"活动报名"列表会按照添加的倒序排列

	Given jobs登录系统
	When jobs添加活动报名
		""" 
		[{
			"name": "活动报名",
			"start_date": "2014-06-16",
			"end_date": "2014-06-19",	
			"detail": "<p>343434<br/></p>",
			"is_non_member": "非会员可参与",
			"is_enable_offline_sign": "启用线下签到",
			"prize_source": "500",
			"prize_type": "3",
			"item_text_data_100000": "",
			"item_text_data_99999": "",	
			"item_text_mandatory_100000": "必填",
			"item_text_mandatory_99999": "必填",
			"item_text_title_100000": "手机号",
			"item_text_title_99999": "姓名"
		}]
		"""
	Then jobs能获取活动列表
		"""
		[{
			"name": "活动报名"
		}]
		"""
	And bill能获取活动列表
		"""
		[]
		"""
		
		
