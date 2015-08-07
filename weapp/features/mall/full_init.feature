Feature: 安装完整测试所需的各种数据

@full_init @ignore
Scenario: 安装完整测试数据
	Given jobs登录系统
	#商品
	And jobs已添加商品规格
		'''
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "红色",
				"image": "/standard_static/test_resource_img/icon_color/icon_1.png"
			}, {
				"name": "黄色",
				"image": "/standard_static/test_resource_img/icon_color/icon_5.png"
			}, {
				"name": "蓝色",
				"image": "/standard_static/test_resource_img/icon_color/icon_9.png"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}, {
				"name": "L"
			}]
		}]
		'''
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品
		"""
		[{
			"name": "东坡肘子",
			"category": "分类1,分类2,分类3",
			"physical_unit": "包",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"introduction": "东坡肘子的简介",
			"detail": "东坡肘子的详情",
			"remark": "东坡肘子的备注",
			"shelve_type": "上架",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"category": "分类1",
			"physical_unit": "盘",
			"price": 12.0,
			"weight": 5.5,
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou2.jpg",
			"introduction": "叫花鸡的简介",
			"detail": "叫花鸡的详情",
			"shelve_type": "下架",
			"stock_type": "有限",
			"stocks": 3,
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.5,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "水晶虾仁",
			"category": "分类2,分类3",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/hangzhou3.jpg",
			"pic_url": "/standard_static/test_resource_img/hangzhou3.jpg",
			"introduction": "水晶虾仁的简介",
			"detail": "水晶虾仁的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"红色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"黄色 M": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"蓝色 M": {
						"price": 11.1,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}, {
			"name": "莲藕排骨汤",
			"category": "分类3",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/tang1.jpg",
			"pic_url": "/standard_static/test_resource_img/tang1.jpg",
			"introduction": "莲藕排骨汤的简介",
			"detail": "莲藕排骨汤的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/tang1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 5.0
					}
				}
			}
		}, {
			"name": "冬荫功汤",
			"category": "分类3",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/tang2.jpg",
			"pic_url": "/standard_static/test_resource_img/tang2.jpg",
			"introduction": "冬荫功汤的简介",
			"detail": "冬荫功汤的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/tang2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 6.0
					}
				}
			}
		}, {
			"name": "松鼠桂鱼",
			"category": "分类3",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/yu3.jpg",
			"pic_url": "/standard_static/test_resource_img/yu3.jpg",
			"introduction": "松鼠桂鱼的简介",
			"detail": "松鼠桂鱼的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/yu3.jpg"
			}],
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"S": {
						"price": 6.0
					}, 
					"L": {
						"price": 8.0
					}, 
					"M": {
						"price": 7.0
					}
				}
			}
		}, {
			"name": "武昌鱼",
			"category": "",
			"physical_unit": "盘",
			"thumbnails_url": "/standard_static/test_resource_img/yu1.jpg",
			"pic_url": "/standard_static/test_resource_img/yu1.jpg",
			"introduction": "武昌鱼的简介",
			"detail": "武昌鱼的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/yu1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 11.0,
						"weight": 20,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "黄桥烧饼",
			"category": "",
			"physical_unit": "个",
			"thumbnails_url": "/standard_static/test_resource_img/mian1.jpg",
			"pic_url": "/standard_static/test_resource_img/mian1.jpg",
			"introduction": "黄桥烧饼的简介",
			"detail": "黄桥烧饼的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/mian1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 2.0
					}
				}
			}
		}, {
			"name": "热干面",
			"category": "",
			"physical_unit": "碗",
			"thumbnails_url": "/standard_static/test_resource_img/mian2.jpg",
			"pic_url": "/standard_static/test_resource_img/mian2.jpg",
			"introduction": "热干面的简介",
			"detail": "热干面的详情",
			"swipe_images": [{
				"url": "/standard_static/test_resource_img/mian2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 1.5
					}
				}
			}
		}]	
		"""
	#促销活动
	When jobs创建限时抢购活动
		"""
		[{
			"name": "东坡肘子限时抢购",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["东坡肘子"],
			"promotion_price": 1.1
		}, {
			"name": "叫花鸡限时抢购",
			"promotion_title": "叫花鸡限时抢购年末大放血",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["叫花鸡"],
			"limit_period": 2,
			"limit_counts": 2,
			"count_per_purchase": 2,
			"promotion_price": 2
		}]
		"""
	When jobs创建满减活动
		"""
		[{
			"name": "水晶虾仁满减",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["水晶虾仁", "热干面"],
			"price_threshold": 3.0,
			"cut_money": 0.5
		}, {
			"name": "莲藕排骨汤满减",
			"promotion_title": "莲藕排骨汤满减年末大放血",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["莲藕排骨汤"],
			"price_threshold": 1.0,
			"cut_money": 0.6,
			"is_enable_cycle_mode": true
		}]
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "武昌鱼买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["武昌鱼"],
			"premium_products": [{
				"name": "松鼠桂鱼",
				"count": 1
			}],
			"count": 2,
			"is_enable_cycle_mode": false
		}]
		"""
	When jobs结束促销活动'武昌鱼买一赠一'
	When jobs创建买赠活动
		"""
		[{
			"name": "武昌鱼买一赠二",
			"promotion_title": "武昌鱼买赠年末大放血（赠送松鼠桂鱼）",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["武昌鱼"],
			"premium_products": [{
				"name": "东坡肘子",
				"count": 1
			}, {
				"name": "叫花鸡",
				"count": 2
			}],
			"count": 1,
			"is_enable_cycle_mode": true
		}]
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "冬荫功汤积分应用",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["冬荫功汤"],
			"discount": 100,
			"discount_money": 0.0,
			"is_permanant_active": false
		}, {
			"name": "松鼠桂鱼积分应用",
			"promotion_title": "松鼠桂鱼积分应用年末大放血",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["松鼠桂鱼"],
			"discount": 50,
			"discount_money": 6.0,
			"is_permanant_active": true
		}]
		"""
	#邮费配置
	When jobs添加邮费配置
		"""
		[{
			"name" : "圆通",
			"first_weight" : 40,
			"first_weight_price" : 4,
			"is_enable_added_weight" : 1,
            "added_weight" : 1,
            "added_weight_price" : 6
		}, {
			"name" : "顺丰",
            "first_weight" : 41,
            "first_weight_price" : 5
        }, {
			"name" : "EMS",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00,
			"special_area": [{
				"to_the":"北京市",
				"first_weight_price":20.00,
				"added_weight_price":10.00
			},{
				"to_the":"上海市,重庆市,江苏省",
				"first_weight_price":30.00,
				"added_weight_price":20.00
			}]
		}]	
		"""
	#支付方式
	Given jobs已添加支付方式
		"""
		[{
			"type": "微信支付",
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
	#积分
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的50会员积分
	Given jobs登录系统
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 5
		}
		"""
	#优惠券
	Given jobs已添加了优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 1,
			"start_date": "今天",
			"end_date": "1天后"
		}, {
			"name": "优惠券2",
			"money": 100,
			"start_date": "今天",
			"end_date": "1天后"
		}, {
			"name": "优惠券3",
			"money": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满5元可以使用"
		}]
		"""
	When bill访问jobs的webapp
	When bill领取jobs的优惠券
		"""
		[{
			"name": "优惠券1",
			"coupon_ids": ["coupon_12", "coupon_11"]
		}, {
			"name": "优惠券2",
			"coupon_ids": ["coupon_22", "coupon_21"]
		}, {
			"name": "优惠券3",
			"coupon_ids": ["coupon_32", "coupon_31"]
		}]
		"""
	#bill收货地址
	And bill设置jobs的webapp的默认收货地址
	
	# bill发消息
	And bill在微信中向jobs的公众号发送消息'你好，这是bill发给jobs的消息01'
	And bill在微信中向jobs的公众号发送消息'你好，这是bill发给jobs的消息02'
	# tom关注并发消息
	When tom关注jobs的公众号
	And tom在微信中向jobs的公众号发送消息'你好，这是tom发给jobs的消息01'
	# nokia关注并发消息
	When nokia关注jobs的公众号
	And nokia在微信中向jobs的公众号发送消息'你好，这是nokia发给jobs的消息01'
	# guo关注并发消息
	When guo关注jobs的公众号
	And guo在微信中向jobs的公众号发送消息'你好，这是guo发给jobs的消息01'

	Given jobs登录系统
	And jobs已添加关键词自动回复规则
		"""
		[{
			"patterns": "词1_1|词1_2",
			"answer": "answer1"
		}, {
			"patterns": "keyword2_1",
			"answer": "answer2"
		}, {
			"patterns": "keyword3",
			"answer": "answer3"
		}]	
		"""
	When jobs创建分组
		"""
		[{
			"category_name": "星标组"
		}, {
			"category_name": "铁杆粉丝"
		}]
		"""
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "星标组"
		}, {
			"category_name": "铁杆粉丝"
		}]
		"""

	# 添加渠道扫码的初始化信息
	Given jobs登录系统
	And jobs已添加'渠道扫码'营销活动
		"""
		[{
			"setting_id": 0,
			"name": "渠道扫码测试1",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"xxx\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"grade_id": 16,
			"remark": "备注1"
		}, {
			"setting_id": 0,
			"name": "渠道扫码测试2",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"xxx\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"grade_id": 16,
			"remark": "备注2"
		}, {
			"setting_id": 0,
			"name": "渠道扫码测试3",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"xxx\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"grade_id": 16,
			"remark": "备注3"
		}, {
			"setting_id": 0,
			"name": "渠道扫码测试4",
			"prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"xxx\"}",
			"reply_type": 0,
			"reply_material_id": 0,
			"re_old_member": 0,
			"grade_id": 16,
			"remark": "备注4"
		}]
		"""
	#And bill关注jobs的公众号
	When bill通过扫描'渠道扫码测试1'二维码关注
	And tom通过扫描'渠道扫码测试1'二维码关注
	And nokia通过扫描'渠道扫码测试1'二维码关注
	Given jobs登录系统
	Then jobs能看到的渠道扫码列表
		"""
		[{
			"name": "渠道扫码测试1",
			"remark": "备注1"
		}, {
			"name": "渠道扫码测试2",
			"remark": "备注2"
		}, {
			"name": "渠道扫码测试3",
			"remark": "备注3"
		}, {
			"name": "渠道扫码测试4",
			"remark": "备注4"
		}]
		"""

	# 构造抽奖数据
	Given jobs已添加'微信抽奖'活动配置
		"""
		[{
			"id": 0,
			"name": "抽奖测试1",
			"award_hour": 0,
			"award_type": 0,
			"daily_play_count": 1,
			"detail": "<p>测试2<br/></p>",
			"start_at": "2015-06-16",
			"end_at": "2015-06-30",
			"expend_integral": 0,
			"no_prize_odd": 0,
			"not_win_desc": "谢谢参与",
			"prize_count|1": 1,
			"prize_name|1": "一等奖",
			"prize_odds|1": 100,
			"prize_source|1": 0,
			"prize_type|1": 1,
			"type": 0
		}, {
			"id": 0,
			"name": "抽奖测试2",
			"award_hour": 0,
			"award_type": 0,
			"daily_play_count": 1,
			"detail": "<p>测试2<br/></p>",
			"start_at": "2015-06-16",
			"end_at": "2015-06-30",
			"expend_integral": 0,
			"no_prize_odd": 0,
			"not_win_desc": "谢谢参与",
			"prize_count|1": 1,
			"prize_name|1": "一等奖",
			"prize_odds|1": 100,
			"prize_source|1": 0,
			"prize_type|1": 1,
			"type": 0
		}]
		"""
	#And bill关注jobs的公众号
	When bill访问jobs的webapp
	And bill参加抽奖活动'抽奖测试1'
	And tom参加抽奖活动'抽奖测试1'
	And nokia参加抽奖活动'抽奖测试1'
	And guo参加抽奖活动'抽奖测试1'


@ignore @wip.init
Scenario: 安装完整测试数据
	Given jobs登录系统
	When jobs添加抽奖活动配置
		"""
		[{
			"id": 0,
			"name": "抽奖测试",
			"award_hour": 0,
			"award_type": 0,
			"daily_play_count": 1,
			"detail": "<p>测试<br/></p>",
			"start_at": "2015-06-16",
			"end_at": "2015-06-30",
			"expend_integral": 0,
			"no_prize_odd": 0,
			"not_win_desc": "谢谢参与",
			"prize_count|1": 1,
			"prize_name|1": "一等奖",
			"prize_odds|1": 100,
			"prize_source|1": 0,
			"prize_type|1": 1,
			"type": 0
		}]
		"""
	And bill关注jobs的公众号
	And bill参加抽奖活动'抽奖测试'
