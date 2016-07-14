# __author__ : "王新蕊"
# __author__ : "王丽"

Feature: 群发优惠券
	"""
		会员列表的群发优惠券
		1、给会员列表中的会员群发优惠券
			（1）给选中的人发优惠券(已取消关注的除外)
				给勾选的会员发优惠券，多页会员的只能给当前页会员勾选，自动过滤"已取消关注"的
				没有勾选会员或者勾选的会员中没有关注状态的会员，给出提示"请先选择会员"
			（2）给筛选出来的所有人发优惠券(已取消关注的除外)
				给筛选结果中所有人，包含多页会员，自动过滤"已取消关注"的
				筛选结果的会员中没有关注状态的会员，给出提示"请先选择会员"
		2、选择优惠券二级窗体
			（1）只列出处于"进行中"和"未开始"的优惠券，不列出处于"已过期"、"已失效"状态的优惠券，
				按照优惠券创建顺序的倒序排列
			（2）选择优惠券列表
				【优惠券名称】：优惠券的名称
				【类型】：优惠券的类型：全店通用券、单品券
				【价值】：优惠券的面值
				【有效期】：优惠券的有效期：优惠券活动的开始和结束日期时间
				【限领】：每人限领的张数
				【发放张数】：默认是1，有加减按钮
					1）当"发放张数等于限领"时，不能再增加
					2）当（【发放张数】*【发放人数】）=（优惠券库存），或不够每人再增加一个时
						'+'置灰，再点击'+'给出红色提示"库存不足"
						【操作】列的"选择"按钮使能可以选取
					3）当开始弹出窗体（【默认发放张数'1'】*【发放人数】）< （优惠券库存）时,
						此列直接只显示红色提示"库存不足"，
						【操作】列的"选择"按钮不显示
				【操作】：选取按钮，单选，只能选择一个优惠券，选择一个，在选择另一个，前面选择的自动变为取消选择状态
					1）"选取"按钮可以选择时，是蓝色，点击选择之后变为灰色"已选择"
					2）灰色"已选择"按钮，点击取消选取，按钮变为蓝色"选择"按钮
			（3）选择优惠券窗体上的发送会员相关提示信息
				无论选择的是"给选中的人发优惠券(已取消关注的除外)"，还是"给筛选出来的所有人发优惠券(已取消关注的除外)"
					1）在过滤取消关注会员后，只有一个发送会员时，提示"您将为XXX发放优惠券"，XXX代表会员昵称
					2）在过滤取消关注会员后，有两个以上发送会员时，提示"您将为X人发放优惠券"，X代表会员人数
			（4）点击"发送"按钮，提示"优惠券发放成功"
	"""

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		},{
			"name": "商品2",
			"price": 200.00
		},{
			"name": "商品3",
			"price": 200.00
		},{
			"name": "商品4",
			"price": 200.00
		},{
			"name": "商品5",
			"price": 200.00
		}]
		"""

	#添加"进行中"单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券1",
				"money": 10.00,
				"limit_counts": "无限",
				"count": 10,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon1_id_",
				"coupon_product": "商品1"
			}]
			"""
		Then jobs能获得优惠券'单品券1'的码库
			"""
			{
				"coupon1_id_1": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_2": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_3": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_4": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_5": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_6": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_7": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_8": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_9": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_10": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#添加"已过期"的单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券2",
				"money": 10.00,
				"limit_counts": "无限",
				"count": 5,
				"start_date": "2天前",
				"end_date": "1天前",
				"coupon_id_prefix": "coupon2_id_",
				"coupon_product": "商品2"
			}]
			"""
		Then jobs能获得优惠券'单品券2'的码库
			"""
			{
				"coupon2_id_1": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_2": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_3": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_4": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_5": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#添加"进行中"数量不足单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券3",
				"money": 10.00,
				"limit_counts": 1,
				"count": 3,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon3_id_",
				"coupon_product": "商品3"
			}]
			"""
		Then jobs能获得优惠券'单品券3'的码库
			"""
			{
				"coupon3_id_1": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon3_id_2": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon3_id_3": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#添加"未开始"单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券4",
				"money": 10.00,
				"limit_counts": "无限",
				"count": 2,
				"start_date": "1天后",
				"end_date": "2天后",
				"coupon_id_prefix": "coupon4_id_",
				"coupon_product": "商品4"
			}]
			"""
		Then jobs能获得优惠券'单品券4'的码库
			"""
			{
				"coupon4_id_1": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon4_id_2": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#添加"已失效"单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券5",
				"money": 10.00,
				"limit_counts": "无限",
				"count": 2,
				"start_date": "1天前",
				"end_date": "2天后",
				"coupon_id_prefix": "coupon5_id_",
				"coupon_product": "商品5"
			}]
			"""
		When jobs失效优惠券'单品券5'
		Then jobs能获得优惠券'单品券5'的码库
			"""
			{
				"coupon5_id_1": {
					"money": 10.00,
					"status": "已失效",
					"consumer": "",
					"target": ""
				},
				"coupon5_id_2": {
					"money": 10.00,
					"status": "已失效",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#构造系统会员
		Given nokia关注jobs的公众号
		And tom关注jobs的公众号
		And tom2关注jobs的公众号
		And tom3关注jobs的公众号
		And tom5关注jobs的公众号

		And tom5取消关注jobs的公众号

@mall2 @memberList @promotionCoupon
Scenario:1 选择优惠券的列表
	Given jobs登录系统

	#优惠券库存满足人数发放，已过期、已失效的优惠不能进入选择优惠券列表，
	#只有"进行中"和"未开始"的优惠券可以选择
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"全部"
			}]
			"""


		When jobs选择会员
			| member_name | member_rank |
			|     tom     |   普通会员  |
			|     tom5    |   普通会员  |

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给选中的人发优惠券(已取消关注的除外)"
			}]
			"""
		Then jobs获得发送提示您将为'tom'发放优惠券
		Then jobs获得选择优惠券列表
			"""
			[{
				"name":"单品券4",
				"type":"单品券",
				"money":10.00,
				"start_date": "1天后",
				"end_date": "2天后",
				"limit_counts":"不限",
				"is_select":"true"
			},{
				"name":"单品券3",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts": 1,
				"is_select":"true"
			},{
				"name":"单品券1",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts":"不限",
				"is_select":"true"
			}]
			"""

	#"进行中"和"未开始"的优惠券进入选择优惠券列表，库存不足的不能选择
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部"
			}]
			"""

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给筛选出来的所有人发优惠券(已取消关注的除外)"
			}]
			"""
		Then jobs获得发送提示您将为'4'人发放优惠券
		Then jobs获得选择优惠券列表
			"""
			[{
				"name":"单品券4",
				"type":"单品券",
				"money":10.00,
				"start_date": "1天后",
				"end_date": "2天后",
				"limit_counts":"不限",
				"is_select":"false"
			},{
				"name":"单品券3",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts": 1,
				"is_select":"false"
			},{
				"name":"单品券1",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts":"不限",
				"is_select":"true"
			}]
			"""

	#筛选结果只有一人，选择给所有的人发优惠券，也是提示接收的者的名字
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom3",
				"status":"全部"
			}]
			"""

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给筛选出来的所有人发优惠券(已取消关注的除外)"
			}]
			"""
		Then jobs获得发送提示您将为'tom3'发放优惠券
		Then jobs获得选择优惠券列表
			"""
			[{
				"name":"单品券4",
				"type":"单品券",
				"money":10.00,
				"start_date": "1天后",
				"end_date": "2天后",
				"limit_counts":"不限",
				"is_select":"true"
			},{
				"name":"单品券3",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts": 1,
				"is_select":"true"
			},{
				"name":"单品券1",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts":"不限",
				"is_select":"true"
			}]
			"""

@mall2 @memberList @promotionCoupon
Scenario:2 给筛选出选中的部分会员发送优惠券

	Given jobs登录系统

	#给筛选出来的选中的部分会员发放优惠券
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"全部"
			}]
			"""
		When jobs选择会员
			| member_name | member_rank |
			|     tom     |   普通会员  |
			|     tom5    |   普通会员  |

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给选中的人发优惠券(已取消关注的除外)",
				"coupon_name":"单品券1",
				"count":2
			}]
			"""
		#Then jobs优惠券发放成功

	#校验会员领取优惠券
		When tom访问jobs的webapp
		Then tom能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_1",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon1_id_2",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom2访问jobs的webapp
		Then tom2能获得webapp优惠券列表
			"""
			[ ]
			"""

		When tom3访问jobs的webapp
		Then tom3能获得webapp优惠券列表
			"""
			[ ]
			"""

		When tom5访问jobs的webapp
		Then tom5能获得webapp优惠券列表
			"""
			[ ]
			"""

		When nokia访问jobs的webapp
		Then nokia能获得webapp优惠券列表
			"""
			[ ]
			"""
	#校验jobs后台发放优惠券的情况
		Given jobs登录系统
		Then jobs能获得优惠券'单品券1'的码库
			"""
			{
				"coupon1_id_1": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon1_id_2": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon1_id_3": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_4": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_5": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_6": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_7": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_8": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_9": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_10": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

@mall2 @memberList @promotionCoupon
Scenario:3 给筛选出会员发送优惠券

	Given jobs登录系统

	#给筛选出来的会员发放优惠券
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"全部"
			}]
			"""
		When jobs选择会员
			| member_name | member_rank |

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给筛选出来的所有人发优惠券(已取消关注的除外)",
				"coupon_name":"单品券1",
				"count":2
			}]
			"""
		#Then jobs优惠券发放成功

	#校验会员领取优惠券
		When tom访问jobs的webapp
		Then tom能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_1",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon1_id_2",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom2访问jobs的webapp
		Then tom2能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_3",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon1_id_4",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom3访问jobs的webapp
		Then tom3能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_5",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon1_id_6",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom5访问jobs的webapp
		Then tom5能获得webapp优惠券列表
			"""
			[ ]
			"""

		When nokia访问jobs的webapp
		Then nokia能获得webapp优惠券列表
			"""
			[ ]
			"""
	#校验jobs后台发放优惠券的情况
		Given jobs登录系统
		Then jobs能获得优惠券'单品券1'的码库
			"""
			{
				"coupon1_id_1": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon1_id_2": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon1_id_3": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom2"
				},
				"coupon1_id_4": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom2"
				},
				"coupon1_id_5": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom3"
				},
				"coupon1_id_6": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom3"
				},
				"coupon1_id_7": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_8": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_9": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_10": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

@memberList @promotionCoupon
Scenario:4 给部分会员发放'仅未下单用户可领取的'优惠券
	Given jobs登录系统
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "未下单用户全体券",
			"money": 100.00,
			"each_limit": "1",
			"limit_counts": 10,
			"is_no_order_user":"true",
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon4_id_"
		}]
		"""
	#给存在不同订单状态的用户发放优惠券
		#未支付订单用户，可以领取优惠券
			When bill访问jobs的webapp::apiserver
			When bill购买jobs的商品::apiserver
				"""
				{
					"order_id":"001",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then bill成功创建订单::apiserver
				"""
				{
					"order_no":"001",
					"status": "待支付",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

		#待发货订单用户，不可以领取优惠券
			When tom访问jobs的webapp::apiserver
			When tom购买jobs的商品::apiserver
				"""
				{
					"order_id":"002",
					"pay_type": "货到付款",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom成功创建订单::apiserver
				"""
				{
					"order_no":"002",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

		#已发货订单用户，不可以领取优惠券
			Given tom1关注jobs的公众号
			When tom1访问jobs的webapp::apiserver
			When tom1购买jobs的商品::apiserver
				"""
				{
					"order_id":"003",
					"pay_type": "货到付款",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom1成功创建订单::apiserver
				"""
				{
					"order_no":"003",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "003",
					"logistics": "申通快递",
					"number": "229388967650",
					"shipper": "jobs"
				}
				"""

		#已完成订单用户，不可以领取优惠券
			Given tom2关注jobs的公众号
			When tom2访问jobs的webapp::apiserver
			When tom2购买jobs的商品::apiserver
				"""
				{
					"order_id":"004",
					"pay_type": "货到付款",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom2成功创建订单::apiserver
				"""
				{
					"order_no":"004",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "004",
					"logistics": "申通快递",
					"number": "229388967650",
					"shipper": "jobs"
				}
				"""
			When jobs完成订单'004'
		
		#退款中订单用户，可以领取优惠券
			Given tom3关注jobs的公众号
			When tom3访问jobs的webapp::apiserver
			When tom3购买jobs的商品::apiserver
				"""
				{
					"order_id":"005",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			When tom3使用支付方式'微信支付'进行支付
			Then tom3成功创建订单::apiserver
				"""
				{
					"order_no":"005",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "004",
					"logistics": "申通快递",
					"number": "229388967650",
					"shipper": "jobs"
				}
				"""
			
			When jobs'申请退款'订单'005'

			When jobs创建优惠券发放规则发放优惠券
				"""
				{
					"name": "未下单用户单品券",
					"count": 1,
					"members": ["tom3"],
					"coupon_ids": ["coupon3_id_2"]
				}
				"""
			When tom3访问jobs的webapp
			Then tom3能获得webapp优惠券列表
				"""
				[{
					"coupon_id": "coupon3_id_2",
					"money": 10.00,
					"status": "未使用"
				}]
				"""

			Given jobs登录系统
			When jobs通过财务审核'退款成功'订单'005'

		#退款完成订单用户，可以领取优惠券
			Given tom4关注jobs的公众号
			When tom4访问jobs的webapp::apiserver
			When tom4购买jobs的商品::apiserver
				"""
				{
					"order_id":"006",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			When tom4使用支付方式'微信支付'进行支付
			Then tom4成功创建订单::apiserver
				"""
				{
					"order_no":"006",
					"status": "待发货",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs对订单进行发货
				"""
				{
					"order_no": "004",
					"logistics": "申通快递",
					"number": "229388967650",
					"shipper": "jobs"
				}
				"""			
			When jobs'申请退款'订单'006'
			When jobs通过财务审核'退款成功'订单'006'

		#已取消订单用户，可以领取优惠券
			When tom5访问jobs的webapp::apiserver
			When tom5购买jobs的商品::apiserver
				"""
				{
					"order_id":"007",
					"pay_type": "微信支付",
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""
			Then tom5成功创建订单::apiserver
				"""
				{
					"order_no":"007",
					"status": "待支付",
					"final_price": 200.00,
					"product_price": 200.00,
					"products":[{
						"name":"商品1",
						"price":200.00,
						"count":1
					}]
				}
				"""

			Given jobs登录系统
			When jobs取消订单'007'

	#给多人群发优惠券，只有符合条件的用户可以领取到优惠券，限领一张
		Given jobs登录系统
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部"
			}]
			"""
		When jobs选择会员
			| member_name | member_rank |
			|    bill     |   普通会员  |
			|    tom      |   普通会员  |
			|    tom1     |   普通会员  |
			|    tom2     |   普通会员  |
			|    tom3     |   普通会员  |
			|    tom4     |   普通会员  |
			|    tom5     |   普通会员  |

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给选中的人发优惠券(已取消关注的除外)",
				"coupon_name":"未下单用户全体券",
				"count":2
			}]
			"""
		When bill访问jobs的webapp
		Then bill能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon4_id_1",
				"money": 100.00,
				"status": "未使用"
			}]
			"""

		When tom访问jobs的webapp
		Then tom能获得webapp优惠券列表
			"""
			[]
			"""

		When tom1访问jobs的webapp
		Then tom1能获得webapp优惠券列表
			"""
			[]
			"""

		When tom2访问jobs的webapp
		Then tom2能获得webapp优惠券列表
			"""
			[]
			"""

		When tom3访问jobs的webapp
		Then tom3能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon4_id_2",
				"money": 100.00,
				"status": "未使用"
			}]
			"""

		When tom4访问jobs的webapp
		Then tom4能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon4_id_3",
				"money": 100.00,
				"status": "未使用"
			}]
			"""

		When tom5访问jobs的webapp
		Then tom5能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon4_id_4",
				"money": 100.00,
				"status": "未使用"
			}]
			"""
