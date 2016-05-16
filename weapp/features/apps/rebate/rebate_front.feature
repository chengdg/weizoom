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
	And jobs已创建微众卡
	"""
	{
		"cards":[{
			"id":"0000001",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000002",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000003",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000004",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000005",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000006",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000007",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000008",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000009",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000010",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000011",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000012",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000013",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000014",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000015",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000016",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000017",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000018",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000019",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000020",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000021",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000022",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000023",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000024",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		},{
			"id":"0000041",
			"password":"1234567",
			"status":"未使用",
			"price":5.00
		}]
	}
	"""
	When jobs已添加商品
	 """
		[{
			"name": "商品1",
			"price": 1.00,
			"postage":0.00
		},{
			"name": "商品2",
			"price": 0.50,
			"postage":0.00
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
	Given jobs已添加支付方式
	"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		},{
			"type": "支付宝",
			"is_active": "启用"
		}]
	"""
	When jobs新建返利活动
	"""
		[{
			"code_name":"返利活动1",
			"is_attention_in":"true",
			"is_limit_first_buy":"true",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"1.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000001",
			"weizoom_card_id_to":"0000003",
			"card_counts":5,
			"start_time":"今天",
			"end_time":"后天",
			"reply_type": "文字",
			"scan_code_reply": "返利活动1"
		},{
			"code_name":"返利活动2",
			"is_attention_in":"true",
			"is_limit_first_buy":"true",
			"is_limit_cash":"false",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000004",
			"weizoom_card_id_to":"0000006",
			"card_counts":5,
			"start_time":"明天",
			"end_time":"后天",
			"reply_type": "文字",
			"scan_code_reply": "返利活动2"

		},{
			"code_name":"返利活动3",
			"is_attention_in":"true",
			"is_limit_first_buy":"false",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"1.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000007",
			"weizoom_card_id_to":"0000008",
			"card_counts":5,
			"start_time":"今天",
			"end_time":"后天",
			"reply_type": "文字",
			"scan_code_reply": "返利活动3"
		},{
			"code_name":"返利活动4",
			"is_attention_in":"true",
			"is_limit_first_buy":"false",
			"is_limit_cash":"false",
			"order_rebate":{
				"rebate_order_price":"1.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000009",
			"weizoom_card_id_to":"0000012",
			"card_counts":5,
			"start_time":"今天",
			"end_time":"后天",
			"reply_type": "文字",
			"scan_code_reply": "返利活动4"
		},{
			"code_name":"返利活动5",
			"is_attention_in":"false",
			"is_limit_first_buy":"false",
			"is_limit_cash":"false",
			"order_rebate":{
				"rebate_order_price":"1.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000013",
			"weizoom_card_id_to":"0000015",
			"card_counts":5,
			"start_time":"今天",
			"end_time":"后天",
			"reply_type": "文字",
			"scan_code_reply": "返利活动5"
		},{
			"code_name":"返利活动6",
			"is_attention_in":"false",
			"is_limit_first_buy":"false",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"1.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000016",
			"weizoom_card_id_to":"0000018",
			"card_counts":5,
			"start_time":"今天",
			"end_time":"后天",
			"reply_type": "文字",
			"scan_code_reply": "返利活动6"
		},{
			"code_name":"返利活动7",
			"is_attention_in":"false",
			"is_limit_first_buy":"true",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"1.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000019",
			"weizoom_card_id_to":"0000021",
			"card_counts":5,
			"start_time":"今天",
			"end_time":"后天",
			"reply_type": "文字",
			"scan_code_reply": "返利活动7"
		},{
			"code_name":"返利活动8",
			"is_attention_in":"false",
			"is_limit_first_buy":"true",
			"is_limit_cash":"false",
			"order_rebate":{
				"rebate_order_price":"1.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000022",
			"weizoom_card_id_to":"0000024",
			"card_counts":5,
			"start_time":"今天",
			"end_time":"后天",
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
	#未关注微信账号扫码关注，关注数量增加
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill扫描返利活动'返利活动1'的二维码

	Given jobs登录系统
	Then jobs获得返利活动'返利活动1'的列表
	"""
		{
			"code_name": "返利活动1",
			"attention_number": 1
		}
	"""
	#已关注会员扫码，关注数量增加
	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom扫描返利活动'返利活动1'的二维码

	Given jobs登录系统
	Then jobs获得返利活动'返利活动1'的列表
	"""
		{
			"code_name": "返利活动1",
			"attention_number": 2
		}
	"""
	#扫码返利活动后取消关注的会员，关注数量减少1
	When 清空浏览器
	When tom取消关注jobs的公众号

	Given jobs登录系统
	Then jobs获得返利活动'返利活动1'的列表
	"""
		{
			"code_name": "返利活动1",
			"attention_number": 1
		}
	"""
	

@mall @rebate @aix1111
Scenario:2 带参数返利活动[扫码后成交金额]-已关注会员可参与；首单；现金

	Given jobs登录系统
	When 清空浏览器
	When bill扫描返利活动'返利活动1'的二维码

	Given 等待1秒
	When 清空浏览器
	When zhouxun关注jobs的公众号
	When zhouxun访问jobs的webapp
	When zhouxun扫描返利活动'返利活动1'的二维码

	Given 等待1秒
	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom扫描返利活动'返利活动1'的二维码

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp

	When 微信用户批量消费jobs的商品
		| order_id | date       | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*  | weizoom_card   | action     | order_status  |
		|   0001   | 今天       |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00    | 1.00    |     1.00        |                | jobs,完成  |    已完成     |
		|   0002   | 今天       |   tom    | 商品1,1 |   支付  |  货到付款   |   0.00    | 1.00    |     1.00        | 0000041,1234567| jobs,完成  |    已完成     |
		|   0003   | 今天       |  zhouxun | 商品1,1 |   支付  |   支付宝  |   0.00    | 1.00    |     1.00        |                | jobs,完成  |    已完成     |

	Given jobs登录系统
	#默认显示扫码后的新会员
	Then jobs能获取'返利活动1'会员列表
	"""
		[{
			"fans_name": "bill",
			"buy_number": 1,
			"integral": 0,
			"price":1.00
		}]
	"""
	When jobs取消对'返利活动1'进行'仅显示扫码后关注会员'操作
	#显示所有的的会员
	Then jobs能获取'返利活动1'会员列表
	"""
		[{
			"fans_name": "tom",
			"buy_number": 1,
			"integral": 0,
			"price":1.00
		},{
			"fans_name": "zhouxun",
			"buy_number": 1,
			"integral": 0,
			"price":1.00
		},{
			"fans_name": "bill",
			"buy_number": 1,
			"integral": 0,
			"price":1.00
		}]
	"""

	Given jobs登录系统
	#默认显示扫码后成交的订单
	Then jobs能获取'返利活动1'订单列表
	"""
		[{
			"order_id":"0001",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
				"name": "商品1",
				"price": 1.00,
				"count": 1
			}]
		},{
			"order_id":"0002",
			"status": "已完成",
			"final_price": 0.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
			}]
		},{
			"order_id":"0003",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
			}]

		}]
	"""

	Then jobs获得总消费金额
	"""
		{
			"cash_payment":2.00,
			"card_payment":1.00
		}

	"""



	When 清空浏览器
	When zhouxun绑定手机号'13563223667'

	Given jobs登录系统
	Then jobs发放返利微众卡

	When 清空浏览器
	Then zhouxun能获得返利微众卡
	"""
		[{
			"id":"0000001"
		}]

	"""
	When 清空浏览器
	When bill绑定手机号'13563223668'

	Given jobs登录系统
	Then jobs发放返利微众卡

	When 清空浏览器
	Then bill能获得返利微众卡
	"""
		[{
			"id":"0000002"
		}]

	"""

@mall @rebate @sunhan1
Scenario:3 带参数返利活动[扫码后成交金额]-已关注会员可参与；首单；非现金
	#已关注会员可参与；
	#必须是首单；
	#可不用现金支付；
	Given jobs登录系统

	#已关注会员在扫码之前已经下单
	When 清空浏览器
	When bill关注jobs的公众号于'1天前'
	When bill访问jobs的webapp
	When bill扫描返利活动'返利活动2'的二维码

	Given 等待1秒
	When 清空浏览器
	When tom关注jobs的公众号于'后天'
	When tom访问jobs的webapp
	When tom扫描返利活动'返利活动2'的二维码

	#用户参加已结束的活动，不会获得返利
	Given 等待1秒
	When 清空浏览器
	When zhouxun关注jobs的公众号于'3天后'
	When zhouxun访问jobs的webapp
	When zhouxun扫描返利活动'返利活动2'的二维码

	When 微信用户批量消费jobs的商品
		| order_id | date        | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 1天前      |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00    | 1.00    |     1.00        |                | jobs,完成  |    已完成     |
		|   0002   | 今天        |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00    | 1.00    |     1.00        |                | jobs,完成  |    已完成     |
		|   0003   | 后天        |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00    | 1.00    |     1.00        | 0000041,1234567| jobs,完成  |    已完成     |
		|   0004   | 3天后      |  zhouxun | 商品1,1 |   支付  |  货到付款   |   0.00    | 1.00    |     1.00        |                | jobs,完成  |    已完成     |

	Given jobs登录系统
	#勾选仅显示扫码后的成交的订单(默认显示)
	Then jobs能获取'返利活动2'订单列表
	"""
		[{
			"order_id":"0003",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
				"name": "商品1",
				"price": 1.00,
				"count": 1
			}]
		}]
	"""

#	#显示所有的订单
#	When jobs取消对'返利活动2'进行'仅显示扫码后关注会员'操作
#	Then jobs能获取'返利活动2'订单列表
	"""
		[{
			"order_id":"0003",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
				"name": "商品1",
				"price": 1.00,
				"count": 1
			}]
		}]
	"""
#
#	Then jobs获得总消费金额
#	"""
#		{
#			"cash_payment":3.00,
#			"card_payment":1.00
#		}
#
#	"""





