#editor:王丽 2015.10.13

Feature: 管理在售商品
	"""
		Jobs能通过管理系统管理商城中的"在售商品列表"
	"""

Background:
	Given jobs登录系统
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
			"name": "东坡肘子",
			"categories": "分类1,分类2,分类3",
			"model": {
				"models": {
					"standard": {
						"user_code": "1",
						"price": 11.0,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"categories": "分类1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 M": {
						"user_code": "2",
						"price": 8.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.2,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.1,
						"stock_type": "无限"
					}
				}
			}
		}]	
		"""

@mall2 @product @saleingProduct   @mall @mall.product_category
Scenario:1 浏览在售商品
	Given jobs登录系统
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"categories": [],
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.1,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"is_enable_model": "启用规格",
			"categories": ["分类1"],
			"model": {
				"models": {
					"黑色 M": {
						"user_code": "2",
						"price": 8.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.2,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "东坡肘子",
			"is_enable_model": "不启用规格",
			"categories": ["分类1", "分类2", "分类3"],
			"model": {
				"models": {
					"standard": {
						"user_code": "1",
						"price": 11.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	
@mall2 @product @saleingProduct   @mall @mall.product_category
Scenario:2 下架商品
	jobs进行'批量下架'或'单个下架'后
	1. jobs的待售商品列表发生变化
	2. jobs的在售商品列表发生变化

	Given jobs登录系统
	When jobs'下架'商品'东坡肘子'
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "东坡肘子"
		}]
		"""
	When jobs批量下架商品
		"""
		[
			"水晶虾仁", 
			"叫花鸡"
		]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "东坡肘子"
		}]
		"""

@product @saleingProduct
Scenario:3 修改商品价格
	Given jobs登录系统
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"categories": [],
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.1,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"is_enable_model": "启用规格",
			"categories": ["分类1"],
			"model": {
				"models": {
					"黑色 M": {
						"user_code": "2",
						"price": 8.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.2,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "东坡肘子",
			"is_enable_model": "不启用规格",
			"categories": ["分类1", "分类2", "分类3"],
			"model": {
				"models": {
					"standard": {
						"user_code": "1",
						"price": 11.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When jobs修改商品'水晶虾仁'的价格为
		"""
		[{
			"price": 7.0
		}]
		"""
	When jobs修改商品'东坡肘子'的价格为
		"""
		[{
			"price": 14.0
		}]
		"""
	When jobs修改商品'叫花鸡'的价格为
		"""
		[{
			"user_code": "2",
			"price": 8.0,
			"stock_type": "有限",
			"stocks": 3
		}, {
			"user_code": "3",
			"price": 8.0,
			"stock_type": "有限",
			"stocks": 2
		}]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"categories": [],
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.0,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"is_enable_model": "启用规格",
			"categories": ["分类1"],
			"model": {
				"models": {
					"黑色 M": {
						"user_code": "2",
						"price": 8.0,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.0,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "东坡肘子",
			"is_enable_model": "不启用规格",
			"categories": ["分类1", "分类2", "分类3"],
			"model": {
				"models": {
					"standard": {
						"user_code": "1",
						"price": 14.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When jobs查看商品'叫花鸡'的规格为
		"""
		[{
			"name": "黑色 M",
			"user_code": "2",
			"price": 8.0,
			"stocks": 3
		}, {
			"name": "白色 M",
			"user_code": "3",
			"price": 8.0,
			"stocks": 2
		}]
		"""
