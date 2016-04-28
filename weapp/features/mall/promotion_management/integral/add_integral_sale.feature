#_author_: "张三香"
#_editor_:雪静 2015.10.15
#_editor_:三香 2016.10.15

Feature: 创建积分应用活动
		Jobs能通过管理系统在商城中添加'积分应用'活动
	"""
		补充规则2016-04-27
		1、创建积分应用选择商品：
			不填写商品查询条件，点击"查询"弹出选择"已上架商品"和"商品分组"的弹窗
			（1）"已上架商品"页签
				【商品条码】：商品详情中的"商品条码"
				【商品名称】：商品详情中的"商品名称"
				【商品价格(元)】：商品详情中的"商品价格"
				【商品库存】：商品详情中的"商品库存"
				【以参与促销】：参与"积分应用"和"团购"活动（进行中和未开始）的，显示此活动对应的活动名称；参与其他促销活动的直接显示空
				【操作】："选取"或者空；参与"积分应用"和"团购"活动（进行中和未开始）的商品，为空，不能选择；参与其他促销活动的，为"选取"，可以被选择
				1）空条件查询：已上架商品页签 "在售商品"列表商品按创建时间排列显示，并分页显示
				2）按照【商品名称】和【商品条码】模糊匹配查询，只过滤"已上架商品"页签
				3）选择已上架商品页签，多选
			（2）"商品分组"页签
					【标题】：商品分组名称
					【创建时间】：商品分组创建时间
					【操作】："选取"；
			(3)“已上架商品”与“商品分组”为“多选”，可以混合选择，在分页间多选，切换页签，不保留之前的选择；选择后，将选择的商品和选择的分组内的商品进行去重，并去掉分组中参与"积分应用"和"团购"活动（进行中和未开始）的商品，带入积分商品列表
		2、积分应用活动设置规则
			1）【活动名称】：必填字段，1-20个字内
			2）【广告语】：在商品名称后红字显示
			3）【比例设置】
				（1）统一设置：
					为全部等级的会员设置统一的积分抵扣上限
				（2）分级设置：
					为系统中所有等级的会员分别设置积分抵扣上限
				（3）抵扣上限和金额占比的显示和计算规则
					抵扣上限：
						允许输入大于等于0，小于等于商品价格（选取多个商品时，需小于等于最小的商品价格）
						支持最多2为小数
					金额占比:抵扣上限/商品价格,保留两位小数（选取多个商品时，商品价格选取最小的商品价格进行计算）
			4）【活动时间】：开始结束时间只能选择今天及其之后的时间，结束时间必须在开始时间之后
				勾选"永久"，清空活动时间，此活动永久有效，除非手动结束活动
		3、结束积分应用活动
			‘进行中’和‘未开始’的积分应用活动，可以手动进行'结束'操作
			‘永久’和‘非永久’的积分应用活动，一旦结束在购买时就不能使用了
			选取一个或多个商品的积分应用活动，所有商品删除后，活动状态变为"已结束"
			选取一个或多个商品的积分应用活动，所有商品下架后，活动状态不变化
		4、删除积分应用活动
			‘已结束’的积分应用活动才可以删除
		5、积分使用规则
			1）积分和优惠券不能在同一个订单中同时使用，即使两个活动针对的是不同的商品
			2）一个订单包含多个具有积分活动的商品，每个商品分别使用自己的积分活动
			3）会员既具有会员等级价又具有会员积分活动权限的，会员看到的商品显示会员价，购买时会员价下单，并在会员价的基础上使用积分抵扣
		6、【保存】新建积分应用时，进行校验，存在不符合条件（下架、删除、参与参与"积分应用"和"团购"活动（进行中和未开始））的商品给出提示"部分商品已发生其他操作，请查证后再操作",对应商品在积分应用商品列表中的"删除"列标红
		7、积分应用活动列表及详情页
			1）积分应用活动列表中显示该活动的所有商品，并且共用'抵扣上限'、'金额占比'、'状态'、'起止时间'和'操作'5个字段，对应的字段值居中显示；
			2）积分活动中的商品状态发生变化，下架或者删除，列表中对应商品图片下方位置显示该商品的状态（待售和已删除）
			3）积分活动中的商品状态发生变化，下架或者删除，积分应用活动详情页中，商品列表商品状态对应发生变化，标记"待售"或"已删除"
	"""

