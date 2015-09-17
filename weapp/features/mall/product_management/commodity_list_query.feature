#_author_:王丽

Feature: 微商城管理-商品管理-在售商品管理 -“查询”
"""
	（1）库存查询，任何查询条件下查询都会查询出来库存为”无限“的商品
	（2）库存查询，多规格商品只要有一个规格的库存满足查询条件，就可以查询出来此商品
	（3）销量查询，多规格商品按照各规格商品销量的和去匹配查询条件，进行查询
"""

Background:
	Given jobs登录系统

	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		},{
			"name": "分类2"
		},{
			"name": "分类3"
		},{
			"name": "分类4"
		}]
		"""

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
		}]
		"""

	Given jobs已添加商品
		|    name    |  bar_code  |      categories      |shelve_type|  price  |   weight  | stock_type  |  stocks  |  postage  |    created_at   |
		|    商品1   |            |    分类1             |   上架    |  0.01   |   1       |      无限   |    0     |   免运费  |  2015-04-02 23:59  |
		|    商品2   |  1234561   |    分类1,分类2       |   上架    |  10     |   0       |      有限   |    0     |    顺丰   |  2015-04-03 00:00  |
		|    商品3   |  1234562   |    分类1,分类2,分类3 |   上架    |   1     |   0.0001  |      有限   |   100    |   免运费  |  2015-07-02 10:20  |
		|    商品2   |  1234562   |                      |   上架    |  0      |   2       |      有限   |  100000  |    顺丰   |  2015-08-01 05:36      |
		|    商品4   |  1234563   |    分类2             |   下架    |  10     |   1       |      无限   |    0     |   免运费  |  2015-04-01 11:12  |

	When bill关注jobs的公众号
	And tom关注jobs的公众号

	When 微信用户批量消费jobs的商品
		| date       | consumer | type      |businessman|   product | payment | payment_method | freight |   price  | paid_amount |  alipay | wechat | cash  |     action    |  order_status   |
		| 2015-4-5   | bill     | 	 购买   | jobs      | 商品1,1   | 支付    | 支付宝         |  0      |   0.01  |    0.01    |  0.01  | 0      | 0     | jobs,完成     |  已完成         |
		| 2015-4-6   | bill     | 	 购买   | jobs      | 商品1,1   | 支付    | 微信支付       |  0      |   0.01  |    0.01    |  0      | 0.01  | 0     | jobs,发货     |  已发货         |
		| 2015-4-7   | bill     | 	 购买   | jobs      | 商品1,1   | 支付    | 微信支付       |  0      |   0.01  |    0.01    |  0      | 0.01  | 0     | jobs,退款     |  退款中         |
		| 2015-4-7   | bill     | 	 购买   | jobs      | 商品1,1   | 支付    | 货到付款       |  0      |   0.01  |    0.01    |  0      | 0      | 0.01 | jobs,无操作     |  待发货         |
		| 2015-7-3   | tom      | 	 购买   | jobs      | 商品3,1   | 支付    | 货到付款       |  0      |   1      |    1        |  0      | 0      | 0     | jobs,取消     |  已取消         |
		| 2015-7-4   | tom      | 	 购买   | jobs      | 商品3,1   | 支付    | 支付宝         |  0      |   1      |    1        |  1      | 0      | 0     | jobs,发货     |  已发货         |
		| 2015-7-1   | -tom2    | 	 购买   | jobs      | 商品1,1   | 支付    | 支付宝         |  0      |   0.01  |    0.01    |  0.01  | 0      | 0     | jobs,发货     |  已发货         |
		| 2015-7-10  | tom      | 	 购买   | jobs      | 商品3,1   |        | 微信支付       |  0      |   1      |    1        |  0      | 1      | 0     | jobs,无操作   |  待支付         |
		| 2015-07-02 10:20       | tom      | 	 购买   | jobs      | 商品3,1   | 未支付  | 微信支付       |  0      |   1      |    1        |  0      | 0      | 0     | jobs,完成退款 |  退款成功       |

