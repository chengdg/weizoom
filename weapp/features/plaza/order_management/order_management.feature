# __author__ : "王丽"

Feature: 自营平台订单管理
"""
	一、后台订单列表
		自营平台单或者多供货商品商品的订单，支付之前不拆单，支付之后拆单

		1 所有订单都按照母子订单的方式展示
			1）待支付的订单，【订单状态】显示在合并的订单状态对应处'待支付'
			2）支付之后的订单，【订单状态】和【操作按钮】拆分到各个子订单
			3）子订单状态和对应的按钮
				母订单状态         操作按钮
				待支付             支付、取消订单

				子订单状态         操作按钮
				已取消             无
				待发货             发货、申请退款
				已发货             标记完成、修改物流、申请退款
				已完成             申请退款
				退款中             无  （在财务审核中有按钮'退款完成'）
				退款完成           无

				备注特殊订单
				团购订单
				1） 组团成功的订单
					订单状态           操作按钮
					待发货             发货
					已发货             标记完成
					已完成             无
				2） 没有组团成功，自动退款
					订单状态           操作按钮
					退款中             无（在财务审核中无按钮）
					退款成功           无

			4）母订单的状态根据子订单的状态按照如下规则定义
				按照订单状态优先级排序规则，取优先级最低的子订单状态显示
				订单状态优先级由低到高排序为：
				待支付->待发货->已发货->退款中->已完成->退款完成->已取消
		2 对子订单进行退款
			1）某个子订单点击【申请退款】，弹出退款录入的界面
				（1）展示出当前订单应退金额：
					即：“退款录入，当前订单应退￥50.00”（即子订单的商品总金额(按照商品的售价（限时抢购、会员价）计算)+运费）
					    “母订单支付金额：现金￥30.00+微众卡￥20.00+优惠券￥15.00+积分￥10.00=￥75.00”（各种支付方式对应金额）
				（2）运营人员需要输入当前订单退款的各个方式对应的金额
					"现金"：输入的金额必须为大于零的整数或者小数（保留两位小数）；不能大于母订单的现金支付金额减去子订单退款完成的退款现金金额,否则给出红色提示'最多可退XX.XX元'
					"微众卡"：输入的金额必须为大于零的整数或者小数（保留两位小数）；不能大于当前母订单的微众卡支付金额减去子订单退款完成的退款的微众卡的金额,否则给出红色提示'最多可退XX.XX元'
					"优惠券"：输入的金额必须为大于零的整数或者小数（保留两位小数）；
					"积分"：积分比例按照系统当前的抵扣比例展示，输入积分值，只能是零或正整数，自动按照现在的积分比例计算出抵扣金额
				（3）当母订单中已经有订单的退款录入时，再对其他子订单操作退款时，展示添加【已退款金额】详情；录入时，现金、微众卡可退金额需要扣除“已退款金额”的相应部分
				"已退款金额"：现金￥15.00+微众卡￥15.00+优惠券￥15.00+积分￥5.00=￥50.00
				（4）"共计"：XX.XX元
				需要根据已填写的四项金额实时计算变化；当"共计金额"与"退款录入，当前订单应退"相等时，才可以提交退款申请；否则点击提交后提示“退款金额不等于XX.XX元”
		3 母订单【实付金额】数据，需减掉退款完成的子订单退掉的相应金额（即现金+微众卡金额）
		4 订单状态为"退款中"、"退款完成"的子订单，在订单状态后给出详情图标，鼠标悬停时展示其退款详细信息；
			退款详情信息的展示方式：
			1）所有退款项的金额都不为零；如：现金￥50.00+微众卡￥20.00+优惠券￥10.00+积分￥5.00=￥85.00
			2）某种退款项金额为0时，不显示该退款方式；如：现金￥10.00+优惠券￥5.20=￥15.20
			3）只有一种退款项时，直接显示退款项及金额，如：优惠券¥ 20.00

	二、后台订单详情
		1 母订单基本信息
			订单编号：母订单的订单编号
			订单状态：母订单的订单状态
			按钮：只有母订单的订单状态为'待支付'的时候显示按钮"支付"、"取消订单"
			订单时间轨迹：母订单订单状态变化的时间轨迹
				备注：这里的轨迹可能比较多，显示不下的时候怎么显示？？

		2 买家信息
			1）收货信息
				收货人：
				联系电话：
				收货地址：
				买家留言：
			2）发票信息
				发票抬头：没有发票抬头显示"--"
			3）商家备注
				点击编辑按钮可以添加商家备注

		3 物流信息
			分页签显示不同子订单的不同商家的物流信息，页签名为同步商家名称
			物流公司名称：发货时填写的物流公司名称
			运单号：发货时填写的运单号
			物流信息展示在下面

		4 在物流信息后的最后一个页签"订单操作日志"
			时间：精确到秒
			操作：买家和后台对订单的每步操作；不同商家的操作展示成如下格式"XXX-商家名"
			操作人：客户或者商家名

		5 订单信息
			1)支付方式：订单的支付方式
			2)供货商：商品订单对应的商家名称
			3)商品信息：商品名称和商品图片
			4)单价(元)/数量：商品的单价（商品的原始单价，不包含任何促销活动）和购买的数量
			5)单品优惠：显示使用单品积分"XX积分，抵扣XX.XX元"
						显示限时抢购优惠"直降XX.XX元"
			6)运费：订单的运费
			7)订单状态：分别显示各个子订单的订单状态；
					"退款中"和"退款完成"的订单的订单状态后显示查看图标，
					移动到查看图标显示退款的详情"现金￥30.00+微众卡￥0.00+优惠券￥15.00+积分￥10.00=￥55.00"
			8)整单优惠：显示优惠券优惠"多商品劵 :XX.XX（优惠券券码）"
						显示使用全店积分"XX积分，抵扣XX.XX"

			9)微众卡支付金额：显示微众卡支付金额"XX.XX"和查看图标，移动到查看图标，显示卡号
			10)共计商品：XX件；商品的个数总和
			11)商品金额：￥XX.XX；Σ商品单价*商品数量
			12)运费：+￥XX.XX（没有运费的时候显示成0.00）
			13)优惠金额：-￥XX.XX；（没有优惠的时候不显示）
			14)支付金额："现金￥XX.XX+微众卡￥XX.XX=￥XX.XX"；没有的项直接显示成0.00
			15)已退款金额："现金￥30.00+微众卡￥0.00+优惠券￥15.00+积分￥10.00=￥55.00";
							有退款完成的子订单，实付金额计算栏下方展示已退款金额合计详情

	三、手机端订单列表
		1 展示母订单状态
		2 当有子订单状态为“退款完成”时，“实付款”的数据应该扣减掉相应退的现金金额（即支付的现金金额）

	四、手机端订单详情
		1 母订单基本信息
			1）母订单的订单状态
			2）订单号：母订单的订单号
			3）收货人：收货人姓名、电话、地址
		2 订单商品信息
			1）商家名称
			2）本商家子订单状态，放在商家名称后，右对齐
			3）购买商家的商品列表
				商品信息：商品图片（活动商品标记：积分抵扣、优惠券、赠品）、商品名称、商品售价（原价、限时抢购价、会员价）、购买数量
				运费：运费信息和金额
				物流信息：没有物流信息时显示"暂无物流信息"
			4）支付方式：显示整个母订单的支付方式
			5）商品金额：￥XX.XX；Σ商品售价*购买数量
			6）运费：+￥XX.XX；包邮时显示0.00
			7）优惠抵扣：-￥XX.XX；包含积分、优惠券；没有时不显示此项
			8）微众卡抵扣：-￥XX.XX；没有时不显示此项
			9）实退金额：-￥XX.XX；
						当有子订单状态为“退款完成”时，结算栏需添加【实退金额】，展示数据为录入退款的相应现金的金额总计；为0时（即全部退微众卡或优惠券或积分），也展示，数据展示0.00就可以；
			10）实付金额：￥XX.XX；=商品金额+运费-优惠抵扣-微众卡抵扣-实退金额
			11）下单时间：精确到秒

"""

