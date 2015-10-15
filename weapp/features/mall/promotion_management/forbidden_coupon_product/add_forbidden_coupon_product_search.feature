#_author_:张三香
#editor:雪静 2015.10.15
Feature:添加禁用优惠券商品时商品查询弹窗信息校验
	"""
		1、商品查询弹窗中字段包括：商品条码、商品名称、商品价格（元）、商品库存、禁用状态和操作
		2、已添加禁用优惠券的商品，弹窗中"禁用状态"列显示'已禁用',"操作"列为空
		3、参与其他促销活动（限时抢购、买赠、积分应用和单品券）的商品,弹窗中"禁用状态"列显示空,"操作"列显示"选取"按钮
	"""
Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"price":10.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"禁用优惠券",
			"price":10.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"限时抢购",
			"price":10.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"买赠",
			"price":10.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"积分应用",
			"price":10.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"单品券",
			"price":10.00,
			"stock_type": "有限",
			"stocks": "10",
			"status":"在售"
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"discount": "8"
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2,
			"use_ceiling": -1
		}
		"""

@mall2 @promotion @promotionForbiddenCoupon
Scenario: 1 添加禁用商品时商品查询弹框信息校验
	Given jobs登录系统
	When jobs添加禁用优惠券商品
		"""
		[{
			"products":[{
				"name":"禁用优惠券"
			}],
			"start_date": "今天",
			"end_date": "1天后",
			"is_permanant_active": 0
		}]
		"""
	When jobs创建限时抢购活动
		"""
		[{
			"name": "限时抢购活动",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name":"限时抢购",
			"member_grade": "全部会员",
			"count_per_purchase": 2,
			"promotion_price": 99.00
		}]
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "买赠活动",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "1天后",
			"member_grade": "全部会员",
			"product_name": "买赠",
			"premium_products": 
			[{
				"name": "买赠",
				"count": 1
			}],
			"count": 2,
			"is_enable_cycle_mode": true
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "积分应用活动",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "积分应用",
			"is_permanant_active": false,
			"rules": 
				[{
					"member_grade": "普通会员",
					"discount": 100,
					"discount_money": 100.0
				},{
					"member_grade": "铜牌会员",
					"discount": 90,
					"discount_money": 90.0
				},{
					"member_grade": "银牌会员",
					"discount": 80,
					"discount_money": 80.0
				}]
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "单品券1",
			"money": 1.00,
			"count": 5,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "单品券"
		}]
		"""
	When jobs新建活动时设置参与活动的商品查询条件
		"""
		{}
		"""
	Then jobs新建禁用优惠券商品活动时能获得已上架商品列表
		| name       | price | stocks | status | actions |
		| 商品1      |10.00  | 无限   |        | 选取    |
		| 禁用优惠券 |10.00  | 无限   | 已禁用 |         |
		| 限时抢购   |10.00  | 无限   |        | 选取    |
		| 买赠       |10.00  | 无限   |        | 选取    |
		| 积分应用   |10.00  | 无限   |        | 选取    |
		| 单品券     |10.00  | 10     |        | 选取    |