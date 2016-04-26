#_author_:宋温馨

Feature:促销管理-新建积分活动页面的商品查询

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
			"name":"多商品失效",
			"categories": "分类2,分类3",
			"price":100.00,
			"stock_type": "无限",
			"status":"在售"
		},{
			"name":"团购商品",
			"categories": "分类1,分类2,分类3",
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
	
	And jobs创建团购活动
		"""
		[{
			"group_name":"团购活动",
			"start_date":"今天",
			"end_date":"2天后",
			"product_name":"团购商品",
			"group_dict":
				[{
					"group_type":5,
					"group_days":1,
					"group_price":90.00
				}],
				"ship_date":20,
				"product_counts":100,
				"material_image":"1.jpg",
				"share_description":"团购活动1分享描述"
		}]
		"""

@mall2 @promotion @promotionIntegral @ztq
Scenario: 1 积分应用-新建活动页面的商品查询
	Given jobs登录系统
	When jobs新建活动时设置参与活动的商品查询条件4
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
		| 多商品失效 |100.00 | 无限   |                | 选取    |
		| 团购商品   |100.00 | 无限   | 团购活动       |         |

	Then jobs新建多商品券活动时能获得商品分组列表
		| name     | created_at | actions |
		| 分类1    |    今天    |   选取  |
		| 分类2    |    今天    |   选取  |
		| 分类3    |    今天    |   选取  |