#	Given jobs登录系统
#	Then jobs发放返利微众卡
#
#	When 清空浏览器
#	Then tom能获得返利微众卡手机号绑定页面
#
#	When tom绑定手机号'13562336987'
#
#	Given jobs登录系统
#	Then jobs发放返利微众卡
#
#	When 清空浏览器
#	When tom关注jobs的公众号
#	When tom访问jobs的webapp
#	Then tom能获得返利微众卡
#	"""
#		[{
#			"id":"0000004"
#		}]
#
#	"""


	


@mall @rebate
Scenario:4 带参数返利活动[扫码后成交金额]-已关注会员可参与；不限；现金
	#已关注会员可参与；
	#必须是不限；
	#现金支付；
	Given jobs登录系统

	When 清空浏览器
	When tom关注jobs的公众号于'今天'
	When tom访问jobs的webapp
	When tom扫描返利活动'返利活动3'的二维码


	When 清空浏览器
	When zhouxun关注jobs的公众号于"今天"
	When zhouxun访问jobs的webapp
	When zhouxun扫描返利活动'返利活动3'的二维码

	When 微信用户批量消费jobs的商品
		| order_id | date       | consumer | product | payment | pay_type  |postage*   |price* | paid_amount*   | weizoom_card   | action     | order_status  |
		|   0001   | 明天       |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0002   | 明天       |   tom    | 商品2,1 |   支付  |  支付宝   |   0.00   | 0.50   |     0.50       |                | jobs,完成  |    已完成     |
		|   0003   | 明天       |  zhouxun | 商品1,1 |   支付  |  货到付款   |   0.00   | 1.00   |     1.00       | 0000041,1234567| jobs,完成  |    已完成     |


	When 清空浏览器
	When tom关注jobs的公众号于'今天'
	When tom访问jobs的webapp
	When tom绑定手机号'13563223668'

	Given jobs登录系统
	Then jobs发放返利微众卡

	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	#未满设置的金额，不符合满减条件
	Then tom能获得返利微众卡
	"""
		[{
			"id":"0000007"
		}]

	"""