Background:
	Given 重置'weizoom_card'的bdd环境
	Given 重置'apiserver'的bdd环境
	Given jobs登录系统
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""
	When jobs开通使用微众卡权限
	When jobs已添加支付方式
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
		},{
			"type": "微众卡",
			"is_active": "启用"
		}]
		"""

	#创建微众卡
	Given test登录管理系统::weizoom_card
	When test新建通用卡::weizoom_card
		"""
		[{
			"name":"100元微众卡",
			"prefix_value":"100",
			"type":"virtual",
			"money":"100.00",
			"num":"5",
			"comments":"微众卡"
		}]
		"""
	#微众卡审批出库
	When test下订单::weizoom_card
		"""
		[{
			"card_info":[{
				"name":"100元微众卡",
				"order_num":"1",
				"start_date":"2015-04-07 00:00",
				"end_date":"2220-10-07 00:00"
			}],
			"order_info":{
				"order_id":"0001"
				}		
		}]
		"""
	And test批量激活订单'0001'的卡::weizoom_card

	When jobs已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	#所有商品开通所有支付方式
	When jobs已添加商品
		"""
		[{
			"name": "商品1-1",
			"supplier": "供货商1",
			"postage":"满100包邮，否则收取运费10",
			"price": 50.00,
			"stock_type": "有限",
			"stocks": 100
		},{
			"name": "商品1-2",
			"supplier": "供货商1",
			"postage":"满100包邮，否则收取运费10",
			"model": {
				"models": {
					"M": {
						"price": 10.00,
						"stock_type": "有限",
						"stocks": 100
					},
					"S": {
						"price": 20,
						"stock_type": "有限"
						"stocks": 100
					}
				}
			}
		},{
			"name": "商品2-1",
			"supplier": "供货商2",
			"price": 30.00,
			"stock_type": "有限",
			"stocks": 100
		},{
			"name": "商品2-2",
			"supplier": "供货商2",
			"price": 20.00,
			"stock_type": "有限",
			"stocks": 100
		}]
		"""

	#创建优惠券活动
	When jobs添加优惠券规则
		"""
		[{
			"name": "全店通用券1",
			"money": 10.00,
			"limit_counts": "无限",
			"count": 5,
			"start_date": "2013-10-10",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""

	#创建积分活动
	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品券",
			"start_date": "2010-01-01 10:00:00",
			"end_date": "1天后",
			"product_name": "商品1-2,商品2-2",
			"is_permanant_active": false,
			"discount": 50,
			"discount_money": 5.00
		}]
		"""

	Given bill关注jobs的公众号

	#给会员加积分
	Given jobs登录系统
	When jobs给"bill"加积分
		"""
		{
			"integral":500,
			"reason":""
		}
		"""

@order @allOrder
Scenario:1 单个供应商商品订单-微信支付+优惠券(不满足满额包邮)；退现金优惠券
	Given jobs登录系统
	When jobs创建优惠券发放规则发放优惠券
		"""
		{
			"name": "全店通用券1",
			"count": 1,
			"members": ["bill"]
		}
		"""

	When bill访问jobs的webapp::apiserver
	When bill购买jobs的商品::apiserver
		"""
		{
			"order_id":"001",
			"date":"2016-01-01 10:00:00",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"coupon": "coupon1_id_1",
			"products":[{
				"name":"商品1-1",
				"price":50.00,
				"count":1,
				"postage": 10.00
			}],
			"postage": 10.00,
			"customer_message": "bill的订单备注"
		}
		"""
	#待支付订单
		#手机端订单列表
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "待支付",
				"order_time":"2016-01-01 10:00:00",
				"products"[{
					"name":"商品1-1"
				}],
				"products_count": 1,
				"final_price": 50.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'001'::apiserver
			"""
			{
				"order_no": "001",
				"status":"待支付",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"products": [{
					"name": "商品1-1",
					"price": 50.00,
					"count": 1
				}],
				"methods_of_payment":"微信支付",
				"product_price": 50.00,
				"postage": 10.00,
				"save_money": -10.00,
				"final_price": 50.00,
				"order_time":"2016-01-01 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"001",
				"methods_of_payment":"微信支付",
				"order_time":"2016-01-01 10:00:00",
				"save_money": 10.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 50.00,
				"postage": 10.00,
				"status":"待支付",
				"actions": ["支付","取消订单"],
				"group":[{
					"供货商1":{
						"order_no":"001-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":1
						}]
					}
				}]
			}]
			"""
		Then jobs获得自营订单'001'
			"""
			{
				"order_no":"001",
				"status":"待支付",
				"actions": ["支付","取消订单"],
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"微信支付",
				"group":[{
					"供货商1":{
						"order_no":"001-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":1,
							"single_save":""
						}],
						"postage": 10.00,
						"status":"待支付"
					}
				}],
				"total_save":"多品券：10.00(coupon1_id_1)",
				"weizoom_card":"",
				"products_count":1,
				"product_price": 50.00,
				"postage": 10.00,
				"save_money": -10.00,
				"cash":50.00,
				"weizoom_card_money": 0.00,
				"final_price": 50.00
			}
			"""
		Then jobs能获得订单'001'操作日志
			| action                  | operator |
			| 下单                    | 客户     |

	#待发货订单
		When bill访问jobs的webapp::apiserver
		When bill使用支付方式'微信支付'进行支付订单'001'于'2016-01-02 10:00:00'::apiserver

		#手机端订单列表
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "待发货",
				"order_time":"2016-01-01 10:00:00",
				"products"[{
					"name":"商品1-1"
				}],
				"products_count": 1,
				"final_price": 50.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'001'::apiserver
			"""
			{
				"order_no": "001",
				"status":"待发货",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"products": [{
					"name": "商品1-1",
					"price": 50.00,
					"count": 1
				}],
				"methods_of_payment":"微信支付",
				"product_price": 50.00,
				"postage": 10.00,
				"save_money": -10.00,
				"final_price": 50.00,
				"order_time":"2016-01-01 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"001",
				"methods_of_payment":"微信支付",
				"order_time":"2016-01-01 10:00:00",
				"payment_time":"2016-01-02 10:00:00",
				"save_money": 10.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 50.00,
				"postage": 10.00,
				"status":"待发货",
				"group":[{
					"供货商1":{
						"order_no":"001-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":1
						}],
						"status":"待发货",
						"actions": ["发货","申请退款"],
					}
				}]
			}]
			"""
		Then jobs获得自营订单'001'
			"""
			{
				"order_no":"001",
				"status":"待发货",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"微信支付",
				"group":[{
					"供货商1":{
						"order_no":"001-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":1,
							"single_save":""
						}],
						"postage": 10.00,
						"status":"待发货"
					}
				}],
				"total_save":"多品券：10.00(coupon1_id_1)",
				"weizoom_card":"",
				"products_count":1,
				"product_price": 50.00,
				"postage": 10.00,
				"save_money": -10.00,
				"cash":50.00,
				"weizoom_card_money": 0.00,
				"final_price": 50.00
			}
			"""
		Then jobs能获得订单'001'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |

	#退款中
		Given jobs登录系统
		When jobs'申请退款'自营订单'001-供货商1'
			"""
			{
				"cash":10.00,
				"weizoom_card":0.00,
				"coupon_money":50.00,
				"intergal":0,
				"intergal_money":0.00
			}
			"""

		#手机端订单列表
		When bill访问jobs的webapp::apiserver
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "退款中",
				"order_time":"2016-01-01 10:00:00",
				"products"[{
					"name":"商品1-1"
				}],
				"products_count": 1,
				"final_price": 50.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'001'::apiserver
			"""
			{
				"order_no": "001",
				"status":"退款中",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"products": [{
					"name": "商品1-1",
					"price": 50.00,
					"count": 1
				}],
				"methods_of_payment":"微信支付",
				"product_price": 50.00,
				"postage": 10.00,
				"save_money": -10.00,
				"final_price": 50.00,
				"order_time":"2016-01-01 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"001",
				"methods_of_payment":"微信支付",
				"order_time":"2016-01-01 10:00:00",
				"payment_time":"2016-01-02 10:00:00",
				"save_money": 10.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 50.00,
				"postage": 10.00,
				"status":"退款中",
				"group":[{
					"供货商1":{
						"order_no":"001-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":1
						}],
						"status":"退款中",
						"refund_details":{
							"cash": 10.00,
							"weizoom_card": 0.00,
							"coupon_money": 50.00,
							"integral_money": 0.00
						},
						"actions": []
					}
				}]
			}]
			"""
		Then jobs获得自营订单'001'
			"""
			{
				"order_no":"001",
				"status":"退款中",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"微信支付",
				"group":[{
					"供货商1":{
						"order_no":"001-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":1,
							"single_save":""
						}],
						"postage": 10.00,
						"status":"退款中"
					}
				}],
				"total_save":"多品券：10.00(coupon1_id_1)",
				"weizoom_card":"",
				"products_count":1,
				"product_price": 50.00,
				"postage": 10.00,
				"save_money": -10.00,
				"cash":50.00,
				"weizoom_card_money": 0.00,
				"final_price": 50.00
			}
			"""
		Then jobs能获得订单'001'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |
			| 退款                    | jobs     |

	#退款完成
		Given jobs登录系统
		When jobs通过财务审核'退款成功'自营订单'001-供货商1'

		#手机端订单列表
		When bill访问jobs的webapp::apiserver
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "退款成功",
				"order_time":"2016-01-01 10:00:00",
				"products"[{
					"name":"商品1-1"
				}],
				"products_count": 1,
				"final_price": 40.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'001'::apiserver
			"""
			{
				"order_no": "001",
				"status":"退款成功",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"products": [{
					"name": "商品1-1",
					"price": 50.00,
					"count": 1
				}],
				"methods_of_payment":"微信支付",
				"product_price": 50.00,
				"postage": 10.00,
				"save_money": -10.00,
				"final_price": 40.00,
				"refund_money": 10.00,
				"order_time":"2016-01-01 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"001",
				"methods_of_payment":"微信支付",
				"order_time":"2016-01-01 10:00:00",
				"payment_time":"2016-01-02 10:00:00",
				"save_money": 10.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 50.00,
				"postage": 10.00,
				"status":"退款成功",
				"group":[{
					"供货商1":{
						"order_no":"001-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":1
						}],
						"status":"退款成功",
						"refund_details":{
							"cash": 10.00,
							"weizoom_card": 0.00,
							"coupon_money": 50.00,
							"integral_money": 0.00
						},
						"actions": []
					}
				}]
			}]
			"""
		Then jobs获得自营订单'001'
			"""
			{
				"order_no":"001",
				"status":"退款成功",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"微信支付",
				"group":[{
					"供货商1":{
						"order_no":"001-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":1,
							"single_save":""
						}],
						"postage": 10.00,
						"status":"退款成功"
					}
				}],
				"total_save":"多品券：10.00(coupon1_id_1)",
				"weizoom_card":"",
				"products_count":1,
				"product_price": 50.00,
				"postage": 10.00,
				"save_money": -10.00,
				"cash":50.00,
				"final_price": 50.00,
				"refund_details":{
					"cash": 10.00,
					"weizoom_card": 0.00,
					"coupon_money": 50.00,
					"integral_money": 0.00
				}
			}
			"""
		Then jobs能获得订单'001'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |
			| 退款                    | jobs     |
			| 退款完成                | jobs     |

@order @allOrder
Scenario:2 两个供应商商品订单-支付宝+积分(一个不满足满额包邮，一个无运费)；退优惠券，积分(积分按照现在的比例)

	When bill访问jobs的webapp::apiserver
	When bill购买jobs的商品::apiserver
		"""
		{
			"order_id":"002",
			"date":"2016-01-02 10:00:00",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "支付宝",
			"products":[{
				"name":"商品1-2",
				"model": "M",
				"price":10.00,
				"count":2,
				"integral": 20,
				"integral_money": 10.00,
				"postage": 10.00
			},{
				"name":"商品2-2",
				"price":20.00,
				"count":1,
				"integral": 20,
				"integral_money": 10.00,
				"postage": 0.00,
			}],
			"postage": 10.00,
			"customer_message": "bill的订单备注"
		}
		"""
	#待支付订单
		#手机端订单列表
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "待支付",
				"order_time":"2016-01-02 10:00:00",
				"products"[{
					"name":"商品1-2"
				},{
					"name":"商品2-2"
				}],
				"products_count": 3,
				"final_price": 30.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'002'::apiserver
			"""
			{
				"order_no": "002",
				"status":"待支付",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"products": [{
					"name": "商品1-2",
					"price": 10.00,
					"count": 2
				},{
					"name": "商品2-2",
					"price": 20.00,
					"count": 1
				}],
				"methods_of_payment":"支付宝",
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"final_price": 30.00,
				"order_time":"2016-01-02 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"002",
				"methods_of_payment":"支付宝",
				"order_time":"2016-01-02 10:00:00",
				"save_money": 20.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 30.00,
				"postage": 10.00,
				"status":"待支付",
				"actions": ["支付","取消订单"],
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2
						}]
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1
						}]
					}
				}]
			}]
			"""
		Then jobs获得自营订单'002'
			"""
			{
				"order_no":"002",
				"status":"待支付",
				"actions": ["支付","取消订单"],
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"支付宝",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 10.00,
						"status":"待支付"
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":10.00,
							"count":1,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 0.00,
						"status":"待支付"
					}
				}],
				"total_save":"",
				"weizoom_card":"",
				"products_count":3,
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"cash":30.00,
				"weizoom_card_money": 0.00,
				"final_price": 30.00
			}
			"""
		Then jobs能获得订单'001'操作日志
			| action                  | operator |
			| 下单                    | 客户     |

	#待发货订单
		When bill访问jobs的webapp::apiserver
		When bill访问jobs的webapp::apiserver
		When bill使用支付方式'支付宝'进行支付订单'002'于'2016-01-03 10:00:00'::apiserver

		#手机端订单列表
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "待发货",
				"order_time":"2016-01-02 10:00:00",
				"products"[{
					"name":"商品1-2"
				},{
					"name":"商品2-2"
				}],
				"products_count": 3,
				"final_price": 30.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'002'::apiserver
			"""
			{
				"order_no": "002",
				"status":"待发货",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"group":[{
					"供货商1":{
						"products": [{
							"name": "商品1-2",
							"price": 10.00,
							"count": 2
						}],
						"postage": 10.00
					},
					"供货商2":{
						"products": [{
							"name": "商品2-2",
							"price": 20.00,
							"count": 1
						}],
						"postage": 0.00
					}
				}],
				"methods_of_payment":"支付宝",
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"final_price": 30.00,
				"order_time":"2016-01-02 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"002",
				"methods_of_payment":"支付宝",
				"order_time":"2016-01-02 10:00:00",
				"payment_time":"2016-01-03 10:00:00",
				"save_money": 20.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 30.00,
				"postage": 10.00,
				"status":"待发货",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2
						}],
						"status":"待发货",
						"actions": ["发货","申请退款"]
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1
						}],
						"status":"待发货",
						"actions": ["发货","申请退款"]
					}
				}]
			}]
			"""
		Then jobs获得自营订单'002'
			"""
			{
				"order_no":"002",
				"status":"待发货",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"支付宝",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 10.00,
						"status":"待发货"
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 0.00,
						"status":"待发货"
					}
				}],
				"total_save":"",
				"weizoom_card":"",
				"products_count":3,
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"cash":30.00,
				"weizoom_card_money": 0.00,
				"final_price": 30.00
			}
			"""
		Then jobs能获得订单'001'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |

	#已发货
		Given jobs登录系统
		When jobs对订单进行发货
			"""
			{
				"order_no": "002-供货商1",
				"logistics": "申通快递",
				"number": "229388967650",
				"shipper": "jobs"
			}
			"""

		#手机端订单列表
		When bill访问jobs的webapp::apiserver
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "待发货",
				"order_time":"2016-01-02 10:00:00",
				"products"[{
					"name":"商品1-2"
				},{
					"name":"商品2-2"
				}],
				"products_count": 3,
				"final_price": 30.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'002'::apiserver
			"""
			{
				"order_no": "002",
				"status":"待发货",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"group":[{
					"供货商1":{
						"status":"已发货",
						"products": [{
							"name": "商品1-2",
							"price": 10.00,
							"count": 2
						}],
						"postage": 10.00
					},
					"供货商2":{
						"status":"待发货",
						"products": [{
							"name": "商品2-2",
							"price": 20.00,
							"count": 1
						}],
						"postage": 0.00
					}
				}],
				"methods_of_payment":"支付宝",
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"final_price": 30.00,
				"order_time":"2016-01-02 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"002",
				"methods_of_payment":"支付宝",
				"order_time":"2016-01-02 10:00:00",
				"payment_time":"2016-01-03 10:00:00",
				"save_money": 20.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 30.00,
				"postage": 10.00,
				"status":"待发货",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2
						}],
						"status":"已发货",
						"actions": ["标记完成"]
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1
						}],
						"status":"待发货",
						"actions": ["发货","申请退款"]
					}
				}]
			}]
			"""
		Then jobs获得自营订单'002'
			"""
			{
				"order_no":"002",
				"status":"待发货",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"支付宝",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 10.00,
						"status":"已发货"
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 0.00,
						"status":"待发货"
					}
				}],
				"total_save":"",
				"weizoom_card":"",
				"products_count":3,
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"cash":30.00,
				"weizoom_card_money": 0.00,
				"final_price": 30.00
			}
			"""
		Then jobs能获得订单'002'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |
			| 订单发货-供应商1        | jobs     |

	#已完成
		Given jobs登录系统
		When jobs完成订单'002-供货商1'
		When jobs对订单进行发货
			"""
			{
				"order_no": "002-供货商2",
				"logistics": "圆通快递",
				"number": "22200000000",
				"shipper": "jobs"
			}
			"""

		#手机端订单列表
		When bill访问jobs的webapp::apiserver
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "已发货",
				"order_time":"2016-01-02 10:00:00",
				"products"[{
					"name":"商品1-2"
				},{
					"name":"商品2-2"
				}],
				"products_count": 3,
				"final_price": 30.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'002'::apiserver
			"""
			{
				"order_no": "002",
				"status":"已发货",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"group":[{
					"供货商1":{
						"status":"已完成",
						"products": [{
							"name": "商品1-2",
							"price": 10.00,
							"count": 2
						}],
						"postage": 10.00
					},
					"供货商2":{
						"status":"已发货",
						"products": [{
							"name": "商品2-2",
							"price": 20.00,
							"count": 1
						}],
						"postage": 0.00
					}
				}],
				"methods_of_payment":"支付宝",
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"final_price": 30.00,
				"order_time":"2016-01-02 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"002",
				"methods_of_payment":"支付宝",
				"order_time":"2016-01-02 10:00:00",
				"payment_time":"2016-01-03 10:00:00",
				"save_money": 20.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 30.00,
				"postage": 10.00,
				"status":"已发货",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2
						}],
						"status":"已完成",
						"actions": ["申请退款"]
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1
						}],
						"status":"待发货",
						"actions": ["发货","申请退款"]
					}
				}]
			}]
			"""
		Then jobs获得自营订单'002'
			"""
			{
				"order_no":"002",
				"status":"已发货",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"支付宝",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 10.00,
						"status":"已完成"
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 0.00,
						"status":"已发货"
					}
				}],
				"total_save":"",
				"weizoom_card":"",
				"products_count":3,
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"cash":30.00,
				"weizoom_card_money": 0.00,
				"final_price": 30.00
			}
			"""
		Then jobs能获得订单'002'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |
			| 订单发货-供应商1        | jobs     |
			| 订单完成-供应商1        | jobs     |
			| 订单发货-供应商2        | jobs     |

	#退款中
		Given jobs登录系统
		Given jobs设定会员积分策略
			"""
			{
				"integral_each_yuan": 3
			}
			"""
		When jobs'申请退款'自营订单'002-供货商1'
			"""
			{
				"cash":10.00,
				"weizoom_card":0.00,
				"coupon_money":10.00,
				"intergal": 30,
				"intergal_money":10.00
			}
			"""
		When jobs完成订单'002-供货商2'

		#手机端订单列表
		When bill访问jobs的webapp::apiserver
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "退款中",
				"order_time":"2016-01-02 10:00:00",
				"products"[{
					"name":"商品1-2"
				},{
					"name":"商品2-2"
				}],
				"products_count": 3,
				"final_price": 30.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'002'::apiserver
			"""
			{
				"order_no": "002",
				"status":"退款中",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"group":[{
					"供货商1":{
						"status":"退款中",
						"products": [{
							"name": "商品1-2",
							"price": 10.00,
							"count": 2
						}],
						"postage": 10.00
					},
					"供货商2":{
						"status":"已完成",
						"products": [{
							"name": "商品2-2",
							"price": 20.00,
							"count": 1
						}],
						"postage": 0.00
					}
				}],
				"methods_of_payment":"支付宝",
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"final_price": 30.00,
				"order_time":"2016-01-02 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"002",
				"methods_of_payment":"支付宝",
				"order_time":"2016-01-02 10:00:00",
				"payment_time":"2016-01-03 10:00:00",
				"save_money": 20.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 30.00,
				"postage": 10.00,
				"status":"退款中",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2
						}],
						"status":"退款中",
						"refund_details":{
							"cash": 10.00,
							"weizoom_card": 0.00,
							"coupon_money": 10.00,
							"integral_money": 10.00
						},
						"actions": [],
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1
						}],
						"status":"已完成",
						"actions": ["申请退款"],
					}
				}]
			}]
			"""
		Then jobs获得自营订单'002'
			"""
			{
				"order_no":"002",
				"status":"退款中",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"支付宝",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 10.00,
						"status":"退款中"
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 0.00,
						"status":"已完成"
					}
				}],
				"total_save":"",
				"weizoom_card":"",
				"products_count":3,
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"cash":30.00,
				"final_price": 30.00
			}
			"""
		Then jobs能获得订单'002'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |
			| 订单发货-供应商1        | jobs     |
			| 完成-供应商1            | jobs     |
			| 订单发货-供应商2        | jobs     |
			| 退款-供应商1            | jobs     |
			| 完成-供应商2            | jobs     |

	#退款完成
		Given jobs登录系统
		When jobs通过财务审核'退款成功'自营订单'002-供货商1'

		#手机端订单列表
		When bill访问jobs的webapp::apiserver
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "已完成",
				"order_time":"2016-01-02 10:00:00",
				"products"[{
					"name":"商品1-2"
				},{
					"name":"商品2-2"
				}],
				"products_count": 3,
				"final_price": 20.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'002'::apiserver
			"""
			{
				"order_no": "002",
				"status":"已完成",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"group":[{
					"供货商1":{
						"status":"退款成功",
						"products": [{
							"name": "商品1-2",
							"price": 10.00,
							"count": 2
						}],
						"postage": 10.00
					},
					"供货商2":{
						"status":"已完成",
						"products": [{
							"name": "商品2-2",
							"price": 20.00,
							"count": 1
						}],
						"postage": 0.00
					}
				}],
				"methods_of_payment":"支付宝",
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"refund_money": 10.00,
				"final_price": 20.00,
				"order_time":"2016-01-02 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"002",
				"methods_of_payment":"支付宝",
				"order_time":"2016-01-02 10:00:00",
				"payment_time":"2016-01-03 10:00:00",
				"save_money": 20.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 20.00,
				"postage": 10.00,
				"status":"已完成",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2
						}],
						"status":"退款成功",
						"refund_details":{
							"cash": 10.00,
							"weizoom_card": 0.00,
							"coupon_money": 10.00,
							"integral_money": 10.00
						},
						"actions": []
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1
						}],
						"status":"已完成",
						"actions": ["申请退款"]
					}
				}]
			}]
			"""
		Then jobs获得自营订单'002'
			"""
			{
				"order_no":"002",
				"status":"已完成",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"支付宝",
				"group":[{
					"供货商1":{
						"order_no":"002-供货商1",
						"products":[{
							"name":"商品1-2",
							"price":10.00,
							"count":2,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 10.00,
						"status":"退款成功"
					},
					"供货商2":{
						"order_no":"002-供货商2",
						"products":[{
							"name":"商品2-2",
							"price":20.00,
							"count":1,
							"single_save":"20积分，抵扣10.00元"
						}],
						"postage": 0.00,
						"status":"已完成"
					}
				}],
				"total_save":"",
				"weizoom_card":"",
				"products_count":3,
				"product_price": 40.00,
				"postage": 10.00,
				"save_money": -20.00,
				"cash":20.00,
				"final_price": 20.00,
				"refund_details":{
					"cash": 10.00,
					"weizoom_card": 0.00,
					"coupon_money": 10.00,
					"integral_money": 10.00
				}
			}
			"""
		Then jobs能获得订单'002'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |
			| 订单发货-供应商1        | jobs     |
			| 完成-供应商1            | jobs     |
			| 订单发货-供应商2        | jobs     |
			| 退款-供应商1            | jobs     |
			| 完成-供应商2            | jobs     |
			| 退款完成-供货商1        | jobs     |

@order @allOrder
Scenario:3 两个供应商商品订单(限时抢购)-微众卡支付(一个满足满额包邮，一个无运费)
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1-1限时抢购",
			"promotion_title":"",
			"start_date": "2010-01-01 10:00:00",
			"end_date": "1天后",
			"product_name":"商品1-1",
			"member_grade": "全部会员",
			"count_per_purchase": 4,
			"promotion_price": 20.00,
			"limit_period": 1
		}]
		"""

	When bill访问jobs的webapp::apiserver
	When bill购买jobs的商品::apiserver
		"""
		{
			"order_id":"003",
			"date":"2016-01-03 10:00:00",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"weizoom_card_info":{
				"id":"100000001",
				"password":"1234567"
			},
			"products":[{
				"name":"商品1-1",
				"price":20.00,
				"count":2,
				"postage": 0.00
			},{
				"name":"商品2-1",
				"price":30.00,
				"count":1,
				"postage": 0.00
			}],
			"postage": 0.00,
			"customer_message": "bill的订单备注"
		}
		"""

	#待发货订单
		#手机端订单列表
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "待发货",
				"order_time":"2016-01-03 10:00:00",
				"products"[{
					"name":"商品1-1"
				},{
					"name":"商品2-1"
				}],
				"products_count": 3,
				"final_price": 0.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'003'::apiserver
			"""
			{
				"order_no": "003",
				"status":"待发货",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"group":[{
					"供货商1":{
						"products": [{
							"name": "商品1-1",
							"price": 20.00,
							"count": 2
						}],
						"postage": 0.00
					},
					"供货商2":{
						"products": [{
							"name": "商品2-1",
							"price": 30.00,
							"count": 1
						}],
						"postage": 0.00
					}
				}],
				"methods_of_payment":"优惠抵扣",
				"product_price": 70.00,
				"postage": 0.00,
				"weizoom_card": 70.00,
				"final_price": 0.00,
				"order_time":"2016-01-03 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"003",
				"methods_of_payment":"优惠抵扣",
				"order_time":"2016-01-03 10:00:00",
				"payment_time":"2016-01-03 10:00:00",
				"save_money": 60.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 70.00,
				"postage": 0.00,
				"status":"待发货",
				"group":[{
					"供货商1":{
						"order_no":"003-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":2
						}],
						"status":"待发货",
						"actions": ["发货","申请退款"]
					},
					"供货商2":{
						"order_no":"003-供货商2",
						"products":[{
							"name":"商品2-1",
							"price":30.00,
							"count":1
						}],
						"status":"待发货",
						"actions": ["发货","申请退款"]
					}
				}]
			}]
			"""
		Then jobs获得自营订单'003'
			"""
			{
				"order_no":"003",
				"status":"待发货",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"优惠抵扣",
				"group":[{
					"供货商1":{
						"order_no":"003-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":2,
							"single_save":"直降60.00元"
						}],
						"postage": 0.00,
						"status":"待发货"
					},
					"供货商2":{
						"order_no":"003-供货商2",
						"products":[{
							"name":"商品2-1",
							"price":30.00,
							"count":1,
							"single_save":""
						}],
						"postage": 0.00,
						"status":"待发货"
					}
				}],
				"total_save":"",
				"weizoom_card":"70.00",
				"products_count":3,
				"product_price": 130.00,
				"postage": 0.00,
				"save_money": -60.00,
				"cash":0.00,
				"weizoom_card_money": 70.00,
				"final_price": 70.00
			}
			"""
		Then jobs能获得订单'001'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |

	#退款中
		Given jobs登录系统
		When jobs'申请退款'自营订单'003-供货商1'
			"""
			{
				"cash":0.00,
				"weizoom_card":30.00,
				"coupon_money":10.00,
				"intergal": 0,
				"intergal_money":0.00
			}
			"""

		#手机端订单列表
		When bill访问jobs的webapp::apiserver
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "待发货",
				"order_time":"2016-01-03 10:00:00",
				"products"[{
					"name":"商品1-1"
				},{
					"name":"商品2-1"
				}],
				"products_count": 3,
				"final_price": 0.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'003'::apiserver
			"""
			{
				"order_no": "003",
				"status":"待发货",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"group":[{
					"供货商1":{
						"status":"退款中",
						"products": [{
							"name": "商品1-1",
							"price": 20.00,
							"count": 2
						}],
						"postage": 0.00
					},
					"供货商2":{
						"status":"待发货",
						"products": [{
							"name": "商品2-1",
							"price": 30.00,
							"count": 1
						}],
						"postage": 0.00
					}
				}],
				"methods_of_payment":"优惠抵扣",
				"product_price": 70.00,
				"postage": 0.00,
				"weizoom-card": -70.00,
				"final_price": 0.00,
				"order_time":"2016-01-03 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"003",
				"methods_of_payment":"优惠抵扣",
				"order_time":"2016-01-03 10:00:00",
				"payment_time":"2016-01-03 10:00:00",
				"save_money": 60.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 70.00,
				"postage": 0.00,
				"status":"待发货",
				"group":[{
					"供货商1":{
						"order_no":"003-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":2
						}],
						"status":"退款中",
						"refund_details":{
							"cash": 0.00,
							"weizoom_card": 30.00,
							"coupon_money": 10.00,
							"integral_money": 0.00
						},
						"actions": []
					},
					"供货商2":{
						"order_no":"003-供货商2",
						"products":[{
							"name":"商品2-1",
							"price":30.00,
							"count":1
						}],
						"status":"待发货",
						"actions": ["发货",申请退款"]
					}
				}]
			}]
			"""
		Then jobs获得自营订单'003'
			"""
			{
				"order_no":"003",
				"status":"待发货",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"优惠抵扣",
				"group":[{
					"供货商1":{
						"order_no":"003-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":5.00,
							"count":2,
							"single_save":"直降60.00元"
						}],
						"postage": 0.00,
						"status":"退款中"
					},
					"供货商2":{
						"order_no":"003-供货商2",
						"products":[{
							"name":"商品2-1",
							"price":30.00,
							"count":1,
							"single_save":""
						}],
						"postage": 0.00,
						"status":"待发货"
					}
				}],
				"total_save":"",
				"weizoom_card":"70.00",
				"products_count":3,
				"product_price": 130.00,
				"postage": 0.00,
				"save_money": -60.00,
				"cash":0.00,
				"weizoom_card_money":70.00,
				"final_price": 70.00
			}
			"""
		Then jobs能获得订单'002'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |
			| 退款-供应商1            | jobs     |

	#退款完成
		Given jobs登录系统
		When jobs通过财务审核'退款成功'自营订单'003-供货商1'

		#手机端订单列表
		When bill访问jobs的webapp::apiserver
		Then bill获得手机端订单列表::apiserver
			"""
			[{
				"status": "待发货",
				"order_time":"2016-01-0310:00:00",
				"products"[{
					"name":"商品1-1"
				},{
					"name":"商品2-1"
				}],
				"products_count": 3,
				"final_price": 0.00
			}]
			"""

		#手机端订单详情
		Then bill获取手机端订单'003'::apiserver
			"""
			{
				"order_no": "003",
				"status":"待发货",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"group":[{
					"供货商1":{
						"status":"退款成功",
						"products": [{
							"name": "商品1-1",
							"price": 20.00,
							"count": 2
						}],
						"postage": 0.00
					},
					"供货商2":{
						"status":"待发货",
						"products": [{
							"name": "商品2-1",
							"price": 30.00,
							"count": 1
						}],
						"postage": 0.00
					}
				}],
				"methods_of_payment":"优惠抵扣",
				"product_price": 70.00,
				"postage": 0.00,
				"refund_money": 0.00,
				"final_price": 0.00,
				"order_time":"2016-01-03 10:00:00"
			}
			"""

		#后台订单列表
		Given jobs登录系统
		Then jobs获得自营订单列表
			"""
			[{
				"order_no":"003",
				"methods_of_payment":"优惠抵扣",
				"order_time":"2016-01-03 10:00:00",
				"payment_time":"2016-01-03 10:00:00",
				"save_money": 60.00,
				"buyer":"bill",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"final_price": 40.00,
				"postage": 0.00,
				"status":"待发货",
				"group":[{
					"供货商1":{
						"order_no":"003-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":2
						}],
						"status":"退款成功",
						"refund_details":{
							"cash": 0.00,
							"weizoom_card": 30.00,
							"coupon_money": 10.00,
							"integral_money": 0.00
						},
						"actions": []
					},
					"供货商2":{
						"order_no":"003-供货商2",
						"products":[{
							"name":"商品2-1",
							"price":30.00,
							"count":1
						}],
						"status":"待发货",
						"actions": ["发货",申请退款"]
					}
				}]
			}]
			"""
		Then jobs获得自营订单'003'
			"""
			{
				"order_no":"003",
				"status":"待发货",
				"ship_name":"bill",
				"ship_tel":"13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"invoice":"--",
				"business_message":"",
				"methods_of_payment":"优惠抵扣",
				"group":[{
					"供货商1":{
						"order_no":"003-供货商1",
						"products":[{
							"name":"商品1-1",
							"price":50.00,
							"count":2,
							"single_save":"直降60.00元"
						}],
						"postage": 0.00,
						"status":"退款成功"
					},
					"供货商2":{
						"order_no":"003-供货商2",
						"products":[{
							"name":"商品2-1",
							"price":30.00,
							"count":1,
							"single_save":""
						}],
						"postage": 0.00,
						"status":"待发货"
					}
				}],
				"total_save":"",
				"weizoom_card":"70.00",
				"products_count":3,
				"product_price": 130.00,
				"postage": 0.00,
				"save_money": -60.00,
				"cash":0.00,
				"weizoom_card_money":40.00,
				"final_price": 40.00,
				"refund_details":{
					"cash": 0.00,
					"weizoom_card": 30.00,
					"coupon_money": 10.00,
					"integral_money": 0.00
				}
			}
			"""
		Then jobs能获得订单'002'操作日志
			| action                  | operator |
			| 下单                    | 客户     |
			| 支付                    | 客户     |
			| 退款-供应商1            | jobs     |
			| 退款完成-供货商1        | jobs     |
