# __author__ : "崔帅帅"
Feature: 更新优惠券排行榜时间
	Jobs能通过管理系统添加"更新优惠券排行榜时间"


@market_tool.coupon.a @market_tool
Scenario: 更新优惠券排行榜时间
	Given jobs登录系统
	When jobs更新优惠券排行榜时间
		"""
		[{
			"start_date": "2014-07-08",
			"end_date": "2014-07-28"
		}]
		"""
	Then jobs能获得优惠券排行榜时间
		'''
		[{
			"start_date": "2014-07-08",
			"end_date": "2014-07-28"
		}]
		'''