#前端功能不能用feature实现
	#"""
		#			When jobs设置查询条件
		#			"""
		#			{
		#				"name":"",
		#				"bar_code":"",
		#				"start_price":"",
		#				"end_price":"",
		#				"start_stocks":"",
		#				"end-stocks":"10",
		#				"start_sales":"",
		#				"end_sales":"",
		#				"category":"全部",
		#				"start_date":"",
		#				"end_date":""
		#			}
		#			"""
		#
		#			Then jobs获得系统提示"请输入起始库存"

		#			When jobs设置查询条件
		#			"""
		#			{
		#				"name":"",
		#				"bar_code":"",
		#				"start_price":"",
		#				"end_price":"",
		#				"start_stocks":"10",
		#				"end-stocks":"",
		#				"start_sales":"",
		#				"end_sales":"",
		#				"category":"全部",
		#				"start_date":"",
		#				"end_date":""
		#			}
		#			"""
		#
		#			Then jobs获得系统提示"请输入最高库存"

		#			When jobs设置查询条件
		#			"""
		#			{
		#				"name":"",
		#				"bar_code":"",
		#				"start_price":"",
		#				"end_price":"",
		#				"start_stocks":"10",
		#				"end-stocks":"5",
		#				"start_sales":"",
		#				"end_sales":"",
		#				"category":"全部",
		#				"start_date":"",
		#				"end_date":""
		#			}
		#			"""
		#
		#			Then jobs获得系统提示"最高库存不能低于起始库存"

		#			When jobs设置查询条件
		#				"""
		#				{
		#					"name":"",
		#					"bar_code":"",
		#					"start_price":"",
		#					"end_price":"",
		#					"start_stocks":"-1",
		#					"end-stocks":"0",
		#					"start_sales":"",
		#					"end_sales":"",
		#					"category":"全部",
		#					"start_date":"",
		#					"end_date":""
		#				}
		#				"""
		#
		#			Then jobs获得系统提示"请输入正确的库存！仅数字"

		#			When jobs设置查询条件
		#				"""
		#				{
		#					"name":"",
		#					"bar_code":"",
		#					"start_price":"",
		#					"end_price":"",
		#					"start_stocks":"0",
		#					"end-stocks":"-1",
		#					"start_sales":"",
		#					"end_sales":"",
		#					"category":"全部",
		#					"start_date":"",
		#					"end_date":""
		#				}
		#				"""
		#
		#			Then jobs获得系统提示"请输入正确的库存！仅数字"

		#			When jobs设置查询条件
		#				"""
		#				{
		#					"name":"",
		#					"bar_code":"",
		#					"start_price":"",
		#					"end_price":"",
		#					"start_stocks":"0.1",
		#					"end-stocks":"10",
		#					"start_sales":"",
		#					"end_sales":"",
		#					"category":"全部",
		#					"start_date":"",
		#					"end_date":""
		#				}
		#				"""
		#
		#			Then jobs获得系统提示"请输入正确的库存！仅数字"
	#"""