@mall @rebate
Scenario:5 带参数返利活动[扫码后成交金额]-已关注会员可参与；不限；非现金
	#已关注会员可参与；
	#不限订单；
	#可使用非现金支付；
	Given jobs登录系统


	When 清空浏览器
	When bill关注jobs的公众号于'1天前'
	When bill访问jobs的webapp
	When bill扫描返利活动'返利活动4'的二维码

	When 清空浏览器
	When tom关注jobs的公众号于'今天'
	When tom访问jobs的webapp
	When tom扫描返利活动'返利活动4'的二维码


	When 清空浏览器
	When zhouxun关注jobs的公众号于'今天'
	When zhouxun访问jobs的webapp
	When zhouxun扫描返利活动'返利活动4'的二维码

	When 微信用户批量消费jobs的商品
		| order_id | date       | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 今天       |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0002   | 明天       |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0003   | 明天       |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0004   | 明天       |  zhouxun | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       | 0000041,1234567| jobs,完成  |    已完成     |


	When 清空浏览器
	When bill绑定手机号'13563223668'

	When 清空浏览器
	When tom绑定手机号'13563223669'

	When 清空浏览器
	When zhouxun绑定手机号'13563223679'

	Given jobs登录系统
	Then jobs发放返利微众卡

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill能获得返利微众卡
	"""
		[{
			"id":"0000009"
		}]

	"""

	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	Then tom能获得返利微众卡
	"""
		[{
			"id":"0000010"
		},{
			"id":"0000011"
		}]

	"""

	When 清空浏览器
	When zhouxun关注jobs的公众号
	When zhouxun访问jobs的webapp
	Then zhouxun能获得返利微众卡
	"""
		[{
			"id":"0000012"
		}]

	"""


