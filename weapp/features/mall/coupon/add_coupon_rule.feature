#author: 冯雪静
#editor: 张三香 2015.10.15
#editor: 王丽 2016.04.15

Feature: 添加优惠券规则
	Jobs能通过管理系统添加"优惠券规则"
	"""
		补充_2015.10.15:
			1.单商品支持添加多个单品优惠券
			2.商品下架、修改后对优惠券无影响，各个模块均可选择该优惠券且优惠券管理处优惠券不为失效状态，添加劵码可继续使用。
			3.禁止优惠券商品与创建单品券无关
			4.单品优惠券选择商品时,'已参与促销'字段显示规则：
				a.此商品参与了促销活动，那么显示促销的活动名称
				b.此商品被设置了单品优惠券，不管设置了多少单品优惠券，已参与促销的地方都显示'单品券'三个字

		补充需求修改 2016.04.15
		1 单品券修改成"多商品券"，新建优惠券，"优惠券类型"修改成["全店通用"和"部分商品"]
		2 新建优惠券选择"部分商品",点击"添加"，弹出选择"已上架商品"和"商品分组"的弹窗
			（1）"已上架商品"页签
				【商品条码】：商品详情中的"商品条码"
				【商品名称】：商品详情中的"商品名称"
				【商品价格(元)】：商品详情中的"商品价格"
				【商品库存】：商品详情中的"商品库存"
				【以参与促销】：参与一个或多个"多商品券"的，显示"多商品券"；参与其他促销活动的，直接显示"促销活动名称"
				【操作】："选取"或者空；参与"多商品券"活动的商品，为"选取"，可以被选择；参与其他促销活动的，为空，不能选择
				搜索框：模糊匹配
				待售商品列表商品，按照商品的添加时间，正序排列

			（2）"商品分组"页签
				【标题】：商品分组名称
				【创建时间】：商品分组创建时间
				【操作】："选取"；
			(3)“已上架商品”与“商品分组”为“多选”，可以混合选择，在分页间多选，切换页签，保留之前的选择；选择后，将选择的商品和选择的分组内的商品进行去重，带入优惠券商品列表
		3 保存新建优惠券，对多商品券的商品进行校验，存在不符合下面条件的商品给我出提示"部分商品已发生其他操作，请查证后再操作",对应商品在多商品券商品列表中的"删除"列标红
		4 优惠券中的商品状态发生变，下架或者删除，优惠券活动详情中，商品列表商品状态对应发生变化，标记"已下架"或"已删除"
	"""

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		},{
			"name": "商品2",
			"price": 200.00
		},{
			"name": "商品3",
			"price": 200.00
		}]
		"""

@promotion @promotionCoupon @ztqb
Scenario:1 添加优惠券规则-添加通用券
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "全店通用券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	Then jobs获得优惠券规则'全店通用券1'
		"""
		{
			"name": "全店通用券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明"
		}
		"""

@promotion @promotionCoupon
Scenario:2 添加优惠券规则-多商品券(一个商品)
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "多商品券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "商品1",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	Then jobs获得优惠券规则'多商品券1'
		"""
		{
			"name": "多商品券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "商品1",
			"products_status":[{
				"name": "商品1",
				"status": ""
				}],
			"coupon_id_prefix": "coupon1_id_"
		}
		"""

@promotion @promotionCoupon
Scenario:3 添加优惠券规则-多商品券(多个商品)
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "多商品券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "商品1,商品2,商品3",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	Then jobs获得优惠券规则'多商品券1'
		"""
		{
			"name": "多商品券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "商品1,商品2,商品3",
			"products_status":[{
				"name": "商品1",
				"status": ""
				},{
				"name": "商品2",
				"status": ""
				},{
				"name": "商品3",
				"status": ""
			}],
			"coupon_id_prefix": "coupon1_id_"
		}
		"""

@promotion @promotionCoupon
Scenario:4 添加多商品券-多个商品中保存时有不符合条件的商品，给出错误提示
	Given jobs登录系统

	#下架商品
	When jobs'下架'商品'商品1'
	When jobs添加优惠券规则
		"""
		[{
			"name": "多商品券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "商品1,商品2,商品3",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	Then jobs获得优惠券规则添加失败提示'部分商品已发生其他操作，请查证后再操作'

	#删除商品
	When jobs'上架'商品'商品1'
	When jobs'删除'商品'商品2'
	When jobs添加优惠券规则
		"""
		[{
			"name": "多商品券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "商品1,商品2,商品3",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	Then jobs获得优惠券规则添加失败提示'部分商品已发生其他操作，请查证后再操作'

	#添加优惠券的商品参与了其他与优惠券互斥的活动
	When jobs创建限时抢购活动
		"""
		[{
			"name": "商品3限时抢购",
			"promotion_title":"",
			"start_date": "今天",
			"end_date": "5天后",
			"product_name":"商品1",
			"member_grade": "全部会员",
			"count_per_purchase":"",
			"promotion_price": 80.00,
			"limit_period":"",
			"count_per_period":1
		}]
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "多商品券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "商品1,商品3",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	Then jobs获得优惠券规则添加失败提示'部分商品已发生其他操作，请查证后再操作'
