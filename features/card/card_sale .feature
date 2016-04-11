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
			"name":"测试卡",
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
			"comments":"weizoom"
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




@weizoom_card @card_order @hj
Scenario:1.发放发售卡
        #发放通用卡和限制卡
	Given test登录管理系统
	When test下订单
	"""
	[{
		"card_info":[{
			"name":"测试卡",
			"order_num":"4",
			"start_date":"2016-04-07 00:00",
			"end_date":"2016-10-07 00:00"
		},{
			"name":"测试卡1",
			"order_num":"5",
			"start_date":"2016-04-07 00:00",
			"end_date":"2016-10-07 00:00"
		}],
		"order_info":{
			"order_attribute":"发售卡",
			"company":"窝夫小子",
			"responsible_person":"研发",
			"contact":"025-6623558",
			"sale_name":"姜晓明",
			"sale_deparment":"销售",
			"comments":""
		}
	}]
	"""
	Then test能获得订单列表
	"""
	[{
		"card_info":[{
			"name":"10元卡",
			"money":"10.00",
			"num":"4",
			"total_money":"40.00",
			"type":"实体卡",
			"is_limit":"不限制",
			"vip_shop":"",
			"card_range":"000000001-000000004"
		},{
			"name":"测试卡1",
			"money":"10.00",
			"num":"5",
			"total_money":"50.00",
			"type":"条件卡",
			"limit_money":"不限制",
			"vip_shop":"",
			"card_range":"020000001-020000005"
		}],
			"order_attribute":"发售卡",
			"apply_person":"研发",
			"apply_department":"窝夫小子",
			"order_money":"90.00",
			"real_pay":"90.00"
	}]
	"""
	Then test能获得通用卡'10元卡'的库存列表
	
		| card_number  |status| money |rest_money|comments|apply_person|apply_department| 
		|  000000001   |已出库| 10.00 |  10.00   | 微众卡 |    研发    |    窝夫小子    |
		|  000000002   |已出库| 10.00 |  10.00   | 微众卡 |    研发    |    窝夫小子    |
		|  000000003   |已出库| 10.00 |  10.00   | 微众卡 |    研发    |    窝夫小子    |
		|  000000004   |已出库| 10.00 |  10.00   | 微众卡 |    研发    |    窝夫小子    |
		|  000000005   |待出库| 10.00 |  10.00   | 微众卡 |    研发    |    窝夫小子    |
	Then test能获得限制卡'测试卡1'的库存列表
		| card_number  |status| money |rest_money|comments|apply_person|apply_department| 
		|  020000001   |已出库| 10.00 |  10.00   | weizoom|    研发    |    窝夫小子    |
		|  020000002   |已出库| 10.00 |  10.00   | weizoom|    研发    |    窝夫小子    |
		|  020000003   |已出库| 10.00 |  10.00   | weizoom|    研发    |    窝夫小子    |
		|  020000004   |已出库| 10.00 |  10.00   | weizoom|    研发    |    窝夫小子    |
		|  020000005   |已出库| 10.00 |  10.00   | weizoom|    研发    |    窝夫小子    |
		


@weizoom_card @card_order
Scenario:2.创建多条订单，按创建订单时间倒序排列
	When test下订单
	"""
	[{
		"card_info":[{
			"name":"10元卡"
		},{
			"name":"测试卡1"
		}],
		order_info:[{
			"order_id":"1"
		}]		
	},{

		"card_info":[{
			"name":"微众卡"
		},{
			"name":"测试卡2"
		}],
		order_info:[{
			"order_id":"2"
		}]
	}]
	"""
	Then test能获得订单列表
	"""
	[{
		"order_id":"2"
	},{
		"order_id":"1"
	}]
	"""