@mall @rebate
Scenario:6 带参数返利活动[扫码后成交金额]-已关注会员不可参与；不限；非现金
	#已关注会员不可参与；
	#不限订单；
	#f可使用非现金支付；
	Given jobs登录系统


	When 清空浏览器
	When bill关注jobs的公众号于'1天前'
	When bill访问jobs的webapp
	When bill扫描返利活动'返利活动5'的二维码

	When 清空浏览器
	When tom扫描返利活动'返利活动5'的二维码


	When 清空浏览器
	When zhouxun扫描返利活动'返利活动5'的二维码

	When 微信用户批量消费jobs的商品
		| order_id | date       | consumer | product | payment | pay_type  |postage*  |price*  | paid_amount*   | weizoom_card   | action     | order_status  |
		|   0001   | 今天       |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0002   | 明天       |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0003   | 明天       |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0004   | 明天       |  zhouxun | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       | 0000041,1234567| jobs,完成  |    已完成     |

	When 清空浏览器
	When bill绑定手机号'13563223668'

	When 清空浏览器
	When tom绑定手机号'13563223669'

	When 清空浏览器
	When zhouxun绑定手机号'13563223679'

	Given jobs登录系统
	Then jobs发放返利微众卡


	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	Then tom能获得返利微众卡
	"""
		[{
			"id":"0000013"
		},{
			"id":"0000014"
		}]

	"""

	When 清空浏览器
	When zhouxun关注jobs的公众号
	When zhouxun访问jobs的webapp
	Then zhouxun能获得返利微众卡
	"""
		[{
			"id":"0000015"
		}]

	"""




