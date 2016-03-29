#author: 王丽
#editor: 张三香 2015.10.16

Feature: 会员列表-会员详情-传播能力
	"""
		会员分享链接和推广扫码带来的访问量和新增会员数的记录
		1、【二维码引流会员数量】：本会员通过"推广扫码"带来的新增会员数
		2、【分享链接引流会员数量】：本会员通过"分享链接"带来的新增会员数
		3、分享链接明细列表
			【分享链接】：分享链接的页面名称或者活动名称
			【点击】：点击此链接数（包含会员和非会员的点击数），同意人只计算一次
			【关注转化】：通过此链接带来的新增会员数
			【购买转化】：通过此链接带来的付款订单数（订单状态为：待发货、已发货、已完成、退款中、退款成功）
				备注：只能是购买分享的链接的商品
	"""

#author:王丽 2015.10.22
@mall2 @member @memberList
Scenario:1 会员详情-传播能力(二维码引流)
	Given jobs登录系统
	When jobs创建推广扫码
		"""
		{
			"prize_type":"无",
			"page_description":"无奖励，页面描述文本"
		}
		"""
	Then jobs获得推广扫码
		"""
		{
			"prize_type":"无",
			"page_description":"无奖励，页面描述文本"
		}
		"""
		
	#bill带来的传播能力数据创建
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill进入推广扫描链接

	When 清空浏览器
	When marry扫描bill的推广二维码关注jobs公众号

	When 清空浏览器
	When jack扫描bill的推广二维码关注jobs公众号

	When 清空浏览器
	When nokia扫描bill的推广二维码关注jobs公众号

	When 清空浏览器
	When tom扫描bill的推广二维码关注jobs公众号

	When 清空浏览器
	When tom1扫描bill的推广二维码关注jobs公众号

	#校验bill的传播能力
	When 清空浏览器
	Given jobs登录系统
	Then jobs获得'bill'的传播能力
		"""
		{
			"scan_qrcode_new_member": 5
		}
		"""



#author:王丽 2015.10.19
@mall2 @member @memberList
Scenario:2 会员详情-传播能力(二维码引流会员列表)
	#1 二维码引流会员列表展示会员推广扫码带来的会员,按关注时间倒叙排列
	#	会员名称、会员头像、会员等级、会员积分、会员来源、关注时间
	#2 二维码引流会员列表分页显示，每页显示6条记录，不显示滚动条

	Given jobs登录系统
	When jobs创建推广扫码
		"""
		{
			"prize_type":"无",
			"page_description":"无奖励，页面描述文本"
		}
		"""
	Then jobs获得推广扫码
		"""
		{
			"prize_type":"无",
			"page_description":"无奖励，页面描述文本"
		}
		"""
	Given jobs设定会员积分策略
		"""
		{
			"be_member_increase_count":20
		}
		"""
		
	#bill带来的传播能力数据创建
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill进入推广扫描链接

	When 清空浏览器
	When marry扫描bill的推广二维码关注jobs公众号
	When 休眠1秒

	When 清空浏览器
	When jack扫描bill的推广二维码关注jobs公众号
	When 休眠1秒

	When 清空浏览器
	When nokia扫描bill的推广二维码关注jobs公众号
	When 休眠1秒

	When 清空浏览器
	When tom扫描bill的推广二维码关注jobs公众号
	When 休眠1秒

	When 清空浏览器
	When tom1扫描bill的推广二维码关注jobs公众号
	When 休眠1秒

	When 清空浏览器
	Given jobs登录系统
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""

	When jobs访问'bill'二维码引流会员好友列表
	Then jobs获得二维码引流会员好友列表显示共3页

	When jobs浏览二维码引流会员好友列表'第1页'
	Then jobs获得二维码引流会员好友列表
		"""
		[{
			"name": "tom1",
			"member_rank": "普通会员",
			"integral": 20,
			"attention_time": "今天",
			"source": "推广扫码"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"integral": 20,
			"attention_time": "今天",
			"source": "推广扫码"
		}]
		"""
	
	When jobs浏览二维码引流会员好友列表'下一页'
	Then jobs获得二维码引流会员好友列表
		"""
		[{
			"name": "nokia",
			"member_rank": "普通会员",
			"integral": 20,
			"attention_time": "今天",
			"source": "推广扫码"
		},{
			"name": "jack",
			"member_rank": "普通会员",
			"integral": 20,
			"attention_time": "今天",
			"source": "推广扫码"
		}]
		"""

	When jobs浏览二维码引流会员好友列表'第3页'
	Then jobs获得二维码引流会员好友列表
		"""
		[{
			"name": "marry",
			"member_rank": "普通会员",
			"integral": 20,
			"attention_time": "今天",
			"source": "推广扫码"
		}]
		"""

	When jobs浏览二维码引流会员好友列表'上一页'
	Then jobs获得二维码引流会员好友列表
		"""
		[{
			"name": "nokia",
			"member_rank": "普通会员",
			"integral": 20,
			"attention_time": "今天",
			"source": "推广扫码"
		},{
			"name": "jack",
			"member_rank": "普通会员",
			"integral": 20,
			"attention_time": "今天",
			"source": "推广扫码"
		}]
		"""
