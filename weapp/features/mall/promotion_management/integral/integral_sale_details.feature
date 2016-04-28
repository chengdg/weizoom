#_author_:张三香 2016.04.27

Feature:查看积分应用活动详情
	"""
		积分应用活动详情页显示信息:
			1、商品详情：
				商品信息：显示商品名称和商品图片，商品下架或删除后，在对应商品图片下方显示'待售'或'已删除'
				商品价格（元）：显示商品的价格，均保留两位小数（100.00或5.10或25.25）
				总销量：显示商品的销量（和在售商品列表中的销量一致）
			2、促销规则：
				活动名称：显示活动名称
				促销广告：显示促销广告
				活动时间：'永久有效'或'xxxx-xx-xx xx:xx:00至xxxx-xx-xx xx:xx:00'
				金额占比：
					如果是统一设置，则显示格式为'全部会员：最高可抵扣40.0%'
					若是分级设置，则显示格式如下：
						'普通会员：最高可抵扣40.0%'
						'铜牌会员: 最高可抵扣55.25%'
				抵扣金额：
					统一设置，显示格式为'抵扣金额：10.00'
					分级设置，显示格式为'抵扣金额：10.00~50.25'
				永久：是/否
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
						"price": 110.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 210.00,
						"stock_typee": "无限"
					}
				}
			}
		},{
			"name": "商品3",
			"price": 300.00,
			"is_member_product": "on"
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
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""
@mall3 @promotion @promotionIntegral @integral @ztq
Scenario:1 积分应用活动（单商品、统一设置）详情
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "单商品积分应用",
			"promotion_title":"促销标题1",
			"start_date": "2016-04-10",
			"end_date": "2016-04-15",
			"status":"已结束",
			"product_name": "商品1",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.00
			}]
		}]
		"""
	Then jobs获取积分应用活动'单商品积分应用'详情
		"""
		{
			"name": "单商品积分应用",
			"promotion_title":"促销标题1",
			"activity_time":"2016-04-10 00:00:00至2016-04-15 00:00:00",
			"products":[{
				"name": "商品1",
				"price":100.00,
				"sales":0
				}],
			"is_permanant_active": false,
			"discount_info": [{
				"member_grade": "全部会员",
				"discount": "50.0%"
			}],
			"discount_money": 50.00
		}
		"""

@promotion @promotionIntegral @integral @ztqb
Scenario:2 积分应用活动（多商品、分级设置）详情
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		[{
			"name": "多商品积分应用",
			"promotion_title":"促销标题1",
			"status":"进行中",
			"product_name": "商品1,商品2,商品3",
			"is_permanant_active": true,
			"rules": [{
				"member_grade": "普通会员",
				"discount": 50,
				"discount_money": 50.00
			},{
				"member_grade": "铜牌会员",
				"discount": 60,
				"discount_money": 60.00
			},{
				"member_grade": "银牌会员",
				"discount": 80,
				"discount_money": 80.00
			}]
		}]
		"""
	#详情页，多规格商品的价格显示的是最小值，不显示区间
	Then jobs获取积分应用活动'多商品积分应用'详情
		"""
		{
			"name": "多商品积分应用",
			"promotion_title":"促销标题1",
			"activity_time":"永久有效",
			"products":[{
					"name": "商品1",
					"price":100.00,
					"sales":0
				},{
					"name": "商品2",
					"price":110.00,
					"sales":0
				},{
					"name": "商品3",
					"price":300.00,
					"sales":0
				}],
			"is_permanant_active": true,
			"discount_info": [{
				"member_grade": "普通会员",
				"discount":"50.0%"
			},{
				"member_grade": "铜牌会员",
				"discount":"60.0%"
			},{
				"member_grade": "银牌会员",
				"discount":"80.0%"
			}],
			"discount_money": "50.00 ~ 80.00"
		}
		"""
	#下架或删除活动中的商品后，积分应用活动详情页显示对应商品的状态（待售或已删除）
	When jobs'下架'商品'商品1'
	When jobs'删除'商品'商品2'
	Then jobs获取积分应用活动'多商品积分应用'详情
		"""
		{
			"name": "多商品积分应用",
			"promotion_title":"促销标题1",
			"activity_time":"永久有效",
			"products":[{
					"name": "商品1",
					"price":100.00,
					"sales":0,
					"status": "待售"
				},{
					"name": "商品2",
					"price":110.00,
					"sales":0,
					"status": "已删除"
				},{
					"name": "商品3",
					"price":300.00,
					"sales":0
				}],
			"is_permanant_active": true,
			"discount_info": [{
				"member_grade": "普通会员",
				"discount":"50.0%"
			},{
				"member_grade": "铜牌会员",
				"discount":"60.0%"
			},{
				"member_grade": "银牌会员",
				"discount":"80.0%"
			}],
			"discount_money": "50.00 ~ 80.00"
		}
		"""
	#商品下架后再上架，积分应用活动详情页商品状态不再显示'待售'
	When jobs'上架'商品'商品1'
	Then jobs获取积分应用活动'多商品积分应用'详情
		"""
		{
			"name": "多商品积分应用",
			"promotion_title":"促销标题1",
			"activity_time":"永久有效",
			"products":[{
					"name": "商品1",
					"price":100.00,
					"sales":0
				},{
					"name": "商品2",
					"price":110.00,
					"sales":0,
					"status": "已删除"
				},{
					"name": "商品3",
					"price":300.00,
					"sales":0
				}],
			"is_permanant_active": true,
			"discount_info": [{
				"member_grade": "普通会员",
				"discount":"50.0%"
			},{
				"member_grade": "铜牌会员",
				"discount":"60.0%"
			},{
				"member_grade": "银牌会员",
				"discount":"80.0%"
			}],
			"discount_money": "50.00 ~ 80.00"
		}
		"""