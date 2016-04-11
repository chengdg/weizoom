#_author_:许韦 2016.04.07

Feature: 在卡订单页面对订单中微众卡执行批量卡激活操作
"""
	微众卡管理员创建微众卡规则
	微众卡管理员审核发卡，创建发卡订单
	微众卡管理员在发卡订单列表对订单中的卡执行批量激活
"""

Background:
	Given test登录系统
	When test新建通用卡
		"""
		[{
			"name":"",
			"money":"10.00"
		}]
		"""
	And test新建限制卡
		"""
		[{
			"name":"测试卡1"
		}]
		"""
	And test下订单
		"""
		[{
			"card_info":[{
				"name":"测试卡1"
			},{
				"name":"10元卡"
			}],
			"order_info":[{
				"order_id":"1"
				}]
		}]
		"""
		
@weizoom_card @card_option
Scenario: 1.批量激活卡操作
	When test登录管理系统
	Then 'test'能获得订单列表
		"""
		[{
			"order_id":"1",
			"status":"未激活"
		}]
		"""
	When 'test'批量激活订单'1'的卡
	Then 'test'能获得订单列表
		"""
		[{
			"order_id":"1",
			"status":"已激活"
		}]
		"""

@weizoom_card @card_option
Scenario: 2.批量停用卡操作
	When test登录管理系统
	And test批量激活订单'1'的卡
	Then 'test'能获得订单列表
		"""
		[{
			"order_id":"1",
			"status":"已激活"
		}]
		"""
	When 'test'批量停用订单'1'的卡
	Then 'test'能获得订单列表
		"""
		[{
			"order_id":"1",
			"status":"未激活"
		}]
		"""

@weizoom_card @card_option
Scenario: 3.取消订单卡操作
	When test登录管理系统
	Then 'test'能获得订单列表
		"""
		[{
			"order_id":"1",
			"status":"未激活"
		}]
		"""
	When 'test'取消订单'1'
	Then 'test'能获得订单列表
		"""
		[{
			"order_id":"1",
			"status":"已取消"
		}]
		"""

	

		


