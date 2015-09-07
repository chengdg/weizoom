#_author_:王丽

Feature: 销售概况-订单明细分析
	对店铺的订单进行不同维度的查询分析

	查询条件
	1、刷选日期
		1）开始日期和结束日期都为空；选择开始结束日期，精确到日期
		2）开始日期或者结束日期，只有一个为空，给出系统提示“请填写XX日期”
		3）默认为‘最近7天’，筛选日期：‘七天前’到‘今天’
		4）包含筛选日期的开始和结束的边界值
		5）手工设置筛选日期，点击查询后，‘快速查询’的所有项都处于‘未选中状态’，时间和选项匹配的，选项处于选中状态
	2、快速查看
	    首次进入或者刷新，筛选日期默认当前日期，快速查询"今天"选中
	    1）今天：查询的当前日期，例如，今天是2015-6-16，筛选日期是：2015-6-16到2015-6-16
	    2）昨天：查询的前一天，例如，今天是2015-6-16，筛选日期是：2015-6-15到2015-6-15
		3）最近7天：包含今天，向前7天；例如，今天是2015-6-16，筛选日期是：2015-6-10到2015-6-16
		4）最近30天：包含今天，向前30天；例如，今天是2015-6-16，筛选日期是：2015-5-19到2015-6-16
		5）最近90天：包含今天，向前90天；例如，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
		6）全部：筛选日期更新到：2013.1.1到今天，其他查询条件恢复到默认值
			即：【筛选日期】：开始日期：今天，结束日期：今天
			【订单名称】：空；【订单编号】：空；【支付方式】：全部；
			【订单状态】：全部【复购筛选】：全部；
			【优惠抵扣】：全部；

	3、【商品名称】模糊匹配查找，默认为空

		备注：一个订单包含多个商品的，只有一个商品满足查询条件的，列出整个订单，包含订单中的所有商品

	4、【订单编号】完全匹配查找，默认为空
	5、【支付方式】下拉选择支付方式：全部、微信支付、支付宝支付、货到付款，默认‘全部’

		根据手机端订单中的‘支付方式’的选择来判断,不考虑最终的钱是用什么支付。
		手机端‘支付方式’在后台设置：微信支付、支付宝支付、货到付款
		1）微信支付：手机订单的‘支付方式’选择‘微信支付’
		2）支付宝支付：手机订单的‘支付方式’选择‘支付宝支付’
		3）货到付款：手机订单的‘支付方式’选择‘货到付款’

	6、【订单状态】：订单的状态有分为：待发货、已发货、已完成
		复选查询条件；默认待发货、已发货、已完成选中
		复选规则
		1）至少有一个选中
		2）只有一选中的时候，点击不能取消选中

		

	7、【复购筛选】：包含：全部、购买一次、购买多次；默认‘全部’
		1）“初次购买”：在查询区间以前没有发生过购买，在查询区间内发生初次购买的用户订单
		2）“重复购买”：在该时间段以前发生过购买或者在该订单的订单时间之前发生过购买，在该时间段内又发生了购买的用户订单
						满足下面条件的订单；（1）下单时间在查询区间内的‘有效订单’（1）订单的买家在该订单下单时间之前有‘有效订单’

			备注：注意买家在查询区间内发生两次购买，第一次购买为初次购买的统计到'初次购买';
					第二次购买统计到'重复购买'。

	8、【买家来源】：全部、直接关注购买、推荐扫码关注购买、分享链接关注购买、其他
		根据会员的来源来确定订单的来源，默认‘全部’

		备注：1）买家可能会先下订单再关注，即买家的'关注时间'晚于订单的'下单时间'，这种订单的归类到其他
				2）没有关注店铺公众账号，直接下的订单的归类到其他
				即：所有不能确定买家的都归类到其他

	9、【优惠抵扣】：微众卡支付、积分抵扣、优惠券、微众卡+积分、微众卡+优惠券
		根据订单只使用的优惠抵扣方式过滤订单
		复选查询条件；默认‘微众卡支付、积分抵扣、优惠券、微众卡+积分、微众卡+优惠券’不选中，查询所有的，包含使用优惠抵扣和未使用优惠抵扣的订单

		复选规则
		1）可以多选
		2）可以全部不选

		备注：目前的一个订单中不能同时使用‘积分’和‘优惠券’，这样我们的‘优惠抵扣’的图表的最后两项（积分+优惠券；微众卡+积分+优惠券）就可以直接删除了；


	查询结果
	1、查询结果订单数：∑订单.个数[满足查询条件]
	   占总订单比例：∑订单.个数[满足查询条件]/∑订单.个数[订单.状态 in {待发货、已发货、已完成}]*100%
	   
	2、查询结果列：商品名称、订单编号、优惠金额、运费、实付金额、支付方式、买家、下单时间、订单状态

		按照【下单时间】倒序排列

		备注：点击‘订单编号’进入'订单详情'页面；点击‘买家’进入'会员详情'

	功能
		1、重置：查询条件恢复到默认状态
				【筛选日期】：开始日期：今天，结束日期：今天
				【订单名称】：空；【订单编号】：空；【支付方式】：全部；
				【订单状态】：全部选中【复购筛选】：全部；
				【优惠抵扣】：全部不选中；

		2、导出
			查询结果所有订单按照查询结果列，导出到Excel，不受分页影响

