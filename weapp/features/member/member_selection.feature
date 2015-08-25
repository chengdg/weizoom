<<<<<<< HEAD
# __author__ : "冯雪静"
# __editor__ : "新新"
Feature: 筛选会员列表
	jobs能管理会员列表
	#默认展示两列筛选条件，点击展开后显示所有，当点击收起后展示为默认状态
	1.对会员列表进行基础筛选
	2.对会员列表进行消费指数筛选
	#增加最后对话时间筛选条件
	3.筛选出会员发送优惠券
	#除已跑路外
	4.筛选条件下所有会员群发消息
	#除已跑路外
	#鼠标移入“群发消息”时显示群发选项，移出时隐藏
	#选择会员后点击群发消息,可跳转到群发消息页，当选择给选中会员群发消息时显示群发会员名称（无备注的显示昵称、有备注的显示备注名称），鼠标移入会员名称时出现删除标志，点击删除标志后移除该会员，点击重新筛选则回到会员管理页面，当选择按筛选条件群发消息时，显示筛选条件，点击重新筛选则回到会员管理页面。

Background:
	Given jobs登录系统
	And jobs添加会员等级
		"""
		[{
			"name": "银牌会员",
			"upgrade": "不自动升级",
			"shop_discount": "10"
		},{
			"name": "金牌会员",
			"upgrade": "自动升级",
			"shop_discount": "9.8"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "10"
		},{
			"name": "银牌会员",
			"upgrade": "不自动升级",
			"shop_discount": "10"
		},{
			"name": "金牌会员",
			"upgrade": "自动升级",
			"shop_discount": "9.8"
		}]
		"""
	And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2",
			"tag_id_3": "分组3"
		}
		"""
	Then jobs能获取会员分组列表
		"""
		[{
			"name": "未分组"
		},{
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
			"status": "已跑路"
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
			"status": "已跑路"
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
			"status": "已跑路"
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
			"status": "已跑路"
		}]
		"""

@memberList
# __editor__ : "新新"
Scenario:筛选出会员发送优惠券
#除已跑路外
	Given jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "单品券2",
			"money": 10.00,
			"each_limit": "不限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_",
			"coupon_product": "商品1"
		}]
		"""
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_5": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_6": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_7": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_8": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_9": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon2_id_10": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

	Given nokia关注jobs的公众号
	Given tom关注jobs的公众号
	Given tom2关注jobs的公众号
	Given tom3关注jobs的公众号
	Given tom5关注jobs的公众号

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
			"status": "已跑路"
		}]
		"""
	When jobs为会员发放优惠券
		"""
		{
			"name": "单品券2",
			"count": 2,
			"members": ["nokia","tom","tom2","tom3"]
		}
		"""
	Then jobs优惠券发放成功
	When nokia访问jobs的webapp
	Then nokia能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_1",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_2",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom访问jobs的webapp
	Then tom能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_3",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_4",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom2访问jobs的webapp
	Then tom2能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_5",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_6",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom3访问jobs的webapp
	Then tom3能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_7",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_8",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	When tom5访问jobs的webapp
	Then tom5能获得webapp优惠券列表
		"""
		[
			{
				"coupon_id": "coupon2_id_9",
				"money": 10.00,
				"status": "未使用"
			}, {
				"coupon_id": "coupon2_id_10",
				"money": 10.00,
				"status": "未使用"
			}
		]
		"""
	Given jobs登录系统
	Then jobs能获得优惠券'单品券2'的码库
		"""
		{
			"coupon2_id_1": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "nokia"
			},
			"coupon2_id_2": {
				"money": 10.00,
				"status": "未使用",
				"consumer": "",
				"target": "nokia"
			},
			"coupon2_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom"
			},
			"coupon2_id_4": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom"
			},
			"coupon2_id_5": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom2"
			},
			"coupon2_id_6": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom2"
			},
			"coupon2_id_7": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom3"
			},
			"coupon2_id_8": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom3"
			},
			"coupon2_id_9": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom5"
			},
			"coupon2_id_10": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": "tom5"
			}
		}
		"""
@memberList
# __editor__ : "新新"
Scenario:筛选条件下所有会员群发消息
	#除已跑路外
	#任一会员都没有满足4条群发消息
	Given jobs登录系统
	And jobs已有图文
		"""
		[{
			"name": "图文1"
		}]
		"""
	Given nokia关注jobs的公众号
	Given tom关注jobs的公众号
	Given tom2关注jobs的公众号
	Given tom3关注jobs的公众号
	Given tom5关注jobs的公众号
	When tom5取消了关注jobs的公众号
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
			"status": "已跑路"
		}]
		"""
	When jobs添加群发
	"""
		{
			"content":"图文1"
		}
	"""
	When jobs群发
	When nokia访问jobs的webapp
	Then nokia能收到群发
	"""
		{
			"content":"图文1"
		}
	"""
	When tom访问jobs的webapp
	Then tom能收到群发
	"""
		{
			"content":"图文1"
		}
	"""
	When tom2访问jobs的webapp
	Then tom2能收到群发
	"""
		{
			"content":"图文1"
		}
	"""
	When tom3访问jobs的webapp
	Then tom3能收到群发
	"""
		{
			"content":"图文1"
		}
	"""
