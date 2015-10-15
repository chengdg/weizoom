#_author_:张三香

Feature:添加禁用优惠券商品

	"""
	说明：
		1、促销管理模块添加'禁用优惠券商品'功能
		2、禁用优惠券商品功能只针对全店通用券，不限制单品券
		3、不管被限制的商品参与任何活动（限时抢购、买赠、积分应用），都可以被限制使用全店通用券
		4、当商品在被限制使用通用券时，也可以为该商品创建单品券
	"""
Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
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
Scenario: 1 选取普通无规格商品,起止时间非永久有效,添加禁用优惠券
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name":"无规格",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 10.0,
						"weight": 10.0,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			},
			"status":"在售"
		}]
		"""
	When jobs添加禁用优惠券商品
		"""
		[{
			"products":[{
				"name":"无规格"
			}],
			"start_date": "今天",
			"end_date": "1天后",
			"is_permanant_active": 0
		}]
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "无规格",
			"product_price": 10.0,
			"status": "进行中",
			"start_date": "今天",
			"end_date": "1天后"
		}]
		"""

@mall2 @promotion @promotionForbiddenCoupon
Scenario: 2 选取多规格商品,起止时间为永久有效,添加禁用优惠券
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "多规格",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"白色 S": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"黑色 M": {
						"price": 13.0,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"白色 M":{
						"price": 13.0,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			},
			"status":"在售"
		}]
		"""
	When jobs添加禁用优惠券商品
		"""
		[{
			"products":[{
				"name":"多规格"
			}],
			"start_date": "",
			"end_date": "",
			"is_permanant_active": 1
		}]
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "多规格",
			"product_price":"10.0 ~ 13.0",
			"status": "进行中",
			"is_permanant_active": 1
		}]
		"""

@mall2 @promotion @promotionForbiddenCoupon
Scenario: 3 选取多个参与促销活动的商品,添加禁用优惠券
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name":"限时抢购",
			"price":100.0,
			"status":"在售"
		},{
			"name":"买赠",
			"price":100.0,
			"status":"在售"
		},{
			"name":"积分应用",
			"price":100.0,
			"status":"在售"
		},{
			"name":"单品券",
			"price":100.0,
			"status":"在售"
		},{
			"name":"赠品",
			"price":10.0,
			"status":"在售"
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
			"member_grade": "铜牌会员",
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
				"name": "赠品",
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
			"is_permanant_active": 0,
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
	When jobs添加禁用优惠券商品
		"""
		[{
			"products":[{
				"name":"限时抢购"
			},{
				"name":"买赠"
			}],
			"start_date": "明天",
			"end_date": "2天后",
			"is_permanant_active": 0
		}, {
			"products":[{
				"name":"积分应用"
			},{
				"name":"单品券"
			}],
			"start_date": "今天",
			"end_date": "2天后",
			"is_permanant_active": 0
		}]
		"""
	Then jobs能获取禁用优惠券商品列表
		"""
		[{
			"product_name": "单品券",
			"product_price": 100.0,
			"status": "进行中",
			"start_date": "今天",
			"end_date": "2天后"
		},{
			"product_name": "积分应用",
			"product_price": 100.0,
			"status": "进行中",
			"start_date": "今天",
			"end_date": "2天后"
		},{
			"product_name": "买赠",
			"product_price": 100.0,
			"status": "未开始",
			"start_date": "明天",
			"end_date": "2天后"
		},{
			"product_name": "限时抢购",
			"product_price": 100.0,
			"status": "未开始",
			"start_date": "明天",
			"end_date": "2天后"
		}]
		"""