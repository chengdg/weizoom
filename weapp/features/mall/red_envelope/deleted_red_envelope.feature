# __author__ : "崔帅帅"
@func:market_tools.tools.red_envelope.views.list_red_envelope
Feature: 删除红包
	Jobs能通过管理系统删除"微信红包"
	
Background:
	Given jobs登录系统
	And jobs已添加微信红包
		"""
		[{
			"name": "微信红包1"
		}, {
			"name": "微信红包2"
		}, {
			"name": "微信红包3"
		}]
		"""

@weapp.market_tools.red_envelope
Scenario: 删除微信红包
	Jobs删除"微信红包"后，能获取他的微信红包，"微信红包"列表会按照添加的顺序倒序排列

	Given jobs登录系统
	Then jobs能获取红包列表
		"""
		[{
			"name": "微信红包3"
		}, {
			"name": "微信红包2"
		}, {
			"name": "微信红包1"
		}]
		"""
	When jobs删除微信红包'微信红包1'
	Then jobs能获取红包列表
		"""
		[{
			"name": "微信红包3"
		}, {
			"name": "微信红包2"
		}]
		"""
	When jobs删除微信红包'微信红包2'
	Then jobs能获取红包列表
		"""
		[{
			"name": "微信红包3"
		}]
		"""
	When jobs删除微信红包'微信红包3'
	Then jobs能获取红包列表
		"""
		[]
		"""
		
		
