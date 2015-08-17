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

	When jobs已添加商品
		|    name    |  bar_code  |      categories      |shelve_type|  price  |   weight  | stock_type  |  stocks  |  postage  |    create_date   |
		|    商品1   |            |    分类1             |   上架    |  0.01   |   1       |      无限   |    0     |   免运费  |  2015-4-2 23:59  |
		|    商品2   |  1234561   |    分类1,分类2       |   上架    |  10     |   0       |      有限   |    0     |    顺丰   |  2015-4-3 00:00  |
		|    商品3   |  1234562   |    分类1,分类2,分类3 |   上架    |   1     |   0.0001  |      有限   |   100    |   免运费  |  2015-7-2 10:20  |
		|    商品2   |  1234562   |                      |   上架    |  0      |   2       |      有限   |  100000  |    顺丰   |  今天 05:30      |
		|    商品4   |  1234563   |    分类2             |   下架    |  10     |   1       |      无限   |    0     |   免运费  |  2015-4-1 11:12  |
		|    商品5   |  1234564   |                      |   回收站  |  10     |   1       |      有限   |   200    |   免运费  |  2015-2-2 12:00  |

	When bill关注jobs的公众账号于'2015-1-1'
	And tom关注jobs的公众账号于'2015-2-1'
	And bill取消关注jobs的公众账号

	When 微信用户批量消费jobs的商品
		| date       | consumer | type      |businessman|   product | payment | payment_method | freight |   price  | paid_amount |  alipay | wechat | cash  |     action    |  order_status   |
		| 2015-4-5   | bill     | 	 购买   | jobs      | 商品1,1   | 支付    | 支付宝         |  0      |   0.01  |    0.01    |  0.01  | 0      | 0     | jobs,完成     |  已完成         |
		| 2015-4-6   | bill     | 	 购买   | jobs      | 商品1,1   | 支付    | 微信支付       |  0      |   0.01  |    0.01    |  0      | 0.01  | 0     | jobs,发货     |  已发货         |
		| 2015-4-7   | bill     | 	 购买   | jobs      | 商品1,1   | 支付    | 微信支付       |  0      |   0.01  |    0.01    |  0      | 0.01  | 0     | jobs,退款     |  退款中         |
		| 2015-4-7   | bill     | 	 购买   | jobs      | 商品1,1   | 支付    | 货到付款       |  0      |   0.01  |    0.01    |  0      | 0      | 0.01 | jobs,支付     |  待发货         |
		| 2015-7-3   | tom      | 	 购买   | jobs      | 商品3,1   | 支付    | 货到付款       |  0      |   1      |    1        |  0      | 0      | 0     | jobs,取消     |  已取消         |
		| 2015-7-4   | tom      | 	 购买   | jobs      | 商品3,1   | 支付    | 支付宝         |  0      |   1      |    1        |  1      | 0      | 0     | jobs,发货     |  已发货         |
		| 2015-7-1   | -tom2    | 	 购买   | jobs      | 商品1,1   | 支付    | 支付宝         |  0      |   0.01  |    0.01    |  0.01  | 0      | 0     | jobs,发货     |  已发货         |
		| 2015-7-10  | tom      | 	 购买   | jobs      | 商品3,1   | 支付    | 微信支付       |  0      |   1      |    1        |  0      | 1      | 0     | jobs,无操作   |  待支付         |
		| 今天       | tom      | 	 购买   | jobs      | 商品3,1   | 未支付  | 微信支付       |  0      |   1      |    1        |  0      | 0      | 0     | jobs,完成退款 |  退款成功       |

