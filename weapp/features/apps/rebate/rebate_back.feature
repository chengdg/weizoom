#author: 张雪 2016-5-6

Feature:返利活动-添加和修改
"""
	添加返利活动
	1.【二维码名称】：带参数二维码的名称，只在列表中使用；
	2.【已关注会员可参与】：设置已关注会员是否可参与；默认"否"；
	3.【订单返利条件】：已关注会员可参与和条件为并的关系，必须满足所有的条件才能获得返利资格
						(1)购买次数设置为不限：可以任意次数的购买商品；
						   购买次数设置为首单：则只有扫码后关注并首次下单的人；
						(2)订单金额设置为现金：只能现金支付的才能获得返利资格；
						   订单金额设置不是现金：可以任意支付方式；
						(3)设置订单满额条件：只有满足购买金额才能获得奖励资格；
	4.【发放微众卡号段】：
						(1)微众卡号段：微众卡为下单成功后发放卡的号段与批次；如库存不足时，补充库存后继续补发；
						(2)发放详情：显示该卡批次使用详情；
	5.【扫码后回复】：扫码后回复；文本或者图文；必填；字数不能超过600字

"""
#is_attention_in		已关注会员可参与
#order_rebate_condition 订单返利条件
#is_limit_first_buy		订单返利条件是否限制首单
#is_limit_cash			订单金额是否为现金
#order_rebate           订单返利
#rebate_order_price		订单返利需满多少元
#rebate_money			返利返多少元
#weizoom_card_id_from	发放微众卡号段
#weizoom_card_id_to		发放微众卡号段
#scan_code_reply 		扫码后回复

Background:
	Given jobs登录系统
	And jobs已创建微众卡
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
			}]
		}
		"""
	When jobs开通使用微众卡权限

@mall2 @rebate_back
Scenario:1 创建返利活动

	Given jobs登录系统
	When jobs新建返利活动
		"""
		[{
			"code_name":"返利活动1",
			"is_attention_in":"true",
			"is_limit_first_buy":"true",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000001",
			"weizoom_card_id_to":"0000005",
			"start_time":"今天",
			"end_time":"2天后",
			"reply_type": "文字",
			"scan_code_reply": "返利活动1"
		}]
		"""
	Then jobs获得返利活动列表
		"""
		[{
			"code_name": "返利活动1",
			"attention_number":0,
			"order_money": 0.00,
			"first_buy_num":0,
			"start_time":"今天",
			"end_time":"2天后"
		}]
		"""

@mall2 @rebate_back
Scenario:2 编辑返利活动

	Given jobs登录系统
	When jobs新建返利活动
		"""
		[{
			"code_name":"返利活动1",
			"is_attention_in":"true",
			"is_limit_first_buy":"true",
			"is_limit_cash":"true",
			"order_rebate":{
				"rebate_order_price":"10.00",
				"rebate_money":"5.00"
			},
			"weizoom_card_id_from":"0000001",
			"weizoom_card_id_to":"0000005",
			"start_time":"今天",
			"end_time":"2天后",
			"reply_type": "文字",
			"scan_code_reply": "返利活动1"
		}]
		"""
	Then jobs获得返利活动列表
		"""
		[{
			"code_name": "返利活动1",
			"attention_number":0,
			"order_money": 0.00,
			"first_buy_num":0,
			"start_time":"今天",
			"end_time":"2天后"
		}]
		"""
	When jobs编辑返利活动"返利活动1"
		"""
		[{
			"code_name":"返利活动2",
			"is_attention_in":"false",
			"is_limit_first_buy":"false",
			"is_limit_cash":"false",
			"order_rebate":{
				"rebate_order_price":"20.00",
				"rebate_money":"10.00"
			},
			"weizoom_card_id_from":"0000001",
			"weizoom_card_id_to":"0000002",
			"start_time":"今天",
			"end_time":"3天后",
			"reply_type": "文字",
			"scan_code_reply": "返利活动2"
		}]
		"""
	Then jobs获得返利活动列表
		"""
		[{
			"code_name": "返利活动2",
			"attention_number":0,
			"order_money": 0.00,
			"first_buy_num":0,
			"start_time":"今天",
			"end_time":"3天后"
		}]
		"""