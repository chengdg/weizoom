#_author_:王丽

Feature: 会员分析-会员概况-会员详细数据

	对店铺的会员进行不同维度的分析

	说明：1）整个会员的统计只统计真实会员，没有注册直接下单的不统计
		2）新增会员，都是只的真正的新增会员，不包含之前关注，后来取消关注，现在又关注的会员

	一、查询条件

		1、刷选日期
			1）开始日期和结束日期都为空；选择开始结束日期，精确到日期
			2）开始日期或者结束日期，只有一个为空，给出系统提示“请填写XX日期”
			3）默认为‘今天’，筛选日期：‘今天’到‘今天’
			4）包含筛选日期的开始和结束的边界值
			5）手工设置筛选日期，点击查询后，‘快速查询’的所有项都处于‘未选中状态’

		2、快速查看
		    1）今天：查询的当前日期，例如，今天是2015-6-16，筛选日期是：2015-6-16到2015-6-16
		    2）昨天：查询的前一天，例如，今天是2015-6-16，筛选日期是：2015-6-15到2015-6-15
			3）最近7天；包含今天，向前7天；例如，今天是2015-6-16，筛选日期是：2015-6-10到2015-6-16
			4）最近30天；包含今天，向前30天；例如，今天是2015-6-16，筛选日期是：2015-5-19到2015-6-16
			5）最近90天；包含今天，向前90天；例如，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
			6）全部：筛选日期更新到：2013.1.1到今天

	二、详细数据

		按天列出在查询区间内，系统中会员的状况，按日期倒序排列，分页显示，每页10条数据

		1、【日期】：查询区间，按天拆分罗列

		2、【新增会员】：∑会员.个数[(会员.加入时间 in 对应日期当天)]

			备注：对应的【日期】当天新增会员数


			例如：筛选日期：2015-5-1到2015-5-22
					2015-5-10的【新增会员】=∑会员.个数[(2015-5-10 00:00 <= 会员.加入时间 < 2015-5-11 00:00) and (2015-5-1 00:00 <= 会员.加入时间 < 2015-5-23 00:00)]
					其他日期点的【新增会员】依次类推

		3、【手机绑定】：

		4、【发起分享链接】：对应的【日期】当天发起‘有效分享链接’的会员数

			‘有效分享链接’：发起分享链接的并且此链接被第一次点击的时间在查询区间

		5、【分享链接新增】：∑会员.个数[(会员.加入时间 in 对应日期当天) and (会员.来源 = ‘会员分享’)]

			备注：对应的【日期】当天通过分享链接新增的会员数

		6、【发起扫码】：对应的【日期】当天发起‘有效扫码’的会员数

			‘有效扫码’：发起推广扫码，即已经生成了二维码

		7、【扫码新增】：∑会员.个数[(会员.加入时间 in 对应日期当天) and (会员.来源 = ‘推广扫码’)]

			备注：对应的【日期】当天通过推广扫码新增的会员数

