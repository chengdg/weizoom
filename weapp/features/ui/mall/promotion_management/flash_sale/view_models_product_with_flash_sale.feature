#_author_:张三香

Feature:选取多规格商品创建限时抢购活动，手机端商品详情页选择规格时，显示限时抢购价，不显示原价
	#说明：
		#针对线上"bug-3890"补充feature
		#多规格商品参与限时抢购活动：
			#手机端商品列表页：显示该商品促销价格；
			#手机端商品详情页：显示该商品促销价格和促销信息" 优惠：【限时抢购】已优惠 ? 元 "；
			#点击【立即购买】按钮：弹出中默认显示对应规格的原价，选择某规格后，显示促销价格不再显示原价；

Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
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
			"name": "多规格商品",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 100.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 200.00,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""

	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"discount": "10.0"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9.0"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8.0"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7.0"
		}]
		"""

	Given bill关注jobs的公众号
	And tom关注jobs的公众号
	When jobs更新"bill"的会员等级
		"""
		{
			"name": "bill",
			"member_rank": "银牌会员"
		}
		"""
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员"
		}, {
			"name": "bill",
			"member_rank": "银牌会员"
		"""

@promotion @promotionFlash @ui
Scenario:参与限时抢购的多规格商品手机端详情页显示促销价格
	Given jobs登录系统
	When jobs创建限时抢购活动
		"""
		{
			"name": "多规格限时抢购",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["多规格商品"],
			"member_grade": "银牌会员",
			"promotion_price": 80
		}
		"""
	Then jobs获取限时抢购活动列表
		"""
		{
			"name": "活动名称：多规格限时抢购",
			"products":["多规格商品"],
			"product_price":"100.00~200.00",
			"promotion_price":80.00,
			"status":"进行中",
			"start_date": "今天",
			"end_date": "1天后",
			"actions": ["详情","结束"]
		}
		"""
	#满足促销条件的会员访问jobs的webapp
	When bill访问jobs的webapp
	And bill浏览jobs的webapp的'全部'商品列表页
	Then bill获得webapp商品列表
		"""
		[{
			"name": "多规格商品",
			"price":80.00
		}]
		"""
	When bill浏览jobs的webapp的'多规格商品'商品页
	Then webapp页面标题为'多规格商品'
	And bill获得webapp商品
		"""
		[{
			"name": "多规格商品",
			"price": 80.00,
			"promotion": {
					"type": "flash_sale",
					"msg":"已优惠20.00元"
				}
		}]
		"""
	When bill进行"立即购买"操作
	Then bill获得"多规格商品"的商品信息
		"""
			[{
				"name":"多规格商品",
				"price":80.00
				"model":
				{
				"models":
					{
						"type":"尺码",
						"values":
						[
							{ 
								"name":"M",
								"is_active":true
							},
							{
								"name":"S",
								"is_active":true
							}
						]
					}
				}
			}]
		"""
	When bill选择规格"M"
	Then bill获得规格"M"的商品信息
		"""
			[{
				"name":"多规格商品",
				"price":80.00
				"model":
				{
				"models":
					{
						"type":"尺码",
						"values":
						[
							{
								"name":"M",
								"is_active":false
							},
							{
								"name":"S",
								"is_active":true
							}
						]
					}
				}
			}]
		"""

	#不满足促销条件的会员访问jobs的webapp
	When tom访问jobs的webapp
	And tom浏览jobs的webapp的'全部'商品列表页
	Then tom获得webapp商品列表
		"""
		[{
			"name": "多规格商品",
			"price":100.00
		}]
		"""
	When tom浏览jobs的webapp的'多规格商品'商品页
	Then webapp页面标题为'多规格商品'
	And tom获得webapp商品
		"""
		[{
			"name": "多规格商品",
			"price": 100.00
				}
		}]
		"""
	When tom进行"立即购买"操作
	Then tom获得"多规格商品"的商品信息
		"""
			[{
				"name":"多规格商品",
				"price":100.00
				"model":
				{
				"models":
					{
						"type":"尺码",
						"values":
						[
							{ 
								"name":"M",
								"is_active":true
							},
							{
								"name":"S",
								"is_active":true
							}
						]
					}
				}
			}]
		"""
	When tom选择规格"M"
	Then tom获得规格"M"的商品信息
		"""
			[{
				"name":"多规格商品",
				"price":100.00
				"model":
				{
				"models":
					{
						"type":"尺码",
						"values":
						[
							{ 
								"name":"M",
								"is_active":false
							},
							{
								"name":"S",
								"is_active":ture
							}
						]
					}
				}
			}]
		"""



