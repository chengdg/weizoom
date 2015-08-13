# __author__ : "冯雪静"

Feature:模板消息
	jobs可以添加\修改模板消息内容,修改模板消息(启用、停用)状态

Background:
	Given jobs登录系统
	And jobs已有模板消息
		"""
		[{
			"template_id":"muban01",
			"headline":"订单支付成功",
			"industry":"IT科技",
			"type":"主营行业",
			"status":"已启用",
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

@market_tools @market_tools.template_message.test.operate
Scenario:添加\修改模板消息内容
	jobs可以添加\修改模板消息内容
	1.jobs给template_id为"muban03"的模板消息添加内容
	2.jobs给template_id为"muban03"的模板消息修改内容

	When jobs给'消费品'行业标题为'订单支付成功'的模板消息添加内容
		"""
		{
			"template_id":"muban03",
			"first":"我们已收到您的货款,开始为您打包商品,请耐心等待!",
			"remark":""
		}
		"""
	Then jobs查看'消费品'行业标题为'订单支付成功'的模板消息
		"""
		{
			"template_id":"",
			"first":"",
			"remark":""
		}
		"""
	When jobs给'消费品'行业标题为'订单支付成功'的模板消息添加内容
		"""
		{
			"template_id":"muban03",
			"first":"我们已收到您的货款,开始为您打包商品,请耐心等待!",
			"remark":"如有问题咨询微众客服,微众将第一时间为您服务!"
		}
		"""
	Then jobs查看'消费品'行业标题为'订单支付成功'的模板消息
		"""
		{
			"template_id":"muban03",
			"first":"我们已收到您的货款,开始为您打包商品,请耐心等待!",
			"remark":"如有问题咨询微众客服,微众将第一时间为您服务!"
		}
		"""
	When jobs给'消费品'行业标题为'订单支付成功'的模板消息添加内容
		"""
		{
			"template_id":"muban03",
			"first":"我们已收到您的货款,开始为您打包商品,请耐心等待:)!",
			"remark":"如有问题咨询微众客服,微众将第一时间为您服务:(!"
		}
		"""
	Then jobs查看'消费品'行业标题为'订单支付成功'的模板消息
		"""
		{
			"template_id":"muban03",
			"first":"我们已收到您的货款,开始为您打包商品,请耐心等待:)!",
			"remark":"如有问题咨询微众客服,微众将第一时间为您服务:(!"
		}
		"""

@market_tools @market_tools.template_message.test.operate
Scenario:修改模板消息(启用、停用)状态
	jobs可以修改模板消息状态
	1.jobs查看模板消息列表

	When jobs修改'消费品'行业标题为'订单支付成功'的状态
		"""
		{
			"template_id":"muban03",
			"headline":"订单支付成功",
			"industry":"消费品",
			"type":"副营行业",
			"status":"已启用",
			"operate":"查看"
		}
		"""
	Then jobs查看模板消息列表
		"""
		[{
			"template_id":"muban01",
			"headline":"订单支付成功",
			"industry":"IT科技",
			"type":"主营行业",
			"status":"已启用",
			"operate":"查看"
		},{
			"template_id":"muban03",
			"headline":"订单支付成功",
			"industry":"消费品",
			"type":"副营行业",
			"status":"已启用",
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
			"headline":"商品已发出通知",
			"industry":"消费品",
			"type":"副营行业",
			"status":"未启用",
			"operate":"查看"
		}]
		"""
	When jobs修改'IT科技'行业标题为'订单支付成功'的状态
		"""
		{
			"template_id":"muban01",
			"headline":"订单支付成功",
			"industry":"IT科技",
			"type":"主营行业",
			"status":"未启用",
			"operate":"查看"
		}
		"""
	Then jobs查看模板消息列表
		"""
		[{
			"template_id":"muban03",
			"headline":"订单支付成功",
			"industry":"消费品",
			"type":"副营行业",
			"status":"已启用",
			"operate":"查看"
		},{
			"template_id":"muban01",
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
			"headline":"商品已发出通知",
			"industry":"消费品",
			"type":"副营行业",
			"status":"未启用",
			"operate":"查看"
		}]
		"""