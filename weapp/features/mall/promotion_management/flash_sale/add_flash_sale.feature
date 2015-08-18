#_author_:张三香

Feature:创建限时抢购活动

"""
说明：
	1、限时抢购活动的设置规则
		1）【限购广告语】：手机端商品详情页，红字显示显示在商品名称后面
		2）【活动时间】：开始结束时间只能选择今天及其之后的时间，结束时间必须在开始时间之后
		3）【会员等级】：设置什么等级的会员可以参加此次活动，下拉选项为：全部会员、会员等级中设置的会员等级列表；选择"全部会员"或者单选一级会员
		4）【限购价格】：限购价格必须小于商品原价；多规格商品只能定义一个限购价格，不能根据不同规格定义限购价格
		5）【单人单次限购】：单人单次限购的数量；空为不限制
		6）【限购周期】：（？天），设置限购的周期，即设置多少天内只能购买一次；只要提交订单（订单状态不是"已取消"）就算购买一次；空为不限制
	2、限时抢购商品订单规则
		1）设置了"单人单次限购"的，在下订单的时候，数量只能增加到限购的数量，再增加数量不变，会给出提示"限购？件"
		2）购买多规格的有"单人单次限购"的限时抢购商品，在加入购物车时，不同规格分别限购，提交订单时，对限购数量不区分规格计算
		订单中多规格商品数量的总和超过限购数量，给出提示"该订单内商品状态发生变化"
		3）会员既具有会员等级价又具有会员限时抢购权限的，限时抢购活动优先于会员等级价，会员看到的商品的价格是"限时抢购价格"，按照限时抢购的价格形成订单
	3、设置了“限时抢购”的商品，不能再设置“买赠”“优惠券活动”，三个活动是互斥的，只要设置了其中的一个活动，就不能再设置其他两个活动
"""
Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
			[{
				"name":"商品0",
				"price":100.00,
				"purchase_count":2
			},{
				"name":"商品1",
				"price":80.50
			},{
				"name": "商品2",
				"is_enable_model": "启用规格",
				"model":
				{
					"models":
					{
						"M": 
						{
							"price": 100.00,
							"stock_type": "无限"
						},
					"S": {
						"price": 200.00,
						"stock_type": "无限"
						}
					}
				}
			},{
				"name":"商品3",
				"price":100.00,
				"is_member_product": "on"
			},{
				"name":"商品4",
				"price":100.00
			},{
				"name":"商品5",
				"price":100.00,
				"is_member_product": "on"
			},{
				"name":"商品6",
				"price":100.00,
				"is_member_product": "on"
			}]
		"""
		#支付方式
	Given jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""

	#会员等级
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"discount": "10.0"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9.0"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8.0"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7.0"
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品4",
			"is_permanant_active": false,
			"rules": [{
				"member_grade_name": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		},{
			"name": "商品5积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": ["商品5"],
			"is_permanant_active": false,
			"rules": [{
				"member_grade_name": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}]
		"""



#该场景在new_promotion_product_search.feature中覆盖
Scenario: 0 选取起购数量大于1的商品，创建限时抢购活动（起购数量大于1的商品不能参与限时抢购）
	Given jobs登录系统
	#When jobs创建限时抢购活动
	#新建限时抢购页面，商品查询弹窗中的数据列表中不存在'商品0'

@promotion @promotionFlash
Scenario: 1 选取无规格商品，创建限时抢购活动(广告语为空时，显示活动名称)
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
			[{
				"name": "商品1限时抢购",
				"promotion_slogan":"",
				"start_date": "今天",
				"end_date": "1天后",
				"products": ["商品1"],
				"member_grade": "全部会员",
				"count_per_purchase": 2,
				"promotion_price": 80.00,
				"limit_period": 1
			}]
		"""
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "活动名称：商品1限时抢购",
				"products":["商品1"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
		"""

@promotion @promotionFlash
Scenario: 2 选取多规格商品，创建限时抢购活动（广告语非空，显示广告语）
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
			[{
				"name": "商品2限时抢购",
				"promotion_slogan":"抢购抢购啦",
				"start_date": "今天",
				"end_date": "1天后",
				"products": ["商品2"],
				"member_grade": "铜牌会员",
				"count_per_purchase": 2,
				"promotion_price": 80.00
			}]
		"""
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "广告语：抢购抢购啦",
				"products":["商品2"],
				"product_price":"100.00~200.00",
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
		"""

@promotion @promotionFlash
Scenario: 3 选取参与会员折扣的商品，创建限时抢购活动(限时抢购优先)
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
			[{
				"name": "商品3限时抢购",
				"promotion_slogan":"商品3抢购",
				"start_date": "今天",
				"end_date": "1天后",
				"products": ["商品3"],
				"member_grade": "铜牌会员",
				"count_per_purchase": 2,
				"promotion_price": 80.00
			}]
		"""
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "广告语：商品3抢购",
				"products":["商品3"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
		"""

@promotion @promotionFlash
Scenario: 4 选取参与积分应用的商品，创建限时抢购活动
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
			[{
				"name": "商品4限时抢购",
				"promotion_slogan":"商品4抢购",
				"start_date": "今天",
				"end_date": "1天后",
				"products": ["商品4"],
				"member_grade": "铜牌会员",
				"count_per_purchase": 2,
				"promotion_price": 80.00
			}]
		"""
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "广告语：商品4抢购",
				"products":["商品4"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"进行中",
				"start_date": "今天",
				"end_date": "1天后",
				"actions": ["详情","结束"]
			}]
		"""

@promotion @promotionFlash
Scenario: 5 选取参与会员折扣和积分应用的商品，创建限时抢购活动
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
			[{
				"name": "商品5限时抢购",
				"promotion_slogan":"商品5抢购",
				"start_date": "明天",
				"end_date": "3天后",
				"products": ["商品5"],
				"member_grade": "银牌会员",
				"count_per_purchase": 1,
				"promotion_price": 80.00
			}]
		"""
	Then jobs获取限时抢购活动列表
		"""
			[{
				"name": "广告语：商品5抢购",
				"products":["商品5"],
				"product_price":100.00,
				"promotion_price":80.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "3天后",
				"actions": ["详情","结束"]
			}]
		"""

@promotion @promotionFlash
Scenario: 6 创建限时抢购活动，必填字段的校验
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
			[{
				"name": "",
				"promotion_slogan":"",
				"start_date": "",
				"end_date": "",
				"products":"",
				"member_grade": "",
				"count_per_purchase":"",
				"promotion_price":""
			}]
		"""
	Then jobs获得系统提示'请先选择商品'
	And jobs获得系统提示'活动名称必须在1-20个字内'
	And jobs获得系统提示'必须选择一个开始时间，必须选择一个过期时间'
	#限购价格提示：
	And jobs获得系统提示'内容不能为空'

@promotion @promotionFlash
Scenario: 7 创建限时抢购活动，限购价格必须小于商品原价的校验（多规格商品，则必须小于价格最低的规格商品原价）
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
			[{
				"name": "商品6限时抢购",
				"promotion_slogan":"商品6抢购",
				"start_date": "明天",
				"end_date": "3天后",
				"products": ["商品6"],
				"member_grade": "银牌会员",
				"count_per_purchase": 1,
				"promotion_price": 101.00
			}]
		"""
	Then jobs获得系统提示'限购价格必须小于商品原价'

