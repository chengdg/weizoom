#_author_:邓成龙 2016.04.11

Feature: 浏览订单中的卡详情
"""
	微众卡管理员创建微众卡规则
	微众卡管理员审核发卡，创建发卡订单
	微众卡管理员在发卡订单列表对订单中的卡执行批量激活
	微众卡管理员点击订单编号进入订单详情页面选择其中一个卡规则，列表展示订单中该组卡规则的详情信息
"""

Background:
	Given test登录管理系统
	When test新建通用卡
		"""
		[{
			"prefix_value":"999",
			"type":"virtual",
			"money":"10.00",
			"num":"5"
		}]
		"""
	And test新建限制卡
		"""
		[{
			"name":"测试卡1",
			"prefix_value":"777",
			"type":"condition",
			"use_limit":{
					"is_limit":"off"
			},
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
			"order_info":{
				"order_attribute":"发售卡",
				"company":"a",
				"reponsible_person":"b",
				"contact":"025-6623558",
				"sale_name":"c",
				"sale_department":"南京分公司",
				"comments":""
				}
		}]
		"""
	
@weizoom_card @order_card

Scenario: 1.查看订单详情
	Given test登录管理系统
	Then test能获得订单详情列表
		"""
		[{
			"name":"测试卡1",
			"money":"10.00",
			"num":"2",
			"total_money":"20.00",
			"type":"condition",
			"use_limit":{
					"is_limit":"off"
			},
			"card_range":"777000001-777000010"
		},{
			"name":"10元卡",
			"money":"10.00",
			"num":"5",
			"total_money":"50.00",
			"type":"virtual",
			"card_range":"999000001-999000010"
		}]
		"""	
	Then test能获得'测试卡1'微众卡列表
		"""
		[{
			"name":"测试卡1"，
			"status":"未激活",
			"money":"10.00",
			"rest_money":"10.00",
			"start_date":"2016-04-07",
			"end_date":"2016-10-07",
			"comments":""
		},{
			"name":"测试卡1"，
			"status":"未激活",
			"money":"10.00",
			"start_date":"2016-04-07",
			"end_date":"2016-10-07",
			"comments":""
		}]
		"""
