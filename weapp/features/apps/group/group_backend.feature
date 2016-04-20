#_author_:许韦 2016.3.8

Feature:新建团购活动
	"""
		用户参加团购活动，达到报团人数拼团成功
		1.【团购名称】：必填项，限制字数为10个字
		2.【起止时间】：必填项
		3.【选择商品】：必填项，只能添加无规格的上架商品
		4.【拼团人数】：必填项，可以设置3人团和10人团
		5.【团购说明】：必填项
		6.【分享图片】：必填项，不上传使用默认图片，推荐尺寸90px*90px，仅支持jpg、png
		7.【分享描述】：必填项，最多可输入26个字
	"""

Background:
	Given jobs登录系统
	When jobs添加微信证书
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
	And jobs已添加商品规格
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
	And jobs已添加支付方式
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
			"is_active": "启用"
		}]
		"""
	And jobs已添加商品
	#添加商品：
			#促销商品，无分类，上架，无限库存；（促销商品）
			#待售商品，待售，无限库存；
			#会员折扣商品，上架，有限库存50；
			#启用规格商品，有限数量3；
			#酱牛肉，上架，无限库存；
			#花生酱，上架，有限数量200；
			#番茄酱，商家，有限数量100；
			#限时抢购商品，上架，无限库存
			#买赠商品，上架，有限数量20；
			#单品券商品，上架，无限库存；
			#积分抵扣商品；

		"""
		[{
			"name": "促销商品",
			"promotion_title": "促销商品",
			"categories": "",
			"detail": "促销商品的详情",
			"status": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 5,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name":"待售商品",
			"category":"",
			"detail":"待售商品的详情",
			"status":"待售",
			"swipe_images":[{
				"url":"/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"model":{"models": {
					"standard": {
						"price": 12.0,
						"weight": 2.5,
						"stock_type": "无限"
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}],
			"postage": "免运费",
			"distribution_time":"off"
		},{
			"name": "会员折扣商品",
			"is_member_product": "on",
			"category": "",
			"detail": "会员折扣商品的详情",
			"status": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 1.5,
						"weight": 0.5,
						"stock_type": "有限",
						"stocks": 50
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}],
			"postage": "免运费",
			"distribution_time":"off"
		},{
			"name": "启用规格商品",
			"category": "",
			"detail": "启用规格商品的详情",
			"status": "上架",
			"is_enable_model": "启用规格",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou4.jpg"
			}],
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}],
			"postage": "免运费",
			"distribution_time":"off"
		},{
			"name":"酱牛肉",
			"category": "",
			"detail": "酱牛肉的详情",
			"status": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou5.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 50.0,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}],
			"postage": "免运费",
			"distribution_time":"off"
		},{
			"name":"花生酱",
			"category": "",
			"detail": "花生酱的详情",
			"status": "上架",
			"invoice":true,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou6.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.5,
						"weight": 1.5,
						"stock_type": "有限",
						"stocks": 200
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}],
			"postage": "10",
			"distribution_time":"on"
		},{
			"name":"番茄酱",
			"category": "",
			"detail": "番茄酱的详情",
			"status": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou6.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 20,
						"weight": 5,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			},
			"pay_interfaces":[{
				"type": "在线支付"
			},{
				"type": "货到付款"
			}],
			"postage": "10"
		},{
			"name":"限时抢购商品",
			"price":100.00,
			"stock_type": "无限",
			"status":"上架"
		},{
			"name":"买赠商品",
			"price":100.00,
			"stock_type": "有限",
			"stocks": 20,
			"status":"上架"
		},{
			"name":"单品券商品",
			"price":100.00,
			"stock_type": "无限",
			"status":"上架"
		},{
			"name":"积分抵扣商品",
			"price":100.00,
			"stock_type": "无限",
			"status":"上架",
			"purchase_count":2
		},{
			"name": "起购数量商品",
			"price": 15.00,
			"stock_type": "有限",
			"stocks": 200,
			"status": "在售",
			"purchase_count": 3
		}
		]
		"""
	When jobs创建限时抢购活动
		"""
		[{
			"name": "限时抢购活动",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "限时抢购商品",
			"member_grade": "全部会员",
			"count_per_purchase": 2,
			"promotion_price": 90.00
		}]
		"""
	And jobs创建买赠活动
		"""
		[{
			"name": "买赠活动",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "买赠商品",
			"premium_products": [{
				"name": "买赠商品",
				"count": 1
			}],
			"count": 2,
			"is_enable_cycle_mode": false
		}]
		"""
	And jobs创建积分应用活动
		"""
		[{
			"name": "积分应用活动",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "积分抵扣商品",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.0
			}]
		}]
		"""
	And jobs添加优惠券规则
		"""
		[{
			"name": "单品券",
			"money": 1,
			"start_date": "2天前",
			"end_date": "2天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "单品券商品"
		}]
		"""

@mall2 @apps_group @apps_group_backend @apps_group_backend_base
Scenario:1 新建团购活动页面,查询商品列表
	Given jobs登录系统
	#促销商品、会员折扣商品、带规格商品、待售商品不在商品列表中
	When jobs新建团购活动时设置参与活动的商品查询条件
		"""
		{
			"name":""
		}
		"""
	Then job获得团购活动可以访问的已上架商品列表
		|  name         | price | stocks | have_promotion | actions |
		| 促销商品      | 5    |  无限   |                |  选取   |
		| 酱牛肉        | 50    |  无限  |                |  选取   |
		| 花生酱        | 12.5  |  200   |                |  选取   |
		| 番茄酱        | 20    |  100   |                |  选取   |
		| 起购数量商品  | 15    |  200   |                |  选取   |


@mall2 @apps_group @apps_group_backend @apps_group_backend_base
Scenario:2 新建未开启,已结束团购活动
	Given jobs登录系统
	When jobs新建团购活动
	"""
		[{
			"group_name":"团购活动1",
			"start_date":"明天",
			"end_date":"2天后",
			"product_name":"酱牛肉",
			"group_dict":{
				"0":{
					"group_type":"3",
					"group_days":"1",
					"group_price":"45"
					}
			},
			"ship_date":"20",
			"product_counts":"100",
			"material_image":"1.jpg",
			"share_description":"团购分享描述"

		},{
			"group_name":"团购活动2",
			"start_date":"3天前",
			"end_date":"昨天",
			"product_name":"花生酱",
			"group_dict":{
				"0":{
					"group_type":"3",
					"group_days":"1",
					"group_price":"11"
					},
				"1":{
					"group_type":"10",
					"group_days":"2",
					"group_price":9.5
			}},
			"ship_date":"15",
			"product_counts":"200",
			"material_image":"2.jpg",
			"share_description":"团购分享描述"
		}]
		"""
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动1",
			"opengroup_num":"0",
			"consumer_num":"0",
			"visitor_num":"0",
			"status":"未开启",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["参团详情","编辑","开启"]
		},{
			"name":"团购活动2",
			"opengroup_num":"0",
			"consumer_num":"0",
			"visitor_num":"0",
			"status":"已结束",
			"start_date":"3天前",
			"end_date":"昨天",
			"actions": ["参团详情","删除"]
		}]
		"""

