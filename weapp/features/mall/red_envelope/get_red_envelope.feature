# __author__ : "崔帅帅"
@func:market_tools.tools.red_envelope.views.list_red_envelope
Feature: 获取红包
	Jobs下的会员能通过管理系统获取红包
	
Background:
	Given jobs登录系统
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券规则1",
			"money": 1,
			"expire_days": 1,
			"using_limit": "无限制"
		}]
		"""
	And jobs已添加微信红包
		"""
		[{
			"name": "微信红包",
			"prize_type|1": "1",
			"prize_source|1": "优惠券规则1"
		}]
		"""
	And bill关注jobs的公众号
 
@weapp.market_tools.red_envelope 
Scenario: 会员获取红包
	Jobs添加"微信红包"后，会员可获取红包

	Given jobs登录系统
	When bill访问jobs的webapp
	When bill参加微信红包'微信红包'
	   
	