Background:
	Given jobs登录系统

	Given 开启手动清除cookie模式

	When jobs添加商品
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}, {
			"name": "商品3"
		}]	
		"""

	And jobs设置未付款订单过期时间
		"""
		{
			"一元等价的积分数量": 10
		}
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
			"type": "支付宝支付",
			"is_active": "启用"
		}]
		"""

	And jobs已添加微众支付
		"""
		[{
			"is_weizoom_pay":"是"
		}]
		"""

	And jobs设置积分策略
		"""
		[{ 
			"integral_each_yuan": 10
		}]
		"""

	And jobs已添加积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "2014-8-1",
			"end_date": "10天后",
			"products": ["商品1"],
			"is_permanant_active": false,
			"rules": [{
				"member_grade_name": "全部会员",
				"discount": 70,
				"discount_money": 70.0
			}]
		}]
		"""

	And toms已添加优惠券
		"""
		[{
			"name": "商品2优惠券",
			"money": 10,
			"start_date": "2014-8-1",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""

	##微信用户批量关注jobs成为会员

	When bill关注jobs的公众号于'两天前'

	When mary关注jobs的公众号于'一天前'
	When mary访问jobs的webapp
	When mary把jobs的微站链接分享到朋友圈

	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom把jobs的微站链接分享到朋友圈

	When bill1关注jobs的公众号
	When bill1取消关注jobs的公众号

	When 清空浏览器
	When bill1通过tom分享链接关注jobs的公众号
	When bill1访问jobs的webapp

	When 清空浏览器
	When tom1通过tom分享链接关注jobs的公众号
	When tom1访问jobs的webapp

	When 清空浏览器
	When jack点击mary分享链接
	When jack把jobs的微站链接分享到朋友圈
	"""
	When 微信用户批量关注jobs成为会员
		|  memberID   |  name  | launch_spreading_code | launch_share_link |   direct_attention   | spreading_code_attention |          share_link_attention      |   attention_time  |    entry_time     |       current_status         | member_source |
		| memberID000 |  mary  |         是            |        是         | 直接搜索jobs公众账号 |                          |                                    |   2015-4-3 10:50  |   2015-4-3 10:50  |             关注             |    直接关注   |
		| memberID001 |  bill  |         是            |                   | 直接搜索jobs公众账号 |                          |                                    |   2015-5-1 10:50  |   2015-5-1 10:50  |             关注             |    直接关注   |
		| memberID002 |  tom   |                       |        是         | 直接搜索jobs公众账号 |                          |                                    |   2015-5-2 10:50  |   2015-5-2 10:50  |2015-6-2 11:20取消关注；已取消|    直接关注   |
		| memberID003 | bill1  |                       |                   |                      |           bill           |                                    |   2015-5-3 11:20  |   2015-5-3 11:20  |2015-5-4 11:20取消关注； 关注 |    推广扫码   |
		| memberID003 | bill1  |                       |                   |                      |                          |         tom                        |   2015-5-4 13:00  |   2015-5-3 11:20  |             关注             |    推广扫码   |
		| memberID004 |  tom1  |                       |                   |                      |                          |         tom                        |   2015-5-5 14:00  |   2015-5-5 14:00  |             关注             |    会员分享   |
		| memberID005 |  tom1  |         是            |                   |                      |           bill           |                                    |   2015-5-6 15:00  |   2015-5-6 15:00  |2015-5-7 8:00 取消关注，已取消|    推广扫码   |
		| memberID000 |  mary  |         是            |        是         | 直接搜索jobs公众账号 |                          |                                    |   2015-5-7 10:50  |   2015-4-3 10:50  |2015-5-7 8:00取消关注；关注   |    推广扫码   |
		| memberID006 |  jack  |         是            |        是         |                      |                          |         mary                       |   2015-5-9 9:30   |   2015-5-9 9:30   |             关注             |    会员分享   |
		|             |  jack1 |                       |                   |                      |    扫码jack未关注jobs    |                                    |                   |                   |                              |               |
		|             |  jack2 |                       |                   |                      |                          | 2015-5-9 9:30点击jack链接未关注jobs|                   |                   |                              |               |
		| memberID007 |  jack3 |                       |                   |                      |           jack           |                                    |   2015-6-3 10:00  |   2015-6-3 10:00  |2015-6-3 13:00取消关注；已取消|    推广扫码   |
		| memberID008 |  nokia |                       |                   | 直接搜索jobs公众账号 |                          |                                    |   2015-6-1 00:00  |   2015-6-1 00:00  |             关注             |    直接关注   |
	"""
	When 微信用户批量消费jobs的商品
		|       date     	| consumer |businessman|      product     | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action       |  order_status   |
		| 一天前  10:20   	| mary     | jobs      | 商品1,1          | 支付    |   微信支付     | 10      | 100      | 10       | 0      | 100         | 0            | 0      |   100  | 0    |   jobs发货，完成  |    已完成       |
		| 两天前  8:00     	| bill     | jobs      | 商品1,1          |         |   支付宝       | 10      | 100      |  0       | 0      |  0          | 0            | 0      |    0   | 0    |   系统化自动取消  |    已取消       |
		| 今天    10:00   	| tom      | jobs      | 商品2,1          | 支付    |   微信支付     | 15      | 100      |  0       | 0      | 115         | 0            | 0      |    115 | 0    |   jobs发货，完成  |    已完成       |
		| 两天前  9:00    	| bill     | jobs      | 商品1,1          | 支付    |   货到付款     | 10      | 100      |  0       | 30     | 80          | 0            | 0      |    0   | 80   |                   |    待发货       |
		| 今天    9:00    	| tom      | jobs      | 商品1,1          | 支付    |   货到付款     | 10      | 100      |  20      | 0      | 90          | 0            | 0      |    0   | 90   |   jobs发货        |    已发货       |
		| 今天    10:00   	| tom1     | jobs      | 商品1,1          | 支付    |   支付宝       | 10      | 100      |  0       | 0      | 110         | 0            | 110    |    0   | 0    |   jobs发货，完成  |    已完成       |
		| 今天    10:00   	| tom1     | jobs      | 商品2,1          | 支付    |   微信支付     | 15      | 100      |  0       | 0      | 115         | 0            | 0      |   115  | 0    |   jobs发货        |    已发货       |
		| 一天前  13:20   	| mary     | jobs      | 商品2,2          | 支付    |   支付宝       | 15      | 100      |  0       | 20     | 195         | 0            | 195    |    0   | 0    |   jobs发货        |    已发货       |

Scenario: 1  会员概况：会员详细数据

	When jobs设置筛选日期
		"""
		[{
			"begin_date":"今天",
			"end_date":"今天"
		}]
		"""

	Then job获得会员详细数据
		|    date    |  new_member  | mobile_phone_member | launch_share_link_member | share_link_new_member | launch_spreading_code_member | spreading_code_new_member | order_member |
		|    今天    |      3       |          0          |            2             |           1           |               0              |              0            |       2      |
		|   一天前   |      1       |          0          |            0             |           0           |               0              |              0            |       1      |
		|   两天前   |      1       |          0          |            0             |           0           |               0              |              0            |       1      |


Scenario: 2  会员概况：会员详细数据分页

	When jobs设置筛选日期
		"""
		[{
			"begin_date":"两天前",
			"end_date":"今天"
		}]
		"""

	When jobs已设置分页条件
		"""
		{
			"page_count":1
		}
		"""

	Then jobs获得会员详细数据显示共3页

	When jobs浏览第一页

	Then jobs获得会员详细数据
		|    date    |  new_member  | mobile_phone_member | launch_share_link_member | share_link_new_member | launch_spreading_code_member | spreading_code_new_member | order_member |
		|    今天    |      3       |          0          |            2             |           1           |               0              |              0            |       2      |

	When jobs浏览'下一页'

	Then jobs获得会员详细数据
		|    date    |  new_member  | mobile_phone_member | launch_share_link_member | share_link_new_member | launch_spreading_code_member | spreading_code_new_member | order_member |
		|   一天前   |      1       |          0          |            0             |           0           |               0              |              0            |       1      |

	When jobs浏览'第3页'

	Then jobs获得会员详细数据
		|    date    |  new_member  | mobile_phone_member | launch_share_link_member | share_link_new_member | launch_spreading_code_member | spreading_code_new_member | order_member |
		|   两天前   |      1       |          0          |            0             |           0           |               0              |              0            |       1      |

	When jobs浏览'上一页'
	
	Then jobs获得会员详细数据	
		|    date    |  new_member  | mobile_phone_member | launch_share_link_member | share_link_new_member | launch_spreading_code_member | spreading_code_new_member | order_member |
		|   一天前   |      1       |          0          |            0             |           0           |               0              |              0            |       1      |