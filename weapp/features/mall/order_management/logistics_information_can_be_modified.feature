# __author__ : "冯雪静"
@func:webapp.modules.mall.views.update_express_info
Feature:订单的物流信息可以修改
	jobs能通过管理系统对订单的物流信息修改

Background:
	Given jobs登录系统
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	And jobs已有的订单
		"""
		[{
			"order_no": "0000001",
			"logistics": "圆通",
			"number": "100065947315",
			"status": "已发货",
			"member": "bill"
		}, {
			"order_no": "0000002",
			"logistics": "圆通",
			"number": "100065940000",
			"status": "已发货",
			"member": "tom"
		}]
		"""
	And jobs登录系统

@mall2 @order @mall.update_express_info @pyliu
Scenario:1 jobs修改'0000001'的物流信息
	When jobs通过后台管理系统对'0000001'的物流信息进行修改
		"""
		{
			"order_no":"0000001",
			"logistics":"申通",
			"number":"100065947315",
			"status":"已发货"
		}
		"""
	Then bill在webapp查看'0000001'的物流信息
		"""
		{
			"order_no":"0000001",
			"logistics":"申通",
			"number":"100065947315",
			"status":"已发货"
		}
		"""

	When jobs通过后台管理系统对'0000002'的物流信息进行修改
		"""
		{
			"order_no":"0000002",
			"logistics":"顺丰",
			"number":"321321321321",
			"status":"已发货"
		}
		"""
	Then tom在webapp查看'0000002'的物流信息
		"""
		{
			"order_no":"0000002",
			"logistics":"顺丰",
			"number":"321321321321",
			"status":"已发货"
		}
		"""
