# __author__ : "冯雪静"
@func:webapp.modules.mall.order_management_shihuazhiye
Feature:世华智业订单管理

	用户在购买课程支付完成后订单状态自动变为已完成

Background:
	Given jobs登录系统添加课程
		"""
		[{
			"name":"课程1",
			"price":100.00

		}]
		"""
	And bill关注jobs的公共号
	And tom关注jobs的公共号


@mall.order_management_shihuazhiye @ignore
Scenario:bill通过webapp购买用'课程1'
	1.用微信支付
	
	When bill通过webapp购买'课程1'
		"""
		{
			"name":"课程1",
			"price":100.00,
			"number_people":10,
			"registration":[{
				"name":"刘德华",
				"position":"技术主管",
				"corporation":"世华智业集团",
				"phone":"18513853280",
				"referrer":"朱丽倩",
				"district":"北京"
			}],
			"total_price":1000.00,
			"is_commit": "是",
			"is_pay":"是"

		}
		"""
	Then bill在webapp个人中心查看
		"""
		{
			"pay_status":"已完成",
			"payment":"微信支付",
			"registration_number":"20141028999999999",
			"registration_time":"2014年10月28日 13:30",
			"registration":[{
				"刘德华",
				"18513853280",
				"世华智业集团",
				"技术主管",
				"district":"北京"
			}],
			"course_details":[{
				"name":"课程1",
				"price":100.00,
				"number_people":10
			}]

		}
		"""
	Then jobs查看bill的订单
		"""
		{
			"registration_number":"20141028999999999",
			"registration_time":"2014年10月28日 13:30",
			"apply_status":"已完成",
			"total_price":1000.00,
			"number_people":10,
			"payment":"微信支付",
			"student":"刘德华",
			"position":"技术主管",
			"phone":"18513853280",
			"district":"北京",
			"course_details":[{
				"name":"课程1",
				"price":100.00,
				"number_people":10
			}]
		}
		"""


@mall.order_management_shihuazhiye @ignore
Scenario:tom通过webapp购买用'课程1'
	1.用积分支付
	
	When tom通过webapp购买'课程1'
		"""
		{
			"name":"课程1",
			"price":100.00,
			"number_people":20,
			"registration":[{
				"name":"李小龙",
				"position":"总经理",
				"corporation":"世华智业集团",
				"phone":"13012345678",
				"referrer":"张三丰",
				"district":"上海"
			}],
			"total_price":2000.00,
			"is_commit": "是",
			"is_pay":"是"

		}
		"""
	Then tom在webapp个人中心查看
		"""
		{
			"pay_status":"已完成",
			"payment":"积分支付",
			"registration_number":"20141029000000001",
			"registration_time":"2014年10月29日 13:30",
			"registration":[{
				"李小龙",
				"13012345678",
				"世华智业集团",
				"总经理",
				"district":"上海"
			}],
			"course_details":[{
				"name":"课程1",
				"price":100.00,
				"number_people":20
			}]

		}
		"""
	Then jobs查看tom的订单
		"""
		{
			"registration_number":"20141029000000001",
			"registration_time":"2014年10月29日 13:30",
			"apply_status":"已完成",
			"total_price":2000.00,
			"number_people":20,
			"payment":"积分支付",
			"student":"李小龙",
			"position":"总经理",
			"phone":"13012345678",
			"district":"上海",
			"course_details":[{
				"name":"课程1",
				"price":100.00,
				"number_people":20
			}]
		}
		"""