@mall2 @apps_group @apps_group_backend @apps_group_backend_base
Scenario:3 开启团购活动
	Given jobs登录系统
	When jobs新建团购活动
	"""
		[{
			"group_name":"团购活动3",
			"start_date":"明天",
			"end_date":"2天后",
			"product_name":"酱牛肉",
			"group_dict":{
				"0":{
					"group_type":"3",
					"group_days":"1",
					"group_price":"45"
				},
				"1":{
					"group_type":"10",
					"group_days":"2",
					"group_price":"40"
				}},
			"ship_date":"10",
			"product_counts":"200",
			"material_image":"3.jpg",
			"share_description":"团购分享描述"
		}]
		"""
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动3",
			"opengroup_num":"0",
			"consumer_num":"0",
			"visitor_num":"0",
			"status":"未开启",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["参团详情","编辑","开启"]
		}]
		"""
	When jobs开启团购活动'团购活动3'
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动3",
			"opengroup_num":"0",
			"consumer_num":"0",
			"visitor_num":"0",
			"status":"未开启",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["参团详情","编辑","结束"]
		}]
		"""

@mall2 @apps_group @apps_group_backend @apps_group_backend_base
Scenario:4 编辑未开启团购活动
	Given jobs登录系统
	When jobs新建团购活动
		"""
		[{
			"group_name":"团购活动4",
			"start_date":"明天",
			"end_date":"2天后",
			"product_name":"酱牛肉",
			"group_dict":{
				"0":{
						"group_type":10,
						"group_days":3,
						"group_price":45
					}
			},
			"ship_date":"15",
			"product_counts":"150",
			"material_image":"4.jpg",
			"share_description":"团购分享描述"
		}]
		"""
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动4",
			"opengroup_num":"0",
			"consumer_num":"0",
			"visitor_num":"0",
			"status":"未开启",
			"start_date":"明天",
			"end_date":"2天后",
			"actions": ["参团详情","编辑","开启"]
		}]
		"""
	When jobs编辑团购活动'团购活动4'
		"""
		[{
			"group_name":"团购活动5",
			"start_date":"今天",
			"end_date":"明天",
			"product_name":"花生酱",
			"group_dict":{
				"0":{
						"group_type":"3",
						"group_days":"1",
						"group_price":"10"
				},
				"1":{
						"group_type":"10",
						"group_days":"2",
						"group_price":"8"
			}},
			"ship_date":"20",
			"product_counts":"200",
			"material_image":"5.jpg",
			"share_description":"团购分享描述"
		}]
		"""
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动5",
			"opengroup_num":"0",
			"consumer_num":"0",
			"visitor_num":"0",
			"status":"未开启",
			"start_date":"今天",
			"end_date":"明天",
			"actions": ["参团详情","编辑","开启"]
		}]
		"""

