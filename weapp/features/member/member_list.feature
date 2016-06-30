#author: 崔帅帅
#author: 王丽
#editor: 张三香 2015.10.16
#editor: 冯雪静 2016.03.29
#editor: 田丰敏 2016.05.31

Feature: 微信用户关注公众号成为系统会员
"""
	# __author__ : "王丽"
	2015-9新增需求
	1、会员分组默认有个分组："未分组"，不能修改（没有修改框）、不能删除（没有删除按钮）
	2、新增会员和调整没有分组的会员，默认进入"未分组"
	2016-3新增需求
	1、会员列表新增字段“30天内购买频次”
"""

Background:
	Given 添加jobs店铺名称为'jobs商家'
	Given jobs登录系统
	And 开启手动清除cookie模式
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
			"upgrade": "手动升级",
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
	And jobs已添加商品
		"""
		[{
			"name":"商品1",
			"price":100.00
		}]
		"""
	When jobs添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345",
			"weixin_partner_id": "22345",
			"weixin_partner_key": "32345",
			"weixin_sign": "42345"
		},{
			"type": "支付宝",
			"description": "我的支付宝支付",
			"is_active": "启用"
		}]
		"""

@mall2 @member @memberList   @crm
Scenario:1 微信用户关注公众号成为会员
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
			"fans_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": ["未分组"],
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
	When bill获得db中在jobs公众号中的mt为'mt_{bill_jobs}'

	When 清空浏览器
	When tom点击bill分享链接
	Then tom在jobs公众号中有uuid对应的webapp_user
	Then 浏览器cookie包含"[fmt, uuid]"
	Then 浏览器cookie等于
		"""
		{"fmt":"mt_{bill_jobs}"}
		"""
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
			"fans_count": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"fans_count": 1,
			"pay_times": 0,
			"source": "直接关注",
			"tags": ["未分组"],
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

	When 清空浏览器
	When nokia点击bill分享链接
	Then nokia在jobs公众号中有uuid对应的webapp_user
	Then 浏览器cookie包含"[fmt, uuid]"
	Then 浏览器cookie等于
		"""
		{"fmt":"mt_{bill_jobs}"}
		"""
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
			"fans_count": 0,
			"pay_times": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"fans_count": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"fans_count": 2,
			"pay_times": 0,
			"source": "直接关注",
			"tags": ["未分组"],
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
	#tom把jobs的微站二维码推广给tom1
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
			"fans_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"fans_count": 0,
			"pay_times": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"fans_count": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"fans_count": 2,
			"pay_times": 0,
			"source": "直接关注",
			"tags": ["未分组"],
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
	When bill使用支付方式'货到付款'进行支付
	Given jobs登录系统
	When jobs对最新订单进行发货
	When jobs'完成'最新订单
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"fans_count": 0,
			"pay_times": 0,
			"source": "直接关注",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"fans_count": 0,
			"pay_times": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"fans_count": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 100.00,
			"unit_price": 100.00,
			"integral": 20,
			"fans_count": 2,
			"pay_times": 1,
			"source": "直接关注",
			"tags": ["未分组"],
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
	When tom1使用支付方式'货到付款'进行支付
	Given jobs登录系统
	When jobs对最新订单进行发货
	When jobs'完成'最新订单
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "普通会员",
			"pay_money": 100.00,
			"unit_price": 100.00,
			"integral": 20,
			"fans_count": 0,
			"pay_times": 1,
			"source": "直接关注",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"fans_count": 0,
			"pay_times": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"fans_count": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "bill",
			"member_rank": "普通会员",
			"pay_money": 100.00,
			"unit_price": 100.00,
			"integral": 20,
			"fans_count": 2,
			"pay_times": 1,
			"source": "直接关注",
			"tags": ["未分组"],
			"status": "已关注"
		}]
		"""

	When bill取消关注jobs的公众号
	Given jobs登录系统
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom1",
			"member_rank": "普通会员",
			"pay_money": 100.00,
			"unit_price": 100.00,
			"integral": 20,
			"fans_count": 0,
			"pay_times": 1,
			"source": "直接关注",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "nokia",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"integral": 20,
			"fans_count": 0,
			"pay_times": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		},{
			"name": "tom",
			"member_rank": "普通会员",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0,
			"integral": 20,
			"fans_count": 0,
			"source": "会员分享",
			"tags": ["未分组"],
			"status": "已关注"
		}]
		"""


Scenario:2 会员列表
	1.会员列表新增"30天内购买频次"

	When bill关注jobs的公众号于'2015-5-1'
	When nokia关注jobs的公众号于'2015-5-1'
	When tom关注jobs的公众号于'2015-5-1'
	When tom1关注jobs的公众号于'2015-5-1'
	When tom2关注jobs的公众号于'2015-5-1'
	When tom3关注jobs的公众号于'2015-5-1'
	When tom2取消关注jobs的公众号


	When 微信用户批量消费jobs的商品
		| order_id |  date  | consumer | product | payment | pay_type | postage*| price* | paid_amount*| alipay*| wechat*| cash* |    action    | order_status*|
		|   0001   | 30天前 | bill     | 商品1,1 | 支付    | 支付宝   |  0.00   |  100.00| 100.00      | 100.00 | 0.00   | 0.00  | jobs,完成    | 已完成       |
		|   0002   | 30天前 | tom      | 商品1,1 | 支付    | 货到付款 |  0.00   |  100.00| 100.00      | 0.00   | 0.00   | 100.00| jobs,完成    | 已完成       |
		|   0003   | 30天前 | nokia    | 商品1,1 | 支付    | 支付宝   |  0.00   |  100.00| 100.00      | 100.00 | 0.00   | 0.00  | jobs,取消    | 已取消       |
		|   0004   | 30天前 | tom1     | 商品1,1 | 支付    | 微信支付 |  0.00   |  100.00| 100.00      | 0.00   | 100.00 | 0.00  | jobs,完成    | 已完成       |
		|   0005   | 29天前 | bill     | 商品1,1 | 支付    | 微信支付 |  0.00   |  100.00| 100.00      | 0.00   | 100.00 | 0.00  | jobs,完成    | 已完成       |
		|   0006   | 29天前 | tom      | 商品1,1 |         | 微信支付 |  0.00   |  100.00| 100.00      | 0.00   | 0.00   | 0.00  |              | 待支付       |
		|   0007   | 29天前 | nokia    | 商品1,1 | 支付    | 支付宝   |  0.00   |  100.00| 100.00      | 100.00 | 0.00   | 0.00  | jobs,完成退款| 退款成功     |
		|   0008   | 29天前 | tom1     | 商品1,1 | 支付    | 支付宝   |  0.00   |  100.00| 100.00      | 100.00 | 0.00   | 0.00  | jobs,发货    | 已发货       |
		|   0009   | 今天   | bill     | 商品1,1 | 支付    | 货到付款 |  0.00   |  100.00| 100.00      | 0.00   | 0.00   | 100.00| jobs,完成    | 已完成       |
		|   0010   | 今天   | tom      | 商品1,1 | 支付    | 微信支付 |  0.00   |  100.00| 100.00      | 0.00   | 100.00 | 0.00  |              | 待发货       |
		|   0011   | 今天   | nokia    | 商品1,1 | 支付    | 微信支付 |  0.00   |  100.00| 100.00      | 0.00   | 100.00 | 0.00  | jobs,退款    | 退款中       |
		|   0012   | 今天   | tom1     | 商品1,1 | 支付    | 支付宝   |  0.00   |  100.00| 100.00      | 100.00 | 0.00   | 0.00  | jobs,完成    | 已完成       |

	Given jobs登录系统
	Then jobs可以获得会员列表
		|  member  | member_rank |  fans_count |  integral  | pay_money | unit_price | pay_times | 30days_pay_times |  Source  | attention_time |  tags  | status |
		|  tom3    | 普通会员    |    0         |     20     |    0.00   |     0.00   |    0      |         0        | 直接关注 |    2015-5-1    | 未分组 | 已关注 |
		|  tom2    | 普通会员    |    0         |     20     |    0.00   |     0.00   |    0      |         0        | 直接关注 |    2015-5-1    | 未分组 | 已取消 |
		|  tom1    | 普通会员    |    0         |     20     |   200.00  |    100.00  |    2      |         1        | 直接关注 |    2015-5-1    | 未分组 | 已关注 |
		|  tom     | 普通会员    |    0         |     20     |   100.00  |    100.00  |    1      |         0        | 直接关注 |    2015-5-1    | 未分组 | 已取消 |
		|  nokia   | 普通会员    |    0         |     20     |    0.00   |     0.00   |    0      |         0        | 直接关注 |    2015-5-1    | 未分组 | 已取消 |
		|  bill    | 普通会员    |    0         |     20     |   300.00  |    100.00  |    3      |         2        | 直接关注 |    2015-5-1    | 未分组 | 已取消 |

	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs访问会员列表页
	Then jobs获得会员列表显示共3页
	When jobs浏览会员列表第1页
	Then jobs可以获得会员列表
		|  member  | member_rank |  fans_count |  integral  | pay_money | unit_price | pay_times | 30days_pay_times |  Source  | attention_time |  tags  | status |
		|  tom3    | 普通会员    |    0         |     20     |    0.00   |     0.00   |    0      |         0        | 直接关注 |    2015-5-1    | 未分组 | 已关注 |
		|  tom2    | 普通会员    |    0         |     20     |    0.00   |     0.00   |    0      |         0        | 直接关注 |    2015-5-1    | 未分组 | 已取消 |

#补充:张三香 2016.06.29
#针对bug补充-（功能问题）自营平台-后台订单列表中的购买次数和30天内购买频次显示不正常

@member @memberList @mall2
Scenario:3 自营平台，查看会员列表中的购买次数
	#备注-30天内购买次数无法实现steps（这个是执行的脚本）

	Given 设置nokia为自营平台账号
	Given nokia登录系统
	And nokia已添加供货商
		"""
		[{
			"name": "供货商1",
			"responsible_person": "宝宝",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": "备注卖花生油"
		}, {
			"name": "供货商2",
			"responsible_person": "陌陌",
			"supplier_tel": "13811223344",
			"supplier_address": "北京市海淀区泰兴大厦",
			"remark": ""
		}]
		"""
	And nokia已添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	When nokia开通使用微众卡权限
	When nokia添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"is_active": "启用"
		}]
		"""
	And nokia已添加商品
		"""
		[{
			"supplier": "供货商1",
			"name": "商品1a",
			"price": 10.00,
			"purchase_price": 9.00,
			"weight": 1.0,
			"stock_type": "无限",
			"pay_interfaces":[{
				"type": "货到付款"
			}]
		}, {
			"supplier": "供货商1",
			"name": "商品1b",
			"price": 20.00,
			"purchase_price": 19.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 10,
			"pay_interfaces":[{
				"type": "货到付款"
			}]
		}, {
			"supplier": "供货商2",
			"name": "商品2a",
			"price": 20.00,
			"purchase_price": 19.00,
			"weight": 1.0,
			"stock_type": "有限",
			"stocks": 10,
			"pay_interfaces":[{
				"type": "货到付款"
			}]
		}]
		"""
	When nokia将商品'商品1'放入待售于'2015-08-02 10:30'
	When nokia更新商品'商品1'
		"""
		{
			"name":"商品1",
			"supplier":"jobs商家",
			"purchase_price": 99.00,
			"is_member_product":"off",
			"pay_interfaces":[{
				"type": "货到付款"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"user_code":"0102",
						"weight":1.0,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	When nokia'上架'商品'商品1'

	#bill的购买数据
	When bill关注nokia的公众号
	When bill访问nokia的webapp
	#001-单个自建供货商商品
		When bill购买nokia的商品
			"""
			{
				"order_id":"001",
				"pay_type":"货到付款",
				"products":[{
					"name":"商品1a",
					"count":1
				}]
			}
			"""
		Given nokia登录系统
		When nokia对订单进行发货
			"""
			{
				"order_no":"001-供货商1",
				"logistics":"off",
				"shipper": ""
			}
			"""
		When nokia'完成'订单'001-供货商1'
	#002-多个自建供货商的商品
		When bill访问nokia的webapp
		When bill购买nokia的商品
			"""
			{
				"order_id":"002",
				"pay_type":"货到付款",
				"products":[{
					"name":"商品1a",
					"count":1
				},{
					"name":"商品2a",
					"count":1
				}]
			}
			"""
		Given nokia登录系统
		When nokia对订单进行发货
			"""
			{
				"order_no":"002-供货商1",
				"logistics":"off",
				"shipper": ""
			}
			"""
		When nokia对订单进行发货
			"""
			{
				"order_no":"002-供货商2",
				"logistics":"off",
				"shipper": ""
			}
			"""
		When nokia'完成'订单'002-供货商1'
		When nokia'完成'订单'002-供货商2'
	#003-单个同步供货商的商品
		When bill访问nokia的webapp
		When bill购买nokia的商品
			"""
			{
				"order_id":"003",
				"pay_type":"货到付款",
				"products":[{
					"name":"商品1",
					"count":1
				}]
			}
			"""
		Given nokia登录系统
		When nokia对订单进行发货
			"""
			{
				"order_no":"003",
				"logistics":"off",
				"shipper": ""
			}
			"""
		When nokia'完成'订单'003'
	#004-同步和自建供货商的商品
		When bill访问nokia的webapp
		When bill购买nokia的商品
			"""
			{
				"order_id":"004",
				"pay_type":"货到付款",
				"products":[{
					"name":"商品1",
					"count":1
				},{
					"name":"商品1a",
					"count":1
				}]
			}
			"""
		Given nokia登录系统
		When nokia对订单进行发货
			"""
			{
				"order_no":"004-jobs商家",
				"logistics":"off",
				"shipper": ""
			}

			"""
		When nokia对订单进行发货
			"""
			{
				"order_no":"004-供货商1",
				"logistics":"off",
				"shipper": ""
			}
			"""
		When nokia'完成'订单'004-jobs商家'
		When nokia'完成'订单'004-供货商1'

	Given nokia登录系统
	Then nokia可以获得会员列表
		|  member  | member_rank |pay_times |
		|  bill    | 普通会员    |    4     |
