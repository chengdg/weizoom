#_author_:王丽

Feature: 会员分析-会员概况-会员详细数据
"""
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

		3、【手机绑定】：对应的【日期】当天新增‘手机绑定’的会员数

		4、【发起分享链接】：对应的【日期】当天发起‘有效分享链接’的会员数

			‘有效分享链接’：发起分享链接的并且此链接被第一次点击的时间在查询区间

		5、【分享链接新增】：∑会员.个数[(会员.加入时间 in 对应日期当天) and (会员.来源 = ‘会员分享’)]

			备注：对应的【日期】当天通过分享链接新增的会员数

		6、【发起扫码】：对应的【日期】当天发起‘有效扫码’的会员数

			‘有效扫码’：发起推广扫码，即已经生成了二维码

		7、【扫码新增】：∑会员.个数[(会员.加入时间 in 对应日期当天) and (会员.来源 = ‘推广扫码’)]

			备注：对应的【日期】当天通过推广扫码新增的会员数
"""

Background:
	Given jobs登录系统
	And 开启手动清除cookie模式

	When jobs已添加支付方式
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
		}, {
			"type": "支付宝",
			"description": "我的支付宝",
			"is_active": "启用",
			"partner": "11",
			"key": "21",
			"ali_public_key": "31",
			"private_key": "41",
			"seller_email": "a@a.com"
		}]
		"""
	When jobs开通使用微众卡权限
	When jobs添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
		"""

	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}, {
			"name" : "圆通",
			"first_weight":1,
			"first_weight_price":10.00
		}]
		"""
	And jobs选择'顺丰'运费配置
	
	When jobs已添加商品
		"""
		[{
			"name": "商品1",
			"categories": "",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"introduction": "商品1的简介",
			"detail": "商品1的详情",
			"shelve_type": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 11.0,
						"weight": 5,
						"stock_type": "无限"
					}
				}
			},
			"postage": "顺丰"
		}, {
			"name": "商品2",
			"categories": "",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"introduction": "商品2的简介",
			"detail": "商品2的详情",
			"shelve_type": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5,
						"stock_type": "无限",
						"stocks": 3
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			}],
			"postage": 10.0
		}, {
			"name": "商品3",
			"categories": "",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"introduction": "商品3的简介",
			"detail": "商品3的详情",
			"shelve_type": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5,
						"stock_type": "无限",
						"stocks": 3
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			}],
			"postage": 10.0
		}]
		"""
	Then jobs能获取商品列表
		"""
		[{
			"name": "商品3"
		}, {
			"name": "商品2"
		}, {
			"name": "商品1"
		}]
		"""		


	##微信用户批量关注jobs成为会员
	When bill关注jobs的公众号于'2天前'

	When mary关注jobs的公众号于'1天前'
	When mary访问jobs的webapp
	When mary把jobs的微站链接分享到朋友圈

	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom把jobs的微站链接分享到朋友圈

	When bill1关注jobs的公众号
	When bill1取消关注jobs的公众号

	When 清空浏览器
	When bill2通过tom分享链接关注jobs的公众号
	When bill2访问jobs的webapp

	When 清空浏览器
	When tom1通过tom分享链接关注jobs的公众号
	When tom1访问jobs的webapp

	When 清空浏览器
	When jack点击mary分享链接
	When jack把jobs的微站链接分享到朋友圈

	When 微信用户批量消费jobs的商品
		|  date  | consumer | type |businessman|      product     | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |  action |  order_status   |
		| 1天前  | mary     | 购买 | jobs      | 商品1,1          | 支付    |   微信支付     | 10      | 100      |  0       | 0      | 100         | 0            | 0      |   100  | 0    |         |    已完成       |
		| 2天前  | bill     | 购买 | jobs      | 商品1,1          |         |   支付宝       | 10      | 100      |  0       | 0      |  0          | 0            | 0      |    0   | 0    |         |    未支付       |
		| 今天   | tom      | 购买 | jobs      | 商品2,1          | 支付    |   微信支付     | 15      | 100      |  0       | 0      | 115         | 0            | 0      |    115 | 0    |jobs,取消|    已取消       |
		| 2天前  | bill     | 购买 | jobs      | 商品1,1          | 支付    |   货到付款     | 10      | 100      |  0       | 30     | 80          | 0            | 0      |    0   | 80   |         |    待发货       |
		| 今天   | tom      | 购买 | jobs      | 商品1,1          | 支付    |   货到付款     | 10      | 100      |   0      | 0      | 90          | 0            | 0      |    0   | 90   |         |    已发货       |
		| 今天   | tom1     | 购买 | jobs      | 商品1,1          | 支付    |   支付宝       | 10      | 100      |  0       | 0      | 110         | 0            | 110    |    0   | 0    |         |    已完成       |
		| 今天   | tom1     | 购买 | jobs      | 商品2,1          | 支付    |   微信支付     | 15      | 100      |  0       | 0      | 115         | 0            | 0      |   115  | 0    |         |    已发货       |
		| 今天   | -lilei   | 购买 | jobs      | 商品2,1          | 支付    |   微信支付     | 15      | 100      |  0       | 0      | 115         | 0            | 0      |   115  | 0    |         |    已发货       |
		| 1天前  | mary     | 购买 | jobs      | 商品2,2          | 支付    |   支付宝       | 15      | 100      |  0       | 20     | 195         | 0            | 195    |    0   | 0    |         |    已发货       |
		| 1天前  | -lisi    | 购买 | jobs      | 商品2,2          | 支付    |   支付宝       | 15      | 100      |  0       | 20     | 195         | 0            | 195    |    0   | 0    |         |    已发货       |

@mall2 @stats @wip.member1
Scenario: 1  会员概况：会员详细数据
	Given jobs登录系统
	When jobs设置筛选日期
		"""
		{
			"start_date":"2天前",
			"end_date":"今天"
		}
		"""

	Then job获得会员详细数据
		|    date    |  new_member  | mobile_phone_member | launch_share_link_member | share_link_new_member | launch_spreading_code_member | spreading_code_new_member | order_member |
		|    今天    |      4       |          0          |            2             |           2           |               0              |              0            |       3      |
		|   1天前    |      1       |          0          |            0             |           0           |               0              |              0            |       2      |
		|   2天前    |      1       |          0          |            0             |           0           |               0              |              0            |       1      |
