#author: 冯雪静
#editot: 张三香 2015.10.16

Feature:模板消息
	jobs可以选择\修改主行业和副行业

Background:
	Given jobs登录系统
	And jobs已有行业
		"""
		[{
			"name":"IT科技"
		},{
			"name":"消费品"
		},{
			"name":"金融"
		}]
		"""

@mall2 @message @templateMessage   @market_tools @market_tools.template_message.test.view
Scenario:1 选择主营行业和副营行业
	jobs选择主营行业和副营行业
	1.模板消息列表正序排列

	When jobs选择行业
		"""
		{
			"host_industry":"IT科技",
			"deputy_industry":"消费品"
		}
		"""

	Then jobs查看模板消息列表
		"""
		[{
			"template_id":"",
			"headline":"订单支付成功",
			"industry":"IT科技",
			"type":"主营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"商品已发出通知",
			"industry":"IT科技",
			"type":"主营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"订单支付成功",
			"industry":"消费品",
			"type":"副营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"商品已发出通知",
			"industry":"消费品",
			"type":"副营行业",
			"status":"未启用",
			"operate":"查看"
		}]
		"""

@mall2 @message @templateMessage   @market_tools @market_tools.template_message.test.view
Scenario:2 选择主营行业不选副营行业
	jobs选择主营行业不选副营行业
	1.模板消息列表正序排列

	When jobs选择行业
		"""
		{
			"host_industry":"IT科技",
			"deputy_industry":""
		}
		"""
	Then jobs查看模板消息列表
		"""
		[{	
			"template_id":"",
			"headline":"订单支付成功",
			"industry":"IT科技",
			"type":"主营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"商品已发出通知",
			"industry":"IT科技",
			"type":"主营行业",
			"status":"未启用",
			"operate":"查看"
		}]
		"""

@mall2 @message @templateMessage   @market_tools @market_tools.template_message.test.view
Scenario:3 不选主营行业选择副营行业
	jobs不选主营行业选择副营行业
	1.模板消息列表正序排列

	When jobs选择行业
		"""
		{
			"host_industry":"",
			"deputy_industry":"消费品"
		}
		"""
	Then jobs查看模板消息列表
		"""
		[]
		"""

@mall2 @message @templateMessage   @market_tools @market_tools.template_message.test.view
Scenario:4 不选主营行业不选副营行业
	jobs不选主营行业不选副营行业
	1.模板消息列表正序排列

	When jobs选择行业
		"""
		{
			"host_industry":"",
			"deputy_industry":""
		}
		"""
	Then jobs查看模板消息列表
		"""
		[]
		"""

@mall2 @message @templateMessage   @market_tools @market_tools.template_message.test.view 
Scenario:5 修改主行业和副行业
	jobs可以修改主行业和副行业
	1.模板消息列表正序排列

	When jobs选择行业
		"""
		{
			"host_industry":"IT科技",
			"deputy_industry":"消费品"
		}
		"""
	Then jobs查看模板消息列表
		"""
		[{
			"template_id":"",
			"headline":"订单支付成功",
			"industry":"IT科技",
			"type":"主营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"商品已发出通知",
			"industry":"IT科技",
			"type":"主营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"订单支付成功",
			"industry":"消费品",
			"type":"副营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"商品已发出通知",
			"industry":"消费品",
			"type":"副营行业",
			"status":"未启用",
			"operate":"查看"
		}]
		"""
	When jobs选择行业
		"""
		{
			"host_industry":"金融",
			"deputy_industry":"IT科技"
		}
		"""
	Then jobs查看模板消息列表
		"""
		[{
			"template_id":"",
			"headline":"订单支付成功",
			"industry":"金融",
			"type":"主营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"商品已发出通知",
			"industry":"金融",
			"type":"主营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"订单支付成功",
			"industry":"IT科技",
			"type":"副营行业",
			"status":"未启用",
			"operate":"查看"
		},{
			"template_id":"",
			"headline":"商品已发出通知",
			"industry":"IT科技",
			"type":"副营行业",
			"status":"未启用",
			"operate":"查看"
		}]
		"""