Background:
	Given jobs登录系统

	And jobs已添加商品规格
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
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00
		}, {
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 100.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 200.00,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品3",
			"is_member_product": "on",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 100.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 100.00,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name": "商品4",
			"price": 100.00
		},{
			"name": "商品5",
			"is_member_product": "on",
			"price": 100.00
		},{
			"name": "商品6",
			"price": 100.00
		},{
			"name": "赠品6",
			"price": 10.00
		},{
			"name": "商品7",
			"is_member_product": "on",
			"price": 100.00
		},{
			"name": "赠品7",
			"price": 10.00
		},{
			"name": "商品8",
			"price": 100.00
		},{
			"name": "商品9",
			"is_member_product": "on",
			"price": 100.00
		}]
		"""

	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品4限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品4",
			"member_grade": "全部",
			"count_per_purchase": 2,
			"promotion_price": 90.00
		},{
			"name": "商品5限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品5",
			"member_grade": "全部",
			"promotion_price": 90.00,
			"limit_period": 1
			}]
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品6买二赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品6",
			"premium_products": 
			[{
				"name": "赠品6",
				"count": 1
			}],
			"count": 2,
			"is_enable_cycle_mode": true
		},{
			"name": "商品7买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品7",
			"premium_products":
			[{
				"name": "赠品7",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "单品券商品8",
			"money": 1.00,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品8"
		},{
			"name": "单品券商品9",
			"money": 10.00,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品9"
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
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2,
			"use_ceiling": -1
		}
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 1 选取普通商品，创建统一设置积分应用活动
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"is_permanant_active": false,
			"discount": 50,
			"discount_money": 50.00
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品1积分应用",
			"products":[{
				"name": "商品1",
				"price":100.00,
				"status":""
				}],
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 2 选取多规格商品，创建分级设置积分应用活动
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品2积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品2",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "普通会员",
					"discount": 100,
					"discount_money": 100.00
				},{
					"member_grade": "铜牌会员",
					"discount": 90,
					"discount_money": 90.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品2积分应用",
			"products":[{
				"name": "商品2",
				"price":"100.00 ~ 200.00",
				"status":""
				}],
			"discount": "90.0%~100.0%",
			"discount_money": "90.00~100.00",
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 3 选取有会员价的商品，创建分级设置积分应用活动（后台抵扣金额按照商品原价进行计算显示，手机端购买时按照会员价进行计算）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品3",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "普通会员",
					"discount": 100,
					"discount_money": 100.00
				},{
					"member_grade": "铜牌会员",
					"discount": 90,
					"discount_money": 90.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品3积分应用",
			"products":[{
				"name": "商品3",
				"price":100.00,
				"status":""
				}],
			"discount": "90.0%~100.0%",
			"discount_money": "90.00~100.00",
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 4 选取无会员价且已参与'限时抢购'活动的商品，创建积分应用活动（后台抵扣金额按照商品原价进行计算显示，手机端购买时显示限购价格，）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品4",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "普通会员",
					"discount": 100,
					"discount_money": 100.00
				},{
					"member_grade": "铜牌会员",
					"discount": 90,
					"discount_money": 90.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品4积分应用",
			"products":[{
				"name": "商品4",
				"price":100.00,
				"status":""
				}],
			"discount": "90.0%~100.0%",
			"discount_money": "90.00~100.00",
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 5 选取有会员价且已参与'限时抢购'活动的商品，创建积分应用活动
	#（后台抵扣金额按照商品原价进行计算显示，限时抢购优先，手机端抵扣金额按照当前页面显示的商品价格进行计算）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品5积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品5",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品5积分应用",
			"products":[{
				"name": "商品5",
				"price":100.00,
				"status":""
				}],
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 6 选取无会员价且已参与'买赠'活动的商品，创建积分应用活动（后台抵扣金额按照商品原价进行计算显示）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品6积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品6",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品6积分应用",
			"products":[{
				"name": "商品6",
				"price":100.00,
				"status":""
				}],
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 7 选取有会员价且已参与'买赠'活动的商品，创建积分应用活动 （后台抵扣金额按照商品原价进行计算显示，买赠优先，手机端抵扣金额按照当前页面显示的商品价格进行计算）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品7积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品7",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品7积分应用",
			"products":[{
				"name": "商品7",
				"price":100.00,
				"status":""
				}],
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 8 选取无会员价且已设置单品券的商品，创建积分应用活动（后台抵扣金额按照商品原价进行计算显示，手机端购买时积分和优惠券不能同时使用）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品8积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品8",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品8积分应用",
			"products":[{
				"name": "商品8",
				"price":100.00,
				"status":""
				}],
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 9 选取有会员价且已设置单品券的商品，创建积分应用活动（后台抵扣金额按照商品原价进行计算显示，手机端购买时积分抵扣按照会员价计算，但积分和优惠券不能同时使用）
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品9积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品9",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"商品9积分应用",
			"products":[{
				"name": "商品9",
				"price":100.00,
				"status":""
				}],
			"discount": "50.0%",
			"discount_money": 50.00,
			"status":"进行中"
		}]
		"""

