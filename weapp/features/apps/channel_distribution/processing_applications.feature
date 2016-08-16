#author: 邓成龙 2016-08-02

Feature:分销会员结算页返现状态转换
"""
		1.无状态,默认状态,没有申请的时候
		2.正在返现中,当前台用户申请返现时
		3.已完成/切换为无状态,管理返现完成时切换到当前状态,系统自动转为无状态
		4.最低返现折扣若设置为80，则商品在优惠的价格在80%以下不参与返佣金
		5.整体概况(包括已返现总额:所有已返现金额；未返现总金额：目前未返现的金额；总交易额：所有的交易流水额。)
		6.会员结算列表查询
			按返现金额查询:(1)满足(2)未满足
			按提交时间查询:(1)满足(2)未满足
			混合查询
		7.上一期未完成,微信用户扫码下单返现的整体概况和分销会员列表
"""

Background:
	Given jobs登录系统

	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": "无限",
			"using_limit": "满200元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "优惠券00",
			"money": 50.00,
			"count": 3,
			"limit_counts": "无限",
			"using_limit": "满1元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1"
		}
		"""
	And jobs已添加多图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"单条图文1文本内容"
		}]
		"""
	And bigs关注jobs的公众号于'2015-10-01 10:00:00'
	And bill关注jobs的公众号于'2015-10-02 10:00:00'
	Given jobs登录系统
	When jobs新建渠道分销二维码
		"""
		[{
			"code_name": "分销二维码1",
			"relation_member": "bigs",
			"distribution_prize_type": "佣金",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":50.00,
			"settlement_time":"0",
			"tags": "未分组",
			"prize_type": "无",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本",
			"create_time": "2015-10-10 10:20:30"
		},{
			"code_name": "分销二维码2",
			"relation_member": "bill",
			"distribution_prize_type": "佣金",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":50.00,
			"settlement_time":"0",
			"tags": "分组1",
			"prize_type": "积分",
			"integral": "100",
			"reply_type": "图文",
			"scan_code_reply": "图文1",
			"create_time": "2015-10-10 10:20:30"
		}]
		"""
	When jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""
	And jobs已添加支付方式
		"""
		[{
			"type":"货到付款"
		},{
			"type":"微信支付"
		},{
			"type":"支付宝"
		}]
		"""

	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"count":"10"
		},{
			"name": "商品2",
			"price": 100.00,
			"count":"10"
		}]
		"""

	#扫码关注成为会员
		When 清空浏览器
		And jack扫描渠道二维码"分销二维码1"于2015-08-10 10:00:00
		And jack访问jobs的webapp

		When 清空浏览器
		And nokia扫描渠道二维码"分销二维码2"于2015-08-11 10:00:00
		And nokia关注jobs的公众号于'2015-08-11 10:00:00'
		And nokia访问jobs的webapp

		When jobs为会员发放优惠券
			"""
			{
				"name": "优惠券00",
				"count": 1,
				"members": ["nokia"],
				"coupon_ids": ["coupon2_id_1"]
			}
			"""

	#会员购买
		When jack购买jobs的商品
			"""
			{
				"relation_member":"bigs",
				"order_id": "002",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品
			"""
			{
				"relation_member":"bigs",
				"order_id": "003",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品
			"""
			{
				"relation_member":"bigs",
				"order_id": "004",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品
			"""
			{
				"relation_member":"bigs",
				"order_id": "005",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品
			"""
			{
				"relation_member":"bigs",
				"order_id": "006",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品
			"""
			{
				"relation_member":"bigs",
				"order_id": "007",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When nokia购买jobs的商品
			"""
			{
				"relation_member":"bill",
				"order_id": "008",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When nokia购买jobs的商品
			"""
			{
				"relation_member":"bill",
				"order_id": "009",
				"pay_type": "货到付款",
				"coupon_id":"coupon2_id_1",
				"products":[{
					"name":"商品1",
					"count":1 
				}]
			}
			"""
		#When nokia购买jobs的商品
		#	"""
		#	{
		#		"relation_member":"bill",
		#		"order_id": "010",
		#		"pay_type": "货到付款",
		#		"integral_money":50.00,
		#		"integral":100.00,
		#		"products":[{
		#			"name":"商品1",
		#			"count":1 
		#		}]
		#	}
		#	"""
		
@mall2 @apps @senior @processing_applications @sjq
Scenario:1 分销会员结算页初次没有提交时的显示
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When jobs完成订单"007"
		When jobs完成订单"008"
		When jobs完成订单"009"
		#When jobs完成订单"010"
		When 后台执行channel_distribution_update		
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"----",
				"current_transaction_amount":600.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":60.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			},{
				"relation_member": "bill",
				"submit_time":"----",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			}]
			"""
@mall2 @apps @senior @processing_applications
Scenario:2 分销会员结算页等待审核状态
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When jobs完成订单"008"
		When jobs完成订单"009"
		When jobs完成订单"010"
		When 后台执行channel_distribution_update
		When bigs访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":500.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":50.00,
				"cash_back_amount":50.00,
				"cash_back_state":"等待审核"
			}{
				"relation_member": "bill",
				"submit_time":"----",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			}]
			"""

@mall2 @apps @senior @processing_applications
Scenario:3 分销会员结算页正在返现状态
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When jobs完成订单"007"
		When jobs完成订单"008"
		When jobs完成订单"009"
		When jobs完成订单"010"
		When 后台执行channel_distribution_update
		When bigs访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		
		When jobs更改返现状态为"正在返现"
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":600.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":60.00,
				"cash_back_amount":60.00,
				"cash_back_state":"正在返现"
			}{
				"relation_member": "bill",
				"submit_time":"----",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			}]
			"""
@mall2 @apps @senior @processing_applications
Scenario:4 分销会员结算页已完成/切换为无状态
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When jobs完成订单"007"
		When jobs完成订单"008"
		When jobs完成订单"009"
		When jobs完成订单"010"
		When 后台执行channel_distribution_update
		When bigs访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		When jobs更改返现状态为"已完成/切换为无状态"
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":600.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":0,
				"cash_back_amount":0,
				"cash_back_state":"无状态"
			}{
				"relation_member": "bill",
				"submit_time":"----",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			}]
			"""

