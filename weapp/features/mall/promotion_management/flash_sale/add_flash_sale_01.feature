#_author_:张三香 2016.03.30

Feature:创建限时抢购活动,设置购买次数限制
	"""
		2016.03.30新增需求8619-限时抢购添加限购购买次数的限定
			1.新建限时抢购活动页面中添加字段"购买次数"
			2.默认"购买次数"不勾选;
			3.勾选"购买次数"后显示输入框且为必填项，验证为正整数
			4.如不勾选"购买次数",则限购逻辑保持原有不变
			5.若勾选"购买次数":
				未设置"限购周期",设置"购买次数"的情况下,指活动时间内，每人可购买x次
				设置"限购周期",且设置"购买次数",指限购周期内,每人可购买x次
			6.限时抢购活动详情页:
				购买次数不勾选,活动详情页则不显示该字段
				购买次数勾选,并设置为x,活动详情页则显示"购买次数:x次"
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
		},{
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model":
			{
				"models":
				{
					"M": {
						"price": 100.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 200.00,
						"stock_typee": "无限"
					}
				}
			}
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
		}]
		"""

@promotion @flash_sale
Scenario:1 创建限时抢购活动,设置购买次数限制
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品1限时抢购",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "5天后",
			"product_name":"商品1",
			"member_grade": "全部会员",
			"count_per_purchase":"",
			"promotion_price": 80.00,
			"limit_period":"",
			"count_per_period":1
		},{
			"name": "商品2限时抢购",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "5天后",
			"product_name":"商品2",
			"member_grade": "铜牌会员",
			"count_per_purchase":2,
			"promotion_price": 80.00,
			"limit_period":1,
			"count_per_period":2
		}]
		"""
	Then jobs获取限时抢购活动列表
		"""
		[{
			"name": "商品2限时抢购",
			"product_name": "商品2",
			"product_price":"100.0~200.0",
			"promotion_price": 80,
			"status":"进行中",
			"start_date": "今天",
			"end_date": "5天后",
			"actions": ["详情","结束"]
		},{
			"name": "商品1限时抢购",
			"product_name": "商品1",
			"product_price": 100,
			"promotion_price": 80,
			"status":"进行中",
			"start_date": "今天",
			"end_date": "5天后",
			"actions": ["详情","结束"]
		}]
		"""