Scenario:在售商品列表查询

	#空查询、默认查询（空查询）
		When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"",
				"start_stocks":"",
				"end-stocks":"",
				"start_sales":"",
				"end_sales":"",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

		Then jobs获得在售商品列表
			|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
			|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  今天 05:30     |
			|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |
			|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-4-3 00:00 |
			|  商品1 |           |  分类1             |  0.01  |   无限   |    4    |  2015-4-2 23:59 |

	#商品名称

		#完全匹配
			When jobs设置查询条件
				"""
				{
					"name":"商品2",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  今天 05:30     |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-4-3 00:00 |

		#部分匹配
			When jobs设置查询条件
				"""
				{
					"name":"商品",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  今天 05:30     |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-4-3 00:00 |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    4    |  2015-4-2 23:59 |

		#查询结果为空

			When jobs设置查询条件
				"""
				{
					"name":"商  2",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    |

	#商品条码

		#完全匹配

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"1234562",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  今天 05:30     |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |

		#查询结果为空
			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"123456",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 

	#商品价格

		#填写条件校验

			When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"10",
				"start_stocks":"",
				"end-stocks":"",
				"start_sales":"",
				"end_sales":"",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

			Then jobs获得系统提示"请输入起始价格"

			When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"10",
				"end_price":"",
				"start_stocks":"",
				"end-stocks":"",
				"start_sales":"",
				"end_sales":"",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

			Then jobs获得系统提示"请输入最高价格"

			When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"10",
				"end_price":"5",
				"start_stocks":"",
				"end-stocks":"",
				"start_sales":"",
				"end_sales":"",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

			Then jobs获得系统提示"最高价格不能低于起始价格"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"-1",
					"end_price":"5",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入正确的价格"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"0",
					"end_price":"-1",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入正确的价格"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"0.01",
					"end_price":"1",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入正确的价格"

		#价格区间查询

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"0",
					"end_price":"1",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  今天 05:30     |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |
				|  商品1 |           |  分类1             |  0.01   |   无限   |    4    |  2015-4-2 23:59 |

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"0",
					"end_price":"0",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  今天 05:30     |

		#查询结果为空

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"10.01",
					"end_price":"100",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 

	#商品库存（任何查询条件，查询结果都查询出库存为无限的商品）

		#填写条件校验

			When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"",
				"start_stocks":"",
				"end-stocks":"10",
				"start_sales":"",
				"end_sales":"",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

			Then jobs获得系统提示"请输入起始库存"

			When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"",
				"start_stocks":"10",
				"end-stocks":"",
				"start_sales":"",
				"end_sales":"",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

			Then jobs获得系统提示"请输入最高库存"

			When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"",
				"start_stocks":"10",
				"end-stocks":"5",
				"start_sales":"",
				"end_sales":"",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

			Then jobs获得系统提示"最高库存不能低于起始库存"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"-1",
					"end-stocks":"0",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入正确的库存！仅数字"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"0",
					"end-stocks":"-1",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入正确的库存！仅数字"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"0.1",
					"end-stocks":"10",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入正确的库存！仅数字"

		#库存区间查询

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"0",
					"end-stocks":"99",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-4-3 00:00 |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    4    |  2015-4-2 23:59 |

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"100000",
					"end-stocks":"100000",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  今天 05:30     |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    4    |  2015-4-2 23:59 |

		#查询结果为无区间数据

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"10",
					"end-stocks":"20",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    4    |  2015-4-2 23:59 |

	#商品销量

		#填写条件校验

			When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"",
				"start_stocks":"",
				"end-stocks":"",
				"start_sales":"",
				"end_sales":"10",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

			Then jobs获得系统提示"请输入起始销量"

			When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"",
				"start_stocks":"",
				"end-stocks":"",
				"start_sales":"10",
				"end_sales":"",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

			Then jobs获得系统提示"请输入最高销量"

			When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"",
				"start_stocks":"",
				"end-stocks":"",
				"start_sales":"10",
				"end_sales":"5",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

			Then jobs获得系统提示"最高销量不能低于起始销量"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"-1",
					"end_sales":"0",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入正确的销量！仅数字"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"0",
					"end_sales":"-1",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入正确的销量！仅数字"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"0.1",
					"end_sales":"10",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入正确的销量！仅数字"

		#销量区间查询

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"0",
					"end_sales":"4",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品2 |  1234562  |                    |  0      |  100000  |    0    |  今天 05:30     |
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-4-3 00:00 |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    4    |  2015-4-2 23:59 |

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"1",
					"end_sales":"1",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |

		#查询结果为空

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"5",
					"end_sales":"10",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 

	#店内分组

		#查询单个分组商品
			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"分类1",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-4-3 00:00 |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    4    |  2015-4-2 23:59 |

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"分类3",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |

		#查询结果为空

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"分类4",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 

	#创建时间

		#查询条件校验

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"2015-1-1",
					"end_date":""
				}
				"""

			Then jobs获得系统提示"请输入结束日期"

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":"2015-1-1"
				}
				"""

			Then jobs获得系统提示"请输入开始日期"

		#查询商品创建时间

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"2015-4-1 00:00",
					"end_date":"2015-4-3 00:00"
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
				|  商品2 |  1234561  |  分类1,分类2       |  10     |    0     |    0    |  2015-4-3 00:00 |
				|  商品1 |           |  分类1             |  0.01  |   无限   |    4    |  2015-4-2 23:59 |

		#查询结果为空

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"",
					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"2015-7-10 00:00",
					"end_date":"2015-7-20 00:00"
				}
				"""

			Then jobs获得在售商品列表
				|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 

	#条件混合查询

		When jobs设置查询条件
			"""
			{
				"name":"商品",
				"bar_code":"1234562",
				"start_price":"0",
				"end_price":"1",
				"start_stocks":"2",
				"end-stocks":"100000",
				"start_sales":"0",
				"end_sales":"1",
				"category":"分类3",
				"start_date":"2015-7-2 10:20",
				"end_date":"2015-7-20 10:20"
			}
			"""

		Then jobs获得在售商品列表
			|  name  |  bar_code |      category      |  price  |  stocks  |  sales  |  create_date    | 
			|  商品3 |  1234562  |  分类1,分类2,分类3 |  1      |   99     |    1    |  2015-7-2 10:20 |