@mall @rebate
Scenario:7 带参数返利活动[扫码后成交金额]-已关注会员不可参与；不限；现金
	#已关注会员不可参与；
	#不限订单；
	#现金支付；
	Given jobs登录系统

	#未关注过的用户下单
	When 清空浏览器
	When bill关注jobs的公众号于'1天前'
	When bill访问jobs的webapp
	When bill扫描返利活动'返利活动6'的二维码

	When 清空浏览器
	When tom扫描返利活动'返利活动6'的二维码


	When 清空浏览器
	When zhouxun扫描返利活动'返利活动6'的二维码

	When 微信用户批量消费jobs的商品
		| order_id | date       | consumer | product | payment | pay_type  |postage*   |price* | paid_amount*   | weizoom_card   | action     | order_status  |
		|   0001   | 今天       |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0002   | 明天       |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0003   | 明天       |  zhouxun | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       | 0000041,1234567| jobs,完成  |    已完成     |


	When 清空浏览器
	When bill绑定手机号'13563223668'

	When 清空浏览器
	When tom绑定手机号'13563223669'

	When 清空浏览器
	When zhouxun绑定手机号'13563223679'

	Given jobs登录系统
	Then jobs发放返利微众卡

	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	Then tom能获得返利微众卡
	"""
		[{
			"id":"0000019"
		}]

	"""
	
@mall @rebate
Scenario:8 带参数返利活动[扫码后成交金额]-已关注会员不可参与；首单；现金
	#已关注会员不可参与；
	#首单；
	#现金支付；
	Given jobs登录系统


	When 清空浏览器
	When bill关注jobs的公众号于'今天'
	When bill访问jobs的webapp
	When bill扫描返利活动'返利活动7'的二维码

	When 清空浏览器
	When tom扫描返利活动'返利活动7'的二维码


	When 清空浏览器
	When zhouxun扫描返利活动'返利活动7'的二维码

	When 微信用户批量消费jobs的商品
		| order_id | date       | consumer | product | payment | pay_type  |postage*  |price*  | paid_amount*   | weizoom_card   | action     | order_status  |
		|   0001   | 2天前     |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00   | 0.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0002   | 明天       |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00   | 0.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0003   | 明天       |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00   | 0.00   |     1.00       |                | jobs,完成  |    已完成     |
		|   0004   | 明天       |  zhouxun | 商品1,1 |   支付  |  支付宝   |   0.00   | 0.00   |     1.00       | 0000041,1234567| jobs,完成  |    已完成     |

	When 清空浏览器
	When bill绑定手机号'13563223668'

	When 清空浏览器
	When tom绑定手机号'13563223669'

	When 清空浏览器
	When zhouxun绑定手机号'13563223679'

	Given jobs登录系统
	Then jobs发放返利微众卡


	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	#只要订单号为002的tom可以获得奖励
	Then tom能获得返利微众卡
	"""
		[{
			"id":"0000022"
		}]

	"""


@mall @rebate
Scenario:9 带参数返利活动[扫码后成交金额]-已关注会员不可参与；首单；非现金
	#已关注会员不可参与；
	#首单；
	#非现金支付；
	Given jobs登录系统


	When 清空浏览器
	When bill关注jobs的公众号于'1天前'
	When bill访问jobs的webapp
	When bill扫描返利活动'返利活动8'的二维码

	When 清空浏览器
	When tom扫描返利活动'返利活动8'的二维码


	When 清空浏览器
	When zhouxun扫描返利活动'返利活动8'的二维码

	When 微信用户批量消费jobs的商品
		| order_id | date       | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 1天前     |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成     |    已完成     |
		|   0002   | 今天       |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs          |    待支付     |
		|   0003   | 明天       |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成     |    已完成     |
		|   0004   | 明天       |   tom    | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成     |    已完成     |
		|   0005   | 明天       |  zhouxun | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       | 0000041,1234567| jobs,完成     |    已完成     |
		|   0006   | 明天       |  zhouxun | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       | 0000041,1234567| jobs,完成     |    已完成     |


	When 清空浏览器
	When bill绑定手机号'13563223668'

	When 清空浏览器
	When tom绑定手机号'13563223669'

	When 清空浏览器
	When zhouxun绑定手机号'13563223679'

	Given jobs登录系统
	Then jobs发放返利微众卡


	When 清空浏览器
	Then tom能获得返利微众卡
	"""
		[{
			"id":"0000023"
		}]

	"""
	When 清空浏览器
	Then zhouxun能获得返利微众卡
	"""
		[{
			"id":"0000024"
		}]

	"""

	When 清空浏览器
	When zhouxun访问jobs的webapp
	When zhouxun申请退款订单'0006'
	Then zhouxun退款完成订单'0006'



	Given jobs登录系统
	#默认显示勾选仅显示扫码后的成交的订单
	Then jobs能获取'返利活动8'订单列表
	"""
		[{	
			"order_id":"0003",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
				}]
			}]
			"cash_payment":1.00,
			"card_payment":1.00
		},{
			"order_id":"0004",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
			}]
		},{
			"order_id":"0005",
			"status": "已完成",
			"final_price": 0.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
			}]
		},{
			"order_id":"0006",
			"status": "已完成",
			"final_price": 0.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
		}]
	"""
	Then jobs取消对返利活动订单进行'仅显示扫码后成交订单'操作
	#勾选仅显示扫码后的成交的订单
	#已退款完成的不算入
	Then jobs能获取'返利活动8'订单列表
	"""
		[{
			"order_id":"0003",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
		},{
			"order_id":"0004",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
		},{
			"order_id":"0005",
			"status": "已完成",
			"final_price": 0.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
		}]
	"""