@mall2
Scenario:1. 在售商品列表查询

	#空查询、默认查询（空查询）
		When jobs设置商品查询条件
			"""
			{
				"name":"",
				"barCode":"",
				"lowPrice":"",
				"highPrice":"",
				"lowStocks":"",
				"highStocks":"",
				"lowSales":"",
				"highSales":"",
				"category":"全部",
				"startDate":"",
				"endDate":""
			}
			"""

		Then jobs能获得'在售'商品列表
			|  name  |  barCode |   categories   | price |  stocks  |  sales  |  created_at    |
			|  商品2 |  1234562  |                |   0  |  100000  |    0    |  2015-08-01 05:36 |
			|  商品3 |  1234562  | 分类1,分类2,分类3|   1  |   98     |    1    |  2015-07-02 10:20 |
			|  商品2 |  1234561  | 分类1,分类2     |   10  |    0     |    0    |  2015-04-03 00:00 |
			|  商品1 |           | 分类1          |  0.01 |   无限    |    5    |  2015-04-02 23:59 |

	#商品名称

		#完全匹配
			When jobs设置商品查询条件
				"""
				{
					"name":"商品2",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  2015-08-01 05:36     |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-04-03 00:00 |

		#部分匹配
			When jobs设置商品查询条件
				"""
				{
					"name":"商品",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  2015-08-01 05:36     |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-04-03 00:00 |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    5    |  2015-04-02 23:59 |

		#查询结果为空

			When jobs设置商品查询条件
				"""
				{
					"name":"商  2",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#商品条码

		#完全匹配

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"1234562",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  2015-08-01 05:36     |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   98     |    1    |  2015-07-02 10:20 |

		#查询结果为空
			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"123456",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#商品价格

		#填写条件校验

	#			When jobs设置查询条件
	#			"""
	#			{
	#				"name":"",
	#				"bar_code":"",
	#				"start_price":"",
	#				"end_price":"10",
	#				"start_stocks":"",
	#				"end-stocks":"",
	#				"start_sales":"",
	#				"end_sales":"",
	#				"category":"全部",
	#				"start_date":"",
	#				"end_date":""
	#			}
	#			"""
	#
	#			Then jobs获得系统提示"请输入起始价格"

	#			When jobs设置查询条件
	#			"""
	#			{
	#				"name":"",
	#				"bar_code":"",
	#				"start_price":"10",
	#				"end_price":"",
	#				"start_stocks":"",
	#				"end-stocks":"",
	#				"start_sales":"",
	#				"end_sales":"",
	#				"category":"全部",
	#				"start_date":"",
	#				"end_date":""
	#			}
	#			"""
	#
	#			Then jobs获得系统提示"请输入最高价格"

	#			When jobs设置查询条件
	#			"""
	#			{
	#				"name":"",
	#				"bar_code":"",
	#				"start_price":"10",
	#				"end_price":"5",
	#				"start_stocks":"",
	#				"end-stocks":"",
	#				"start_sales":"",
	#				"end_sales":"",
	#				"category":"全部",
	#				"start_date":"",
	#				"end_date":""
	#			}
	#			"""
	#
	#			Then jobs获得系统提示"最高价格不能低于起始价格"

	#			When jobs设置查询条件
	#				"""
	#				{
	#					"name":"",
	#					"bar_code":"",
	#					"start_price":"-1",
	#					"end_price":"5",
	#					"start_stocks":"",
	#					"end-stocks":"",
	#					"start_sales":"",
	#					"end_sales":"",
	#					"category":"全部",
	#					"start_date":"",
	#					"end_date":""
	#				}
	#				"""
	#
	#			Then jobs获得系统提示"请输入正确的价格"

	#			When jobs设置查询条件
	#				"""
	#				{
	#					"name":"",
	#					"bar_code":"",
	#					"start_price":"0",
	#					"end_price":"-1",
	#					"start_stocks":"",
	#					"end-stocks":"",
	#					"start_sales":"",
	#					"end_sales":"",
	#					"category":"全部",
	#					"start_date":"",
	#					"end_date":""
	#				}
	#				"""
	#
	#			Then jobs获得系统提示"请输入正确的价格"

	#			When jobs设置查询条件
	#				"""
	#				{
	#					"name":"",
	#					"bar_code":"",
	#					"start_price":"0.01",
	#					"end_price":"1",
	#					"start_stocks":"",
	#					"end-stocks":"",
	#					"start_sales":"",
	#					"end_sales":"",
	#					"category":"全部",
	#					"start_date":"",
	#					"end_date":""
	#				}
	#				"""
	#
	#			Then jobs获得系统提示"请输入正确的价格"

		#价格区间查询

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"0",
					"highPrice":"1",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  2015-08-01 05:36     |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   98     |    1    |  2015-07-02 10:20 |
				|  商品1 |           |  分类1             |  0.01   |   无限   |    5    |  2015-04-02 23:59 |

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"0",
					"highPrice":"0",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  2015-08-01 05:36     |

		#查询结果为空

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"10.01",
					"highPrice":"100",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#商品库存（任何查询条件，查询结果都查询出库存为无限的商品）

		#填写条件校验

		#库存区间查询

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"0",
					"highStocks":"98",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-04-03 00:00 |

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"100000",
					"highStocks":"100000",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  2015-08-01 05:36     |

		#查询结果为无区间数据

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"10",
					"highStocks":"20",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#商品销量

		#填写条件校验

			#			When jobs设置查询条件
			#			"""
			#			{
			#				"name":"",
			#				"bar_code":"",
			#				"start_price":"",
			#				"end_price":"",
			#				"start_stocks":"",
			#				"end-stocks":"",
			#				"start_sales":"",
			#				"end_sales":"10",
			#				"category":"全部",
			#				"start_date":"",
			#				"end_date":""
			#			}
			#			"""
			#
			#			Then jobs获得系统提示"请输入起始销量"

			#			When jobs设置查询条件
			#			"""
			#			{
			#				"name":"",
			#				"bar_code":"",
			#				"start_price":"",
			#				"end_price":"",
			#				"start_stocks":"",
			#				"end-stocks":"",
			#				"start_sales":"10",
			#				"end_sales":"",
			#				"category":"全部",
			#				"start_date":"",
			#				"end_date":""
			#			}
			#			"""
			#
			#			Then jobs获得系统提示"请输入最高销量"

			#			When jobs设置查询条件
			#			"""
			#			{
			#				"name":"",
			#				"bar_code":"",
			#				"start_price":"",
			#				"end_price":"",
			#				"start_stocks":"",
			#				"end-stocks":"",
			#				"start_sales":"10",
			#				"end_sales":"5",
			#				"category":"全部",
			#				"start_date":"",
			#				"end_date":""
			#			}
			#			"""
			#
			#			Then jobs获得系统提示"最高销量不能低于起始销量"

			#			When jobs设置查询条件
			#				"""
			#				{
			#					"name":"",
			#					"bar_code":"",
			#					"start_price":"",
			#					"end_price":"",
			#					"start_stocks":"",
			#					"end-stocks":"",
			#					"start_sales":"-1",
			#					"end_sales":"0",
			#					"category":"全部",
			#					"start_date":"",
			#					"end_date":""
			#				}
			#				"""
			#
			#			Then jobs获得系统提示"请输入正确的销量！仅数字"

			#			When jobs设置查询条件
			#				"""
			#				{
			#					"name":"",
			#					"bar_code":"",
			#					"start_price":"",
			#					"end_price":"",
			#					"start_stocks":"",
			#					"end-stocks":"",
			#					"start_sales":"0",
			#					"end_sales":"-1",
			#					"category":"全部",
			#					"start_date":"",
			#					"end_date":""
			#				}
			#				"""
			#
			#			Then jobs获得系统提示"请输入正确的销量！仅数字"

			#			When jobs设置查询条件
			#				"""
			#				{
			#					"name":"",
			#					"bar_code":"",
			#					"start_price":"",
			#					"end_price":"",
			#					"start_stocks":"",
			#					"end-stocks":"",
			#					"start_sales":"0.1",
			#					"end_sales":"10",
			#					"category":"全部",
			#					"start_date":"",
			#					"end_date":""
			#				}
			#				"""
			#
			#			Then jobs获得系统提示"请输入正确的销量！仅数字"

		#销量区间查询

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"0",
					"highSales":"4",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  2015-08-01 05:36     |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-04-03 00:00 |
			#	|  商品1 |           |  分类1             |  0.01  |   无限   |    4    |  2015-04-02 23:59 |

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"1",
					"highSales":"1",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   98     |    1    |  2015-07-02 10:20 |

		#查询结果为空

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"5",
					"highSales":"10",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    5    |  2015-04-02 23:59 |
	#店内分组

		#查询单个分组商品
			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"分类1",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-04-03 00:00 |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    5    |  2015-04-02 23:59 |

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"分类3",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   98     |    1    |  2015-07-02 10:20 |

		#查询结果为空

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"分类4",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#创建时间

		#查询条件校验

			#			When jobs设置查询条件
			#				"""
			#				{
			#					"name":"",
			#					"bar_code":"",
			#					"start_price":"",
			#					"end_price":"",
			#					"start_stocks":"",
			#					"end-stocks":"",
			#					"start_sales":"",
			#					"end_sales":"",
			#					"category":"全部",
			#					"start_date":"2015-1-1",
			#					"end_date":""
			#				}
			#				"""
			#
			#			Then jobs获得系统提示"请输入结束日期"

			#			When jobs设置查询条件
			#				"""
			#				{
			#					"name":"",
			#					"bar_code":"",
			#					"start_price":"",
			#					"end_price":"",
			#					"start_stocks":"",
			#					"end-stocks":"",
			#					"start_sales":"",
			#					"end_sales":"",
			#					"category":"全部",
			#					"start_date":"",
			#					"end_date":"2015-1-1"
			#				}
			#				"""
			#
			#			Then jobs获得系统提示"请输入开始日期"

		#查询商品创建时间

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"2015-04-01 00:00",
					"endDate":"2015-04-03 00:00"
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-04-03 00:00 |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    5    |  2015-04-02 23:59 |

		#查询结果为空

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"",
					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"2015-7-10 00:00",
					"endDate":"2015-07-20 00:00"
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#条件混合查询

		When jobs设置商品查询条件
			"""
			{
				"name":"商品",
				"barCode":"1234562",
				"lowPrice":"0",
				"highPrice":"1",
				"lowStocks":"2",
				"highStocks":"100000",
				"lowSales":"0",
				"highSales":"1",
				"category":"分类3",
				"startDate":"2015-07-02 10:20",
				"endDate":"2015-07-20 10:20"
			}
			"""

		Then jobs能获得'在售'商品列表
			|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |
			|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   98     |    1    |  2015-07-02 10:20 |

@mall2
Scenario:2. 在售多规格商品列表查询

	Given jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""

	And jobs已添加商品
		"""
		[{
			"name": "商品单规格",
			"is_enable_model": "启用规格",
			"created_at": "2015-07-02 10:20",
			"model": {
				"models": {
					"黑色": {
						"price": 10.0,
						"weight": 3,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色": {
						"price": 20.0,
						"weight": 4,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""

	And jobs已添加商品
		"""
		[{
			"name": "商品复合规格",
			"is_enable_model": "启用规格",
			"created_at": "2015-07-02 10:20",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.5,
						"weight": 1,
						"stock_type": "有限",
						"stocks": 100
					},
					"白色 S": {
						"price": 20,
						"weight": 2,
						"stock_type": "有限",
						"stocks": 200
					},
					"黑色 M": {
						"price": 30,
						"weight": 3,
						"stock_type": "有限",
						"stocks": 300
					},
					"白色 M": {
						"price": 40,
						"weight": 4,
						"stock_type": "有限",
						"stocks": 400
					}
				}
			}
		}]
		"""
  	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品单规格",
				"count": 2,
				"model": "黑色"
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品复合规格",
				"count": 1,
				"model": "白色 S"
			},
			{
				"name": "商品复合规格",
				"count": 3,
				"model": "黑色 M"
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付


	#商品价格

		#有一个规格的价格在查询区间
  			Given jobs登录系统
			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"10",
					"highPrice":"10",
					"lowStocks":"",

					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|    name    |  barCode |      categories      |   price    |  stocks  |  sales  |  created_at    |
				|  商品单规格|           |                    |  10.0 ~ 20.0  |          |    2    |  2015-07-02 10:20           |
				|  商品2     |  1234561  |  分类1,分类2       |  10        |    0     |    0    |  2015-04-03 00:00 |

		#没有任何一个价格在查询区间

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"60",
					"highPrice":"70",
					"lowStocks":"",

					"highStocks":"",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|    name    |  barCode |      categories      |   price    |  stocks  |  sales  |  created_at    |

	#商品库存（任何查询条件，查询结果都查询出库存为无限的商品）

		#存在一个规格的库存为”无限“任何条件下都能查询出来
			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"3",
					"highStocks":"10",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|    name    |  barCode |      categories      |   price    |  stocks  |  sales  |  created_at    |

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"100",
					"highStocks":"150",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|     name     |  barCode |      categories      |   price    |  stocks  |  sales  |  created_at    |
				|  商品复合规格|           |                    |  10.5 ~ 40.0   |          |    4    |  2015-07-02 10:20           |

		#查询结果为无区间数据

			When jobs设置商品查询条件
				"""
				{
					"name":"",
					"barCode":"",
					"lowPrice":"",
					"highPrice":"",
					"lowStocks":"700",
					"highStocks":"1000",
					"lowSales":"",
					"highSales":"",
					"category":"全部",
					"startDate":"",
					"endDate":""
				}
				"""

			Then jobs能获得'在售'商品列表
				|     name     |  barCode |      categories      |   price    |  stocks  |  sales  |  created_at    |

	#商品销量（多规格商品是每个规格的销量之和计算）

		When jobs设置商品查询条件
			"""
			{
				"name":"",
				"barCode":"",
				"lowPrice":"",
				"highPrice":"",
				"lowStocks":"",
				"highStocks":"",
				"lowSales":"2",
				"highSales":"3",
				"category":"全部",
				"startDate":"",
				"endDate":""
			}
			"""

		Then jobs能获得'在售'商品列表
			|     name     |  barCode |      categories      |   price    |  stocks  |  sales  |  created_at    |
			|  商品单规格  |           |                    |  10.0 ~ 20.0     |          |    2    |  2015-07-02 10:20           |


		When jobs设置商品查询条件
			"""
			{
				"name":"",
				"barCode":"",
				"lowPrice":"",
				"highPrice":"",
				"lowStocks":"",
				"highStocks":"",
				"lowSales":"4",
				"highSales":"4",
				"category":"全部",
				"startDate":"",
				"endDate":""
			}
			"""

		Then jobs能获得'在售'商品列表
			|     name     |  barCode |      categories      |   price    |  stocks  |  sales  |  created_at    |
			|  商品复合规格|           |                    |  10.5 ~ 40.0   |          |    4    |  2015-07-02 10:20           |
		#	|  商品1       |           |  分类1             |  0.01     |   无限   |    5    |  2015-04-02 23:59 |

@mall2
Scenario:3. 针对线上BUG3669按商品名称查询时，查询结果的商品库存时正确的

		When jobs设置商品查询条件
		"""
		{
			"name":"商品2",
			"barCode":"",
			"lowPrice":"",
			"highPrice":"",
			"lowStocks":"",
			"highStocks":"",
			"lowSales":"",
			"highSales":"",
			"category":"全部",
			"startDate":"",
			"endDate":""
		}
		"""

		Then jobs能获得'在售'商品列表
			|  name  |  barCode |      categories    |  price  |  stocks  |  sales  |  created_at      |
			|  商品2 |  1234562 |                    |  0      |  100000  |    0    |  2015-08-01 05:36|
			|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-04-03 00:00 |


