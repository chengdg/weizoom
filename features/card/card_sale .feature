#_author_:张雪 2016.4.6
Feature:微众卡管理员发放微众卡
"""
	微众卡管理员账号审批发卡，下订单
	1.微众卡管理员账号在系统中发放发售卡
		【卡名称】：必填项；
		【选择卡库】：弹出弹窗，选择通用卡或者限制卡；选择相应面值的卡；
		【出库数量】：大于0的正整数，取库存数量；
		【有效期】：有效期可以设置成不以当前为开始时间，开始时间必须晚于当前系统时间，结束时间必须晚于开始时间；
		【添加卡库】：添加一批卡次，不限制添加批次；
		【订单属性】：为必选项，选择其中一种卡属性；
		【客户企业信息】：为必填项，最多可输入XX个字符；
		【客户联系方式】：为必填项，最多可输入XX个字符；
		【销售员姓名】:为必填项，最多可输入XX个字符；
		【销售部分】为必填项，最多可输入XX个字符；
		【备注】：非必填项，最多可输入XX个字符；

		"""
Background:
	Given test登录管理系统
	When  test新建通用卡
	"""
		[{
			"name":"",
			"prefix_value":"000",
			"type":"entity",
			"money":"10.00",
			"num":"5",
			"comments":""
		},{
			"name":"微众卡",
			"prefix_value":"010",
			"type":"virtual",
			"money":"10.00",
			"num":"10",
			"comments":"微众卡"
		}]

		"""	
	And test新建限制卡
		"""
		[{
			"name":"测试卡1",
			"prefix_value":"020",
			"type":"condition",
			"use_limit":{
				"is_limit":"off"
			},
			"money":"10.00",
			"num":"5",
			"comments":""
		},{
			"name":"测试卡2",
			"prefix_value":"030",			
			"type":"condition",
			"use_limit":{
				"is_limit":"on",
				"limit_money":"50"
			},
			"money":"10.00",
			"num":"10",
			"comments":""
		}]
		"""


@weizoom_card @card_order
Scenario:1.发放发售卡
        #发放通用卡
	Given test登录管理系统
	When test下订单
	"""
	[{
		"card_info":[{
			"name":"10元卡",
			"order_num":"3",
			"start_date":"2016-04-07",
			"end_date":"2016-10-07"
		},{
			"name":"微众卡",
			"order_num":"3",
			"start_date":"2016-04-07",
			"end_date":"2016-10-07"
		}],
		"order_info":[{
			"order_attribute":"发售卡",
			"company":"南京纳容",
			"responsible_person":"纳容",
			"contact":"025-6623558",
			"sale_name":"土小宝",
			"sale_deparment":"碧根果部门",
			"comments":""
			}]
	}]
	"""
	Then 'test'能获得订单列表
	"""
	[{
		"card_info":[{
			"name":"10元卡",
			"money":"10.00",
			"num":"3",
			"total_money":"30.00",
			"type":"实体卡",
			"is_limit":"不限制",
			"vip_shop":"",
			"card_range":"000000001-000000003",
		},{
			"name":"微众卡",
			"money":"10.00",
			"num":"3",
			"total_money":"30.00",
			"type":"电子卡",
			"is_limit":"不限制",
			"vip_shop":"",
			"card_range":"010000001-010000003"
		}]
		"order_attribute ":"发售卡",
		"apply_person":"纳容",
		"apply_department":"南京纳容",
		"order_money":"60.00",
		"real_pay":"60.00"
	}]
	"""
	Then 'test'能获得通用卡'10元卡'的库存列表
	
		| card_number |status| money |rest_money|comments|apply_person|apply_department| 
		|  000000001  |已出库| 10.00 |  10.00   |        |    纳容    |    南京纳容    |
		|  000000002  |已出库| 10.00 |  10.00   |        |    纳容    |    南京纳容    |
		|  000000003  |已出库| 10.00 |  10.00   |        |    纳容    |    南京纳容    |
		|  000000004  |待出库| 10.00 |  10.00   |        |    纳容    |    南京纳容    |
		|  000000005  |待出库| 10.00 |  10.00   |        |    纳容    |    南京纳容    |
	Then 'test'能获得通用卡'微众卡'库存列表
		| card_number  |status| money |rest_money|comments|apply_person|apply_department| 
		|  010000001   |已出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
		|  010000002   |已出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
		|  010000003   |已出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
		|  010000004   |待出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
		|  010000005   |待出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
		|  010000006   |待出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
		|  010000007   |待出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
		|  010000008   |待出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
		|  010000009   |待出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
		|  010000010   |待出库| 10.00 |  10.00   |        |   纳容     |    南京纳容    |
				



		            																 

@weizoom_card @card_order
Scenario:2.发放发售卡
        #发放限制卡
	Given test登录系统
	When test下订单
	"""
	[{
		"card_info":[{
			"name":"测试卡1",
			"order_num":"3",
			"start_date":"2016-04-07",
			"end_date":"2016-10-07"
		},{
			"name":"测试卡2",
			"order_num":"3",
			"start_date":"2016-04-07",
			"end_date":"2016-10-07"
		}],
		order_info:[{
			"order_attribute":"发售卡",
			"company":"北京微众",
			"responsible_person":"微众",
			"contact":"025-6623558",
			"sale_name":"爱昵咖啡",
			"sale_deparment":"咖啡部门",
			"comments":""
		}]		
	}]
	"""
	Then 'test'能获得订单列表
	"""
	[{
		"card_info":[{
			"name":"测试卡1",
			"money":"10.00",
			"num":"3",
			"total_money":"30.00",
			"type":"条件卡",
			"is_limit":"不限制",
			"vip_shop":"",
			"card_range":"020000001-020000003"
		},{
			"name":"测试卡2",
			"money":"10.00",
			"num":"3",
			"total_money":"30.00",
			"type":"条件卡",
			"limit_money":"满50使用",
			"vip_shop":"",
			"card_range":"030000001-030000003"
		}]
			"order_attribute":"发售卡",
			"apply_person":"微众",
			"apply_department":"北京微众",
			"order_money":"60.00",
			"real_pay":"60.00"
	}]
	"""
	Then 'test'能获得限制卡'测试卡1'的库存列表
	
		| card_number  |status| money |rest_money|comments|apply_person|apply_department| 
		|  020000001   |已出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  020000002   |已出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  020000003   |已出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  020000004   |待出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  020000005   |待出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
	Then 'test'能获得限制卡'测试卡2'的库存列表
		| card_number  |status| money |rest_money|comments|apply_person|apply_department| 
		|  030000001   |已出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  030000002   |已出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  030000003   |已出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  030000004   |待出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  030000005   |待出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  030000006   |待出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  030000007   |待出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  030000008   |待出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  030000009   |待出库| 10.00 |  10.00   |        |    微众    |    北京微众    |
		|  030000010   |待出库| 10.00 |  10.00   |        |    微众    |    北京微众    | 

		