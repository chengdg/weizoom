#author: 张雪 2016-5-6

Feature:参加返利活动
"""
	1.管理员能够查看到所有扫过该码并关注过的微信用户信息
	2.管理员能够查看到所有扫过该码之后产生的订单信息
	3.管理员给达到返利条件的微信用户发微众卡
	4.微信用户查看自己的微众卡信息
	5.管理员查看发放详情：为使用者使用微众卡详情

"""

Background:
	Given jobs登录系统
	When jobs已创建微众卡
	"""
	{
		"cards":[{
			"id":"0000001",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000002",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000003",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000004",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000005",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000006",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000007",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000008",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000009",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000010",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000011",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000012",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000013",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000014",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000015",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000016",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000017",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000018",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000019",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000020",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000021",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000022",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000023",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000024",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000025",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000026",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000027",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000028",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000029",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000030",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000031",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000032",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000033",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000034",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000035",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000036",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000037",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000038",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000039",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		},{
			"id":"0000040",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
	}
	"""
	When jobs已添加商品
	 """
		[{
			"name": "商品1",
			"price": 10.00,
			"postage":100,
			"synchronized_mall":"是"
		}, {
			"name": "商品2",
			"price": 10.00,
			"postage":100,
			"synchronized_mall":"是"
		}]
	 """
	And jobs开通使用微众卡权限
	And jobs添加支付方式
	"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
	"""
	And jobs已添加支付方式
	"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		},{
			"type": "支付宝支付",
			"is_active": "启用"
		}]
	"""
	When jobs新建返利活动
	"""
		[{
			"code_name":"返利活动1",
			"is_attention_in":"true",
			"is_limit_first_buy	":"true",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
				}
			"weizoom_card_id_from":"0000001",
			"weizoom_card_id_to":"0000005",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-11 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动1"
		},{
			"code_name":"返利活动2",
			"is_attention_in":"true",
			"is_limit_first_buy	":"true",
			"is_limit_cash":"false",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
				}
			"weizoom_card_id_from":"0000006",
			"weizoom_card_id_to":"00000010",
			"card_counts":5,
			"start_time":"2016-05-07 00:00:00",
			"end_time":"2016-05-11 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动2"

		},{
			"code_name":"返利活动3",
			"is_attention_in":"true",
			"is_limit_first_buy	":"false",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
				}
			"weizoom_card_id_from":"0000011",
			"weizoom_card_id_to":"0000015",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-11 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动3"
		},{
			"code_name":"返利活动4",
			"is_attention_in":"true",
			"is_limit_first_buy	":"false",
			"is_limit_cash":"false",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
				}
			"weizoom_card_id_from":"0000016",
			"weizoom_card_id_to":"0000020",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-11 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动4"
		},{
			"code_name":"返利活动5",
			"is_attention_in":"false",
			"is_limit_first_buy	":"false",
			"is_limit_cash":"false",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
				}
			"weizoom_card_id_from":"0000021",
			"weizoom_card_id_to":"0000025",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"22016-05-11 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动5"
		},{
			"code_name":"返利活动6",
			"is_attention_in":"false",
			"is_limit_first_buy	":"false",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
				}
			"weizoom_card_id_from":"0000026",
			"weizoom_card_id_to":"0000030",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-11 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动6"
		},{
			"code_name":"返利活动7",
			"is_attention_in":"false",
			"is_limit_first_buy	":"true",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
				}
			"weizoom_card_id_from":"0000031",
			"weizoom_card_id_to":"0000035",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-11 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动7"
		},{
			"code_name":"返利活动8",
			"is_attention_in":"false",
			"is_limit_first_buy	":"true",
			"is_limit_cash":"false",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
				}
			"weizoom_card_id_from":"0000036",
			"weizoom_card_id_to":"0000040",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-11 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动8"
		}]
	"""


	