#_补充:张三香 2016.04.27
@mall2 @promotion @promotionIntegral @integral @ztq
Scenario:10 创建多商品的积分应用活动
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品积分应用1",
			"start_date": "今天",
			"end_date": "10天后",
			"product_name": "商品1,商品2,商品3,商品4,赠品6",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 5.00
				}]
		},{
			"name": "多商品积分应用2",
			"start_date": "今天",
			"end_date": "10天后",
			"product_name": "商品5,商品6,赠品7",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "普通会员",
					"discount": 25,
					"discount_money": 2.50
				},{
					"member_grade": "铜牌会员",
					"discount": 50,
					"discount_money": 5.00
				},{
					"member_grade": "银牌会员",
					"discount": 62.5,
					"discount_money": 6.25
				},{
					"member_grade": "金牌会员",
					"discount": 100,
					"discount_money": 10.00
				}]
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name":"多商品积分应用2",
			"products":[{
					"name": "商品5",
					"price":100.00,
					"status":""
				},{
					"name": "商品6",
					"price":100.00,
					"status":""
				},{
					"name": "赠品7",
					"price":10.00,
					"status":""
				}],
			"discount":"25.0%~100.0%",
			"discount_money":"2.50~10.00",
			"status":"进行中"
		},{
			"name":"多商品积分应用1",
			"products":[{
					"name": "商品1",
					"price":100.00,
					"status":""
				},{
					"name": "商品2",
					"price":"100.00 ~ 200.00",
					"status":""
				},{
					"name": "商品3",
					"price":100.00,
					"status":""
				},{
					"name": "商品4",
					"price":100.00,
					"status":""
				},{
					"name": "赠品6",
					"price":10.00,
					"status":""
				}],
			"discount": "50.0%",
			"discount_money": 5.00,
			"status":"进行中"
		}]
		"""

@mall2 @promotion @promotionIntegral @integral @ztq
Scenario:11 创建多商品积分应用活动-多个商品中保存时有不符合条件的商品，给出错误提示
	Given jobs登录系统
	#下架商品
	When jobs'下架'商品'商品1'
	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品积分应用1",
			"start_date": "今天",
			"end_date": "10天后",
			"product_name": "商品1,商品2,商品3",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 5,
					"discount_money": 5.00
				}]
		}]
		"""
	Then jobs获得积分应用活动创建失败提示'部分商品已发生其他操作，请查证后再操作'
	#删除商品
	When jobs'上架'商品'商品1'
	When jobs'删除'商品'商品2'
	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品积分应用1",
			"start_date": "今天",
			"end_date": "10天后",
			"product_name": "商品1,商品2,商品3",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 5,
					"discount_money": 5.00
				}]
		}]
		"""
	Then jobs获得积分应用活动创建失败提示'部分商品已发生其他操作，请查证后再操作'

	#添加积分应用的商品参与了其他与优惠券互斥的活动（团购活动和积分应用）
	When jobs添加微信证书
	When jobs新建团购活动
		"""
		[{
			"group_name":"团购活动1",
			"start_date":"今天",
			"end_date":"明天",
			"product_name":"商品1",
			"group_dict":{
				"0":{
					"group_type":"5",
					"group_days":"1",
					"group_price":45.00},
				"1":{
						"group_type":"10",
						"group_days":"2",
						"group_price":30.00
				}},
			"ship_date":"10",
			"product_counts":"200",
			"material_image":"1.jpg",
			"share_description":"团购分享描述"
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品积分应用1",
			"start_date": "今天",
			"end_date": "10天后",
			"product_name": "商品1,商品2,商品3",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 5,
					"discount_money": 5.00
				}]
		}]
		"""
	Then jobs获得积分应用活动创建失败提示'部分商品已发生其他操作，请查证后再操作'

	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品积分应用0",
			"start_date": "今天",
			"end_date": "10天后",
			"product_name": "商品1",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 50,
					"discount_money": 50.00
				}]
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品积分应用1",
			"start_date": "今天",
			"end_date": "10天后",
			"product_name": "商品1,商品2,商品3",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "全部",
					"discount": 5,
					"discount_money": 5.00
				}]
		}]
		"""
	Then jobs获得积分应用活动创建失败提示'部分商品已发生其他操作，请查证后再操作'





