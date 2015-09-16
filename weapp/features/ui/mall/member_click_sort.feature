# __editor__ : "新新9.9"

Feature: 会员列表排序
	#点击好友数,积分,消费总额,客单价,购买次数,关注时间来源,点击都可以进行排序(并且正序为上箭头,倒序为下箭头)
	#第一次点击都为倒序(下箭头),再次点击为正序(上箭头)
	#默认关注时间来源倒序显示
	#默认关注时间来源倒序显示,再次点击正序
	
Background:
	Given jobs登录系统
	When jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "10"
		}]
		"""
	When jobs能获取会员分组列表
		"""
		[{
			"name": "未分组"
		}]
		"""

	And jobs已有会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已跑路"
		}]
		"""
Scenario: 1 默认关注时间来源倒序显示
	When jobs登录系统
	Then jobs获取会员列表:ui
	"""
		[{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已取消"
		}]
		"""

Scenario: 2 默认关注时间来源倒序显示,再次点击正序
	When jobs关注时间来源倒序点击为正序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已取消"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		}]
	"""

Scenario: 3 好友数第一次点击倒序排序
	When jobs好友数点击为倒序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已取消"
		}]
	"""
	When jobs好友数点击为正序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已取消"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		}]
	"""

Scenario: 4 积分第一次点击倒序排序
	When jobs积分数点击为倒序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已跑路"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		}]
	"""
	When jobs积分点击为正序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已跑路"
		}]
	"""

Scenario: 5 消费总额第一次点击倒序排序
	When jobs消费总额点击为倒序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已跑路"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		}]
	"""
	When jobs消费总额点击为正序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已跑路"
		}]
	"""

Scenario: 6 客单价第一次点击倒序排序
	When jobs客单价点击为倒序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已跑路"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		}]
	"""
	When jobs客单价点击为正序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已跑路"
		}]
	"""

Scenario: 7 购买次数第一次点击倒序排序
	When jobs购买次数点击为倒序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已跑路"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		}]
	"""
	When jobs购买次数点击为正序:ui
	Then jobs获取会员列表:ui
	"""
	[{
			"name": "tom1",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"integral": 50,
			"friends_sum": 5,
			"per_customer_transaction": 100,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 2,
			"per_customer_transaction": 150,
			"sources": "会员分享",
			"packet": "未分组",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 196.00,
			"buy_sum": 2,
			"integral": 20,
			"friends_sum": 1,
			"per_customer_transaction": 1,
			"sources": "推广扫码",
			"packet": "未分组",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 3,
			"integral": 120,
			"friends_sum": 0,
			"per_customer_transaction": 220,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已跑路"
		}]
	"""