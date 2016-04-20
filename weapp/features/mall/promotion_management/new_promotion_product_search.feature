#_author_:张三香

Feature:促销管理-新建活动页面的商品查询

	#说明：
		#a.查询条件：【商品名称】和【商品编码】；【查询】和【重置】按钮
		#b.点击【查询】按钮，出现'已上架商品'弹窗：
			#弹窗数据列表字段：【商品条码】、【商品名称】、【商品价格（元）】、【商品库存】、【已参与促销】、【操作】
			#按钮：【选取】-操作列中显示  【完成选择】-列表最下方显示；
			#商品起购数量大于1的商品不显示在限时抢购活动对应的商品弹窗列表中；
			#同一商品只能参与一个促销活动（限时抢购、买赠、多商品券）
			#使失效的多商品券，只有过期后才能创建其他促销活动
			#积分应用活动与其他活动不互斥
		#c.补充（新增需求-4917）：
			1.单商品支持添加多个多商品优惠券
			2.商品下架、修改后对优惠券无影响，各个模块均可选择该优惠券且优惠券管理处优惠券不为失效状态，添加劵码可继续使用。
			3.禁止优惠券商品与创建多商品券无关
			4.多商品优惠券选择商品时,'已参与促销'字段显示规则：
				a.此商品参与了促销活动，那么显示促销的活动名称
				b.此商品被设置了多商品优惠券，不管设置了多少多商品优惠券，已参与促销的地方都显示'多商品券'三个字