=======
# __author__ : "王丽"

Feature: 筛选会员列表
"""
	jobs能管理会员列表
	1、默认展示两行筛选条件，点击展开后显示所有，当点击收起后展示为默认状态
		筛选条件顺序如下
		会员名称、会员状态、关注时间
		会员等级、会员分组、会员来源
		消费总额、购买次数、最后购买时间
		积分范围、最后对话时间
	2、筛选规则
	（1）【会员名称】：模糊匹配
	（2）【会员状态】：下拉选择（已关注、全部、取消关注）；默认"已关注"
	（3）【关注时间】：开始和结束时间，过滤会员的关注时间；
					开始时间必须小于结束时间，不能清空；
					开始时间为空，提示"请输入关注开始时间"；
					结束时间为空，提示"请输入关注结束时间"；
	（4）【会员等级】：下拉选择（全部、会员等级列表按照创建的顺序）；默认"全部"
	（5）【会员分组】：下拉选择（全部、会员分组列表按照创建的顺序）；默认"全部"
	（6）【会员来源】：下拉选择（全部、直接关注、推广扫码、会员分享）；默认"全部"
	（7）【消费总额】：会员提交支付的所有订单的实付金额总和
				=∑ 订单.实付金额[(订单.买家=当前会员) and (订单.状态 in {待发货、已发货、已完成、退款中、退款成功})]
	（8）【购买次数】：会员提交支付的所有订单的总和
				=∑ 订单.个数[(订单.买家=当前会员) and (订单.状态 in {待发货、已发货、已完成、退款中、退款成功})]
	（9）【最后购买时间】：会员最后一个提交已支付的订单的下单时间
	（10）【积分范围】：会员目前拥有的积分
	（11）【最后对话时间】：会员发送给公众账号的最后一条消息的时间

"""

