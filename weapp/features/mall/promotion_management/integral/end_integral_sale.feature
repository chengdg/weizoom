#_author_：张三香
#editor:雪静 2015.10.15

Feature:结束积分应用活动
	Jobs能结束状态为'未开始'和'进行中'的积分应用活动

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"shelve_type": "上架"
		}, {
			"name": "商品2",
			"price": 100.00,
			"shelve_type": "上架"
		}, {
			"name": "商品3",
			"price": 100.00,
			"shelve_type": "上架"
		}, {
			"name": "商品4",
			"price": 100.00,
			"shelve_type": "上架"
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "明天",
			"end_date": "3天后",
			"status":"未开始",
			"product_name": "商品4",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"status":"进行中",
			"product_name": "商品3",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}, {
			"name": "商品2积分应用",
			"status":"进行中",
			"product_name": "商品2",
			"is_permanant_active": true,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}, {
			"name": "商品1积分应用",
			"start_date": "2015-07-11",
			"end_date": "2015-08-10",
			"status":"已结束",
			"product_name": "商品1",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}]
		"""

@mall2 @promotionIntegral @integral
Scenario: 1 结束状态为'未开始'的积分应用活动
	Given jobs登录系统
	When jobs"结束"促销活动"商品4积分应用"
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "商品1积分应用",
			"status":"已结束"
		}, {
			"name": "商品2积分应用",
			"status":"进行中",
			"is_permanant_active": true
		}, {
			"name": "商品3积分应用",
			"status":"进行中"
		}, {
			"name": "商品4积分应用",
			"status":"已结束"
		}]
		"""

@mall2 @promotionIntegral @integral
Scenario: 2 结束状态为'进行中'，非永久有效的积分应用活动
	Given jobs登录系统
	When jobs"结束"促销活动"商品3积分应用"
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "2015-07-11",
			"end_date": "2015-08-10",
			"status":"已结束"
		}, {
			"name": "商品2积分应用",
			"status":"进行中",
			"is_permanant_active": true
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"status":"已结束"
		}, {
			"name": "商品4积分应用",
			"start_date": "明天",
			"end_date": "3天后",
			"status":"未开始"
		}]
		"""

@mall2 @promotionIntegral @integral
Scenario: 3 结束状态为'进行中'，且为永久有效的积分应用活动
	Given jobs登录系统
	When jobs"结束"促销活动"商品2积分应用"
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "2015-07-11",
			"end_date": "2015-08-10",
			"status":"已结束"
		}, {
			"name": "商品2积分应用",
			"status":"已结束",
			"is_permanant_active": true
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"status":"进行中"
		}, {
			"name": "商品4积分应用",
			"start_date": "明天",
			"end_date": "3天后",
			"status":"未开始"
		}]
		"""

@mall2 @promotionIntegral @integral
Scenario: 4 批量结束积分应用活动（不包含已结束状态）
	Given jobs登录系统
	When jobs批量'结束'促销活动
		"""
		[{
			"name": "商品4积分应用"
		}, {
			"name": "商品3积分应用"
		}, {
			"name": "商品2积分应用"
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "商品1积分应用",
			"status":"已结束"
		}, {
			"name": "商品2积分应用",
			"status":"已结束",
			"is_permanant_active": true
		}, {
			"name": "商品3积分应用",
			"status":"已结束"
		}, {
			"name": "商品4积分应用",
			"status":"已结束"
		}]
		"""

@mall2 @promotionIntegral @integral
Scenario: 5 商品下架导致积分应用活动结束
	Given jobs登录系统
	When jobs批量下架商品
		"""
		["商品3", "商品4"]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "商品2",
			"price": 100.00
		}, {
			"name": "商品1",
			"price": 100.00
		}]
		"""
	And jobs获取积分应用活动列表
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "2015-07-11",
			"end_date": "2015-08-10",
			"status":"已结束",
			"product_name": "商品1"
		}, {
			"name": "商品2积分应用",
			"status":"进行中",
			"product_name": "商品2",
			"is_permanant_active": true
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"status":"已结束",
			"product_name": "商品3"
		}, {
			"name": "商品4积分应用",
			"start_date": "明天",
			"end_date": "3天后",
			"status":"已结束",
			"product_name": "商品4"
		}]
		"""