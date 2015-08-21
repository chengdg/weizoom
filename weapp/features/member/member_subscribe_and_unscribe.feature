# __author__ : "崔帅帅"

Feature: 微信用户关注公众号成为系统会员

Background:
	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"be_member_increase_count": 20
		}
		"""
	And jobs添加会员等级
		"""
		[{
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "1"
		},{
			"name": "金牌会员",
			"upgrade": "自动升级",
			"shop_discount": "9.8"
		}]
		"""
	And jobs添加会员分组
		"""
		[{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2",
			"tag_id_3": "分组3"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"price":100.00
		}]
		"""
	And jobs已添加了支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		}]
		"""
@crm @member @eugeneX
Scenario: 微信用户关注公众号成为会员
	微信用户关注jobs公众号成为jobs的会员
	1.bill直接关注jobs的公众号,生成会员列表
	2.tom通过bill分享的链接关注jobs的公众号,生成会员列表
	3.nokia通过bill分享的链接关注jobs的公众号,生成会员列表
	4.tom1通过tom推荐扫码关注jobs的公众号,生成会员列表

	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	Given jobs登录系统
	Then jobs可以获得会员列表
		"""
		[{
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		}]
		"""
	And jobs能获得bill的积分日志
		"""
		[{
			"content": "首次关注",
			"integral": 20
		}]
		"""
	#When bill把jobs的微站链接分享到朋友圈
	When bill把jobs的商品"商品1"的链接分享到朋友圈
	When tom点击bill分享链接
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom获得jobs的20会员积分
	Then tom在jobs的webapp中拥有20会员积分
	Given jobs登录系统
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"friend_count": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		}]
		"""
	And jobs能获得tom的积分日志
		"""
		[{
			"content": "首次关注",
			"integral": 20
		}]
		"""
	When nokia点击bill分享链接
	When nokia关注jobs的公众号
	When nokia访问jobs的webapp
	When nokia获得jobs的20会员积分
	Then nokia在jobs的webapp中拥有20会员积分
	Given jobs登录系统
	Then jobs可以获得会员列表
		"""
		[{
			"name": "nokia",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"friend_count": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		}]
		"""
	And jobs能获得nokia的积分日志
		"""
		[{
			"content": "首次关注",
			"integral": 20
		}]
		"""
	#When tom把jobs的微站二维码推广给tom1
	When tom访问jobs的webapp
	#When tom把jobs的二维码推广给tom1
	When tom1关注jobs的公众号
	When tom1访问jobs的webapp
	When tom1获得jobs的20会员积分
	Then tom1在jobs的webapp中拥有20会员积分
	Given jobs登录系统
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"friend_count": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		}]
		"""
	And jobs能获得tom1的积分日志
		"""
		[{
			"content": "首次关注",
			"integral": 20
		}]
		"""


	When bill访问jobs的webapp
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	When jobs"完成"最新订单
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"friend_count": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "金牌会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		}]
		"""
	When tom1访问jobs的webapp
	When tom1购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	Given jobs登录系统
	When jobs"完成"最新订单
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "金牌会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"friend_count": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "金牌会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		}]
		"""

	When bill取消关注jobs的公众号
	Given jobs登录系统
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "金牌会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"friend_count": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已关注"
		},{
			"name": "",
			"member_rank": "金牌会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"friend_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": [],
			"status": "已取消"
		}]
		"""
