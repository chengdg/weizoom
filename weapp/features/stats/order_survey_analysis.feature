#_author_:王丽
#edit：张三香

Feature: 销售概况-订单概况
	对店铺的订单进行不同维度的数据统计分析，不分析商城的订单，即订单的订单来源为'本店'

	备注：
		名词解释
			已支付的订单：已支付订单和货到付款提交成功订单
			有效订单：订单状态为 待发货、已发货、已完成的订单
			订单.实付金额：=现金支付金额+微众卡支付金额；不包含优惠券和积分抵扣的金额，包含微众卡支付的金额；

	查询条件
		1、刷选日期
			1）开始日期和结束日期都为空；选择开始结束日期，精确到日期
			2）开始日期或者结束日期，只有一个为空，给出系统提示“请填写XX日期”
			3）默认为‘今天’，筛选日期：‘今天’到‘今天’
			4）包含筛选日期的开始和结束的边界值
			5）手工设置筛选日期，点击查询后，‘快速查询’的所有项都处于‘未选中状态’
		2、快速查看
		    1）今天：查询的当前日期，例如，今天是2015-6-16，筛选日期是：2015-6-16到2015-6-16
		    2）昨天：查询的前一天，例如，今天是2015-6-16，筛选日期是：2015-6-15到2015-6-15
			3）最近7天；包含今天，向前7天；例如，今天是2015-6-16，筛选日期是：2015-6-10到2015-6-16
			4）最近30天；包含今天，向前30天；例如，今天是2015-6-16，筛选日期是：2015-5-19到2015-6-16
			5）最近90天；包含今天，向前90天；例如，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
			6）全部：筛选日期更新到：2013.1.1到今天

	订单概况
		1、【成交订单】=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) 

			"？"说明弹窗：当前所选时段内该店铺已发货、待发货、已完成的订单数之和

									and (订单.来源='本店')]
		2、【成交金额】=∑订单.实付金额[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)
									and (订单.来源='本店')]

			"？"说明弹窗：当前所选时段内该店铺已支付订单和货到付款提交成功订单的总金额

		3、【客单价】=【成交金额】/【成交订单】

			备注：保留小数点后两位

			"？"说明弹窗：当前所选时段内平均每个订单的金额

		4、【成交商品】=∑订单.商品件数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)
										and (订单.来源='本店')]

			"？"说明弹窗：当前所选时段内所有成交订单内商品总件数

			备注：注意一个订单包含多个商品和一个商品购买多件的情况

		5、【优惠抵扣】=∑订单.积分抵扣金额[(订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')] 
							+∑订单.优惠券抵扣金额[(订单状态 in {待发货、已发货、已完成}) 
													and (订单.下单时间 in 查询区间) and (订单.来源='本店')] 

			"？"说明弹窗：当前所选时段内成交订单中使用积分或优惠券抵扣的总金额

		6、【总运费】=∑订单.运费金额[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) 
										and (订单.来源='本店')]

			"？"说明弹窗：当前所选时段内所有成交订单中总支付的运费金额

		备注：订单来源为本店的订单，支付方式只有三种：在线支付(微信支付、支付宝支付)、货到付款

		#虽然现在‘在线支付’只有支付宝、微信两种方式，为了增加可扩展性，修改为用整体减去‘货到付款’来得到‘在线支付’，
		#这样以后再增加了其他的在线支付方式也是不用再调整的
		
		#【在线付款订单】=∑订单.个数[(支付方式 in {'微信支付'、'支付宝支付'}) 
		#								and (订单状态 in {待发货、已发货、已完成}) 
		#								and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
		7、【在线付款订单】=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) 
							-(∑订单.个数[(支付方式 in {'货到付款'}) 
										and (订单状态 in {待发货、已发货、已完成}) 
										and (订单.下单时间 in 查询区间) and (订单.来源='本店')])

			"？"说明弹窗：当前所选时段内除货到付款之外的成交订单数

		#8、【在线付款订单金额】=∑订单.实付金额[(支付方式 in {'微信支付'、'支付宝支付'}) 
		#										and (订单状态 in {待发货、已发货、已完成}) 
		#										and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
		8、【在线付款订单金额】=∑订单.实付金额[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) 
												and (订单.来源='本店')]
								-(∑订单.实付金额[(支付方式 in {'微信支付'、'支付宝支付'}) 
												and (订单状态 in {待发货、已发货、已完成}) 
												and (订单.下单时间 in 查询区间) and (订单.来源='本店')])

			"？"说明弹窗：当前所选时段内除货到付款之外的成交订单金额

		9、【货到付款订单】=∑订单.个数[(支付方式 ='货到付款') and (订单状态 in {待发货、已发货、已完成}) 
										and (订单.下单时间 in 查询区间) and (订单.来源='本店')]

			"？"说明弹窗：当前所选时段内使用货到付款方式的订单数

		10、【货到付款金额】=∑订单.实付金额[(支付方式 ='货到付款') and (订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]

			"？"说明弹窗：当前所选时段内使用货到付款方式的订单金额

	订单分析图表
		店铺内订单来源为'本店'，订单的'下单时间'在查询区间内的，有效订单(订单状态为：待发货、已发货、已完成)进行分析
		1、订单趋势
			店铺内订单来源为'本店'的，订单的'下单时间'在查询区间内的，订单不同状态的订单占比
			1）订单总量：=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)
				备注：待发货、已发货、已完成，三种订单状态的订单来源为'本店'的，订单的'下单时间'在查询区间内的订单数之和
			2）图形划过展开，展示内容为（该区域订单状态、订单量、订单量占比）
			3）点击详情跳转到，带入的查询条件
				【订单名称】：空；【订单编号】：空；【支付方式】：全部；【订单状态】：当前的图形对应的订单状态
				【复购筛选】：全部；【优惠抵扣】：全部；【仅显示微众卡抵扣订单】：否
		2、复购率
			店铺内订单来源为'本店'的订单，买家在本店购买次数的统计分析
			1）订单总量：=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) 
									and (订单.来源='本店')]
			2）“初次购买”：在查询区间以前没有发生过购买，在查询区间内发生初次购买的用户订单数和其在总订单数占比
			3）“重复购买”：在该时间段以前发生过购买或者在该订单的订单时间之前发生过购买，在该时间段内又发生了购买的用户订单数和其在总订单数占比
							满足下面条件的订单个数总和；（1）下单时间在查询区间内的‘有效订单’（1）订单的买家在该订单下单时间之前有‘有效订单’
			4）图形划过展开，展示内容为（该区域类型、订单量、订单量占比）
			5）点击详情跳转到，带入的查询条件
				【订单名称】：空；【订单编号】：空；【支付方式】：全部；【订单状态】：待发货、已发货、已完成
				【复购筛选】：当前的图形对应的类；【优惠抵扣】：全部；【仅显示微众卡抵扣订单】：否

			备注：1）注意买家在查询区间内发生两次购买，第一次购买为初次购买的统计到'初次购买';
					第二次购买统计到'重复购买'。
				2）买家未知的订单按照内部的ID计算复购

		3、买家来源
			店铺内订单来源为'本店'的订单，订单的'下单时间'在查询区间内的，"有效订单"的买家来源的占比
			1）订单总量：=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) 
									and (订单.来源='本店')]
			2）“直接关注购买”：=∑订单.个数[(买家来源 ='直接关注') and (订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			3）“推广扫码关注购买”：=∑订单.个数[(买家来源 ='推广扫码') and (订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			4）“分享链接关注购买”：=∑订单.个数[(买家来源 ='分享链接') and (订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			5）“其他”：=∑订单.个数[(买家来源不确定) and (订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			6）图形划过展开，展示内容为（该区域类型、订单量、订单量占比）
			7）点击详情跳转到，带入的查询条件
				【订单名称】：空；【订单编号】：空；【支付方式】：全部；【订单状态】：待发货、已发货、已完成
				【复购筛选】：当前的图形对应的类；【优惠抵扣】：全部；【仅显示微众卡抵扣订单】：否

			备注：1）买家可能会先下订单再关注，即买家的'关注时间'晚于订单的'下单时间'，这种订单的归类到其他
				2）没有关注店铺公众账号，直接下的订单的归类到其他
				即：所有不能确定买家的都归类到其他

		4、支付金额
			店铺内订单来源为'本店'的订单，订单的'下单时间'在查询区间内的，"有效订单"的支付方式的支付金额占比
			1）订单总金额：=∑订单.实付金额[(订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			2）支付宝支付金额:=∑订单.支付宝支付金额[(订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			3）微信支付金额:=∑订单.微信支付金额[(订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			4）货到付款支付金额:=∑订单.货到付款支付金额[(订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			5）微众卡支付金额:=∑订单.微众卡支付金额[(订单状态 in {待发货、已发货、已完成}) 
											and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			6）图形划过展开，展示内容为（该区域类型、金额、金额占比）

			备注：金额维度的分析，没有点击详情进入订单明细分析界面的功能					
		
		5、优惠抵扣
			店铺内订单来源为'本店'的订单，订单的'下单时间'在查询区间内的，"有效订单"的优惠抵扣方式的订单占比
			1）订单总量：=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) 
									and (订单.来源='本店') and (优惠抵扣使用 in {积分、优惠券、微众卡})]
			2）微众卡支付：=∑订单.个数[(订单.优惠抵扣 = {微众卡}) and (订单状态 in {待发货、已发货、已完成}) 
									and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
				（1）微众卡支付金额：=∑订单.微众卡支付金额[(订单.优惠抵扣 = {微众卡}) and (订单状态 in {待发货、已发货、已完成}) 
									and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			3）积分抵扣：=∑订单.个数[(订单.优惠抵扣 = {积分抵扣}) and (订单状态 in {待发货、已发货、已完成}) 
				（1）积分抵扣金额：=∑订单.积分抵扣金额[(订单.优惠抵扣 = {积分抵扣}) and (订单状态 in {待发货、已发货、已完成}) 
									and (订单.下单时间 in 查询区间) and (订单.来源='本店')]	
			4）优惠券：=∑订单.个数[(订单.优惠抵扣 = {优惠券}) and (订单状态 in {待发货、已发货、已完成}) 
									and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
				（1）优惠券金额：=∑订单.优惠券金额[(订单.优惠抵扣 = {优惠券}) and (订单状态 in {待发货、已发货、已完成}) 
									and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			5）微众卡+积分：=∑订单.个数[(订单.优惠抵扣 = {微众卡+积分}) 
									and (订单状态 in {待发货、已发货、已完成}) 
									and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
				（1）(微众卡+积分)金额：=∑订单.(微众卡+积分)金额[(订单.优惠抵扣 = {微众卡+积分}) 
									and (订单状态 in {待发货、已发货、已完成}) 
									and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
			6）微众卡+优惠券：=∑订单.个数[(订单.优惠抵扣 = {微众卡+优惠券}) 
									and (订单状态 in {待发货、已发货、已完成}) 
									and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
				（1）(微众卡+优惠券)金额：=∑订单.(微众卡+优惠券)金额[(订单.优惠抵扣 = {微众卡+优惠券}) 
									and (订单状态 in {待发货、已发货、已完成}) 
									and (订单.下单时间 in 查询区间) and (订单.来源='本店')]
             备注：目前的一个订单中不能同时使用‘积分’和‘优惠券’，这样我们的‘优惠抵扣’的图表的两项（积分+优惠券；微众卡+积分+优惠券）就不存在了


			9）图形划过展开，展示内容为（该区域类型、订单量、订单量占比、金额）
			10）点击详情跳转到，带入的查询条件
				【筛选日期】：当前‘订单概况’的筛选日期
				【订单名称】：空；【订单编号】：空；【支付方式】：全部；
				【订单状态】：待发货、已发货、已完成【复购筛选】：全部；
				【优惠抵扣】：当前的图形对应的优惠抵扣方式；【仅显示微众卡抵扣订单】：否

Background:
	#说明：toms代表微众商城，jobs代表商户
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
			"一元等价的积分数量": 10
		}
		"""
	When jobs已添加支付方式
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
	When jobs已添加商品
		"""
		[{
			"name": "商品1",
			"promotion_title": "促销商品1",
			"category": "分类1",
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
		
		When bill关注jobs的公众号
		And tom关注jobs的公众号
		And nokia关注jobs的公众号
		# tom2 => mary
		And mary关注jobs的公众号
		# tom3 => jim
		And jim关注jobs的公众号
		# tom4 => kate
		And kate关注jobs的公众号


@wip.order_survey  @ignore
Scenario: 1 订单概况数据，默认筛选日期当天
	Given jobs登录系统

	# 原来是'jobs首次进入订单概况或者刷新订单概况'
	When 浏览'销售分析-订单概况'页面
	#      data: [{'content': {'cod_amount': 0.0, 'paid_amount': 0.0, 'weixinpay_amount': 0.0, 'discount_stats': {'discount_order_num': 0, 'integral_coupon_amount':0.0, 'coupon_amount': 0.0, 'coupon_num': 0, 'wezoom_integral_coupon_num': 0, 'wezoom_coupon_num': 0, 'wezoom_integral_coupon_amount': 0.0, 'wezoom_coupon_amount': 0.0, 'integral_amount': 0.0, 'wezoom_integral_num': 0, 'wezoom_amount': 0.0,'integral_num': 0, 'integral_coupon_num': 0, 'wezoom_integral_amount': 0.0, 'wezoom_num': 0}, 'start_time': '2015-06-24 00:00:00', 'product_num': 0, 'alipay_amount': 0.0, 'online_order_num': 0, 'wezoom_card_amount': 0.0, 'repeated_num': 0,'postage_amount': 0.0, 'cod_order_num': 0, 'end_time': '2015-06-24 23:59:59', 'order_num': 0, 'online_paid_amount': 0.0, 'order_trend_stats': {'cancel_num': 0,'refunding_num': 0, 'wait_num': 0, 'refunded_num': 0, 'succeeded_num': 0, 'not_shipped_num': 0, 'shipped_num': 0}, 'buyer_source_stats': {'sub_source_num': 0, 'url_source_num': 0, 'qrcode_source_num': 0, 'other_source_num': 0}, 'discount_amount': 0.0}, 'name': 'stats_data'}]


	Then 页面上的'筛选日期'
		"""
		{
			"begin_time": "$(今天) 00:00:00",
			"end_time": "$(今天) 23:59:59"
		}
		"""



Scenario: Background

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


			When jobs已添加积分应用活动
				"""
				[{
					"name": "商品1积分应用",
					"start_date": "2014-8-1",
					"end_date": "10天后",
					"products": ["商品1"],
					"is_permanant_active": "false",
					"rules": [{
						"member_grade_name": "全部会员",
						"discount": 70,
						"discount_money": 70.0
					}]
				}]
				"""
			And jobs已添加优惠券
				"""
				[{
					"name": "商品2优惠券",
					"money": 10,
					"start_date": "2014-8-1",
					"end_date": "10天后",
					"coupon_id_prefix": "coupon1_id_"
				}]
				"""




			When jobs已获取微信用户
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

	#用toms登录后，同样的消费者 bill，tom等购买jobs同步到商城的商品，然后验证统计时只统计在jobs店铺消费的订单，不统计在商城消费的订单
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
				| 2014-9-2  8:00  	| tom      | toms      | 商品1,1          | 支付    | 微信支付       | 10      | 100      | 0        | 0      | 110         | 0            | 0      | 110    | 0    | jobs,发货         |  已发货         |
				| 2014-9-3  7:59  	| bill     | toms      | 商品1,1          | 支付    | 货到付款       | 10      | 100      | 20       | 0      | 90          | 0            | 0      | 0      | 90   |                   |  待发货         |
#'''

Scenario: 1 订单概况数据，默认筛选日期当天

	#订单概况
		Then jobs获得订单概况
		|    item     | quantity |
		|   成交订单  |    2     |
		|   成交金额  |   190    |
		|   客单价    |   95     |
		|   成交商品  |   2      |
		|   优惠抵扣  |   30     |
		|   总运费    |   20     |
		| 在线支付订单|    2     |
		| 在线支付金额|   190    |
		| 货到付款订单|    0     |
		| 货到付款金额|    0     |

	#订单趋势
		And jobs获得订单趋势
		| order_status | order_quantity | proportion |
		|  待支付      |       0        |     0%     |
		|  已取消      |       0        |     0%     |
		|  待发货      |       0        |     0%     |
		|  已发货      |       1        |     50%    |
		|  已完成      |       1        |     50%    |
		|  退款中      |       0        |     0%     |
		|  退款成功    |       0        |     0%     |

		#订单趋势详情
		#已发货
			When jobs进入'已发货'详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"今天",
				"end_date":"今天",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":"已发货",
				"re_purchase":"",
				"preferential_deduction":"",
				"only_weizoom_card":""
			}]
			"""
			And jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号 |    10           |   10    |   100       |  微信支付      |  tom     | 今天 00:2       |  已发货      |

		#已完成
			When jobs进入'已完成'详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"今天",
				"end_date":"今天",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":"已完成",
				"re_purchase":"",
				"preferential_deduction":"",
				"only_weizoom_card":""
			}]
			"""
			And jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号 |    20           |   10    |   90        |  支付宝支付    |          |  今天 00:10     |  已完成      |

	#复购率
		And jobs获得复购率
			|   item    | order_quantity | proportion |
			|  初次购买 |       1        |   50%      |
			|  重复购买 |       1        |   50%      |

		#复购详情

			#重复购买
			When jobs进入'初次购买'详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"今天",
				"end_date":"今天",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"初次购买",
				"preferential_deduction":"",
				"only_weizoom_card":"",
				"buyers_source":""
			}]
			"""
			Then jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号 |    20           |   10    |   90        |  支付宝支付    |          | 今天 00:10      |  已完成      |
			

			#重复购买
			When jobs进入'重复购买'详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"今天",
				"end_date":"今天",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"重复购买",
				"preferential_deduction":"",
				"only_weizoom_card":"",
				"buyers_source":""
			}]
			"""
			Then jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号 |    10           |   10    |   100       |  微信支付      |  tom     | 今天 00:2       |  已发货      |

	#买家来源
		And jobs获得买家来源
			|     item         |  order_quantity  |  proportion  |
			| 直接关注购买     |        0         |     0%       |
			| 推广扫码关注购买 |        1         |    50%       |
			| 分享链接关注购买 |        0         |     0%       |
			| 其他             |        1         |    50%       |

		#买家来源详情

			#推广扫码关注购买
				When jobs进入'推广扫码关注购买'详情
				Then jobs获得查询条件
				"""
				[{
					"begin_date":"今天",
					"end_date":"今天",
					"product_name":"",
					"order_number":"",
					"payment_method":"",
					"order_status":["待发货","已发货","已完成"],
					"re_purchase":"",
					"preferential_deduction":"",
					"only_weizoom_card":"",
					"buyers_source":"推广扫码关注购买"
				}]
				"""
				Then jobs获得订单列表
				| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号 |    10           |   10    |   100       |  微信支付      |  tom     | 今天 00:2       |  已发货      |	

			#其他
				When jobs进入'其他'详情
				Then jobs获得查询条件
				"""
				[{
					"begin_date":"今天",
					"end_date":"今天",
					"product_name":"",
					"order_number":"",
					"payment_method":"",
					"order_status":["待发货","已发货","已完成"],
					"re_purchase":"",
					"preferential_deduction":"",
					"only_weizoom_card":"",
					"buyers_source":"其他"
				}]
				"""
				Then jobs获得订单列表
				| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号 |    20           |   10    |   90        |  支付宝支付    |          |  今天 00:10     |  已完成      |

	#支付金额
		And jobs获得支付金额
			|     item     |  sum_money  |  proportion  |	
			|    支付宝    |     90      |     47.37%   |
			|   微信支付   |     50      |     26.32%   |
			|   货到付款   |      0      |     0%       |
			|  微众卡支付  |     50      |     26.32%   |

	#优惠抵扣
		And jobs获得优惠抵扣
			|         item           |  order_quantity  |  proportion  |  sum_money  |
			|     微众卡支付         |      0           |      0%      |     0       |	
			|     积分抵扣           |      1           |     50%      |     20      |	
			|     优惠券             |      0           |      0%      |     0       |	
			|     微众卡+积分        |      0           |      0%      |     0       |	

		#优惠抵扣详情

			#积分抵扣 
				When jobs进入'积分抵扣 '详情
				Then jobs获得查询条件
				"""
				[{
					"begin_date":"今天",
					"end_date":"今天",
					"product_name":"",
					"order_number":"",
					"payment_method":"",
					"order_status":["待发货","已发货","已完成"],
					"re_purchase":"",
					"preferential_deduction":"积分抵扣",
					"only_weizoom_card":"",
					"buyers_source":""
				}]
				"""
				Then jobs获得订单列表
				| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号 |    20           |   10    |   90        |  支付宝支付    |          |  今天 00:10     |  已完成      |

			#微众卡+优惠券 
				When jobs进入'微众卡+优惠券'详情
				Then jobs获得查询条件
				"""
				[{
					"begin_date":"今天",
					"end_date":"今天",
					"product_name":"",
					"order_number":"",
					"payment_method":"",
					"order_status":["待发货","已发货","已完成"],
					"re_purchase":"",
					"preferential_deduction":"微众卡+优惠券",
					"only_weizoom_card":"",
					"buyers_source":""
				}]
				"""
				Then jobs获得订单列表
				| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品1     | 对应订单编号 |    10           |   10    |   100       |  微信支付      |  tom     | 今天 00:2       |  已发货      |	

Scenario: 2 订单概况数据，查询区间

	Given jobs登录系统

	When jobs筛选日期
		"""
		[{
			"begin_date":"2014-9-1",
			"end_date":"2014-9-21"
		}]
		"""

	#订单概况
		Then jobs获得订单概况
			|    item     | quantity |
			|   成交订单  |    8     |
			|   成交金额  |   1230   |
			|   客单价    |   153.75 |
			|   成交商品  |   12     |
			|   优惠抵扣  |   90     |
			|   总运费    |   120    |
			| 在线支付订单|    7     |
			| 在线支付金额|   1140   |
			| 货到付款订单|    1     |
			| 货到付款金额|    90    |

	#订单趋势
		And jobs获得订单趋势
			| order_status | order_quantity | proportion |
			|  待发货      |       4        |   36.36%   |
			|  已发货      |       2        |   18.18%   |
			|  已完成      |       2        |   18.18%   |

		#订单趋势详情

			#待发货
				When jobs进入'待发货'详情
				Then jobs获得查询条件
				"""
				[{
					"begin_date":"2014-9-1",
					"end_date":"2014-9-21",
					"product_name":"",
					"order_number":"",
					"payment_method":"",
					"order_status":"待发货",
					"re_purchase":"",
					"preferential_deduction":"",
					"only_weizoom_card":""
				}]
				"""
				And jobs获得订单列表
				| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				| 商品1，商品2 | 对应订单编号 |    30           |   25    |   295       |  支付宝        |  Tom     | 2014-9-7  12:00 |  待发货      |
				| 商品1，商品2 | 对应订单编号 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
				|    商品1     | 对应订单编号 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
				|    商品1     | 对应订单编号 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |

			#已发货
				When jobs进入'已发货'详情
				Then jobs获得查询条件
				"""
				[{
					"begin_date":"2014-9-1",
					"end_date":"2014-9-21",
					"product_name":"",
					"order_number":"",
					"payment_method":"",
					"order_status":"已发货",
					"re_purchase":"",
					"preferential_deduction":"",
					"only_weizoom_card":""
				}]
				"""
				And jobs获得订单列表
				| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
				|    商品1     | 对应订单编号 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |			

			#已完成
				When jobs进入'已完成'详情
				Then jobs获得查询条件
				"""
				[{
					"begin_date":"2014-9-1",
					"end_date":"2014-9-21",
					"product_name":"",
					"order_number":"",
					"payment_method":"",
					"order_status":"已完成",
					"re_purchase":"",
					"preferential_deduction":"",
					"only_weizoom_card":""
				}]
				"""
				And jobs获得订单列表
				| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
				|    商品2     | 对应订单编号 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  已完成      |
				|    商品1     | 对应订单编号 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |		

	#复购率
		And jobs获得复购率
			|   item    | order_quantity | proportion |
			|  初次购买 |       2        |   25%      |
			|  重复购买 |       6        |   75%      |

		#复购详情
		#初次购买
		When jobs进入'初次购买'详情
		Then jobs获得查询条件
		"""
		[{
			"begin_date":"2014-9-1",
			"end_date":"2014-9-21",
			"product_name":"",
			"order_number":"",
			"payment_method":"",
			"order_status":["待发货","已发货","已完成"],
			"re_purchase":"初次购买",
			"preferential_deduction":"",
			"only_weizoom_card":"",
			"buyers_source":""
		}]
		"""
		Then jobs获得订单列表
		| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		| 商品2        | 对应订单编号 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |
		| 商品1        | 对应订单编号 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |		

		#重复购买
		When jobs进入'重复购买'详情
		Then jobs获得查询条件
		"""
		[{
			"begin_date":"2014-9-1",
			"end_date":"2014-9-21",
			"product_name":"",
			"order_number":"",
			"payment_method":"",
			"order_status":["待发货","已发货","已完成"],
			"re_purchase":"重复购买",
			"preferential_deduction":"",
			"only_weizoom_card":"",
			"buyers_source":""
		}]
		"""
		Then jobs获得订单列表
		| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		| 商品2        | 对应订单编号 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  待发货      |
		| 商品1，商品2 | 对应订单编号 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
		| 商品1，商品2 | 对应订单编号 |    0            |   25    |   325       |  支付宝        |  -bill   | 2014-9-6  10:00 |  待发货      |
		| 商品1        | 对应订单编号 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
		| 商品1        | 对应订单编号 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
		| 商品1        | 对应订单编号 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |

	#买家来源
		And jobs获得买家来源
			|     item         |  order_quantity  |  proportion  |
			| 直接关注购买     |        3         |    37.5%     |
			| 推广扫码关注购买 |        3         |    37.5%     |
			| 分享链接关注购买 |        2         |     25%      |
			| 其他             |        0         |     0%       |

		#买家来源详情
		#直接关注购买
			When jobs进入'直接关注购买'详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"2014-9-1",
				"end_date":"2014-9-21",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"",
				"preferential_deduction":"",
				"only_weizoom_card":"",
				"buyers_source":"直接关注购买"
			}]
			"""
			Then jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			| 商品1，商品2 | 对应订单编号 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |
			|    商品1     | 对应订单编号 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |
			|    商品1     | 对应订单编号 |    0            |   10    |   110       |  支付宝        |  bill    | 2014-9-1  10:00 |  待发货      |						

		#推广扫码关注购买
			When jobs进入'推广扫码关注购买'详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"2014-9-1",
				"end_date":"2014-9-21",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"",
				"preferential_deduction":"",
				"only_weizoom_card":"",
				"buyers_source":"推广扫码关注购买"
			}]
			"""
			Then jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			| 商品1，商品2 | 对应订单编号 |    30           |   25    |   295       |  支付宝        |  tom     | 2014-9-7  12:00 |  待发货      |
			| 商品1        | 对应订单编号 |    10           |   10    |   100       |  微信支付      |  tom     | 2014-9-5  10:00 |  已完成      |
			| 商品1        | 对应订单编号 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2  00:00 |  已发货      |

		#分享链接关注购买
			When jobs进入'分享链接关注购买'详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"2014-9-1",
				"end_date":"2014-9-21",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"",
				"preferential_deduction":"",
				"only_weizoom_card":"",
				"buyers_source":"分享链接关注购买"
			}]
			"""
			Then jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			| 商品2        | 对应订单编号 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  待发货      |
			| 商品2        | 对应订单编号 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |

	#支付金额
		And jobs获得支付金额
			|     item     |  sum_money  |  proportion  |	
			|    支付宝    |    305      |    24.80%    |
			|   微信支付   |    215      |    17.48%    |
			|   货到付款   |    90       |     7.32%    |
			|  微众卡支付  |    620      |    50.41%    |

	#优惠抵扣
		And jobs获得优惠抵扣
			|         item           |  order_quantity  |  proportion  |  sum_money  |
			|     微众卡支付         |      1           |  16.67%      |  325        |	
			|     积分抵扣           |      1           |  16.67%      |  20         |	
			|     优惠券             |      1           |  16.67%      |  10         |	
			|     微众卡+积分        |      1           |  16.67%      |  115        |	
			|     微众卡+优惠券      |      1           |  16.67%      |  110        |	

		#优惠抵扣详情
		#微众卡支付 
			When jobs进入'微众卡支付 '详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"2014-9-1",
				"end_date":"2014-9-21",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"",
				"preferential_deduction":"微众卡支付",
				"only_weizoom_card":"是",
				"buyers_source":""
			}]
			"""
			Then jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			| 商品1，商品2 | 对应订单编号 |    0            |   25    |   325       |  支付宝        |  bill    | 2014-9-6  10:00 |  待发货      |

		#积分抵扣 
			When jobs进入'积分抵扣 '详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"2014-9-1",
				"end_date":"2014-9-21",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"",
				"preferential_deduction":"积分抵扣",
				"only_weizoom_card":"",
				"buyers_source":""
			}]
			"""
			Then jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品1     | 对应订单编号 |    20           |   10    |   90        |  货到付款      |  bill    | 2014-9-3  23:59 |  待发货      |

		#优惠券 
			When jobs进入'优惠券 '详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"2014-9-1",
				"end_date":"2014-9-21",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"",
				"preferential_deduction":"优惠券",
				"only_weizoom_card":"",
				"buyers_source":""
			}]
			"""
			Then jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			|    商品2     | 对应订单编号 |    10           |   15    |   105       |  微信支付      |  tom2    | 2014-9-20 12:00 |  已发货      |

		#微众卡+积分 
			When jobs进入'微众卡+积分 '详情
			Then jobs获得查询条件
			"""
			[{
				"begin_date":"2014-9-1",
				"end_date":"2014-9-21",
				"product_name":"",
				"order_number":"",
				"payment_method":"",
				"order_status":["待发货","已发货","已完成"],
				"re_purchase":"",
				"preferential_deduction":"微众卡+积分",
				"only_weizoom_card":"",
				"buyers_source":""
			}]
			"""
			Then jobs获得订单列表
			| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
			| 商品2        | 对应订单编号 |    20           |   15    |   95        |  微信支付      |  tom2    | 2014-9-21 14:00 |  待发货      |

Scenario: 3 订单概况数据，筛选日期，默认筛选日期当天；快速查询；重置

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

	#备注：昨天，今天是2015-6-16，筛选日期：2015-6-15到2015-6-15
		When jobs昨天
		Then jobs筛选日期
			"""
			[{
				"begin_date":"昨天",
				"end_date":"昨天"
			}]
			"""

	#备注：最近7天，今天是2015-6-16，筛选日期：2015-6-10到2015-6-16
		When jobs最近7天
		Then jobs筛选日期
			"""
			[{
				"begin_date":"7天前",
				"end_date":"今天"
			}]
			"""

	#备注：最近30天，今天是2015-6-16，筛选日期：2015-5-19到2015-6-16
		When jobs最近30天
		Then jobs筛选日期
			"""
			[{
				"begin_date":"30天前",
				"end_date":"今天"
			}]
			"""

	#备注：最近90天，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
			When jobs最近90天
			Then jobs筛选日期
				"""
				[{
					"begin_date":"90天前",
					"end_date":"今天"
				}]
				"""

	#重置
		When jobs设置筛选日期
		"""
		[{
			"begin_date":"2014-9-1",
			"end_date":"2014-9-10"
		}]
		"""
		When jobs重置

		Then jobs获得查询条件
		"""
		[{
			"begin_date":"",
			"end_date":""
		}]
		"""

Scenario: 4 订单概况数据,补充复购率对买家为‘未知’的订单的统计错误

	Given jobs登录系统

	When 微信用户批量消费jobs的商品
			| order_datetime  	| consumer |businessman|      product     | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action       |  order_status   |
			| 今天  10:00    	|          | jobs      | 商品1,1          | 支付    | 支付宝支付     | 10      | 100      | 0        | 0      | 110         | 0            | 110    | 0      | 0    |                   |  待发货         |

	When jobs筛选日期
	"""
	[{
		"begin_date":"今天",
		"end_date":"今天"
	}]
	"""

	#复购率
	Then jobs获得复购率
		|   item    | order_quantity | proportion |
		|  初次购买 |       2        |   66.67%   |
		|  重复购买 |       1        |   33.33%   |

	#复购详情

		#初次购买
		When jobs进入'初次购买'详情
		Then jobs获得查询条件
		"""
		[{
			"begin_date":"今天",
			"end_date":"今天",
			"product_name":"",
			"order_number":"",
			"payment_method":"",
			"order_status":["待发货","已发货","已完成"],
			"re_purchase":"初次购买",
			"preferential_deduction":"",
			"only_weizoom_card":"",
			"buyers_source":""
		}]
		"""
		Then jobs获得订单列表
		| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		|    商品1     | 对应订单编号 |    0            |   10    |   110       |  支付宝支付    |          | 今天 10:00      |  待发货      |
		|    商品1     | 对应订单编号 |    20           |   10    |   90        |  支付宝支付    |          | 今天 00:10      |  已完成      |


		#重复购买
		When jobs进入'重复购买'详情
		Then jobs获得查询条件
		"""
		[{
			"begin_date":"今天",
			"end_date":"今天",
			"product_name":"",
			"order_number":"",
			"payment_method":"",
			"order_status":["待发货","已发货","已完成"],
			"re_purchase":"重复购买",
			"preferential_deduction":"",
			"only_weizoom_card":"",
			"buyers_source":""
		}]
		"""
		Then jobs获得订单列表
		| product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer | order_datetime  | order_status |
		|    商品1     | 对应订单编号 |    10           |   10    |   100       |  微信支付      |  tom     | 今天 00:2       |  已发货      |

