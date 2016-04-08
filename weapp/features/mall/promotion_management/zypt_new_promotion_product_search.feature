# watcher: zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_:张三香 2016.03.31

Feature:自营平台-新建促销活动页面的商品查询
	"""
	1、从'供货商'同步到'商城'的商品,其商品详情页面增加"下单位置:商城/供货商",默认选择'商城'
	2、供货商-指商家；商城-微众系列的公众号统称（微众家、微众学生等等）
	3、'下单位置'当勾选'供货商'并保存时，验证该商品是否正在参与活动，如果参与则不能保存并提示： "请先停止该商品参与的活动"
	4、'下单位置'为'供货商'的商品不能参与活动,包括：限时抢购、买赠、积分应用、优惠券、禁用优惠券商品
	5、新建以下促销活动时,商品选择弹窗的商品列表中隐藏掉'下单位置'为'供货商'的商品：
		(限时抢购、买赠、积分应用、单品券及禁用优惠券商品)
	6、商品若参与了'未开始'或'进行中'状态的促销活动，修改下单位置为'供货商'保存时会弹出提示信息
	"""

#特殊说明：jobs、表示自营平台;bill、tom表示商家;

Background:
	#自营平台jobs的信息
		Given 设置jobs为自营平台账号
		Given jobs登录系统
		And jobs已添加支付方式
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
		When jobs开通使用微众卡权限
		When jobs添加支付方式
			"""
			[{
				"type": "微众卡支付",
				"is_active": "启用"
			}]
			"""
		And jobs已添加商品
			"""
			[{
				"name":"jobs自建商品0",
				"price":10.00
			}]
		"""

	#商家bill的信息
		Given 添加bill店铺名称为'bill商家'
		Given bill登录系统
		And bill已添加支付方式
			"""
			[{
				"type": "微信支付",
				"is_active": "启用"
			}]
			"""
		And bill已添加商品规格
			"""
			[{
				"name": "颜色",
				"type": "图片",
				"values": [{
					"name": "黑色",
					"image": "/standard_static/test_resource_img/icon_color/icon_1.png"
				}, {
					"name": "白色",
					"image": "/standard_static/test_resource_img/icon_color/icon_5.png"
				}]
			},{
				"name": "尺寸",
				"type": "文字",
				"values": [{
					"name": "M"
				}, {
					"name": "S"
				}]
			}]
			"""
		And bill已添加商品
			"""
			[{
				"name":"bill商品1",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.0
			},{
				"name":"bill商品2",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"0102",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				}
			},{
				"name":"bill商品3",
				"is_enable_model": "启用规格",
				"model": {
					"models": {
						"黑色 S": {
							"price": 30.0,
							"weight": 1,
							"stock_type": "有限",
							"stocks": 100
						},
						"白色 S": {
							"price": 30.0,
							"weight": 2,
							"stock_type": "无限"
						}
					}
				}
			}]
			"""

	#商家tom的信息
		When tom暂停1秒
		Given 添加tom店铺名称为'tom商家'
		Given tom登录系统
		And tom已添加支付方式
			"""
			[{
				"type": "微信支付",
				"is_active": "启用"
			}]
			"""
		And tom已添加商品
			"""
			[{
				"name":"tom商品1",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0201",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"status":"在售"
			}]
			"""

	#jobs后台商品信息
		Given jobs登录系统
		Then jobs获得商品池商品列表
			"""
			[{
				"name": "tom商品1",
				"user_code":"0201",
				"supplier":"tom商家",
				"stocks":"无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill商品1",
				"user_code":"0101",
				"supplier":"bill商家",
				"stocks": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			},{
				"name": "bill商品2",
				"user_code":"0102",
				"supplier":"bill商家",
				"stocks": "无限",
				"status":"未选择",
				"sync_time":"",
				"actions": ["放入待售"]
			}]
			"""
		When jobs批量将商品放入待售
			"""
			["tom商品1","bill商品2","bill商品1"]
			"""
		When jobs更新商品'bill商品1'
			"""
			{
				"name":"bill商品1下单位置商城",
				"supplier":"bill商家",
				"purchase_price": 9.00,
				"buy_position":"商城",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0101",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
		When jobs更新商品'bill商品2'
			"""
			{
				"name":"bill商品2下单位置商城",
				"supplier":"bill商家",
				"purchase_price": 19.00,
				"buy_position":"商城",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 20.00,
							"user_code":"0102",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":0.00
			}
			"""
		When jobs更新商品'tom商品1'
			"""
			{
				"name":"tom商品1下单位置供货商",
				"supplier":"tom商家",
				"purchase_price": 9.00,
				"buy_position":"供货商",
				"is_member_product":"off",
				"model": {
					"models": {
						"standard": {
							"price": 10.00,
							"user_code":"0201",
							"weight":1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":10.00
			}
			"""
		When jobs批量上架商品
			"""
			["bill商品1下单位置商城","bill商品2下单位置商城","tom商品1下单位置供货商"]
			"""

@mall2 @promotion @eugene @product_pool
Scenario:1 促销活动-新建活动页面的商品查询

	#限时抢购
		Given jobs登录系统
		When jobs新建活动时设置参与活动的商品查询条件
			"""
			{
				"name":"tom商品1下单位置供货商"
			}
			"""
		Then jobs新建限时抢购活动时能获得已上架商品列表
			| name     | price | stocks | have_promotion | actions |

	#买赠活动
		When jobs新建活动时设置参与活动的商品查询条件
			"""
			{
				"name":"tom商品1下单位置供货商"
			}
			"""
		Then jobs新建买赠活动时能获得已上架商品列表
			| name     | price | stocks | have_promotion | actions |

	#积分应用
		When jobs新建活动时设置参与活动的商品查询条件
			"""
			{
				"name":"tom商品1下单位置供货商"
			}
			"""
		Then jobs新建积分应用活动时能获得已上架商品列表
			| name     | price | stocks | have_promotion | actions |

	#单品券
		Given jobs登录系统
		Then jobs新建单品券活动时能获得已上架商品列表
		| name                   | price | stocks | have_promotion | actions |
		| jobs自建商品0          |10.00  | 无限   |                |  选取   |
		| bill商品1下单位置商城  |10.00  | 无限   |                |  选取   |
		| bill商品2下单位置商城  |20.00  | 无限   |                |  选取   |

	#禁用优惠券商品
		Given jobs登录系统
		When jobs新建活动时设置参与活动的商品查询条件
			"""
			{
				"name":"tom商品1下单位置供货商"
			}
			"""
		Then jobs新建禁用优惠券商品活动时能获得已上架商品列表
			| name     | price | stocks | have_promotion | actions |

