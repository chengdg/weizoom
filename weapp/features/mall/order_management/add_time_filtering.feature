# __author__ : "冯雪静"

Feature:订单筛选添加时间段筛选
	jobs可以对订单进行"时间段筛选"

Background:
	Given job已有订单
		"""
		[{
			"order_no":"0000008",
			"order_time":"2014-10-08 12:00"
		},{
			"order_no":"0000007",
			"order_time":"2014-10-07 12:00"
		},{
			"order_no":"0000006",
			"order_time":"2014-10-06 12:00"
		},{
			"order_no":"0000005",
			"order_time":"2014-10-05 12:00"
		},{
			"order_no":"0000004",
			"order_time":"2014-10-04 12:00"
		},{
			"order_no":"0000003",
			"order_time":"2014-10-03 12:00"
		},{
			"order_no":"0000002",
			"order_time":"2014-10-02 12:00"
		},{
			"order_no":"0000001",
			"order_time":"2014-10-01 12:00"
		}]
		"""

@ignore 
Scenario:选择时间段
	jobs选择时间段确认后
	1.jobs选择时间段时,获取对应的订单列表

	Given jobs登录系统
	When jobs选择时间段
		"""
		{
			"time_quantum":"2014-10-01~2014-10-03",
			"submit":"点击"
		}
		"""
	Then jobs获取对应的订单
		"""
		[{
			"order_no":"0000003",
			"order_time":"2014-10-03 12:00"
		},{
			"order_no":"0000002",
			"order_time":"2014-10-02 12:00"
		},{
			"order_no":"0000001",
			"order_time":"2014-10-01 12:00"
		}]
		"""

	When jobs选择时间段
		"""
		{
			"time_quantum":"2014-10-01~2014-10-31",
			"submit":"点击"
		}
		"""
	Then jobs获取对应的订单
		"""
		[{
			"order_no":"0000008",
			"order_time":"2014-10-08 12:00"
		},{
			"order_no":"0000007",
			"order_time":"2014-10-07 12:00"
		},{
			"order_no":"0000006",
			"order_time":"2014-10-06 12:00"
		},{
			"order_no":"0000005",
			"order_time":"2014-10-05 12:00"
		},{
			"order_no":"0000004",
			"order_time":"2014-10-04 12:00"
		},{
			"order_no":"0000003",
			"order_time":"2014-10-03 12:00"
		},{
			"order_no":"0000002",
			"order_time":"2014-10-02 12:00"
		},{
			"order_no":"0000001",
			"order_time":"2014-10-01 12:00"
		}]
		"""

	When jobs选择时间段
		"""
		{
			"time_quantum":"2014-09-01~2014-09-30",
			"submit":"点击"
		}
		"""
	Then jobs获取对应的订单
		"""
		[]
		"""