Background:
	#jobs的基础数据设置

	Given jobs登录系统
	When jobs设置未付款订单过期时间:
		"""
		{
			"no_payment_order_expire_day":"1天"
		}
		"""
	Given jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}]
		"""
	And jobs设定会员积分策略
		# 即: "integral_each_yuan": 10	
		"""
		{
			"integral_each_yuan": 10
		}
		"""
	When jobs添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345", 
			"weixin_partner_id": "22345", 
			"weixin_partner_key": "32345", 
			"weixin_sign": "42345"
		},{
			"type": "支付宝",
			"description": "我的支付宝支付",
			"is_active": "启用"
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
	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"promotion_title": "促销商品1",
			"category": "分类1",
			"postage": 10,
			"detail": "商品1详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"freight":"10",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"synchronized_mall":"是"
		}, {
			"name": "商品2",
			"promotion_title": "促销商品2",
			"category": "分类1",
			"postage": 15,
			"detail": "商品2详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"freight":"15",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"synchronized_mall":"是"
		}]

		"""
	And jobs已创建微众卡
		"""
		{
			"cards":[{
				"id":"0000001",
				"password":"1234567",
				"status":"未使用",
				"price":110.00
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
			},{
				"id":"0000004",
				"password":"1234567",
				"status":"未使用",
				"price":95.00
			},{
				"id":"0000005",
				"password":"1234567",
				"status":"未使用",
				"price":80.00
			},{
				"id":"0000006",
				"password":"1234567",
				"status":"未使用",
				"price":50.00
			},{
				"id":"0000007",
				"password":"1234567",
				"status":"未使用",
				"price":50.00
			}]
		}
		"""

	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "2014-8-1",
			"end_date": "10天后",
			"product_name": "商品1",
			"is_permanant_active": "true",
			"rules": [{
				"member_grade": "全部",
				"discount": 70,
				"discount_money": 70.0
			}]
		}, {
			"name": "商品2积分应用",
			"start_date": "2014-8-1",
			"end_date": "10天后",
			"product_name": "商品2",
			"is_permanant_active": "true",
			"rules": [{
				"member_grade": "全部",
				"discount": 70,
				"discount_money": 70.0
			}]
		}]
		"""
	And jobs添加优惠券规则
		"""
		[{
			"name": "全体券1",
			"money": 10,
			"start_date": "2014-8-1",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	# 暂时不起作用
	# Given jobs已添加'渠道扫码'营销活动
	# 	"""
	# 	[{
	# 		"setting_id": 0,
	# 		"name": "渠道扫码01",
	# 		"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"积分\"}",
	# 		"reply_type": 0,
	# 		"reply_material_id": 0,
	# 		"re_old_member": 1,
	# 		"grade_id": 16,
	# 		"remark": "备注1",
	# 		"create_time":"2015-06-24 09:00:00"
	# 	}]
	# 	"""

	#When 已有一批微信用户关注jobs
	When jobs批量获取微信用户关注
		| member_name   | attention_time 	| member_source |    extra   |
		| bill 			| 2014-8-5 8:00:00  | 直接关注      | -          |
		| tom 			| 2014-9-1 8:00:00 	| 推广扫码      | 渠道扫码01 |
		| marry 	    | 2014-9-1 10:00:00 | 会员分享      | bill       |
		| tom1 			| 2014-9-1 8:00:00  | 会员分享      | bill       |
		| tom2 			| 2014-9-3 8:00:00  | 会员分享      | bill       |
		| tom3          | 2014-6-1 8:00:00  | 推广扫码      | 渠道扫码01 |

		#在查询区间之前有有效订单；
		#在查询区间之前有无效订单；
		#在查询区间之前无订单；
		#三种有效订单类型：待发货、已发货、已完成
		#无效订单类型：待支付、已取消、退款中、退款完成
		#三种支付方式：支付宝、微信支付、货到付款
		#优惠期扣：微众卡、优惠券、积分、微众卡+优惠券、微众卡+积分
	When 微信用户批量消费jobs的商品
		|	order_id	  | date       | consumer | type      |businessman|   product | payment | payment_method | freight |   price  | product_integral |  	 coupon  		| paid_amount | 		weizoom_card 		| alipay | wechat | cash |      action       |  order_status   |
		|对应订单编号082  | 2014-8-5   | bill     |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      | 		 |               		| 110         |              				| 110    | 0      | 0    | jobs,支付         |  待发货         |
		|                 | 2014-8-6   | tom      |    购买   | jobs      | 商品2,2   | 未支付  | 支付宝         | 15      | 100      |          |        				| 0           |              				| 0      | 0      | 0    | jobs,取消         |  已取消         |	
		|对应订单编号083  | 2014-9-1   | bill     |    购买   | jobs      | 商品2,2   | 支付    | 支付宝         | 15      | 100      |          |        				| 215         |              				| 215    | 0      | 0    | jobs,支付         |  待发货         |
		|对应订单编号084  | 2014-9-2   | tom      |    购买   | jobs      | 商品1,1   | 支付    | 微信支付       | 10      | 100      |          |        				| 110         |              				| 0      | 110    | 0    | jobs,发货         |  已发货         |
		|对应订单编号085  | 2014-9-3   | marry    |    购买   | jobs      | 商品1,1   | 支付    | 货到付款       | 10      | 100      |          |       				| 110         |              				| 0      | 0      | 110  | jobs,支付         |  待发货         |
		|				  | 2014-9-3   | tom1     |    购买   | jobs      | 商品1,1   | 未支付  | 货到付款       | 10      | 100      |          |       				| 0           |              				| 0      | 0      | 0    | jobs,取消         |  已取消         |
		|对应订单编号086  | 2014-9-4   | bill     |    购买   | jobs      | 商品1,1   | 支付    | 货到付款       | 10      | 100      |          |        				| 110         | 0000001,1234567     		| 0      | 0      | 0    | jobs,支付         |  待发货         |
		|对应订单编号087  | 2014-9-4   | marry    |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      | 200      |        				| 90          |              				| 90     | 0      | 0    | jobs,发货         |  已发货         |
		|对应订单编号089  | 2014-9-5   | bill     |    购买   | jobs      | 商品1,2   | 支付    | 微信支付       | 10      | 100      |          | 全体券1,coupon1_id_1 | 200         |              				| 0      | 200    | 0    | jobs,支付         |  待发货         |
		|				  | 2014-9-5   | marry    |    购买   | jobs      | 商品1,1   | 支付    | 微信支付       | 10      | 100      | 200      |        				| 90          | 0000002,1234567 			| 0      | 0      | 0    | jobs,退款         |  退款中         |
		|对应订单编号090  | 2014-9-6   | tom      |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      |          | 全体券1,coupon1_id_2	| 100         | 0000003,1234567			  	| 0      | 0      | 0    | jobs,完成         |  已完成         |		
		|对应订单编号094  | 2014-9-7   | tom1     |    购买   | jobs      | 商品2,1   | 支付    | 微信支付       | 15      | 100      | 200      |        				| 95          | 0000004,1234567 			| 0      | 0      | 0    | jobs,完成         |  已完成         |
		|对应订单编号096  | 2014-9-8   | tom2     |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      |          | 全体券1,coupon1_id_3	| 100         | 0000005,1234567				| 20     | 0      | 0    | jobs,完成         |  已完成         |
		|对应订单编号097  | 2014-9-9   | tom3     |    购买   | jobs      | 商品2,1   | 支付    | 微信支付       | 15      | 100      | 200      |        				| 95          | 0000006,1234567				| 0      | 45     | 0    | jobs,完成         |  已完成         |
		|对应订单编号099  | 2014-9-10  | -tom4    |    购买   | jobs      | 商品2,1   | 支付    | 货到付款       | 15      | 100      |          |        				| 115         | 0000007,1234567				| 0      | 0      | 65   | jobs,完成         |  已完成         |
		|				  | 2014-9-11  | -tom4    |    购买   | jobs      | 商品2,1   | 支付    | 货到付款       | 15      | 100      |          |        				| 115         |              				| 0      | 0      | 115  | jobs,完成退款     | 退款成功        |
		|				  | 今天       | bill     |    购买   | jobs      | 商品2,1   | 未支付  | 支付宝         | 15      | 100      | 200      |        				| 95          |              				| 0      | 0      | 0    | jobs,无操作  	 |  待支付         |
		|对应订单编号100  | 今天       | tom      |    购买   | jobs      | 商品2,1   | 支付    | 支付宝         | 15      | 100      | 200      |       				| 95          |              				| 95     | 0      | 0    | jobs,发货   	 	 |  已发货         |

@ignore
Scenario: 1 订单查询 筛选日期，默认筛选日期当天；快速查询；重置

	Given jobs登录系统

	#筛选日期

		When jobs首次进入订单明细分析或者刷新订单明细分析
		Then jobs快速查询"今天"选中
		And jobs获得筛选日期
			"""
			[{
				"begin_date":"今天",
				"end_date":"今天"
			}]
			"""
		#筛选日期设置至少有一个为空
			When jobs设置筛选日期
			"""
			[{
				"begin_date":"2014-9-1",
				"end_date":""
			}]
			"""
			Then jobs系统给出提示“请添加结束日期”

			When jobs设置筛选日期
			"""
			[{
				"begin_date":"",
				"end_date":"2014-9-1"
			}]
			"""
			Then jobs系统给出提示“请添加开始日期”

		#备注：昨天，今天是2015-6-16，筛选日期：2015-6-16到2015-6-16
			When jobs快速查询"昨天"选中
			Then jobs获得筛选日期
				"""
				[{
					"begin_date":"昨天",
					"end_date":"昨天"
				}]
				"""

		#备注：最近7天，今天是2015-6-16，筛选日期：2015-6-10到2015-6-16
			When jobs快速查询"最近7天"选中
			Then jobs获得筛选日期
				"""
				[{
					"begin_date":"7天前",
					"end_date":"今天"
				}]
				"""

		#备注：最近30天，今天是2015-6-16，筛选日期：2015-5-18到2015-6-16
			When jobs快速查询"最近30天"选中
			Then jobs获得筛选日期
				"""
				[{
					"begin_date":"30天前",
					"end_date":"今天"
				}]
				"""

		#备注：最近90天，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
			When jobs快速查询"最近90天"选中
			Then jobs获得筛选日期
				"""
				[{
					"begin_date":"90天前",
					"end_date":"今天"
				}]
				"""

	#默认查询条件、重置
		When jobs首次进入订单明细分析或者刷新订单明细分析
	
		Then jobs获得默认订单查询条件
		"""
		[{
			"begin_date":"今天",
			"end_date":"今天",
			"product_name":"",
			"order_id":"",
			"payment_method":"全部",
			"order_status":[{待发货},{已发货},{已完成}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""
		When jobs设置订单查询条件
		"""
		[{
			"begin_date":"2015-5-2",
			"end_date":"2015-5-20",
			"product_name":"商品",
			"order_id":"22220",
			"payment_method":"微信支付",
			"order_status":"已完成",
			"re_purchase":"初次购买",
			"preferential_deduction":[{微众卡支付}],
			"buyers_source":"推荐扫码关注购买"
		}]
		"""
		Given jobs设置订单统计查询条件"重置"

		Then jobs获得订单查询条件
		"""
		[{
			"begin_date":"今天",
			"end_date":"今天",
			"product_name":"",
			"order_id":"",
			"payment_method":"全部",
			"order_status":[{待发货},{已发货},{已完成}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	

	#快速查询：全部，今天是2015-6-16，筛选日期：2013-1-1到2015-6-16；其他查询条件回复到默认状态

		When jobs设置订单查询条件
		"""
		[{
			"begin_date":"今天",
			"end_date":"今天",
			"product_name":"商品",
			"order_id":"22220",
			"payment_method":"微信支付",
			"order_status":"已完成",
			"re_purchase":"初次购买",
			"preferential_deduction":"微众卡支付",
			"buyers_source":"推荐扫码关注购买"
		}]
		"""
		When jobs快速查询"全部"选中

		Then jobs获得订单查询条件
		"""
		[{
			"begin_date":"2013-1-1",
			"end_date":"今天",
			"product_name":"",
			"order_id":"",
			"payment_method":"全部",
			"order_status":[{待发货},{已发货},{已完成}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	

@stats @stats.order_detail
Scenario: 2 订单查询 空条件查询

	Given jobs登录系统

	#空条件查询,查全部
		And jobs设置订单统计查询条件
		"""
		{
			"begin_date":"2014-1-1",
			"end_date":"今天",
			"product_name":"",
			"order_id":"",
			"payment_method":"全部",
			"order_status":["待发货","已发货","已完成"],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}
		"""
		When jobs查询订单明细统计

		# """
		# {
		# 	"result_order_count":"13",
		# 	"result_order_proportion":"100.00%"
		# }
		# """
		Then jobs获得订单占比统计数据
			"""
			{
				"result_order_count":"13",
				"result_order_proportion":"100.00%"
			}
			"""
		Then jobs获得订单统计列表
			| product_name | order_id        | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
			|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |
			|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
			|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |
			|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |
			|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |
			|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
			|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
			|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |
			|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |
			|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |
			|    商品2     | 对应订单编号083 |    0            |   15    |   215       |  支付宝        |   bill   |   2014-9-1      |   待发货     |
			|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |   bill   |   2014-8-5      |   待发货     |

@stats @stats.order_detail
Scenario: 3 订单查询 商品名称、订单编号、支付方式、买家来源、优惠抵扣、复购筛选
	
	Given jobs登录系统

	#商品名称查询

		#完全匹配
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"商品1",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计

			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"8",
					"result_order_proportion":"61.54%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |
				|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |
				|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
				|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
				|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |
				|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |
				|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |   bill   |   2014-8-5      |   待发货     |

		#模糊匹配
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"商品",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计

			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"13",
					"result_order_proportion":"100.00%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id        | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
				|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |
				|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
				|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |
				|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |
				|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |
				|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
				|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
				|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |
				|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |
				|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |
				|    商品2     | 对应订单编号083 |    0            |   15    |   215       |  支付宝        |   bill   |   2014-9-1      |   待发货     |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |   bill   |   2014-8-5      |   待发货     |

		#查询结果为空
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"商品名称查询结果为空",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"0",
					"result_order_proportion":"0.00%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |

	#订单编号查询

		#完全匹配
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"对应订单编号100",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"1",
					"result_order_proportion":"7.69%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id        | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |

		#查询结果为空
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"对应订单编号",
				"payment_method":"全部",
				"order_status":"全部",
				"re_purchase":["待发货","已发货","已完成"],
				"preferential_deduction":"全部不选中",
				"only_weizoom_card":"否",
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"0",
					"result_order_proportion":"0.00%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |

	#订单支付方式

		#支付宝
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"支付宝",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"6",
					"result_order_proportion":"46.15%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
				|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |
				|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |
				|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
				|    商品2     | 对应订单编号083 |    0            |   15    |   215       |  支付宝        |   bill   |   2014-9-1      |   待发货     |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |   bill   |   2014-8-5      |   待发货     |

		#微信支付
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"微信支付",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"3",
					"result_order_proportion":"23.08%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id        | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
				|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
				|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |

		#货到付款
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"货到付款",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"2",
					"result_order_proportion":"15.38%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |
				|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |

	#买家来源

		#直接关注购买
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"直接关注购买"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"4",
					"result_order_proportion":"30.77%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
				|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |
				|    商品2     | 对应订单编号083 |    0            |   15    |   215       |  支付宝        |   bill   |   2014-9-1      |   待发货     |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |   bill   |   2014-8-5      |   待发货     |

		#推荐扫码关注购买
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"推荐扫码关注购买"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"4",
					"result_order_proportion":"30.77%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
				|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
				|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |
				|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |

		#分享链接关注购买
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"分享链接关注购买"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"4",
					"result_order_proportion":"30.77%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |
				|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |
				|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
				|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |

		#其他
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"其他"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"1",
					"result_order_proportion":"7.69%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |

	#优惠抵扣

		#微众卡支付
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":["微众卡支付"],
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"2",
					"result_order_proportion":"15.38%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |
				|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |

		#积分抵扣
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":["积分抵扣"],
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"2",
					"result_order_proportion":"15.38%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
				|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |

		#优惠券
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":["优惠券"],
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"1",
					"result_order_proportion":"7.69%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |

		#微众卡+积分
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":["微众卡+积分"],
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"2",
					"result_order_proportion":"15.38%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
				|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |

		#微众卡+优惠券
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":["微众卡+优惠券"],
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"2",
					"result_order_proportion":"15.38%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |
				|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |

		#微众卡支付 和 积分抵扣 复选
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"全部",
				"preferential_deduction":["微众卡支付","积分抵扣"],
				"buyers_source":"全部"
			}
			"""
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"4",
					"result_order_proportion":"30.77%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
				|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |
				|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
				|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |


	#复购筛选

		#购买一次
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"购买一次",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}
			"""	
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"7",
					"result_order_proportion":"53.85%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |
				|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
				|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |
				|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |
				|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |
				|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |   bill   |   2014-8-5      |   待发货     |

		#购买多次
			Given jobs设置订单统计查询条件
			"""
			{
				"begin_date":"2014-1-1",
				"end_date":"今天",
				"product_name":"",
				"order_id":"",
				"payment_method":"全部",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"购买多次",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}
			"""	
			When jobs查询订单明细统计
			Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"6",
					"result_order_proportion":"46.15%"
				}
				"""
			Then jobs获得订单统计列表
				| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
				|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |
				|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
				|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
				|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |
				|    商品2     | 对应订单编号083 |    0            |   15    |   215       |  支付宝        |   bill   |   2014-9-1      |   待发货     |

@stats @stats.order_detail
Scenario: 4 订单查询 订单状态

	Given jobs登录系统

	#全部
		Given jobs设置订单统计查询条件
		"""
		{
			"begin_date":"2014-1-1",
			"end_date":"今天",
			"product_name":"",
			"order_id":"",
			"payment_method":"全部",
			"order_status":["待发货","已发货","已完成"],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}
		"""	
		When jobs查询订单明细统计
		Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"13",
					"result_order_proportion":"100.00%"
				}
				"""
		Then jobs获得订单统计列表
			| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
			|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |
			|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
			|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |
			|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |
			|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |
			|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
			|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
			|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |
			|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |
			|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |
			|    商品2     | 对应订单编号083 |    0            |   15    |   215       |  支付宝        |   bill   |   2014-9-1      |   待发货     |
			|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |   bill   |   2014-8-5      |   待发货     |

	#待发货
		Given jobs设置订单统计查询条件
		"""
		{
			"begin_date":"2014-1-1",
			"end_date":"今天",
			"product_name":"",
			"order_id":"",
			"payment_method":"全部",
			"order_status":["待发货"],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}
		"""	
		When jobs查询订单明细统计
		Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"5",
					"result_order_proportion":"38.46%"
				}
				"""
		Then jobs获得订单统计列表
			| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
			|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |
			|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |
			|    商品2     | 对应订单编号083 |    0            |   15    |   215       |  支付宝        |   bill   |   2014-9-1      |   待发货     |
			|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |   bill   |   2014-8-5      |   待发货     |

	#已发货
		Given jobs设置订单统计查询条件
		"""
		{
			"begin_date":"2014-1-1",
			"end_date":"今天",
			"product_name":"",
			"order_id":"",
			"payment_method":"全部",
			"order_status":["已发货"],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}
		"""	
		When jobs查询订单明细统计
		Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"3",
					"result_order_proportion":"23.08%"
				}
				"""
		Then jobs获得订单统计列表
			| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
			|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
			|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |

	#已完成
		Given jobs设置订单统计查询条件
		"""
		{
			"begin_date":"2014-1-1",
			"end_date":"今天",
			"product_name":"",
			"order_id":"",
			"payment_method":"全部",
			"order_status":["已完成"],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}
		"""	
		When jobs查询订单明细统计
		Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"5",
					"result_order_proportion":"38.46%"
				}
				"""
		Then jobs获得订单统计列表
			| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |
			|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
			|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |
			|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |
			|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |


	#多选查询：待发货、已发货
		Given jobs设置订单统计查询条件
		"""
		{
			"begin_date":"2014-1-1",
			"end_date":"今天",
			"product_name":"",
			"order_id":"",
			"payment_method":"全部",
			"order_status":["待发货","已发货"],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}
		"""	
		When jobs查询订单明细统计
		Then jobs获得订单占比统计数据
				"""
				{
					"result_order_count":"8",
					"result_order_proportion":"61.54%"
				}
				"""
		Then jobs获得订单统计列表
			| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
			|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
			|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |
			|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |
			|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |
			|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |
			|    商品2     | 对应订单编号083 |    0            |   15    |   215       |  支付宝        |   bill   |   2014-9-1      |   待发货     |
			|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |   bill   |   2014-8-5      |   待发货     |

@ignore
Scenario: 5 订单查询 查询结果链接，导出

	Given jobs登录系统

	#空条件查询
		Given jobs设置订单统计查询条件
		"""
		[{
			"begin_date":"2014-9-5",
			"end_date":"2014-9-21",
			"product_name":"商品",
			"order_id":"",
			"payment_method":"微信支付",
			"order_status":"["已完成"]",
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	
		Then jobs获得订单占比统计数据
				"""
				[{
					"result_order_count":"2",
					"result_order_proportion":"15.38%"
				}]
				"""
		Then jobs获得订单统计列表
			| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
			|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |


		#点击‘订单编号’，跳转到‘订单详情’；点击‘买家’，跳转到‘会员详情’
			When jobs订单编号
			Then jobs获得重新打开新页面，跳转到当前订单的‘订单详情’

			When jobs买家
			Then jobs获得重新打开新页面，跳转到当前买家的‘会员详情’


		When jobs批量导出
		Then jobs成功导出数据
			| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
			|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |
@stats @stats.order_detail
Scenario: 6 订单查询 分页

	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":4
		}
		"""
	And jobs设置订单统计查询条件
		"""
		{
			"begin_date":"2014-1-1",
			"end_date":"今天",
			"product_name":"商品",
			"order_id":"",
			"payment_method":"全部",
			"order_status":["待发货","已发货","已完成"],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}
		"""	
	When jobs查询订单明细统计
	Then jobs获取订单统计列表显示共4页
	When jobs浏览第1页
	Then jobs获得订单统计列表
		| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		|    商品2     | 对应订单编号100 |    20           |   15    |   95        |  支付宝        |   tom    |      今天       |   已发货     |
		|    商品2     | 对应订单编号099 |    0            |   15    |   115       |  货到付款      |   未知   |   2014-9-10     |   已完成     |
		|    商品2     | 对应订单编号097 |    20           |   15    |   95        |  微信支付      |   tom3   |   2014-9-9      |   已完成     |
		|    商品1     | 对应订单编号096 |    10           |   10    |   100       |  支付宝        |   tom2   |   2014-9-8      |   已完成     |

	When jobs浏览下一页
	Then jobs获得订单统计列表
		| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |
		|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |
		|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
		|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |

	When jobs浏览第3页
	Then jobs获得订单统计列表
		| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		|    商品1     | 对应订单编号086 |    0            |   10    |   110       |  优惠抵扣      |   bill   |   2014-9-4      |   待发货     |
		|    商品1     | 对应订单编号085 |    0            |   10    |   110       |  货到付款      |   marry  |   2014-9-3      |   待发货     |
		|    商品1     | 对应订单编号084 |    0            |   10    |   110       |  微信支付      |   tom    |   2014-9-2      |   已发货     |
		|    商品2     | 对应订单编号083 |    0            |   15    |   215       |  支付宝        |   bill   |   2014-9-1      |   待发货     |

	When jobs浏览上一页
	Then jobs获得订单统计列表
		| product_name | order_id    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		|    商品2     | 对应订单编号094 |    20           |   15    |   95        |  优惠抵扣      |   tom1   |   2014-9-7      |   已完成     |
		|    商品1     | 对应订单编号090 |    10           |   10    |   100       |  支付宝        |   tom    |   2014-9-6      |   已完成     |
		|    商品1     | 对应订单编号089 |    10           |   10    |   200       |  微信支付      |   bill   |   2014-9-5      |   待发货     |
		|    商品1     | 对应订单编号087 |    20           |   10    |   90        |  支付宝        |   marry  |   2014-9-4      |   已发货     |








		