@mall @rebate
Scenario:1 管理员能够查看到所有扫过该码并关注过的微信用户信息，带参数返利活动[关注人数]-会员数量变化；
	#设置已关注会员可参与
	#购买次数为首单
	#订单金额为现金
	#满10元返5元
	Given jobs登录系统
	#未关注微信账号扫码关注，关注数量增加
	When 清空浏览器
	When bill扫描返利活动"返利活动1"
	When bill访问jobs的webapp
	

	Given jobs登录系统
	Then jobs获得返利活动列表
	"""
		[{
			"code_name": "返利活动1",
			"attention_number": 1
		}]
	"""
	#已关注会员扫码，关注数量增加
	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom扫描返利活动"返利活动1"
	
	Given jobs登录系统
	Then jobs获得返利活动列表
	"""
		[{
			"code_name": "返利活动1",
			"attention_number": 2
		}]
	"""
	#扫码之前取消关注的会员再次扫码返利活动，关注数量增加
	When 清空浏览器
	When zhouxun关注jobs的公众号
	When zhouxun访问jobs的webapp
	When zhouxun取消关注jobs的公众号
	When zhouxun扫描带参数二维码"返利活动1"
	

	Given jobs登录系统
	Then jobs获得带参数二维码列表
	"""
		[{
			"code_name": "返利活动1",
			"attention_number": 3
		}]
	"""

	When 微信用户批量消费jobs的商品
		| order_i  | date       | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 今天       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       | 0000001,1234567| jobs,发货  |    已发货     |
		|   0002   | 今天       |   tom    | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0003   | 今天       |  zhouxun | 商品1,1 |   支付  |  微众卡   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |    
		

	When jobs对"返利活动1"的"关注人数"操作
	#仅显示扫码后成交订单-勾选
	Then jobs能获取"仅显示通过二维码新关注会员"列表
	"""
		[{
			"fans_name": "zhouxun",
			"buy_number": 1,
			"integral": 0,
			"price":20.00
		}]
	"""
	#显示所有的的会员
	Then jobs能获取会员列表
	"""
		[{
			"fans_name": "zhouxun",
			"buy_number": 1,
			"integral": 0,
			"price":20.00
		},{
			"fans_name": "tom",
			"buy_number": 1,
			"integral": 0,
			"price":20.00
		},{
			"fans_name": "bill",
			"buy_number": 1,
			"integral": 0,
			"price":20.00
		}]
	"""

	When 清空浏览器
	When zhouxun关注jobs的公众号于"2016-05-09 10:00:00"
	When zhouxun绑定手机号"13563223667"

	Given jobs登录系统
	Then jobs发放返利微众卡

	When 清空浏览器
	Then zhouxun能获得返利微众卡
	"""
	[{
		"id":"0000001"
	}]

	"""



@mall @rebate
Scenario:2 带参数返利活动[扫码后成交金额]-已关注会员可参与；首单；非现金
	#已关注会员可参与；
	#必须是首单；
	#可不用现金支付；
	Given jobs登录系统

	When 清空浏览器
	When bill关注jobs的公众号于"2016-04-09 10:00:00"
	When bill扫描带参数二维码"返利活动2"

	When 清空浏览器
	When tom关注jobs的公众号于"2016-05-09 10:00:00"
	When tom扫描带参数二维码"返利活动2"


	When 清空浏览器
	When zhouxun关注jobs的公众号于"2016-05-09 10:00:00"
	When zouxun扫描带参数二维码"返利活动2"

	When 微信用户批量消费jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-04-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0002   | 2016-05-10       |   tom    | 商品2,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0003   | 2016-05-10       |  zhouxun | 商品1,1 |   支付  |  微众卡   |   10.00   | 10.00   |     20.00       | 0000001,1234567| jobs,发货  |    已发货     |


	Given jobs登录系统	
	When jobs对"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品2",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""


