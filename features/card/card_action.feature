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
			"card_name":"",
			"prefix_value":"999",
			"type":"virtual",
			"money":"10.00",
			"num":"5",
			"comments":""
		}]
		"""
	And test新建限制卡
		"""
		[{
			"name":"测试卡1",
			"prefix_value":"777",
			"type":"condition",
			"use_limit":[{
					"is_limit":"off"
			}],
			"money":"10.00",
			"num":"10",
			"comments":""
		}]
		"""
	And test下订单
		"""
		[{
			"card_info":[{
				"name":"测试卡1",
				"order_num":"10",
				"start_date":"2016-04-07",
				"end_date":"2016-10-07"
			},{
				"name":"10元卡",
				"order_num":"5",
				"start_date":"2016-05-01",
				"end_date":"2016-08-01"
			}],
			"order_info":[{
				"order_attribute":"发售卡",
				"company":"a",
				"reponsible_person":"b",
				"contact":"025-6623558",
				"sale_name":"c",
				"sale_department":"南京分公司",
				"comments":""
				}]
		}]
		"""
		
@weizoom_card @card_option
Scenario: 1.批量激活卡操作
	When test登录管理系统
	Then 'test'能获得订单"2016040810001"列表
		"""
		[{
			"card_info":[{
				"name":"测试卡1"，
				"money":"10.00",
				"num":"10",
				"total_money":"100.00",
				"type":"条件卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"777000001-777000010"
			},{
				"name":"10元卡"，
				"money":"10.00",
				"num":"5",
				"total_money":"50.00",
				"type":"电子卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"999000001-999000005"
			}],
			"order_attribute":"发售卡",
			"apply_person":"b",
			"apply_department":"a",
			"action":["卡激活","编辑订单","取消订单","备注"],
			"order_money":"150.00",
			"real_pay":"150.00"
		}]
		"""
	When 'test'批量激活订单"2016040810001"卡片
	Then 'test'能获得订单'2016040810001'状态变更
		"""
		[{
			"card_info":[{
				"name":"测试卡1"，
				"money":"10.00",
				"num":"10",
				"total_money":"100.00",
				"type":"条件卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"777000001-777000010"
			},{
				"name":"10元卡"，
				"money":"10.00",
				"num":"5",
				"total_money":"50.00",
				"type":"电子卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"999000001-999000005"
			}]
			"order_attribute":"发售卡",
			"apply_person":"b",
			"apply_department":"a",
			"action":["卡停用","编辑订单","取消订单","备注"],
			"order_money":"150.00",
			"real_pay":"150.00"
		}]
		"""

@weizoom_card @card_option
Scenario: 2.批量停用卡操作
	When test登录管理系统
	And test批量激活订单"2016040810001"卡片
	Then 'test'能获得订单'2016040810001'状态变更
		"""
		[{
			"card_info":[{
				"name":"测试卡1"，
				"money":"10.00",
				"num":"10",
				"total_money":"100.00",
				"type":"条件卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"777000001-777000010"
			},{
				"name":"10元卡"，
				"money":"10.00",
				"num":"5",
				"total_money":"50.00",
				"type":"电子卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"999000001-999000005"
			}],
			"order_attribute":"发售卡",
			"apply_person":"b",
			"apply_department":"a",
			"action":["卡停用","编辑订单","取消订单","备注"],
			"order_money":"150.00",
			"real_pay":"150.00"
		}]
		"""
	When 'test'批量停用订单"2016040810001"卡片
	Then 'test'能获得订单'2016040810001'状态更新
		"""
		[{
			"card_info":[{
				"name":"测试卡1"，
				"money":"10.00",
				"num":"10",
				"total_money":"100.00",
				"type":"条件卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"777000001-777000010"
			},{
				"name":"10元卡"，
				"money":"10.00",
				"num":"5",
				"total_money":"50.00",
				"type":"电子卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"999000001-999000005"
			}],
			"order_attribute":"发售卡",
			"apply_person":"b",
			"apply_department":"a",
			"action":["卡激活","编辑订单","取消订单","备注"],
			"order_money":"150.00",
			"real_pay":"150.00"
		}]
		"""

@weizoom_card @card_option
Scenario: 3.取消订单卡操作
	When test登录管理系统
	Then 'test'能获得订单"2016040810001"列表
		"""
		[{
			"card_info":[{
				"name":"测试卡1"，
				"money":"10.00",
				"num":"10",
				"total_money":"100.00",
				"type":"条件卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"777000001-777000010"
			},{
				"name":"10元卡"，
				"money":"10.00",
				"num":"5",
				"total_money":"50.00",
				"type":"电子卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"999000001-999000005"
			}],
			"order_attribute":"发售卡",
			"apply_person":"b",
			"apply_department":"a",
			"action":["卡激活","编辑订单","取消订单","备注"],
			"order_money":"150.00",
			"real_pay":"150.00"
		}]
		"""
	When 'test'取消订单"2016040810001"
	Then 'test'能获得订单'2016040810001'状态更新
		"""
		[{
			"card_info":[{
				"name":"测试卡1"，
				"money":"10.00",
				"num":"10",
				"total_money":"100.00",
				"type":"条件卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"777000001-777000010"
			},{
				"name":"10元卡"，
				"money":"10.00",
				"num":"5",
				"total_money":"50.00",
				"type":"电子卡",
				"is_limit":"不限制",
				"vip_shop":"",
				"card_range":"999000001-999000005"
			}],
			"order_attribute":"发售卡",
			"apply_person":"b",
			"apply_department":"a",
			"action":["编辑订单","备注"],
			"order_money":"150.00",
			"real_pay":"150.00"
		}]
		"""

	

		


