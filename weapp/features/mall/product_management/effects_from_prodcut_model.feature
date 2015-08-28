#_author_:张三香

Feature:删除规格或规格值对商品的影响
"""
	#说明：
		#针对线上"bug3741"和"bug4257"补充feature
		#删除规格或规格值会导致使用该规格或规格值的商品下架(待售商品列表中：价格变为0,库存变为0)
		#创建如下商品数据
			#无规格:没有规格的商品
			#商品1：S
			#商品2：黑,白
			#商品3：黑M  白M
			#商品4: 白S
			#商品5：黑M 黑S 白M 白S
"""

Background:
	Given jobs登录系统
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
	And jobs已添加商品
		"""
		[{
			"name":"无规格",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 10.0,
						"weight": 10.0,
						"stock_type": "有限",
						"stocks": 10
					}
				}
			}
		},{
			"name": "商品1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"S": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
						}
				}
			}
		},{
			"name": "商品2",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"白色": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 M": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"白色 M": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name": "商品4",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"白色 S": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name": "商品5",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"白色 S": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"黑色 M": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					},
						"白色 M": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""

@wip.ob1 @product @property @toSaleProduct @online_bug
Scenario: 1 删除商品规格值'S'
	Given jobs登录系统
	When jobs删除商品规格'尺寸'的值'S'
	Then jobs能获取商品'商品1'
		"""
		{
			"name": "商品1",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	And jobs能获取商品'商品4'
		"""
		{
			"name": "商品4",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	And jobs能获取商品'商品5'
		"""
		[{
			"name": "商品5",
			"shelve_type": "下架",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 M": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
						},{
					"白色 M": {
						"price": 10.0,
						"weight": 1.0,
						"stock_type": "无限"
						}
					}
				}
			}
		}]
		"""

@product @property @toSaleProduct @online_bug
Scenario: 2 删除商品规格'颜色'
	Given jobs登录系统
	When jobs删除商品规格'颜色'
	Then jobs能获取商品'商品2'
		"""
		{
			"name":"商品2",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	And jobs能获取商品'商品3'
		"""
		{
			"name":"商品3",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	And jobs能获取商品'商品4'
		"""
		{
			"name":"商品4",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	And jobs能获取商品'商品5'
		"""
		{
			"name":"商品5",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""

@product @property @toSaleProduct @online_bug
Scenario: 3 删除商品规格值 '黑'和 'M'
	Given jobs登录系统
	When jobs删除商品规格'颜色'的值'黑'
	When jobs删除商品规格'尺寸'的值'M'
	Then jobs能获取商品'商品2'
		"""
		{
			"name":"商品2",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	Then jobs能获取商品'商品3'
		"""
		{
			"name":"商品3",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	Then jobs能获取商品'商品5'
		"""
			{
				"name": "商品5",
				"shelve_type": "下架",
				"is_enable_model": "启用规格",
				"model": {
					"models": {
						"白色 S": {
							"price":10.0,
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				}
			}
		"""

@product @property @toSaleProduct @online_bug
Scenario: 4 删除商品规格'颜色'和'尺寸'
	Given jobs登录系统
	When jobs删除商品规格'颜色'
	And jobs删除商品规格'尺寸'
	Then jobs能获取商品'商品1'
		"""
		{
			"name":"商品1",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	And jobs能获取商品'商品2'
		"""
		{
			"name":"商品2",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	And jobs能获取商品'商品3'
		"""
		{
			"name":"商品3",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	And jobs能获取商品'商品4'
		"""
		{
			"name":"商品4",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""
	And jobs能获取商品'商品5'
		"""
		{
			"name":"商品5",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 0.0,
						"weight": 0.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""

@product @property @toSaleProduct @online_bug
Scenario: 5 无规格商品修改成多规格后,再删除商品规格
	#无规格商品修改成多规格后，删除商品规格会导致:
		#商品下架,库存变为0,会保留无规格时的价格和重量
	Given jobs登录系统
	When jobs更新商品'无规格'
		"""
		{
			"name":"无规格",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色": {
						"price": 11.0,
						"weight": 11.0,
						"stock_type": "无限"
					},
					"白色": {
						"price": 11.0,
						"weight": 11.0,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	Then jobs能获取商品'无规格'
		"""
		{
			"name":"无规格",
			"shelve_type": "上架",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色": {
						"price": 11.0,
						"weight": 11.0,
						"stock_type": "无限"
					},
					"白色": {
						"price": 11.0,
						"weight": 11.0,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	When jobs删除商品规格'颜色'
	Then jobs能获取商品'无规格'
		"""
		{
			"name":"无规格",
			"shelve_type": "下架",
			"is_enable_model": "不启用规格",
			"model": {
				"models": {
					"standard": {
						"price": 10.0,
						"weight": 10.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}
		"""