@mall @rebate
Scenario:10 带参数返利活动-多个返利活动同时存在，并且同一个人扫多个返利活动的码且下单
	Given jobs登录系统

	When 清空浏览器
	When bill关注jobs的公众号于'今天'
	When bill访问jobs的webapp
	When bill扫描返利活动'返利活动1'的二维码
	When bill购买jobs的商品
		| order_id | date        | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 今天      |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成        |
		
	When 清空浏览器
	When bill扫描返利活动'返利活动2'的二维码
	When bill访问jobs的weapp
	When bill购买jobs的商品
		| order_id | date       | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0003   | 今天       |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00   | 1.00   |     1.00       |                | jobs,完成  |    已完成     |	



	Given jobs登录系统	
	#默认显示勾选仅显示扫码后的成交的订单
	Then jobs能获取'返利活动1'订单列表
	"""
		[{"order_id":"0002",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
			}]
		}]
	"""


	#默认显示勾选仅显示扫码后的成交的订单
	Then jobs能获取'返利活动2'订单列表
	"""
		[{
			"order_id":"0003",
			"status": "已完成",
			"final_price": 1.00,
			"products": [{
			"name": "商品1",
			"price": 1.00,
			"count": 1
			}]
		}]
	"""


@mall @rebate
Scenario:11 带参数返利活动-查看发放详情
	Given jobs登录系统
	When 清空浏览器
	When bill关注jobs的公众号于'1天前'
	When bill访问jobs的weapp
	When bill扫描返利活动'返利活动1'的二维码
	
	When bill购买jobs的商品
		| order_id | date         | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status  |
		|   0001   | 一天前       |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00    | 1.00    |     1.00        |                | jobs,完成  |    已完成     |


	When bill绑定手机号'13563223667'

	Given jobs登录系统
	Then jobs发放返利微众卡

	When 清空浏览器
	Then bill能获得返利微众卡
	"""
		[{
			"id":"0000001"
		}]

	"""
	Given jobs登录系统
	Then jobs能获得发放详情页
	"""
		[{
			"card_id":"0000003",
			"price":5.00,
			"rest_money":0.00,
			"used_money":0.00,
			"consumer":""
		}]
	"""
	When 清空浏览器
	When bill访问jobs的weapp
	When bill购买jobs的商品
		| order_id | date         | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card    | action     | order_status  |
		|   0001   | 3天后       |   bill   | 商品1,1 |   支付  |  支付宝   |   0.00    | 1.00    |     1.00        | 0000001,1234567 | jobs,完成  |    已完成     |

	Given jobs登录系统
	Then jobs能获得发放详情页
	"""
		[{
			"card_id":"0000001",
			"price":5.00,
			"rest_money":4.00,
			"used_money":1.00,
			"consumer":"bill"
		}]
	"""





	

	