Background:

	Given jobs登录系统

	#添加相关基础数据
		When jobs已添加商品
			"""
			[{
				"name": "商品1",
				"postage":10,
				"price":100,
				"model": {
					"models": {
						"standard": {
							"stock_type": "无限"
						}
					}
				}
			}, {
				"name": "商品2",
				"postage":15,
				"price":100,
				"model": {
					"models": {
						"standard": {
							"stock_type": "无限"
						}
					}
				}
			}]
			"""
		And jobs已添加支付方式
			"""
			[{
				"type": "货到付款",
				"is_active": "启用"
			},{
				"type": "微信支付",
				"is_active": "启用"
			},{
				"type": "支付宝",
				"is_active": "启用"
			}]
			"""
		And jobs添加会员等级
			"""
			[{
				"name": "银牌会员",
				"upgrade": "手动升级",
				"shop_discount": "10"
			},{
				"name": "金牌会员",
				"upgrade": "自动升级",
				"shop_discount": "9"
			}]
			"""

		When jobs添加会员分组
			"""
			{
				"tag_id_1": "分组1",
				"tag_id_2": "分组2",
				"tag_id_3": "分组3"
			}
			"""

	#批量获取微信用户关注
		When jobs批量获取微信用户关注
			| member_name   | attention_time 	 | member_source |   grade  |    tags     |
			| tom1 			| 2014-8-4 23:59:59  | 直接关注      | 银牌会员 | 分组1       |
			| tom2 			| 2014-8-5 00:00:00  | 推广扫码      | 普通会员 | 分组1       |
			| tom3	 	    | 2014-8-5 8:00:00   | 会员分享      | 银牌会员 | 分组1,分组3 |
			| tom4 			| 2014-8-5 23:59:59  | 会员分享      | 金牌会员 | 分组3       |
			| tom5 			| 2014-8-6 00:00:00  | 会员分享      | 金牌会员 | 分组3       |
			| tom6          | 2014-10-1 8:00:00  | 推广扫码      | 普通会员 |             |
			| tom7          | 2014-10-1 8:00:00  | 直接关注      | 金牌会员 |             |

		And tom2取消关注jobs的公众号
		And tom4取消关注jobs的公众号

	#好友
		#bill和tom1建立好友关系
			When tom1访问jobs的webapp
			When tom1把jobs的微站链接分享到朋友圈

			When 清空浏览器
			When bill点击tom1分享链接
			When bill关注jobs的公众号
			When bill访问jobs的webapp

		#bill2和tom1建立好友关系
			When 清空浏览器
			When bill2关注jobs的公众号
			When bill2访问jobs的webapp
			When bill2点击tom1分享链接

		#bill3和tom3建立好友关系
			When tom3访问jobs的webapp
			When tom3把jobs的微站链接分享到朋友圈

			When 清空浏览器
			When bill3关注jobs的公众号
			When bill3点击tom3分享链接
			When bill3访问jobs的webapp

	#获取会员积分

		When tom2访问jobs的webapp
		When tom2获得jobs的50会员积分
		Then tom2在jobs的webapp中拥有50会员积分

		When tom3访问jobs的webapp
		When tom3获得jobs的100会员积分
		Then tom3在jobs的webapp中拥有100会员积分

		When tom4访问jobs的webapp
		When tom4获得jobs的20会员积分
		Then tom4在jobs的webapp中拥有20会员积分

	#微信用户批量下订单
		When 微信用户批量消费jobs的商品
			| date       | consumer | type      |businessman|   product | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action       |  order_status   |
			| 2015-1-1   | tom1     | 	 购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      | 		   |        | 110         |              | 110    | 0      | 0    | jobs,支付         |  待发货         |
			| 2015-1-2   | tom1     | 	 购买   | jobs      | 商品2,2   | 未支付  | 支付宝         | 15      | 100      |          |        | 0           |              | 0      | 0      | 0    | jobs,取消         |  已取消         |
			| 2015-2-1   | tom2     |    购买   | jobs      | 商品2,2   | 支付    | 支付宝         | 15      | 100      |          |        | 215         |              | 215    | 0      | 0    | jobs,发货         |  已发货         |
			| 2015-2-2   | tom2     |    购买   | jobs      | 商品1,1   | 支付    | 微信支付       | 10      | 100      |          |        | 110         |              | 0      | 110    | 0    | jobs,完成         |  已完成         |
			| 2015-2-4   | tom2     |    购买   | jobs      | 商品1,1   | 未支付  | 微信支付       | 10      | 100      |          |        | 0           |              | 0      | 0      | 0    | jobs,无操作       |  未支付         |
			| 2015-3-2   | tom3     |    购买   | jobs      | 商品1,1   | 支付    | 货到付款       | 10      | 100      |          |        | 110         |              | 0      | 0      | 110  | jobs,完成         |  已完成         |
			| 2015-3-4   | tom3     |    购买   | jobs      | 商品2,1   | 支付    | 微信支付       | 15      | 100      |          |        | 115         |              | 0      | 115    | 0    | jobs,退款         |  退款中         |
			| 2015-3-5   | tom3     |    购买   | jobs      | 商品1,1   | 支付    | 支付宝         | 10      | 100      |          |        | 110         |              | 110    | 0      | 0    | jobs,完成退款     |  退款完成       |

