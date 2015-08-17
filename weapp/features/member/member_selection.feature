# __author__ : "冯雪静"
Feature: 筛选会员列表
	jobs能管理会员列表

Background:
	Given jobs登录系统
	And jobs添加会员等级
		"""
		[{
			"name": "银牌会员",
			"upgrade": "不自动升级",
			"shop_discount": "100%"
		},{
			"name": "金牌会员",
			"upgrade": "自动升级",
			"shop_discount": "98%"
		}]
		"""
	And jobs添加会员分组
		"""
		[{
			"name": "分组1"
		},{
			"name": "分组2"
		},{
			"name": "分组3"
		}]
		"""
	And jobs已有会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "金牌会员",
			"price": 196.00,
			"buy_sum": 2,
			"buy_time": "2015-01-01",
			"integral": 20,
			"friends_sum": 1,
			"sources": "推广扫码",
			"packet": "分组3",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"buy_time": "2014-12-31",
			"integral": 20,
			"friends_sum": 1,
			"sources": "会员分享",
			"packet": "分组2",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"buy_time": "2014-12-22",
			"integral": 20,
			"friends_sum": 2,
			"sources": "会员分享",
			"packet": "分组1",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "银牌会员",
			"price": 300.00,
			"buy_sum": 3,
			"buy_time": "2014-12-15",
			"integral": 120,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 4,
			"buy_time": "2014-11-30",
			"integral": 220,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-11-30",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 500.00,
			"buy_sum": 5,
			"buy_time": "2014-09-01",
			"integral": 300,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-09-01",
			"status": "已关注"
		},{
			"name": "tom4",
			"member_rank": "金牌会员",
			"price": 1000.00,
			"buy_sum": 11,
			"buy_time": "2014-5-30",
			"integral": 1000,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已关注"
		},{
			"name": "tom5",
			"member_rank": "普通会员",
			"price": 0.00,
			"buy_sum": 0,
			"buy_time": "2014-5-30",
			"integral": 20,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已关注"
		}]
		"""
	And jobs获取当前时间为
		"""
		{
			"time":"2015-01-01"
		}
		"""

@ignore
Scenario:对会员列表进行基础筛选
	1.jobs选择一个条件时,获取对应的会员列表
	2.jobs选择多个条件时,获取对应的会员列表
	3.jobs选择全部条件时,获取对应的会员列表

	When jobs选择条件为
		"""
		{
			"member_rank":"普通会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "nokia",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"buy_time": "2014-12-31",
			"integral": 20,
			"friends_sum": 1,
			"sources": "会员分享",
			"packet": "分组2",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"buy_time": "2014-12-22",
			"integral": 20,
			"friends_sum": 2,
			"sources": "会员分享",
			"packet": "分组1",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 4,
			"buy_time": "2014-11-30",
			"integral": 220,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-11-30",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 500.00,
			"buy_sum": 5,
			"buy_time": "2014-09-01",
			"integral": 300,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-09-01",
			"status": "已关注"
		},{
			"name": "tom5",
			"member_rank": "普通会员",
			"price": 0.00,
			"buy_sum": 0,
			"buy_time": "2014-5-30",
			"integral": 20,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已关注"
		}]
		"""
	When jobs选择条件为
		"""
		{
			"packet":"分组2",
			"sources":"会员分享"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "nokia",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"buy_time": "2014-12-31",
			"integral": 20,
			"friends_sum": 1,
			"sources": "会员分享",
			"packet": "分组2",
			"add_time": "2014-12-29",
			"status": "已关注"
		}]
		"""
	When jobs选择条件为
		"""
		{
			"packet":"分组2",
			"member_rank": "金牌会员",
			"sources":"推广扫码"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[]
		"""
	When jobs选择条件为
		"""
		{}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "金牌会员",
			"price": 196.00,
			"buy_sum": 2,
			"buy_time": "2015-01-01",
			"integral": 20,
			"friends_sum": 1,
			"sources": "推广扫码",
			"packet": "分组3",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"buy_time": "2014-12-31",
			"integral": 20,
			"friends_sum": 1,
			"sources": "会员分享",
			"packet": "分组2",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"buy_time": "2014-12-22",
			"integral": 20,
			"friends_sum": 2,
			"sources": "会员分享",
			"packet": "分组1",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "银牌会员",
			"price": 300.00,
			"buy_sum": 3,
			"buy_time": "2014-12-15",
			"integral": 120,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 4,
			"buy_time": "2014-11-30",
			"integral": 220,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-11-30",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 500.00,
			"buy_sum": 5,
			"buy_time": "2014-09-01",
			"integral": 300,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-09-01",
			"status": "已关注"
		},{
			"name": "tom4",
			"member_rank": "金牌会员",
			"price": 1000.00,
			"buy_sum": 11,
			"buy_time": "2014-5-30",
			"integral": 1000,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已关注"
		},{
			"name": "tom5",
			"member_rank": "普通会员",
			"price": 0.00,
			"buy_sum": 0,
			"buy_time": "2014-5-30",
			"integral": 20,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已关注"
		}]
		"""

@ignore
Scenario:对会员列表进行消费指数筛选
	1.jobs选择一个条件时,获取对应的会员列表
	2.jobs选择多个条件时,获取对应的会员列表
	3.jobs选择全部条件时,获取对应的会员列表

	When jobs选择条件为
		"""
		{
			"buy_sum": "3+"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "bill",
			"member_rank": "银牌会员",
			"price": 300.00,
			"buy_sum": 3,
			"buy_time": "2014-12-15",
			"integral": 120,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 4,
			"buy_time": "2014-11-30",
			"integral": 220,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-11-30",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 500.00,
			"buy_sum": 5,
			"buy_time": "2014-09-01",
			"integral": 300,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-09-01",
			"status": "已关注"
		},{
			"name": "tom4",
			"member_rank": "金牌会员",
			"price": 1000.00,
			"buy_sum": 11,
			"buy_time": "2014-5-30",
			"integral": 1000,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已关注"
		}]
		"""
	When jobs选择条件为
		"""
		{
			"buy_sum": "10+"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom4",
			"member_rank": "金牌会员",
			"price": 1000.00,
			"buy_sum": 11,
			"buy_time": "2014-5-30",
			"integral": 1000,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已关注"
		}]
		"""
	When jobs选择条件为
		"""
		{
			"buy_sum": "1+",
			"buy_time": "三天内"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "金牌会员",
			"price": 196.00,
			"buy_sum": 2,
			"buy_time": "2015-01-01",
			"integral": 20,
			"friends_sum": 1,
			"sources": "推广扫码",
			"packet": "分组3",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"buy_time": "2014-12-31",
			"integral": 20,
			"friends_sum": 1,
			"sources": "会员分享",
			"packet": "分组2",
			"add_time": "2014-12-29",
			"status": "已关注"
		}]
		"""
	When jobs选择条件为
		"""
		{
			"buy_sum": "1+",
			"buy_time": "二周内",
			"add_time": "二周内",
			"integral": 1-100
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "金牌会员",
			"price": 196.00,
			"buy_sum": 2,
			"buy_time": "2015-01-01",
			"integral": 20,
			"friends_sum": 1,
			"sources": "推广扫码",
			"packet": "分组3",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"buy_time": "2014-12-31",
			"integral": 20,
			"friends_sum": 1,
			"sources": "会员分享",
			"packet": "分组2",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"buy_time": "2014-12-22",
			"integral": 20,
			"friends_sum": 2,
			"sources": "会员分享",
			"packet": "分组1",
			"add_time": "2014-12-21",
			"status": "已关注"
		}]
		"""
	When jobs选择条件为
		"""
		{
			"buy_sum": "5+",
			"buy_time": "二周内",
			"add_time": "半年内",
			"integral": 100-300
		}
		"""
	Then jobs可以获得会员列表
		"""
		[]
		"""
	When jobs选择条件为
		"""
		{}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "金牌会员",
			"price": 196.00,
			"buy_sum": 2,
			"buy_time": "2015-01-01",
			"integral": 20,
			"friends_sum": 1,
			"sources": "推广扫码",
			"packet": "分组3",
			"add_time": "2015-01-01",
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"price": 100.00,
			"buy_sum": 1,
			"buy_time": "2014-12-31",
			"integral": 20,
			"friends_sum": 1,
			"sources": "会员分享",
			"packet": "分组2",
			"add_time": "2014-12-29",
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"price": 200.00,
			"buy_sum": 2,
			"buy_time": "2014-12-22",
			"integral": 20,
			"friends_sum": 2,
			"sources": "会员分享",
			"packet": "分组1",
			"add_time": "2014-12-21",
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "银牌会员",
			"price": 300.00,
			"buy_sum": 3,
			"buy_time": "2014-12-15",
			"integral": 120,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-12-15",
			"status": "已关注"
		},{
			"name": "tom2",
			"member_rank": "普通会员",
			"price": 300.00,
			"buy_sum": 4,
			"buy_time": "2014-11-30",
			"integral": 220,
			"friends_sum": 2,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-11-30",
			"status": "已关注"
		},{
			"name": "tom3",
			"member_rank": "普通会员",
			"price": 500.00,
			"buy_sum": 5,
			"buy_time": "2014-09-01",
			"integral": 300,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-09-01",
			"status": "已关注"
		},{
			"name": "tom4",
			"member_rank": "金牌会员",
			"price": 1000.00,
			"buy_sum": 11,
			"buy_time": "2014-5-30",
			"integral": 1000,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已关注"
		},{
			"name": "tom5",
			"member_rank": "普通会员",
			"price": 0.00,
			"buy_sum": 0,
			"buy_time": "2014-5-30",
			"integral": 20,
			"friends_sum": 0,
			"sources": "直接关注",
			"packet": "未分组",
			"add_time": "2014-01-03",
			"status": "已关注"
		}]
		"""

	