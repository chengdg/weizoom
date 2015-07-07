#_author_:王丽

Feature: 销售概况-订单明细分析
	对店铺的订单进行不同维度的查询分析

	查询条件
	1、刷选日期
		1）开始日期和结束日期都为空；
		2）开始日期或者结束日期，只有一个为空，给出系统提示“请填写XX日期”
		3）默认为‘当前日期’
		4）选择开始结束日期，精确到日期
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
	   占总订单比例：∑订单.个数[满足查询条件]/∑订单.个数[(订单.来源='本店') and 订单.状态 in {待发货、已发货、已完成}]*100%
	   
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

	#toms代表商城
	#jobs代表商户

	#jobs的基础数据设置

		Given jobs登录系统

		When jobs设置未付款订单过期时间
			"""
			{
				"no_payment_order_expire_day":"1天"
			}
			"""

		And jobs已添加商品
			"""
			[{
				"product_name": "商品1",
				"price": 100,
				"freight":"10",
				"stock_type": "无限",
				"synchronized_mall":"是"
			},{
				"product_name": "商品2",
				"price": 100,
				"freight":"15",
				"stock_type": "无限",
				"synchronized_mall":"是"
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
		And jobs已添加微众支付
			"""
			[{
				"is_weizoom_pay":"是"
			}]
			"""

		And jobs设置积分策略
			"""
			[{ 
				"integral_each_yuan": 10
			}]
			"""

		And jobs已添加积分应用活动
			"""
			[{
				"name": "商品1积分应用",
				"start_date": "2014-8-1",
				"end_date": "10天后",
				"products": ["商品1"],
				"is_permanant_active": false,
				"rules": [{
					"member_grade_name": "全部会员",
					"discount": 70,
					"discount_money": 70.0
				}]
			}]
			"""
		And toms已添加优惠券
			"""
			[{
				"name": "商品2优惠券",
				"money": 10,
				"start_date": "2014-8-1",
				"end_date": "10天后",
				"coupon_id_prefix": "coupon1_id_"
			}]
			"""

		And bill关注jobs的公众号
    	And tom关注jobs的公众号
    	And nokia关注jobs的公众号
    	And tom2关注jobs的公众号
    	And tom3关注jobs的公众号
    	And tom4关注jobs的公众号

		When jobs获得微信用户
			| member_name | attention_time | member_source |
			| bill        | 2014-8-5 8:00  | 直接关注      |
			| tom         | 2014-9-1 8:00  | 推广扫码      |
			| nokia       | 2014-9-1 8:00  | 会员分享      |
			| tom2        | 2014-9-3 8:00  | 会员分享      |
			| tom3        | 2014-6-1 8:00  | 推广扫码      |
			| tom4        | 2014-9-1 8:00  | 会员分享      |

		#备注：账户名前加”-“代表该账户处于未关注状态

		When 微信用户批量消费jobs的商品
			| order_datetime  	| consumer |businessman|      product     | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action       |  order_status   |
			| 2014-8-5  10:00  	| bill     | jobs      | 商品1,1          | 支付    | 支付宝支付     | 10      | 100      | 0        | 0      | 110         | 0            | 110    | 0      | 0    |                   |  待发货         |
			| 2014-9-1  10:00  	| bill     | jobs      | 商品1,1          | 支付    | 支付宝支付     | 10      | 100      | 0        | 0      | 110         | 0            | 110    | 0      | 0    |                   |  待发货         |
			| 2014-9-2  00:00  	| tom      | jobs      | 商品1,1          | 支付    | 微信支付       | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 110    | 0    | jobs,发货         |  已发货         |
			| 2014-9-3  23:59  	| bill     | jobs      | 商品1,1          | 支付    | 货到付款       | 10      | 100      | 20       | 0      | 90          | 0            | 0      | 0      | 90   |                   |  待发货         |
			| 2014-9-5  10:00  	| tom      | jobs      | 商品1,1          | 支付    | 微信支付       | 10      | 100      | 0        | 10     | 100         | 100          | 0      | 0      | 0    | jobs,发货，完成   |  已完成         |
			| 2014-9-6  10:00  	| -bill    | jobs      | 商品1,1，商品2,2 | 支付    | 支付宝支付     | 10,15   | 100，200 | 0        | 0      | 325         | 325          | 0      | 0      | 0    |                   |  待发货         |
			| 2014-9-7  13:00  	| bill     | jobs      | 商品1,1，商品2,2 | 未支付  | 支付宝支付     | 10,15   | 100，200 | 20       | 10     | 295         | 0            | 0      | 0      | 0    |                   |  已取消         |
			| 2014-9-7  12:00  	| tom      | jobs      | 商品1,1，商品2,2 | 支付    | 支付宝支付     | 10,15   | 100，200 | 20       | 10     | 295         | 100          | 195    | 0      | 0    |                   |  待发货         |
			| 2014-9-20 12:00  	| tom2     | jobs      | 商品2,1          | 支付    | 微信支付       | 15      | 100      | 0        | 10     | 105         | 0            | 0      | 105    | 0    | jobs,发货         |  已发货         |
			| 2014-9-21 14:00  	| tom2     | jobs      | 商品2,1          | 支付    | 微信支付       | 15      | 100      | 20       | 0      | 95          | 95           | 0      | 0      | 0    | jobs,发货，完成   |  已完成         |
			| 2014-9-21 15:00   | nokia    | jobs      | 商品1,1          | 支付    | 微信支付       | 10      | 100      | 20       | 0      | 90          | 90           | 0      | 0      | 0    | jobs,发货，退款   |  退款中         |
			| 2014-9-21  16:00 	| tom4     | jobs      | 商品2,1          | 支付    | 货到付款       | 15      | 100      | 0        | 0      | 115         | 0            | 0      | 0      | 115  | jobs,发货，退款完成| 退款成功       |
			| 7天前 14:00    	| nokia    | jobs      | 商品1,1          | 支付    | 微信支付       | 10      | 100      | 20       | 0      | 90          | 90           | 0      | 0      | 0    | jobs,发货，退款   |  退款中         |
			| 7天前 14:00    	| tom4     | jobs      | 商品2,1          | 支付    | 货到付款       | 15      | 100      | 0        | 0      | 115         | 0            | 0      | 0      | 115  | jobs,发货         |  已完成         |
			| 6天前 15:00    	| tom4     | jobs      | 商品2,1          | 支付    | 货到付款       | 15      | 100      | 0        | 0      | 115         | 0            | 0      | 0      | 115  | jobs,发货，退款完成| 退款成功       |
			| 5天前 15:00    	| bill     | jobs      | 商品1,1          | 支付    | 微信支付       | 10      | 100      | 20       | 0      | 90          | 40           | 0      | 50     | 0    | jobs,发货         |  已发货         |
			| 昨天 15:00    	| tom      | jobs      | 商品1,1          | 支付    | 微信支付       | 10      | 100      | 20       | 0      | 90          | 40           | 0      | 50     | 0    | jobs,发货         |  已发货         |
			| 今天 00:1     	| bill     | jobs      | 商品2,1          | 未支付  | 支付宝支付     | 15      | 100      | 20       | 0      | 95          | 0            | 0      | 0      | 0    |                   |  待支付         |
			| 今天 00:2     	| tom      | jobs      | 商品1,1          | 支付    | 微信支付       | 10      | 100      | 0        | 10     | 100         | 50           | 0      | 50     | 0    |  jobs,发货        |  已发货         |
			| 今天 00:10     	|          | jobs      | 商品1,1          | 支付    | 支付宝         | 10      | 100      | 20       |        | 90          | 0            | 90     | 0      | 0    |  jobs,发货，完成  |  已完成         |

	#toms的基础数据设置

		Given toms登录系统

		When toms设置未付款订单过期时间:
			"""
			{
				"no_payment_order_expire_day":"1天"
			}
			"""

		And toms已添加支付方式
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
		And toms已添加微众支付
			"""
			[{
				"is_weizoom_pay":"是"
			}]
			"""

		And toms设置积分策略
			"""
			[{ 
				"integral_each_yuan": 10
			}]
			"""

		And toms已添加积分应用活动
			"""
			[{
				"name": "商品1积分应用",
				"start_date": "2014-8-1",
				"end_date": "10天后",
				"products": ["商品1"],
				"is_permanant_active": false,
				"rules": [{
					"member_grade_name": "全部会员",
					"discount": 70,
					"discount_money": 70.0
				}]
			}]
			"""
		And toms已添加优惠券
			"""
			[{
				"name": "商品2优惠券",
				"money": 10,
				"start_date": "2014-8-1",
				"end_date": "10天后",
				"coupon_id_prefix": "coupon1_id_"
			}]
			"""
		And bill关注toms的公众号
    	And tom关注toms的公众号

		When 微信用户批量消费toms的商品:
			| order_datetime  	| consumer |businessman|      product     | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action       |  order_status   |
			| 2014-9-1  9:00  	| bill     | toms      | 商品1,1          | 支付    | 支付宝支付     | 10      | 100      | 0        | 0      | 110         | 0            | 110    | 0      | 0    |                   |  待发货         |
			| 2014-9-2  8:00  	| tom      | toms      | 商品1,1          | 支付    | 微信支付       | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 110    | 0    | toms,发货         |  已发货         |
			| 2014-9-3  7:59  	| bill     | toms      | 商品1,1          | 支付    | 货到付款       | 10      | 100      | 20       | 0      | 90          | 0            | 0      | 0      | 90   |                   |  待发货         |

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
			"order_number":"",
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
			"order_number":"22220",
			"payment_method":"微信支付",
			"order_status":"已完成",
			"re_purchase":"初次购买",
			"preferential_deduction":[{微众卡抵扣}],
			"buyers_source":"推广扫码关注购买"
		}]
		"""
		When jobs订单查询条件"重置"

		Then jobs获得订单查询条件
		"""
		[{
			"begin_date":"今天",
			"end_date":"今天",
			"product_name":"",
			"order_number":"",
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
			"order_number":"22220",
			"payment_method":"微信支付",
			"order_status":"已完成",
			"re_purchase":"初次购买",
			"preferential_deduction":"微众卡抵扣",
			"buyers_source":"推广扫码关注购买"
		}]
		"""
		When jobs快速查询"全部"选中

		Then jobs获得订单查询条件
		"""
		[{
			"begin_date":"2013-1-1",
			"end_date":"今天",
			"product_name":"",
			"order_number":"",
			"payment_method":"全部",
			"order_status":[{待发货},{已发货},{已完成}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	

Scenario: 2 订单查询 空条件查询

	Given jobs登录系统

	#空条件查询
		When jobs订单查询条件
		"""
		[{
			"begin_date":"",
			"end_date":"",
			"product_name":"",
			"order_number":"",
			"payment_method":"全部",
			"order_status":[{待发货},{已发货},{已完成}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	
		Then jobs获得查询结果占比
			"""
			[{
				"result_order_count":"14",
				"result_order_proportion":"100%"
			}]
			"""
		Then jobs获得订单列表
			| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
			|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |   已发货     |
			|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
			|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
			|    商品2     | 对应订单编号094 |    0            |   15    |   115       |  货到付款      |    tom4  |   7天前 14:00   |   已完成     |
			|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
			|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
			| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
			| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
			|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
			|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
			|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |
			|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |
			|    商品1     | 对应订单编号081 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-8-5  10:00 |  待发货      |

Scenario: 3 订单查询 商品名称、订单编号、支付方式、买家来源、优惠抵扣、复购筛选
	
	Given jobs登录系统

	#商品名称查询

		#完全匹配
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"商品1",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"11",
					"result_order_proportion":"78.57%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
				|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |   已发货     |
				|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
				|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
				| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
				| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
				|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
				|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
				|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |
				|    商品1     | 对应订单编号081 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-8-5  10:00 |  待发货      |

		#模糊匹配
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"商品",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"14",
					"result_order_proportion":"100%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
				|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
				|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
				|    商品2     | 对应订单编号094 |    0            |   15    |   115       |  货到付款      |    tom4  |   7天前 14:00   |   已完成     |
				|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
				|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
				| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
				| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
				|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
				|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
				|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |
				|    商品1     | 对应订单编号081 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-8-5  10:00 |  待发货      |

		#查询结果为空
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"商品名称查询结果为空",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"0",
					"result_order_proportion":"0%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |

	#订单编号查询

		#完全匹配
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"对应订单编号100",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"1",
					"result_order_proportion":"7.14%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |

		#查询结果为空
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"对应订单编号",
				"payment_method":"全部",
				"order_status":"全部",
				"re_purchase":[{待发货},{已发货},{已完成}],
				"preferential_deduction":"全部不选中",
				"only_weizoom_card":"否",
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"0",
					"result_order_proportion":"0%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |

	#订单支付方式

		#支付宝
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"支付宝",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"5",
					"result_order_proportion":"35.71%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
				| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
				| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |
				|    商品1     | 对应订单编号081 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-8-5  10:00 |  待发货      |

		#微信支付
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"微信支付",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"7",
					"result_order_proportion":"50%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |   已发货     |
				|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
				|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
				|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
				|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
				|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
				|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |

		#货到付款
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"货到付款",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"2",
					"result_order_proportion":"14.29%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号094 |    0            |   15    |   115       |  货到付款      |    tom4  |   7天前 14:00   |   已完成     |
				|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |

	#买家来源

		#直接关注购买
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"直接关注购买"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"5",
					"result_order_proportion":"35.71%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
				| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
				|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |
				|    商品1     | 对应订单编号081 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-8-5  10:00 |  待发货      |

		#推广扫码关注购买
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"推广扫码关注购买"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"5",
					"result_order_proportion":"35.71%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |   已发货     |
				|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
				| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
				|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
				|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |

		#分享链接关注购买
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"分享链接关注购买"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"3",
					"result_order_proportion":"21.43%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号094 |    0            |   15    |   115       |  货到付款      |    tom4  |   7天前 14:00   |   已完成     |
				|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
				|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |

		#其他
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":"全部不选中",
				"buyers_source":"其他"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"1",
					"result_order_proportion":"7.14%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |

	#优惠抵扣

		#微众卡抵扣
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":[{微众卡抵扣}],
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"1",
					"result_order_proportion":"7.14%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |

		#积分抵扣
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":[{积分抵扣}],
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"2",
					"result_order_proportion":"14.29%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
				|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |   待发货     |

		#优惠券抵扣
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":[{优惠券抵扣}],
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"1",
					"result_order_proportion":"7.14%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |

		#微众卡+积分抵扣
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":[{微众卡+积分抵扣}],
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"3",
					"result_order_proportion":"21.43%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
				|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
				|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |

		#微众卡+优惠券抵扣
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":[{微众卡+优惠券抵扣}],
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"2",
					"result_order_proportion":"14.29%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |  已发货      |
				|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |

		#微众卡支付 和 积分抵扣 复选
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"全部",
				"preferential_deduction":[{微众卡抵扣},{积分抵扣}],
				"buyers_source":"全部"
			}]
			"""
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"3",
					"result_order_proportion":"21.43%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
				|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
				|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |   待发货     |


	#复购筛选

		#购买一次
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"购买一次",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}]
			"""	
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"4",
					"result_order_proportion":"28.57%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
				|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
				|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |
				|    商品1     | 对应订单编号081 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-8-5  10:00 |  待发货      |

		#购买多次
			When jobs订单查询条件
			"""
			[{
				"begin_date":"",
				"end_date":"",
				"product_name":"",
				"order_number":"",
				"payment_method":"全部",
				"order_status":[{待发货},{已发货},{已完成}],
				"re_purchase":"购买多次",
				"preferential_deduction":"全部不选中",
				"buyers_source":"全部"
			}]
			"""	
			Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"10",
					"result_order_proportion":"71.43%"
				}]
				"""
			Then jobs获得订单列表
				| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |   已发货     |
				|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
				|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
				|    商品2     | 对应订单编号094 |    0            |   15    |   115       |  货到付款      |    tom4  |   7天前 14:00   |   已完成     |
				|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
				| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
				| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
				|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
				|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
				|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |

Scenario: 4 订单查询 订单状态

	Given jobs登录系统

	#全部
		When jobs订单查询
		"""
		[{
			"begin_date":"",
			"end_date":"",
			"product_name":"",
			"order_number":"",
			"payment_method":"全部",
			"order_status":[{待发货},{已发货},{已完成}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	
		Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"14",
					"result_order_proportion":"100%"
				}]
				"""
		Then jobs获得订单列表
			| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
			|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |   已发货     |
			|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
			|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
			|    商品2     | 对应订单编号094 |    0            |   15    |   115       |  货到付款      |    tom4  |   7天前 14:00   |   已完成     |
			|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
			|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
			| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
			| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
			|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
			|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
			|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |
			|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |
			|    商品1     | 对应订单编号081 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-8-5  10:00 |  待发货      |

	#待发货
		When jobs订单查询条件
		"""
		[{
			"begin_date":"",
			"end_date":"",
			"product_name":"",
			"order_number":"",
			"payment_method":"全部",
			"order_status":[{待发货}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	
		Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"5",
					"result_order_proportion":"35.71%"
				}]
				"""
		Then jobs获得订单列表
			| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
			| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
			|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
			|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |
			|    商品1     | 对应订单编号081 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-8-5  10:00 |  待发货      |

	#已发货
		When jobs订单查询条件
		"""
		[{
			"begin_date":"",
			"end_date":"",
			"product_name":"",
			"order_number":"",
			"payment_method":"全部",
			"order_status":[{已发货}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	
		Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"5",
					"result_order_proportion":"35.71%"
				}]
				"""
		Then jobs获得订单列表
			| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |   已发货     |
			|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
			|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
			|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |   已发货     |
			|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |   已发货     |

	#已完成
		When jobs订单查询条件
		"""
		[{
			"begin_date":"",
			"end_date":"",
			"product_name":"",
			"order_number":"",
			"payment_method":"全部",
			"order_status":[{已完成}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	
		Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"4",
					"result_order_proportion":"28.57%"
				}]
				"""
		Then jobs获得订单列表
			| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
			|    商品2     | 对应订单编号094 |    0            |   15    |   115       |  货到付款      |  tom4    |   7天前 14:00   |   已完成     |
			|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |   已完成     |
			|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |   已完成     |

	#多选查询：待发货、已发货
		When jobs订单查询条件
		"""
		[{
			"begin_date":"",
			"end_date":"",
			"product_name":"",
			"order_number":"",
			"payment_method":"全部",
			"order_status":[{待发货},{已发货}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	
		Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"10",
					"result_order_proportion":"71.43%"
				}]
				"""
		Then jobs获得订单列表
			| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |   已发货     |
			|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
			|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |
			|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
			| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
			| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
			|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
			|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |
			|    商品1     | 对应订单编号082 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |
			|    商品1     | 对应订单编号081 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-8-5  10:00 |  待发货      |

Scenario: 5 订单查询 查询结果链接，导出

	Given jobs登录系统

	#空条件查询
		When jobs订单查询条件
		"""
		[{
			"begin_date":"2014-9-5",
			"end_date":"2014-9-21",
			"product_name":"商品",
			"order_number":"",
			"payment_method":"微信支付",
			"order_status":"[{已完成}]",
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	
		Then jobs获得查询结果占比
				"""
				[{
					"result_order_count":"2",
					"result_order_proportion":"14.29%"
				}]
				"""
		Then jobs获得订单列表
			| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
			|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |

		#点击‘订单编号’，跳转到‘订单详情’；点击‘买家’，跳转到‘会员详情’
			When jobs订单编号
			Then jobs获得重新打开新页面，跳转到当前订单的‘订单详情’

			When jobs买家
			Then jobs获得重新打开新页面，跳转到当前买家的‘会员详情’


		When jobs批量导出
		Then jobs成功导出数据
			| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
			|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |

Scenario: 6 订单查询 分页

	Given jobs登录系统

	When toms已设置分页条件
		"""
		{
			"page_count":4
		}
		"""
	When jobs订单查询条件
		"""
		[{
			"begin_date":"",
			"end_date":"",
			"product_name":"商品",
			"order_number":"",
			"payment_method":"全部",
			"order_status":[{待发货},{已发货},{已完成}],
			"re_purchase":"全部",
			"preferential_deduction":"全部不选中",
			"buyers_source":"全部"
		}]
		"""	

	Then jobs获取订单列表显示共3页
	When jobs浏览第一页
	Then jobs获得订单列表
		| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		|    商品1     | 对应订单编号100 |    20           |   10    |   90        |  支付宝        |          |   今天 00:10    |   已完成     |
		|    商品1     | 对应订单编号099 |    10           |   10    |   100       |  微信支付      |    tom   |   今天 00:2     |   已发货     |
		|    商品1     | 对应订单编号097 |    20           |   10    |   90        |  微信支付      |    tom   |   昨天 15:00    |   已发货     |
		|    商品1     | 对应订单编号096 |    20           |   10    |   90        |  微信支付      |    bill  |   5天前 15:00   |   已发货     |

	When jobs浏览‘下一页’
	Then jobs获得订单列表
		| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		|    商品2     | 对应订单编号094 |    0            |   15    |   115       |  货到付款      |    tom4  |   7天前 14:00   |   已完成     |
		|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
		|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
		| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |

	When jobs浏览‘第3页’
	Then jobs获得订单列表
		| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		| 商品1，商品2 | 对应订单编号086 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
		|    商品1     | 对应订单编号085 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
		|    商品1     | 对应订单编号084 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
		|    商品1     | 对应订单编号083 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |

	When jobs浏览‘上一页’
	Then jobs获得订单列表
		| product_name | order_number    | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		|    商品2     | 对应订单编号094 |    0            |   15    |   115       |  货到付款      |    tom4  |   7天前 14:00   |   已完成     |
		|    商品2     | 对应订单编号090 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
		|    商品2     | 对应订单编号089 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
		| 商品1，商品2 | 对应订单编号087 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |








		