@eugeneX
Scenario:1 默认条件和空条件查询

	Given jobs登录系统

	#首次进入，默认条件查询
		When jobs访问会员列表
		Then jobs获得会员列表默认查询条件
			"""
			[{
				"status":"已关注"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":8
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  |  source  |    tags     |
			| bill3 |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 |             |
			| bill2 |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |        今天       | 直接关注 |             |
			| bill  |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 |             |
			| tom7  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    | 2014-10-1 8:00:00 | 直接关注 |             |
			| tom6  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    | 2014-10-1 8:00:00 | 推广扫码 |             |
			| tom5  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    | 2014-8-6 00:00:00 | 会员分享 | 分组3       |
			| tom3  |   银牌会员  |       1      |    100   |   335.00  |    111.67  |      3    | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |
			| tom1  |   银牌会员  |       2      |     0    |   110.00  |    110.00  |      1    | 2014-8-4 23:59:59 | 直接关注 | 分组1       |

	#空调条件查询，“重置”查询条件，空调间查询所有数据
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":10
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
			| bill3 | 普通会员    |       1      |     0    |   0.00    |    0.00    |    0      |        今天       | 会员分享 |             |
			| bill2 | 普通会员    |       1      |     0    |   0.00    |    0.00    |    0      |        今天       | 直接关注 |             |
			| bill  | 普通会员    |       1      |     0    |   0.00    |    0.00    |    0      |        今天       | 会员分享 |             |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 直接关注 |             |
			| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 推广扫码 |             |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-8-6 00:00:00 | 会员分享 | 分组3       |
			| tom4  | 金牌会员    |       0      |     20   |   0.00    |    0.00    |    0      | 2014-8-5 23:59:59 | 会员分享 | 分组3       |
			| tom3  | 银牌会员    |       1      |    100   |   335.00  |    111.67  |    3      | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |    162.50  |    2      | 2014-8-5 00:00:00 | 推广扫码 | 分组1       |
			| tom1  | 银牌会员    |       2      |     0    |   110.00  |    110.00  |    1      | 2014-8-4 23:59:59 | 直接关注 | 分组1       |

Scenario:2 过滤条件"会员名称"

	#会员名称部分匹配查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"bill",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time | source   |  tags   |
			| bill3 | 普通会员    |       1      |     0    |   0.00    |    0.00    |    0      |      今天      | 会员分享 |         |
			| bill2 | 普通会员    |       1      |     0    |   0.00    |    0.00    |    0      |      今天      | 直接关注 |         |
			| bill  | 普通会员    |       1      |     0    |   0.00    |    0.00    |    0      |      今天      | 会员分享 |         |

	#会员名称完全匹配查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom5",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-8-6 00:00:00 | 会员分享 | 分组3   |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"marry",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表"没有符合要求的数据"

Scenario:3 过滤条件"会员状态"

	#会员状态匹配
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"取消关注",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs获得会员列表
			| name  |   member_rank  | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source |  tags   |
			| tom4  | 金牌会员 |    0    |     20   |     0.00       |      0.00      |      0     | 2014-8-5 23:59:59 |    会员分享   | 分组3       |
			| tom2  | 普通会员 |    0    |     50   |     325.00     |      162.50    |      2     | 2014-8-5 00:00:00 |    推广扫码   | 分组1       |

Scenario:4 过滤条件"关注时间"

	#区间时间边界值查询，不包含结束时间
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"2014-8-5 00:00:00",
				"attention_end_time":"2014-8-6 00:00:00",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |     tags    |
			| tom4  | 金牌会员    |       0      |     20   |   0.00    |    0.00    |    0      | 2014-8-5 23:59:59 | 会员分享 | 分组3       |
			| tom3  | 银牌会员    |       1      |    100   | 335.00    |  111.67    |    3      | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |
			| tom2  | 普通会员    |       0      |     50   | 325.00    |  162.50    |    2      | 2014-8-5 00:00:00 | 推广扫码 | 分组1       |

	#开始结束时间相同查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"2014-10-1 8:00:00",
				"attention_end_time":"2014-10-1 8:00:00",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 直接关注 |         |
			| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 推广扫码 |         |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"2015-8-10 00:00:00",
				"attention_end_time":"2015-8-11 00:00:00",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表"没有符合要求的数据"

Scenario:5 过滤条件"会员等级"

	#单等级匹配
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"金牌会员",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |      0    | 2014-10-1 8:00:00 | 直接关注 |         |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |      0    | 2014-8-6 00:00:00 | 会员分享 | 分组3   |
			| tom4  | 金牌会员    |       0      |     20   |   0.00    |    0.00    |      0    | 2014-8-5 23:59:59 | 会员分享 | 分组3   |

Scenario:6 过滤条件"会员分组"

	#单会员分组匹配
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"分组1",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
			| tom3  | 银牌会员    |       1      |    100   |   335.00  |   111.67   |      3    | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |   162.50   |      2    | 2014-8-5 00:00:00 | 推广扫码 | 分组1       |
			| tom1  | 银牌会员    |       2      |     0    |   110.00  |   110.00   |      1    | 2014-8-4 23:59:59 | 直接关注 | 分组1       |


		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"分组3",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |   0.00    | 2014-8-6 00:00:00 | 会员分享 | 分组3       |
			| tom4  | 金牌会员    |       0      |     20   |   0.00    |    0.00    |   0.00    | 2014-8-5 23:59:59 | 会员分享 | 分组3       |
			| tom3  | 银牌会员    |       1      |    100   |   0.00    |    0.00    |   0.00    | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"marry",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"分组2",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表"没有符合要求的数据"

Scenario:7 过滤条件"会员来源"

	#单会员来源匹配

		#直接关注
			When jobs设置会员查询条件
				"""
				[{
					"name":"",
					"status":"全部",
					"attention_start_time":"",
					"attention_end_time":"",
					"member_rank":"全部",
					"tags":"全部",
					"source":"直接关注",
					"pay_money_start":"",
					"pay_money_end":"",
					"pay_times_start":"",
					"pay_times_end":"",
					"last_buy_start_time":"",
					"last_buy_end_time":"",
					"integral_start":"",
					"integral_end":"",
					"massage_start_time":"",
					"massage_end_time":""
				}]
				"""
			Then jobs获得刷选结果人数
				"""
				[{
					"result_quantity":3
				}]
				"""
			Then jobs可以获得会员列表
				| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
				| bill2 | 普通会员    |       1      |     0    |   0.00    |    0.00    |    0      |        今天       | 直接关注 |             |
				| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 直接关注 |             |
				| tom1  | 银牌会员    |       2      |     0    |   110.00  |    110.00  |    1      | 2014-8-4 23:59:59 | 直接关注 | 分组1       |

		#直接关注
			When jobs设置会员查询条件
				"""
				[{
					"name":"",
					"status":"全部",
					"attention_start_time":"",
					"attention_end_time":"",
					"member_rank":"全部",
					"tags":"全部",
					"source":"推广扫码",
					"pay_money_start":"",
					"pay_money_end":"",
					"pay_times_start":"",
					"pay_times_end":"",
					"last_buy_start_time":"",
					"last_buy_end_time":"",
					"integral_start":"",
					"integral_end":"",
					"massage_start_time":"",
					"massage_end_time":""
				}]
				"""
			Then jobs获得刷选结果人数
				"""
				[{
					"result_quantity":2
				}]
				"""
			Then jobs可以获得会员列表
				| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
				| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 推广扫码 |             |
				| tom2  | 普通会员    |       0      |     50   |   325.00  |    162.50  |    2      | 2014-8-5 00:00:00 | 推广扫码 | 分组1       |

		#会员分享
			When jobs设置会员查询条件
				"""
				[{
					"name":"",
					"status":"全部",
					"attention_start_time":"",
					"attention_end_time":"",
					"member_rank":"全部",
					"tags":"全部",
					"source":"会员分享",
					"pay_money_start":"",
					"pay_money_end":"",
					"pay_times_start":"",
					"pay_times_end":"",
					"last_buy_start_time":"",
					"last_buy_end_time":"",
					"integral_start":"",
					"integral_end":"",
					"massage_start_time":"",
					"massage_end_time":""
				}]
				"""
			Then jobs获得刷选结果人数
				"""
				[{
					"result_quantity":5
				}]
				"""
			Then jobs可以获得会员列表
				| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
				| bill3 | 普通会员    |       1      |     0    |   0.00    |    0.00    |     0     |        今天       | 会员分享 |             |
				| bill  | 普通会员    |       1      |     0    |   0.00    |    0.00    |     0     |        今天       | 会员分享 |             |
				| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |     0     | 2014-8-6 00:00:00 | 会员分享 | 分组3       |
				| tom4  | 金牌会员    |       0      |     20   |   0.00    |    0.00    |     0     | 2014-8-5 23:59:59 | 会员分享 | 分组3       |
				| tom3  | 银牌会员    |       1      |    100   |   335.00  |    111.67  |     3     | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |

Scenario:8 过滤条件"消费总额"

	#区间查询，包含开始和结束数值
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"110",
				"pay_money_end":"335",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
			| tom3  | 银牌会员    |       1      |    100   |   335.00  |   111.67   |     3     | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |   162.50   |     2     | 2014-8-5 00:00:00 | 推广扫码 | 分组1       |
			| tom1  | 银牌会员    |       2      |     0    |   110.00  |   110.00   |     1     | 2014-8-4 23:59:59 | 直接关注 | 分组1       |

	#开始结束数值相同
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"110",
				"pay_money_end":"110",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| tom1  | 银牌会员    |       2      |     0    |   110.00  |   110.00   |     1     | 2014-8-4 23:59:59 | 直接关注 | 分组1   |

	#特殊数据查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"0",
				"pay_money_end":"10",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":10
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| bill3 | 普通会员    |       1      |     0    |   0.00    |    0.00    |     0     |        今天       | 会员分享 |         |
			| bill2 | 普通会员    |       1      |     0    |   0.00    |    0.00    |     0     |        今天       | 直接关注 |         |
			| bill  | 普通会员    |       1      |     0    |   0.00    |    0.00    |     0     |        今天       | 会员分享 |         |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |     0     | 2014-10-1 8:00:00 | 直接关注 |         |
			| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |     0     | 2014-10-1 8:00:00 | 推广扫码 |         |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |     0     | 2014-8-6 00:00:00 | 会员分享 | 分组3   |
			| tom4  | 金牌会员    |       0      |     20   |   0.00    |    0.00    |     0     | 2014-8-5 23:59:59 | 会员分享 | 分组3   |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"-10",
				"pay_money_end":"-1",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表"没有符合要求的数据"

Scenario:9 过滤条件"购买次数"

	#区间查询，包含开始和结束数值
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"1",
				"pay_times_end":"3",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
			| tom3  | 银牌会员    |       1      |    100   |   335.00  |   111.67   |     3     | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |   162.50   |     2     | 2014-8-5 00:00:00 | 推广扫码 | 分组1       |
			| tom1  | 银牌会员    |       2      |     0    |   110.00  |   110.00   |     1     | 2014-8-4 23:59:59 | 直接关注 | 分组1       |

	#开始结束数值相同
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"2",
				"pay_times_end":"2",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |   162.50   |     2     | 2014-8-5 00:00:00 | 推广扫码 | 分组1   |

	#特殊数据查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"-2.2",
				"pay_times_end":"2.3",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |   162.50   |     2     | 2014-8-5 00:00:00 | 推广扫码 | 分组1   |
			| tom1  | 银牌会员    |       2      |     0    |   110.00  |   110.00   |     1     | 2014-8-4 23:59:59 | 直接关注 | 分组1   |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"4",
				"pay_times_end":"10.6",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表"没有符合要求的数据"

Scenario:10 过滤条件"最后购买时间"

	#区间时间边界值查询，不包含结束时间
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"2015-1-1 00:00:00",
				"last_buy_end_time":"2015-3-5 00:00:00",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |   162.50   |     2     | 2014-8-5 00:00:00 | 推广扫码 | 分组1   |
			| tom1  | 银牌会员    |       2      |     0    |   110.00  |   110.00   |     1     | 2014-8-4 23:59:59 | 直接关注 | 分组1   |

	#开始结束时间相同查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"2015-2-2 00:00:00",
				"last_buy_end_time":"2015-2-2 00:00:00",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |   162.50   |     2     | 2014-8-5 00:00:00 | 推广扫码 | 分组1   |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"2015-8-11 00:00:00",
				"last_buy_end_time":"2015-8-12 00:00:00",
				"integral_start":"",
				"integral_end":"",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表"没有符合要求的数据"

Scenario:11 过滤条件"积分范围"

	#区间查询，包含开始和结束数值
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"20",
				"integral_end":"100",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
			| tom4  | 金牌会员    |       0      |     20   |   0.00    |    0.00    |     0     | 2014-8-5 23:59:59 | 会员分享 | 分组3       |
			| tom3  | 银牌会员    |       1      |    100   |   335.00  |    111.67  |     3     | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |    162.50  |     2     | 2014-8-5 00:00:00 | 推广扫码 | 分组1       |

	#开始结束数值相同
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"0",
				"integral_end":"0",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":7
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| bill3 | 普通会员    |       1      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 |         |
			| bill2 | 普通会员    |       1      |     0    |   0.00    |    0.00    |      0    |        今天       | 直接关注 |         |
			| bill  | 普通会员    |       1      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 |         |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |      0    | 2014-10-1 8:00:00 | 直接关注 |         |
			| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |      0    | 2014-10-1 8:00:00 | 推广扫码 |         |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |      0    | 2014-8-6 00:00:00 | 会员分享 | 分组3   |
			| tom1  | 银牌会员    |       2      |     0    |   110.00  |    110.00  |      1    | 2014-8-4 23:59:59 | 直接关注 | 分组1   |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部",
				"attention_start_time":"",
				"attention_end_time":"",
				"member_rank":"全部",
				"tags":"全部 ",
				"source":"全部",
				"pay_money_start":"",
				"pay_money_end":"",
				"pay_times_start":"",
				"pay_times_end":"",
				"last_buy_start_time":"",
				"last_buy_end_time":"",
				"integral_start":"150",
				"integral_end":"300",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表"没有符合要求的数据"

Scenario:12 过滤条件"最后对话时间"

	#无法在feature中模拟到准确的对话时间，不能实现此场景

Scenario:13 过滤条件"条件组合查询"

	#空调条件查询，“重置”查询条件，空调间查询所有数据
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"已关注",
				"attention_start_time":"2014-8-3 00:00:00",
				"attention_end_time":"今天",
				"member_rank":"银牌会员",
				"tags":"分组1 ",
				"source":"推广扫码",
				"pay_money_start":"100",
				"pay_money_end":"325",
				"pay_times_start":"0",
				"pay_times_end":"2",
				"last_buy_start_time":"2015-1-1",
				"last_buy_end_time":"2015-2-2",
				"integral_start":"0",
				"integral_end":"50",
				"massage_start_time":"",
				"massage_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |  tags   |
			| tom2  | 普通会员    |       0      |     50   |   325.00  |   162.50   |     2     | 2014-8-5 00:00:00 | 推广扫码 | 分组1   |

Scenario:14 会员列表分页

	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

		When jobs访问会员列表

		Then jobs获取会员列表显示共3页

		When jobs浏览第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  |  source  |    tags     |
			| bill3 |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 |             |
			| bill2 |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |        今天       | 直接关注 |             |
			| bill  |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 |             |

		When jobs浏览下一页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 直接关注 |             |
			| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 推广扫码 |             |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-8-6 00:00:00 | 会员分享 | 分组3       |

		When jobs浏览第3页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
			| tom3  | 银牌会员    |       1      |    100   |   335.00  |    111.67  |    3      | 2014-8-5 8:00:00  | 会员分享 | 分组1,分组3 |
			| tom1  | 银牌会员    |       2      |     0    |   110.00  |    110.00  |    1      | 2014-8-4 23:59:59 | 直接关注 | 分组1       |

		When jobs浏览上一页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  | source   |    tags     |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 直接关注 |             |
			| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-10-1 8:00:00 | 推广扫码 |             |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      | 2014-8-6 00:00:00 | 会员分享 | 分组3       |



>>>>>>> a3ba4faffbf9c067a718ed4208aa63b2348feab4
