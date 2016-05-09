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
			"price":90.00
		},{
			"id":"0000003",
			"password":"1234567",
			"status":"未使用",
			"price":100.00
		}]
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
			"weizoom_card_id_from":"000000001",
			"weizoom_card_id_to":"000000005",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-08 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动1"
		},{
			"code_name":"返利活动2",
			"is_attention_in":"true",
			"is_limit_first_buy	":"true",
			"is_limit_cash":"否",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
				}
			"weizoom_card_id_from":"000000006",
			"weizoom_card_id_to":"000000010",
			"card_counts":5,
			"start_time":"2016-05-07 00:00:00",
			"end_time":"2016-05-08 00:00:00",
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
			"weizoom_card_id_from":"000000011",
			"weizoom_card_id_to":"000000015",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-08 00:00:00",
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
			"weizoom_card_id_from":"000000016",
			"weizoom_card_id_to":"000000020",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-08 00:00:00",
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
			"weizoom_card_id_from":"000000021",
			"weizoom_card_id_to":"000000025",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"22016-05-08 00:00:00",
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
			"weizoom_card_id_from":"000000026",
			"weizoom_card_id_to":"000000030",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-08 00:00:00",
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
			"weizoom_card_id_from":"000000031",
			"weizoom_card_id_to":"000000035",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-08 00:00:00",
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
			"weizoom_card_id_from":"000000036",
			"weizoom_card_id_to":"000000040",
			"card_counts":5,
			"start_time":"2016-05-06 00:00:00",
			"end_time":"2016-05-08 00:00:00",
			"reply_type": "文字",
			"scan_code_reply": "返利活动8"
		}]
	"""
	When jobs已添加单图文
	"""
		[{
			"title":"返利活动1单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容",
			"jump_url":"返利活动-返利活动1"
		},{
			"title":"返利活动2单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容",
			"jump_url":"返利活动-返利活动2"
		},{
			"title":"返利活动3单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文3文本摘要",
			"content":"单条图文3文本内容",
			"jump_url":"返利活动-返利活动3"
		},{
			"title":"返利活动4单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文4文本摘要",
			"content":"单条图文4文本内容",
			"jump_url":"返利活动-返利活动4"
		},{
			"title":"返利活动5单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文5文本摘要",
			"content":"单条图文5文本内容",
			"jump_url":"返利活动-返利活动5"
		},{
			"title":"返利活动6单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文6文本摘要",
			"content":"单条图文6文本内容",
			"jump_url":"返利活动-返利活动6"
		},{
			"title":"返利活动7单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文7文本摘要",
			"content":"单条图文7文本内容",
			"jump_url":"返利活动-返利活动7"
		},{
			"title":"返利活动8单图文",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文8文本摘要",
			"content":"单条图文8文本内容",
			"jump_url":"返利活动-返利活动8"
		}]
	"""
	When jobs已添加关键词自动回复规则
	"""
		[{
			"rules_name":"返利活动1",
			"keyword": [{
					"keyword": "返利活动1",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"返利活动1单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"返利活动2",
			"keyword": [{
					"keyword": "返利活动2",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"返利活动2单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"返利活动3",
			"keyword": [{
					"keyword": "返利活动3",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"返利活动3单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"返利活动4",
			"keyword": [{
					"keyword": "返利活动4",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"返利活动4单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"返利活动5",
			"keyword": [{
					"keyword": "返利活动5",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"返利活动5单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"返利活动6",
			"keyword": [{
					"keyword": "返利活动6",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"返利活动6单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"返利活动7",
			"keyword": [{
					"keyword": "返利活动7",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"返利活动7单图文",
					"reply_type":"text_picture"
				}]
		},{
			"rules_name":"返利活动8",
			"keyword": [{
					"keyword": "返利活动8",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_content":"返利活动8单图文",
					"reply_type":"text_picture"
				}]
		}]
	"""

	When tom关注jobs的公众号于'2016-05-05 10:00:00'
	When bill关注jobs的公众号于'2016-05-06 10:00:00'
	When bill取消关注jobs的公众号
	When mayun关注jobs的公众号于'2016-05-10 10:00:00'



	#扫码关注成为会员
	When 清空浏览器
	And zhouxun扫描带参数返利活动"返利活动1"于2016-05-06 10:00:00
	And zhouxun访问jobs的webapp


	#已关注或者取消关注的会员，扫码
	When bill扫描带参数返利活动"返利活动1"于2016-05-06 10:00:00
	When tom扫描带参数返利活动"返利活动1"于2016-05-06 10:00:00
	When bigs扫描带参数返利活动"返利活动1"于2016-05-06 10:00:00


	#会员购买
	When 微信用户批量消费jobs的商品
		| order_id |    date    | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    |  action      | order_status* |
		|   0001   | 2015-06-01 |   bill   | 商品1,1 |         |  支付宝   |   10.00   | 100.00  |     110.00      |              |    待支付     |
		|   0002   | 2015-06-02 |   bill   | 商品1,1 |         |  支付宝   |   10.00   | 100.00  |     110.00      | jobs,取消    |    已取消     |
		|   0003   | 2015-06-03 |   bill   | 商品2,2 |   支付  |  微信支付 |   15.00   | 100.00  |     215.00      | jobs,发货    |    已发货     |
		|   0004   | 2015-06-04 |   bill   | 商品2,1 |   支付  |  货到付款 |   15.00   | 100.00  |     115.00      | jobs,完成    |    已完成     |
		|   0005   | 2015-06-05 |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 100.00  |     110.00      | jobs,退款    |    退款中     |
		|   0006   | 今天       |  marry   | 商品1,1 |   支付  |  支付宝   |   10.00   | 100.00  |     110.00      | jobs,完成退款|   退款成功    |
		|   0007   | 今天       |   zhouxun   | 商品1,1 |   支付  |  货到付款 |   10.00   | 100.00  |     110.00      |              |    待发货     |
		|   0008   | 今天       |   tom    | 商品1,1 |   支付  |  支付宝   |   10.00   | 100.00  |     110.00      |              |    待发货     |
		|   0009   | 今天       |   tom    | 商品2,1 |   支付  |  货到付款 |   15.00   | 100.00  |     115.00      | jobs,取消    |    已取消     |
		|   0010   | 今天       |   tom    | 商品2,1 |   支付  |  货到付款 |   15.00   | 100.00  |     115.00      | jobs,发货    |    已发货     |

@mall @rebate
Scenario:1 管理员能够查看到所有扫过该码并关注过的微信用户信息，带参数返利活动[关注人数]-已关注的会员数量不增加；
	#设置已关注会员可参与
	#购买次数为首单
	#订单金额为现金
	#满10元返5元
	Given jobs登录系统
	#未关注微信账号扫码关注，关注数量增加
	When 清空浏览器
	When bill扫描返利活动"返利活动1"
	When bill访问jobs的webapp
	When bill扫描返利活动"返利活动1"
	

	Given jobs登录系统
	Then jobs获得返利活动列表
	"""
		[{
			"code_name": "返利活动1",
			"attention_number": 1
		}]
	"""
	#已关注会员扫码，关注数量不增加
	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom扫描返利活动"返利活动1"
	
	Given jobs登录系统
	Then jobs获得返利活动列表
	"""
		[{
			"code_name": "返利活动1",
			"attention_number": 1
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
			"attention_number": 2
		}]
	"""

	When 微信用户批量消费jobs的商品
		| order_id | date       | consumer | product | payment | pay_type  |postage*   |price*   | paid_amount*    | weizoom_card   | action     | order_status* |
		|   0001   | 今天       |   bill   | 商品1,1 |   支付  |  支付宝   |   10.00   | 100.00  |     110.00      | 0000001,1234567| jobs,发货  |    已发货     |
		|   0002   | 今天       |   tom    | 商品1,1 |   支付  |  支付宝   |   10.00   | 100.00  |     110.00      |                | jobs,发货  |    已发货     |
		|   0003   | 今天       |  zhouxun | 商品1,1 |   支付  |  微众卡   |   10.00   | 100.00  |     110.00      |                | jobs,发货  |    已发货     |    
		

	When jobs对'返利活动1'的'关注人数'操作
	#仅显示扫码后成交订单-勾选
	Then jobs能获取'仅显示通过二维码新关注会员'列表
	"""
		[{
			"fans_name": "zhouxun",
			"buy_number": 1,
			"integral": 0,
			"price":110.00
		}]
	"""
	#显示所有的的会员
	#仅显示扫码后成交订单-勾选
	Then jobs能获取会员列表
	"""
		[{
			"fans_name": "zhouxun",
			"buy_number": 1,
			"integral": 0,
			"price":110.00
		},{
			"fans_name": "tom",
			"buy_number": 1,
			"integral": 0,
			"price":110.00
		},{
			"fans_name": "bill",
			"buy_number": 1,
			"integral": 0,
			"price":110.00
		}]
	"""



@mall @rebate
Scenario:1 管理员能够查看到所有扫过该码并关注过的微信用户信息，带参数返利活动[关注人数]-已关注的会员数量不增加；


	

	
