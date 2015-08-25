
#_author:张三香

Feature:购买单个买赠商品，同时使用单品积分抵扣

	#说明：
		#针对线上"bug4259"补充feature
		#bug4259-（功能问题）【手机端】商品在同时参加买赠和积分应用活动，购买时，点击使用积分，小计显示NAN乱码
		#手机端购买参与买赠同时参与积分应用的商品时，从商品详情页点击【立即购买】,进入待编辑订单页
			#待编辑订单页,可以看到"共计x件商品，小计xx"的信息提示;
			#待编辑订单页,当使用积分抵扣时，"共计x件商品，小计xx"信息提示中的小计会重新计算;

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00
		},{
			"name": "赠品",
			"price": 10.00
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
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
	Given bill关注jobs的公众号

@promotion @promotionPremium @promotionIntegral @online_bug
Scenario: 购买单个买赠商品，同时使用单品积分抵扣
		待编辑订单页面'小计'信息的校验
	Given jobs登录系统
	When jobs创建买赠活动
		"""
		[{
			"name": "商品1买一赠二",
			"start_date": "今天",
			"end_date": "1天后", 
			"product_name": "商品1",
			"premium_products": [{
				"name": "赠品",
				"count": 2,
				"gifts_from":"单位1"
			}],
			"count": 1,
			"member_grade":"全部",
			"is_enable_cycle_mode": true
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "商品1",
			"is_permanant_active": false,
			"rules": {
				"member_grade": "全部",
				"discount": 50,
				"discount_money": 50.0
			}
		}]
		"""

	When bill访问jobs的webapp
	When bill获得jobs的500会员积分
	Then bill在jobs的webapp中拥有500会员积分
	When bill浏览jobs的webapp的'商品1'商品页
	Then webapp页面标题为'商品1'
	And bill获得webapp商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"promotion": {
					"type": "premium_sale",
					"msg":"赠品 x 2 单位1 "
				},{
					"type": "integral_sale",
					"msg":"最多可使用100积分,抵扣50.00元"
				}
		}]
		"""
	When bill进行"立即购买"操作
	Then bill获得待编辑订单
		"""
			[{
				"final_price": 100.0,
				"product_price": 100.0,
				"postage": 0.00,
				"products": [{
					"name": "商品1",
					"count": 1,
					"price": 100.00
				},{
					"name": "赠品",
					"count": 2,
					"promotion": {
						"type": "premium_sale:premium_product"
					}
				}],
				"reminder":{
					"msg":"您有500积分,可使用100积分抵扣50.00元",
					"is_active":true
				},
				"subtotal": {
						"count": 3,
						"money": 100.0
				}
			}]
		"""
	When bill使用'积分抵扣'
	Then bill获得待编辑订单 
		"""
			[{
				"final_price": 50.0,
				"product_price": 100.0,
				"postage": 0.00,
				"integral_money":50.00,
				"products": [{
					"name": "商品1",
					"count": 1,
					"price": 100.00
				},{
					"name": "赠品",
					"count": 2,
					"promotion": {
						"type": "premium_sale:premium_product"
					}
				}],
				"reminder":{
					"msg":"您已使用100积分抵扣50.00元",
					"is_active":false
					},
				"subtotal": {
						"count": 3,
						"money": 50.0
				}
			}]
		"""