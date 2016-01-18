#author: 王丽 2015-01-13

Feature: 发优惠券-选择会员
	Jobs能通过管理系统发优惠券，选择到会员列表的会员，并可以按照过滤条件进行过滤

Background:
	Given jobs登录系统
	And 开启手动清除cookie模式
	#添加相关基础数据
		When jobs已添加商品
			"""
			[{
				"name": "商品1",
				"postage":10,
				"price":100
			}, {
				"name": "商品2",
				"postage":15,
				"price":100
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
				"upgrade": "手动升级",
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
			| member_name   | attention_time 	   | member_source |   grade  |    tags     |
			| tom1 			| 2014-08-04 23:59:59  | 直接关注      | 银牌会员 | 分组1       |
			| tom2 			| 2014-08-05 00:00:00  | 推广扫码      | 普通会员 | 分组1       |
			| tom3	 	    | 2014-08-05 08:00:00  | 会员分享      | 银牌会员 | 分组1,分组3 |
			| tom4 			| 2014-08-05 23:59:59  | 会员分享      | 金牌会员 | 分组3       |
			| tom5 			| 2014-08-06 00:00:00  | 会员分享      | 金牌会员 | 分组3       |
			| tom6          | 2014-10-01 08:00:00  | 推广扫码      | 普通会员 |             |
			| tom7          | 2014-10-01 08:00:00  | 直接关注      | 金牌会员 |             |

		And tom2取消关注jobs的公众号
		And tom4取消关注jobs的公众号

	#获取会员积分
		When 清空浏览器
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
			| order_id | date         | consumer |   product | payment | pay_type | postage*| price* | paid_amount*| alipay*| wechat*| cash*|     action    | order_status*|
			|   0001   | 2015-01-01   | tom1     | 商品1,1   | 支付    | 支付宝   | 10      | 100    | 110         | 110    | 0      | 0    |               | 待发货       |
			|   0002   | 2015-01-02   | tom1     | 商品2,2   |         | 支付宝   | 15      | 100    | 0           | 0      | 0      | 0    | jobs,取消     | 已取消       |
			|   0003   | 2015-02-01   | tom2     | 商品2,2   | 支付    | 支付宝   | 15      | 100    | 215         | 215    | 0      | 0    | jobs,发货     | 已发货       |
			|   0004   | 2015-02-02   | tom2     | 商品1,1   | 支付    | 微信支付 | 10      | 100    | 110         | 0      | 110    | 0    | jobs,完成     | 已完成       |
			|   0005   | 2015-02-04   | tom2     | 商品1,1   |         | 微信支付 | 10      | 100    | 0           | 0      | 0      | 0    |               | 待支付       |
			|   0006   | 2015-03-02   | tom3     | 商品1,1   | 支付    | 货到付款 | 10      | 100    | 110         | 0      | 0      | 110  | jobs,完成     | 已完成       |
			|   0007   | 2015-03-04   | tom3     | 商品2,1   | 支付    | 微信支付 | 15      | 100    | 115         | 0      | 115    | 0    | jobs,退款     | 退款中       |
			|   0008   | 2015-03-05   | tom3     | 商品1,1   | 支付    | 支付宝   | 10      | 100    | 110         | 110    | 0      | 0    | jobs,完成退款 | 退款完成     |

@send_coupon @eugeneXXX
Scenario: 1 发优惠券-选择会员列表查询
	Given jobs登录系统
	#默认条件查询（空条件）
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom6  | 普通会员    |   0.00    |    0.00    |    0      |     0    |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |
			| tom2  | 普通会员    |   325.00  |    162.50  |    2      |     50   |
			| tom1  | 银牌会员    |   110.00  |    110.00  |    1      |     0    |

	#按照会员名称进行查询
		#模糊匹配
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"name":"7"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |

		#完全匹配
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"name":"tom3"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |

		#查询结果为空
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"name":"bill"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |

	#按照会员分组查询
		#单个分组
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"tags":"分组3"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |
		#全部
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"tags":"全部"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom6  | 普通会员    |   0.00    |    0.00    |    0      |     0    |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |
			| tom2  | 普通会员    |   325.00  |    162.50  |    2      |     50   |
			| tom1  | 银牌会员    |   110.00  |    110.00  |    1      |     0    |

	#按照会员等级查询
		#单个等级
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"member_rank":"金牌会员"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
		#全部
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"member_rank":"全部"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom6  | 普通会员    |   0.00    |    0.00    |    0      |     0    |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |
			| tom2  | 普通会员    |   325.00  |    162.50  |    2      |     50   |
			| tom1  | 银牌会员    |   110.00  |    110.00  |    1      |     0    |

	#按照积分范围查询
		#积分相同 0~0
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"start_integral": 0,
				"end_integral": 0
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom6  | 普通会员    |   0.00    |    0.00    |    0      |     0    |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom1  | 银牌会员    |   110.00  |    110.00  |    1      |     0    |

		#积分区间 0~20
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"start_integral": 0,
				"end_integral": 20
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom6  | 普通会员    |   0.00    |    0.00    |    0      |     0    |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom1  | 银牌会员    |   110.00  |    110.00  |    1      |     0    |

		#积分区间 前大于后50~20
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"start_integral": 50,
				"end_integral": 20
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom2  | 普通会员    |   325.00  |    162.50  |    2      |     50   |

		#查询结果为空
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"start_integral": 200,
				"end_integral": 300
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |

	#按照会员来源查询
		#按照单个会员来源
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"source":"会员分享"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |
		#按照全部
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"source":"全部"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom6  | 普通会员    |   0.00    |    0.00    |    0      |     0    |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |
			| tom2  | 普通会员    |   325.00  |    162.50  |    2      |     50   |
			| tom1  | 银牌会员    |   110.00  |    110.00  |    1      |     0    |

	#按照会员状态查询
		#按照单个会员来源
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"status":"取消关注"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom2  | 普通会员    |   325.00  |    162.50  |    2      |     50   |
		#按照全部
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"source":"全部"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom6  | 普通会员    |   0.00    |    0.00    |    0      |     0    |
			| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
			| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |
			| tom2  | 普通会员    |   325.00  |    162.50  |    2      |     50   |
			| tom1  | 银牌会员    |   110.00  |    110.00  |    1      |     0    |

	#条件组合查询
		When jobs设置发送优惠券选择会员查询条件
			"""
			[{
				"name":"4",
				"tags":"分组3",
				"member_rank":"金牌会员",
				"start_integral": 0,
				"end_integral": 20,
				"source":"会员分享",
				"status":"取消关注"
			}]
			"""
		Then jobs获得发送优惠券选择会员列表
			| name  | member_rank | pay_money | unit_price | pay_times | integral |
			| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |

@send_coupon @eugeneXXX
Scenario: 2 发优惠券-选择会员列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	When jobs设置发送优惠券选择会员查询条件
		"""
		[{}]
		"""
	Then jobs获得发送优惠券选择会员列表
		| name  | member_rank | pay_money | unit_price | pay_times | integral |
		| tom7  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
		| tom6  | 普通会员    |   0.00    |    0.00    |    0      |     0    |
		| tom5  | 金牌会员    |   0.00    |    0.00    |    0      |     0    |
	When jobs浏览优惠券选择会员列表的下一页
	Then jobs获得发送优惠券选择会员列表
		| name  | member_rank | pay_money | unit_price | pay_times | integral |
		| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
		| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |
		| tom2  | 普通会员    |   325.00  |    162.50  |    2      |     50   |
	When jobs浏览发送优惠券选择会员列表第'3'页
	Then jobs获得发送优惠券选择会员列表
		| name  | member_rank | pay_money | unit_price | pay_times | integral |
		| tom1  | 银牌会员    |   110.00  |    110.00  |    1      |     0    |
	When jobs浏览优惠券选择会员列表的上一页
	Then jobs获得发送优惠券选择会员列表
		| name  | member_rank | pay_money | unit_price | pay_times | integral |
		| tom4  | 金牌会员    |   0.00    |    0.00    |    0      |     20   |
		| tom3  | 银牌会员    |   335.00  |    111.67  |    3      |    100   |
		| tom2  | 普通会员    |   325.00  |    162.50  |    2      |     50   |
