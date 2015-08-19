#_author_：张三香

Feature:结束积分应用活动
	Jobs能结束状态为'未开始'和'进行中'的积分应用活动

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
		}, {
			"name": "商品2",
			"price": 100.00
		}, {
			"name": "商品3",
			"price": 100.00
		}, {
			"name": "商品4",
			"price": 100.00
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
	When jobs已创建积分应用活动
		"""
		[{
			"name": "商品4积分应用",
			"start_date": "明天",
			"end_date": "3天后",
			"status":"未开始",
			"products": ["商品4"],
			"is_permanant_active": false,
			"rules": [{
				"member_grade_name": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"status":"进行中",
			"products": ["商品3"],
			"is_permanant_active": false,
			"rules": [{
				"member_grade_name": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}, {
			"name": "商品2积分应用",
			"start_date": "",
			"end_date": "",
			"status":"已结束",
			"products": ["商品2"],
			"is_permanant_active": true,
			"rules": [{
				"member_grade_name": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}, {
			"name": "商品1积分应用",
			"start_date": "2015-07-11",
			"end_date": "2015-08-10",
			"status":"已结束",
			"products": ["商品1"],
			"is_permanant_active": false,
			"rules": [{
				"member_grade_name": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}]
		"""

@promotionIntegral @integral
Scenario: 1 结束状态为'未开始'的积分应用活动

@promotionIntegral @integral
Scenario: 2 结束状态为'进行中'，非永久有效的积分应用活动

@promotionIntegral @integral
Scenario: 3 结束状态为'进行中'，且为永久有效的积分应用活动