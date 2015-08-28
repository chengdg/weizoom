#_author_:张三香

Feature:促销管理-新建活动页面的商品查询

	#说明：
		#a.查询条件：【商品名称】和【商品编码】；【查询】和【重置】按钮
		#b.点击【查询】按钮，出现'已上架商品'弹窗：
			#弹窗数据列表字段：【商品条码】、【商品名称】、【商品价格（元）】、【商品库存】、【已参与促销】、【操作】
			#按钮：【选取】-操作列中显示  【完成选择】-列表最下方显示；
			#商品起购数量大于1的商品不显示在限时抢购活动对应的商品弹窗列表中；
			#同一商品只能参与一个促销活动（限时抢购、买赠、单品券）
			#使失效的单品券，只有过期后才能创建其他促销活动
			#积分应用活动与其他活动不互斥

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name":"商品0",
			"price":100.00,
			"stock_type": "无限",
			"min_limit": 7,  #起购数量
			"status":"上架"
		},{
			"name":"限时抢购",
			"price":100.00,
			"stock_type": "无限",
			"status":"上架"
		},{
			"name":"买赠",
			"price":100.00,
			"stock_type": "有限",
			"stocks": 20,
			"status":"上架"
		},{
			"name":"单品券",
			"price":100.00,
			"stock_type": "无限",
			"status":"上架"
		},{
			"name":"赠品",
			"price":100.00,
			"stock_type": "无限",
			"status":"上架"
		},{
			"name":"积分应用",
			"price":100.00,
			"stock_type": "无限",
			"status":"上架"
		},{
			"name":"单品失效",
			"price":100.00,
			"stock_type": "无限",
			"status":"上架"
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
			"name": "单品券活动",
			"money": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "单品券"
		},{
			"name": "单品失效活动",
			"money": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "单品失效"
		}]
		"""
	When jobs失效优惠券'单品失效活动'

@promotion @promotionFlash @duhao
Scenario: 1 限时抢购-新建活动页面的商品查询
	Given jobs登录系统
	#起购数量大于1的商品不在上架列表中（不能参与限时抢购）
	When jobs新建活动时设置商品查询条件
		"""
		{
			"name":"商品0"
		}
		"""
	Then jobs新建活动时能获得已上架商品列表
		| name     | price | stocks | have_promotion | actions |

	When jobs新建活动时设置商品查询条件
		"""
		{
			"name":""
		}
		"""
	Then jobs新建活动时能获得已上架商品列表
		| name     | price | stocks | have_promotion | actions |
		| 限时抢购 |100.00 | 无限   | 限时抢购活动   |         |
		| 买赠     |100.00 | 20     | 买赠活动       |         |
		| 单品券   |100.00 | 无限   | 单品券活动     |         |
		| 赠品     |100.00 | 无限   |                | 选取    |
		| 积分应用 |100.00 | 无限   | 积分应用活动   | 选取    |
		| 单品失效 |100.00 | 无限   | 单品失效活动   |         |

@promotion @promotionPremium
Scenario: 2 买赠-新建活动页面的商品查询
	When jobs新建活动时设置商品查询条件
		"""
		{
			"name":""
		}
		"""
	Then jobs新建活动时能获得已上架商品列表
		| name     | price | stocks | have_promotion | actions |
		| 商品0    |100.00 | 无限   |                | 选取    |
		| 限时抢购 |100.00 | 无限   | 限时抢购活动   |         |
		| 买赠     |100.00 | 20     | 买赠活动       |         |
		| 单品券   |100.00 | 无限   | 单品券活动     |         |
		| 赠品     |100.00 | 无限   |                | 选取    |
		| 积分应用 |100.00 | 无限   | 积分应用活动   | 选取    |
		| 单品失效 |100.00 | 无限   | 单品失效活动   |         |

@promotion @promotionIntegral
Scenario: 3 积分应用-新建活动页面的商品查询
	When jobs新建活动时设置商品查询条件
		"""
		{
			"name":""
		}
		"""
	Then jobs新建活动时能获得已上架商品列表
		| name     | price | stocks | have_promotion | actions |
		| 商品0    |100.00 | 无限   |                | 选取    |
		| 限时抢购 |100.00 | 无限   | 限时抢购活动   | 选取    |
		| 买赠     |100.00 | 20     | 买赠活动       | 选取    |
		| 单品券   |100.00 | 无限   | 单品券活动     | 选取    |
		| 赠品     |100.00 | 无限   |                | 选取    |
		| 积分应用 |100.00 | 无限   | 积分应用活动   |         |
		| 单品失效 |100.00 | 无限   | 单品失效活动   | 选取    |

@promotion @promotionCoupon
Scenario: 4 单品券-新建活动页面的商品查询
	Given jobs登录系统
	When jobs添加部分商品
	Then jobs新建活动时能获得已上架商品列表
		| name     | price | stocks | have_promotion | actions |
		| 商品0    |100.00 | 无限   |                | 选取    |
		| 限时抢购 |100.00 | 无限   | 限时抢购活动   |         |
		| 买赠     |100.00 | 20     | 买赠活动       |         |
		| 单品券   |100.00 | 无限   | 单品券活动     |         |
		| 赠品     |100.00 | 无限   |                | 选取    |
		| 积分应用 |100.00 | 无限   | 积分应用活动   | 选取    |
		| 单品失效 |100.00 | 无限   | 单品失效活动   |         |