@mall2 @apps_group @apps_group_backend @apps_group_backend_base
Scenario:5 删除已结束团购活动
	Given jobs登录系统
	When jobs新建团购活动
		"""
		[{
			"group_name":"团购活动5",
			"start_date":"2天前",
			"end_date":"昨天",
			"product_name":"酱牛肉",
			"group_dict":{
				"0":{
					"group_type":"3",
					"group_days":"1",
					"group_price":"42"
				}
			},
			"ship_date":"20",
			"product_counts":"100",
			"material_image":"5.jpg",
			"share_description":"团购分享描述"
		},{
			"group_name":"团购活动6",
			"start_date":"今天",
			"end_date":"明天",
			"product_name":"花生酱",
			"group_dict":{
				"0":{
					"group_type":"10",
					"group_days":"2",
					"group_price":"10"
					}
			},
			"ship_date":"20",
			"product_counts":"200",
			"material_image":"6.jpg",
			"share_description":"团购分享描述"
		}]
		"""
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动6",
			"opengroup_num":"0",
			"consumer_num":"0",
			"visitor_num":"0",
			"status":"未开启",
			"start_date":"今天",
			"end_date":"明天",
			"actions": ["参团详情","编辑","开启"]
		},{
			"name":"团购活动5",
			"opengroup_num":"0",
			"consumer_num":"0",
			"visitor_num":"0",
			"status":"已结束",
			"start_date":"2天前",
			"end_date":"昨天",
			"actions": ["参团详情","删除"]
		}]
		"""
	When jobs删除团购活动'团购活动5'
	Then jobs获得团购活动列表
		"""
		[{
			"name":"团购活动6",
			"opengroup_num":"0",
			"consumer_num":"0",
			"visitor_num":"0",
			"status":"未开启",
			"start_date":"今天",
			"end_date":"明天",
			"actions": ["参团详情","编辑","开启"]
		}]
		"""