@mall @rebate
Scenario:3 带参数返利活动[扫码后成交金额]-已关注会员；不限；现金
	#已关注会员可参与；
	#必须是不限；
	#现金支付；
	Given jobs登录系统


	When 清空浏览器
	When bill关注jobs的公众号于"2016-04-09 10:00:00"
	When bill扫描带参数二维码"返利活动2"

	When 清空浏览器
	When tom关注jobs的公众号于"2016-05-09 10:00:00"
	When tom扫描带参数二维码"返利活动2"


	When 清空浏览器
	When zhouxun关注jobs的公众号于"2016-05-09 10:00:00"
	When zouxun扫描带参数二维码"返利活动2"

	When 微信用户批量消费jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-04-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0002   | 2016-05-10       |   tom    | 商品2,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0002   | 2016-05-10       |   tom    | 商品2,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0003   | 2016-05-10       |  zhouxun | 商品1,1 |   支付  |  微众卡   |   10.00   | 10.00   |     20.00       | 0000001,1234567| jobs,发货  |    已发货     |


	Given jobs登录系统	
	When jobs对"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品2",
				"price": 10.00,
				"count": 1
			},{
				"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""



@mall @rebate
Scenario:4 带参数返利活动[扫码后成交金额]-已关注会员；不限；非现金
	#已关注会员可参与；
	#不限订单；
	#f可使用非现金支付；
	Given jobs登录系统


	When 清空浏览器
	When bill关注jobs的公众号于"2016-05-09 10:00:00"
	When bill扫描带参数二维码"返利活动2"

	When 清空浏览器
	When tom关注jobs的公众号于"2016-05-09 10:00:00"
	When tom扫描带参数二维码"返利活动2"


	When 清空浏览器
	When zhouxun关注jobs的公众号于"2016-05-09 10:00:00"
	When zouxun扫描带参数二维码"返利活动2"

	When 微信用户批量消费jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-04-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0002   | 2016-05-10       |   tom    | 商品2,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0002   | 2016-05-10       |   tom    | 商品2,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0003   | 2016-05-10       |  zhouxun | 商品1,1 |   支付  |  微众卡   |   10.00   | 10.00   |     20.00       | 0000001,1234567| jobs,发货  |    已发货     |


	Given jobs登录系统	
	When jobs对"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
				"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""

@mall @rebate
Scenario:5 带参数返利活动[扫码后成交金额]-已关注会员不可参与；不限；非现金
	#已关注会员不可参与；
	#不限订单；
	#f可使用非现金支付；
	Given jobs登录系统


	When 清空浏览器
	When bill关注jobs的公众号于"2016-05-09 10:00:00"
	When bill扫描带参数二维码"返利活动2"

	When 清空浏览器
	When tom扫描带参数二维码"返利活动2"


	When 清空浏览器
	When zouxun扫描带参数二维码"返利活动2"

	When 微信用户批量消费jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-05-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0002   | 2016-05-10       |   tom    | 商品2,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0003   | 2016-05-10       |  zhouxun | 商品1,1 |   支付  |  微众卡   |   10.00   | 10.00   |     20.00       | 0000001,1234567| jobs,发货  |    已发货     |


	Given jobs登录系统	
	When jobs对"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品2",
				"price": 10.00,
				"count": 1
			},{
				"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
	
		}]
	"""

@mall @rebate
Scenario:6 带参数返利活动[扫码后成交金额]-已关注会员不可参与；不限；现金
	#已关注会员不可参与；
	#不限订单；
	#现金支付；
	Given jobs登录系统

	#未关注过的用户下单
	When 清空浏览器
	When bill关注jobs的公众号于"2016-05-09 10:00:00"
	When bill扫描带参数二维码"返利活动2"

	When 清空浏览器
	When tom扫描带参数二维码"返利活动2"


	When 清空浏览器
	When zouxun扫描带参数二维码"返利活动2"

	When 微信用户批量消费jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-05-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0002   | 2016-05-10       |   tom    | 商品2,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0003   | 2016-05-10       |  zhouxun | 商品1,1 |   支付  |  微众卡   |   10.00   | 10.00   |     20.00       | 0000001,1234567| jobs,发货  |    已发货     |


	Given jobs登录系统	
	When jobs对"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品2",
				"price": 10.00,
				"count": 1
			},{
				"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
	
		}]
	"""
	