Background:
	Given jobs登录系统
	When jobs添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name":"商品0",
			"categories": "分类1,分类2,分类3",
			"price":100.00,
			"stock_type": "无限",
			"min_limit": 2,
			"status":"在售"
		},{
			"name":"商品1",
			"categories": "分类1,分类2,分类3",
			"price":100.00,
			"stock_type": "无限",
			"min_limit": 1,
			"status":"在售"
		},{
			"name":"商品2",
			"categories": "分类1,分类2,分类3",
			"price":100.00,
			"stock_type": "无限",
			"min_limit": 1,
			"status":"在售"
		},{
			"name":"限时抢购",
			"categories": "分类1",
			"price":100.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"买赠",
			"price":100.00,
			"stock_type": "有限",
			"stocks": 20,
			"status":"在售"
		},{
			"name":"多商品券",
			"categories": "分类2",
			"price":100.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"赠品",
			"price":100.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"积分应用",
			"categories": "分类2,分类3",
			"price":100.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"多商品失效",
			"categories": "分类2,分类3",
			"price":100.00,
			"stock_type": "无限",
			"status":"在售"
		}]
		"""
	When jobs创建限时抢购活动
		"""
		[{
			"name": "限时抢购活动",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "限时抢购",
			"member_grade": "全部会员",
			"count_per_purchase": 2,
			"promotion_price": 90.00
		}]
		"""
	And jobs创建买赠活动
		"""
		[{
			"name": "买赠活动",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "买赠",
			"premium_products":
			[{
				"name": "赠品",
				"count": 1
			}],
			"count": 2,
			"is_enable_cycle_mode": true
		}]
		"""
	And jobs创建积分应用活动
		"""
		[{
			"name": "积分应用活动",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "积分应用",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}]
		"""
	And jobs添加优惠券规则
		"""
		[{
			"name": "多商品券01",
			"money": 1,
			"start_date": "2天前",
			"end_date": "1天前",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "多商品券,商品2"
		},{
			"name": "多商品券02",
			"money": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "多商品券"
		},{
			"name": "多商品券03",
			"money": 10,
			"start_date": "今天",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon3_id_",
			"coupon_product": "多商品券"
		},{
			"name": "多商品失效活动",
			"money": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon4_id_",
			"coupon_product": "多商品失效,商品1"
		}]
		"""
	When jobs失效优惠券'多商品失效活动'

@mall2 @promotion @promotionFlash
Scenario: 1 限时抢购-新建活动页面的商品查询
	Given jobs登录系统
	#起购数量大于1的商品不在在售列表中（不能参与限时抢购）
	When jobs新建活动时设置参与活动的商品查询条件
		"""
		{
			"name":"商品0"
		}
		"""
	Then jobs新建限时抢购活动时能获得已上架商品列表
		| name     | price | stocks | have_promotion | actions |

	When jobs新建活动时设置参与活动的商品查询条件
		"""
		{
			"name":""
		}
		"""
	Then jobs新建限时抢购活动时能获得已上架商品列表
		| name       | price | stocks | have_promotion | actions |
		| 商品1      |100.00 | 无限   | 多商品券       |         |
		| 商品2      |100.00 | 无限   |                | 选取    |
		| 限时抢购   |100.00 | 无限   | 限时抢购活动   |         |
		| 买赠       |100.00 | 20     | 买赠活动       |         |
		| 多商品券   |100.00 | 无限   | 多商品券       |         |
		| 赠品       |100.00 | 无限   |                | 选取    |
		| 积分应用   |100.00 | 无限   |                | 选取    |
		| 多商品失效 |100.00 | 无限   | 多商品券       |         |

@mall2 @promotion @promotionPremium
Scenario: 2 买赠-新建活动页面的商品查询
	When jobs新建活动时设置参与活动的商品查询条件
		"""
		{
			"name":""
		}
		"""
	Then jobs新建买赠活动时能获得已上架商品列表
		| name       | price | stocks | have_promotion | actions |
		| 商品0      |100.00 | 无限   |                | 选取    |
		| 商品1      |100.00 | 无限   | 多商品券       |         |
		| 商品2      |100.00 | 无限   |                | 选取    |
		| 限时抢购   |100.00 | 无限   | 限时抢购活动   |         |
		| 买赠       |100.00 | 20     | 买赠活动       |         |
		| 多商品券   |100.00 | 无限   | 多商品券       |         |
		| 赠品       |100.00 | 无限   |                | 选取    |
		| 积分应用   |100.00 | 无限   |                | 选取    |
		| 多商品失效 |100.00 | 无限   | 多商品券       |         |

@mall2 @promotion @promotionIntegral
Scenario: 3 积分应用-新建活动页面的商品查询
	When jobs新建活动时设置参与活动的商品查询条件
		"""
		{
			"name":""
		}
		"""
	Then jobs新建积分应用活动时能获得已上架商品列表
		| name       | price | stocks | have_promotion | actions |
		| 商品0      |100.00 | 无限   |                | 选取    |
		| 商品1      |100.00 | 无限   |                | 选取    |
		| 商品2      |100.00 | 无限   |                | 选取    |
		| 限时抢购   |100.00 | 无限   |                | 选取    |
		| 买赠       |100.00 | 20     |                | 选取    |
		| 多商品券   |100.00 | 无限   |                | 选取    |
		| 赠品       |100.00 | 无限   |                | 选取    |
		| 积分应用   |100.00 | 无限   | 积分应用活动   |         |
		| 多商品失效 |100.00 | 无限   |                | 选取    |

@mall2 @promotion @promotionCoupon
Scenario: 4 多商品券-新建活动页面的商品查询
	Given jobs登录系统
	Then jobs新建多商品券活动时能获得已上架商品列表
		| name       | price | stocks | have_promotion | actions |
		| 商品0      |100.00 | 无限   |                | 选取    |
		| 商品1      |100.00 | 无限   | 多商品券       | 选取    |
		| 商品2      |100.00 | 无限   |                | 选取    |
		| 限时抢购   |100.00 | 无限   | 限时抢购活动   |         |
		| 买赠       |100.00 | 20     | 买赠活动       |         |
		| 多商品券   |100.00 | 无限   | 多商品券       | 选取    |
		| 赠品       |100.00 | 无限   |                | 选取    |
		| 积分应用   |100.00 | 无限   |                | 选取    |
		| 多商品失效 |100.00 | 无限   | 多商品券       | 选取    |

	Then jobs新建多商品券活动时能获得商品分组列表
		| name     | created_at | actions |
		| 分类3    |    今天    |   选取  |
		| 分类2    |    今天    |   选取  |
		| 分类1    |    今天    |   选取  |

	When jobs新建多商品券设置商品查询条件
		"""
		{
			"name":"商品"
		}
		"""
	Then jobs新建多商品券活动时能获得已上架商品列表
		| name       | price | stocks | have_promotion | actions |
		| 商品0      |100.00 | 无限   |                | 选取    |
		| 商品1      |100.00 | 无限   | 多商品券       | 选取    |
		| 商品2      |100.00 | 无限   |                | 选取    |
		| 多商品券   |100.00 | 无限   | 多商品券       | 选取    |
		| 多商品失效 |100.00 | 无限   | 多商品券       | 选取    |

	When jobs新建多商品券设置商品分组查询条件
		"""
		{
			"name":"分类2"
		}
		"""
	Then jobs新建多商品券活动时能获得商品分组列表
		| name     | created_at | actions |
		| 分类2    |    今天    |   选取  |
