# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

class ExpressRequestParams(object):
	"""
	快递100 请求中的参数定义
	"""
	def __init__(self):
		raise NotImplementedError


	# 选择json则推送也是json，选择xml则推送也是xml，默认是json
	SCHEMA = 'schema'

	# 加入json或xml格式的内容
	PARAM = 'param'

	# 公司代码
	# 公司代码，请参考文档最后（一律小写，要求严格一致）
	COMPANY = 'company'

	# 快递单号	
	NUMBER = 'number'

	# 出发地城市
	# 中文的正确地名，一般到市即可，如果没有，可以提交地址，我们会解析，这个参数不提供也可以，我们会根据快递结果解析获得，主要用途是查询时效数据库。
	FROM = 'from'

	# 到达地城市
	# 中文的正确地名，一般到市即可，也可使用地址，这个参数必需提供，查询时效需要。
	TO = 'TO'

	# 授权码
	KEY = 'key'

	# json中的 属性
	PARAMETERS = 'parameters'

	# 回调地址
	# 推送数据的目标地址,查询结果将通过http协议post到这个地址
	CALLBACK_URL = 'callbackurl'


	# 跟踪的订单状态
	STATUS = 'status'

	# *最新查询结果，全量，倒序（即时间最新的在最前）
	LAST_RESULT = 'lastResult'

	# 快递单当前签收状态，包括
	# 0在途中、1已揽收、2疑难、3已签收、4退签、5同城派送中、6退回、7转单等7个状态
	STATE = 'state'

	# 内容
	CONTEXT = 'context'

	# 时间，原始格式
	time = 'time'
	
	# 格式化后时间
	ftime = 'ftime'

	# 监控状态相关消息，如:3天查询无记录，60天无变化
	MESSAGE = 'message'