@mall @rebate
Scenario:7 带参数返利活动[扫码后成交金额]-已关注会员不可参与；首单；现金
	#已关注会员不可参与；
	#首单；
	#现金支付；
	Given jobs登录系统


	When 清空浏览器
	When bill关注jobs的公众号于"2016-05-09 10:00:00"
	When bill扫描带参数二维码"返利活动2"

	When 清空浏览器
	When tom扫描带参数二维码"返利活动2"


	When 清空浏览器
	When zouxun扫描带参数二维码"返利活动2"

	When 微信用户批量消费jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-04-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0001   | 2016-05-10       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0002   | 2016-05-10       |   tom    | 商品2,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0003   | 2016-05-10       |  zhouxun | 商品1,1 |   支付  |  微众卡   |   10.00   | 10.00   |     20.00       | 0000001,1234567| jobs,发货  |    已发货     |


	Given jobs登录系统	
	When jobs对"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品2",
				"price": 10.00,
				"count": 1
			},{
				"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
	
		}]
	"""

@mall @rebate
Scenario:8 带参数返利活动[扫码后成交金额]-已关注会员不可参与；首单；非现金
	#已关注会员不可参与；
	#首单；
	#非现金支付；
	Given jobs登录系统


	When 清空浏览器
	When bill关注jobs的公众号于"2016-05-09 10:00:00"
	When bill扫描带参数二维码"返利活动2"

	When 清空浏览器
	When tom扫描带参数二维码"返利活动2"


	When 清空浏览器
	When zouxun扫描带参数二维码"返利活动2"

	When 微信用户批量消费jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-04-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0001   | 2016-05-10       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0002   | 2016-05-10       |   tom    | 商品2,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |
		|   0003   | 2016-05-10       |  zhouxun | 商品1,1 |   支付  |  微众卡   |   10.00   | 10.00   |     20.00       | 0000001,1234567| jobs,发货  |    已发货     |


	Given jobs登录系统	
	When jobs对"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		},{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品2",
				"price": 10.00,
				"count": 1
			},{
				"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
	
		}]
	"""

@mall @rebate
Scenario:9 带参数返利活动-参加未开始或者已结束的返利活动不能获得返利
	



@mall @rebate
Scenario:10 带参数返利活动-多个返利活动同时存在，并且同一个人扫多个返利活动的码且下单
	Given jobs登录系统

	When 清空浏览器
	When bill关注jobs的公众号于"2016-05-05 10:00:00"
	When bill访问jobs的weapp
	When bill购买jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-05-05       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |


	When 清空浏览器
	When bill扫描带参数二维码"返利活动3"
	When bill访问jobs的weapp
	When bill购买jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-05-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |

	When bill扫描带参数二维码"返利活动4"
	When bill访问jobs的weapp
	When bill购买jobs的商品
		| order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-05-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |

	When bill扫描带参数二维码"返利活动5"
	When bill访问jobs的weapp
	    | order_id | date             | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 2016-05-09       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 10.00   |     20.00       |                | jobs,发货  |    已发货     |

	

	Given jobs登录系统	
	When jobs对"返利活动3"的"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""

	
	When jobs对"返利活动4"的"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""

	When jobs对"返利活动5"的"扫码后成交金额"操作
	#勾选仅显示扫码后的成交的订单
	Then jobs显示"仅显示扫码后成交订单"
	Then jobs能获取列表
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""
	When jobs取消勾选'仅显示扫码后成交订单'
	"""
		[{
			"status": "已发货",
			"final_price": 20.00,
			"products": [{
				"name": "商品1",
				"price": 10.00,
				"count": 1
			}]
		}]
	"""


	

	