Scenario:在售多规格商品列表查询

	Given jobs已添加商品规格
		'''
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
		'''

	And jobs已添加商品
		"""
		[{
			"name": "商品单规格",
			"is_enable_model": "启用规格",
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
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品单规格",
				"count": 2,
				"model": "黑色"
			}]
		}
		"""

	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品复合规格",
				"count": 1,
				"model": "白色 s"
			},
			{
				"name": "商品复合规格",
				"count": 3,
				"model": "黑色 M"
			}]
		}
		"""


	#商品价格

		#有一个规格的价格在查询区间
			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"10",
					"end_price":"10",
					"start_stocks":"",

					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|    name    |  bar_code |      category      |   price    |  stocks  |  sales  |  create_date    |
				|  商品单规格|           |                    |  10~20     |          |    2    |  今天           | 
				|  商品2     |  1234561  |  分类1,分类2       |  10        |    0     |    0    |  2015-4-3 00:00 |

		#没有任何一个价格在查询区间

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"60",
					"end_price":"70",
					"start_stocks":"",

					"end-stocks":"",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|    name    |  bar_code |      category      |   price    |  stocks  |  sales  |  create_date    | 

	#商品库存（任何查询条件，查询结果都查询出库存为无限的商品）

		#存在一个规格的库存为”无限“任何条件下都能查询出来
			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"3",
					"end-stocks":"10",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|    name    |  bar_code |      category      |   price    |  stocks  |  sales  |  create_date    | 
				|  商品单规格|           |                    |  10~20     |          |    2    |  今天           |
				|  商品1     |           |  分类1             |  0.01     |   无限   |    4    |  2015-4-2 23:59 |

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"100",
					"end-stocks":"150",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|     name     |  bar_code |      category      |   price    |  stocks  |  sales  |  create_date    | 
				|  商品复合规格|           |                    |  10.5~40   |          |    4    |  今天           |
				|  商品单规格  |           |                    |  10~20     |          |    2    |  今天           |
				|  商品1       |           |  分类1             |  0.01     |   无限   |    4    |  2015-4-2 23:59 |

		#查询结果为无区间数据

			When jobs设置查询条件
				"""
				{
					"name":"",
					"bar_code":"",
					"start_price":"",
					"end_price":"",
					"start_stocks":"700",
					"end-stocks":"1000",
					"start_sales":"",
					"end_sales":"",
					"category":"全部",
					"start_date":"",
					"end_date":""
				}
				"""

			Then jobs获得在售商品列表
				|     name     |  bar_code |      category      |   price    |  stocks  |  sales  |  create_date    | 
				|  商品单规格  |           |                    |  10~20     |          |    2    |  今天           |
				|  商品1       |           |  分类1             |  0.01     |   无限   |    4    |  2015-4-2 23:59 |

	#商品销量（多规格商品是每个规格的销量之和计算）
		
		When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"",
				"start_stocks":"",
				"end-stocks":"",
				"start_sales":"2",
				"end_sales":"3",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

		Then jobs获得在售商品列表
			|     name     |  bar_code |      category      |   price    |  stocks  |  sales  |  create_date    | 
			|  商品单规格  |           |                    |  10~20     |          |    2    |  今天           |


		When jobs设置查询条件
			"""
			{
				"name":"",
				"bar_code":"",
				"start_price":"",
				"end_price":"",
				"start_stocks":"",
				"end-stocks":"",
				"start_sales":"4",
				"end_sales":"4",
				"category":"全部",
				"start_date":"",
				"end_date":""
			}
			"""

		Then jobs获得在售商品列表
			|     name     |  bar_code |      category      |   price    |  stocks  |  sales  |  create_date    | 
			|  商品复合规格|           |                    |  10.5~40   |          |    4    |  今天           |
			|  商品1       |           |  分类1             |  0.01     |   无限   |    4    |  2015-4-2 23:59 |

