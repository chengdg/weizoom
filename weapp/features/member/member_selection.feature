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