@mall2 @apps @senior @processing_applications
Scenario:5 整体概况
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When jobs完成订单"007"
		When jobs完成订单"008"
		When jobs完成订单"009"
		When jobs完成订单"010"
		When 后台执行channel_distribution_update
		Then jobs获得分销会员整体概况
			"""
			{
				"cash_back_total":0,
				"not_return_total":70.00,
				"current_return":70.00,
				"turnover_total":800.00
			}
			"""
		When bigs访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		When jobs更改返现状态为"已完成/切换为无状态"

		Then jobs获得分销会员整体概况
			"""
			{
				"cash_back_total":60.00,
				"not_return_total":0,
				"current_return":10.00,
				"turnover_total":800.00
			}
			"""

@mall2 @apps @senior @processing_applications
Scenario:6 会员结算列表查询
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When jobs完成订单"007"
		When jobs完成订单"008"
		When jobs完成订单"009"
		When jobs完成订单"010"
		When 后台执行channel_distribution_update
		When bigs访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		When jobs更改返现状态为"已完成/切换为无状态"
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":600.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":0,
				"cash_back_amount":0,
				"cash_back_state":"无状态"
			}{
				"relation_member": "bill",
				"submit_time":"----",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			}]
			"""
		#返现金额不满足
		When jobs设置分销会员结算查询条件
			"""
			{
				"cash_back_amount_in":0,
				"cash_back_amount_to":10.00
			}
			""" 
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bill",
				"submit_time":"----",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			}]
			"""
		#返现金额满足
		When jobs设置分销会员结算查询条件
			"""
			{
				"cash_back_amount_in":0,
				"cash_back_amount_to":60.00
			}
			""" 
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":600.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":0,
				"cash_back_amount":0,
				"cash_back_state":"无状态"
			}{
				"relation_member": "bill",
				"submit_time":"----",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			}]
			"""
		#提交时间不满足,金额满足
		When jobs设置分销会员结算查询条件
			"""
			{
				"cash_back_amount_in":0,
				"cash_back_amount_to":60.00,
				"submit_time_start":"2015-08-10 10:00:00",
				"submit_time_end":"2015-08-11 10:00:00"
			}
			""" 
		Then jobs获得分销会员结算列表
			"""
			[]
			"""
		#提交时间满足,金额不满足
		When jobs设置分销会员结算查询条件
			"""
			{
				"cash_back_amount_in":0,
				"cash_back_amount_to":10.00,
				"submit_time_start":"2015-08-12 10:00:00",
				"submit_time_end":"2015-08-13 10:00:00"
			}
			""" 
		Then jobs获得分销会员结算列表
			"""
			[]
			"""
		#提交时间满足,金额满足
		When jobs设置分销会员结算查询条件
			"""
			{
				"cash_back_amount_in":0,
				"cash_back_amount_to":60.00,
				"submit_time_start":"2015-08-12 10:00:00",
				"submit_time_end":"2015-08-13 10:00:00"
			}
			""" 
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":600.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":0,
				"cash_back_amount":0,
				"cash_back_state":"无状态"
			}]
			"""
		#提交时间满足
		When jobs设置分销会员结算查询条件
			"""
			{
				"submit_time_start":"2015-08-12 10:00:00",
				"submit_time_end":"2015-08-13 10:00:00"
			}
			""" 
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":600.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":0,
				"cash_back_amount":0,
				"cash_back_state":"无状态"
			}]
			"""
		#提交时间不满足
		When jobs设置分销会员结算查询条件
			"""
			{
				"submit_time_start":"2015-08-11 10:00:00",
				"submit_time_end":"2015-08-11 10:00:00"
			}
			""" 
		Then jobs获得分销会员结算列表
			"""
			[]
			"""
@mall2 @apps @senior @processing_applications
Scenario:7 上一期未完成,微信用户扫码下单返现的整体概况和分销会员列表
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When 后台执行channel_distribution_update
		When bigs访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		Then jobs获得分销会员整体概况
			"""
			{
				"cash_back_total":0,
				"not_return_total":50,
				"current_return":50.00,
				"turnover_total":500.00
			}
			"""
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":500.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":50.00,
				"cash_back_amount":50.00,
				"cash_back_state":"等待审核"
			}]
			"""
		When jobs完成订单"007"
		When jobs完成订单"008"
		When jobs完成订单"009"
		When jobs完成订单"010"
		When 后台执行channel_distribution_update
		Then jobs获得分销会员整体概况
			"""
			{
				"cash_back_total":70.00,
				"not_return_total":100.00,
				"current_return":50.00,
				"turnover_total":800.00
			}
			"""
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":500.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":60.00,
				"cash_back_amount":50.00,
				"cash_back_state":"等待审核"
			},{
				"relation_member": "bill",
				"submit_time":"----",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			}]
			"""
		When jobs更改返现状态为"已完成/切换为无状态"
		Then jobs获得分销会员整体概况
			"""
			{
				"cash_back_total":70.00,
				"not_return_total":20.00,
				"current_return":20.00,
				"turnover_total":800.00
			}
			"""
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":500.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			},{
				"relation_member": "bill",
				"submit_time":"----",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":"暂无",
				"cash_back_state":"无状态"
			}]
			"""