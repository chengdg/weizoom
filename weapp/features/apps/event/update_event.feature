#_author_:王丽 2015.12.03

Feature:更新活动报名
	"""
	1、未开始状态的活动报名可以进行编辑并保存，进行中和已结束状态的不能进行更改；
	2、不同状态的活动报名，对应的操作列按钮不同:
		未开始:【链接】【预览】【查看结果】
		进行中:【关闭】【链接】【预览】【查看结果】
		已结束:【删除】【链接】【预览】【查看结果】
	3、进行中的活动报名可以进行'关闭'操作，关闭后结束时间会随之更改为关闭时的时间，状态变为'已结束'
	4、已结束状态的活动报名，可以进行'删除'操作
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 10,
			"limit_counts": 3,
			"start_date": "4天前",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建活动报名
		"""
		[{
			"title":"活动报名-无奖励",
			"subtitle":"活动报名-副标题-无奖励",
			"content":"内容描述-无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type": "无奖励",
			"items_select":[{
						"item_name":"姓名",
						"is_selected":"true"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"true"
					},{
						"item_name":"QQ",
						"is_selected":"true"
					},{
						"item_name":"职位",
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"false"
					}],
			"items_add":[{
						"item_name":"其他",
						"is_required":"false"
					}]
		},{
			"title":"活动报名-积分",
			"subtitle":"活动报名-副标题-积分",
			"content":"内容描述-积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type": "积分",
			"integral": 50,
			"items_select":[{
						"item_name":"姓名",
						"is_selected":"true"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"false"
					},{
						"item_name":"QQ",
						"is_selected":"false"
					},{
						"item_name":"职位",
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"false"
					}],
			"items_add":[{
						"item_name":"店铺类型",
						"is_required":"true"
					},{
						"item_name":"开店时间",
						"is_required":"true"
					}]
		},{
			"title":"活动报名-优惠券",
			"subtitle":"活动报名-副标题-优惠券",
			"content":"内容描述-优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"permission":"无需关注即可参与",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"items_select":[{
						"item_name":"姓名",
						"is_selected":"true"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"false"
					},{
						"item_name":"QQ",
						"is_selected":"false"
					},{
						"item_name":"职位",
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"true"
					}],
			"items_add":[{
						"item_name":"店铺类型",
						"is_required":"true"
					},{
						"item_name":"开店时间",
						"is_required":"true"
					}]
		}]
		"""

@apps @event @update_event
Scenario:1 编辑'未开始'状态的活动报名
	Given jobs登录系统
	When jobs编辑活动报名活动'活动报名-无奖励'
		"""
		[{
			"title":"活动报名-无奖励2",
			"subtitle":"活动报名-副标题-无奖励2",
			"content":"内容描述-无奖励2",
			"start_date":"1天后",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type": "积分",
			"integral":20,
			"items_select":[{
						"item_name":"姓名",
						"is_selected":"false"
					},{
						"item_name":"手机",
						"is_selected":"true"
					},{
						"item_name":"邮箱",
						"is_selected":"true"
					},{
						"item_name":"QQ",
						"is_selected":"true"
					},{
						"item_name":"职位",
						"is_selected":"false"
					},{
						"item_name":"住址",
						"is_selected":"false"
					}],
			"items_add":[{
						"item_name":"其他",
						"is_required":"true"
					}]
		}]
		"""
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-优惠券",
			"participant_count": 0,
			"prize_type": "优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"status":"已结束",
			"actions": ["删除","链接","预览","查看结果"]
		},{
			"name":"活动报名-积分",
			"participant_count": 0,
			"prize_type": "积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","查看结果"]
		},{
			"name":"活动报名-无奖励2",
			"participant_count": 0,
			"prize_type": "积分",
			"start_date":"1天后",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["链接","预览","查看结果"]
		}]
		"""

@apps @event @update_event
Scenario:2 关闭'进行中'状态的活动报名
	Given jobs登录系统
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-优惠券",
			"participant_count": 0,
			"prize_type": "优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"status":"已结束",
			"actions": ["删除","链接","预览","查看结果"]
		},{
			"name":"活动报名-积分",
			"participant_count": 0,
			"prize_type": "积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","查看结果"]
		},{
			"name":"活动报名-无奖励",
			"participant_count": 0,
			"prize_type": "无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["链接","预览","查看结果"]
		}]
		"""
	When jobs关闭活动报名'活动报名-积分'
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-优惠券",
			"participant_count": 0,
			"prize_type": "优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"status":"已结束",
			"actions": ["删除","链接","预览","查看结果"]
		},{
			"name":"活动报名-积分",
			"participant_count": 0,
			"prize_type": "积分",
			"start_date":"1天前",
			"end_date":"今天",
			"status":"已结束",
			"actions": ["删除","链接","预览","查看结果"]
		},{
			"name":"活动报名-无奖励",
			"participant_count": 0,
			"prize_type": "无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["链接","预览","查看结果"]
		}]
		"""

@apps @event @update_event
Scenario:3 删除'已结束'状态的活动报名
	Given jobs登录系统
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-优惠券",
			"participant_count": 0,
			"prize_type": "优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"status":"已结束",
			"actions": ["删除","链接","预览","查看结果"]
		},{
			"name":"活动报名-积分",
			"participant_count": 0,
			"prize_type": "积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","查看结果"]
		},{
			"name":"活动报名-无奖励",
			"participant_count": 0,
			"prize_type": "无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["链接","预览","查看结果"]
		}]
		"""
	When jobs关闭活动报名'活动报名-积分'
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-优惠券",
			"participant_count": 0,
			"prize_type": "优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"status":"已结束",
			"actions": ["删除","链接","预览","查看结果"]
		},{
			"name":"活动报名-积分",
			"participant_count": 0,
			"prize_type": "积分",
			"start_date":"1天前",
			"end_date":"今天",
			"status":"已结束",
			"actions": ["删除","链接","预览","查看结果"]
		},{
			"name":"活动报名-无奖励",
			"participant_count": 0,
			"prize_type": "无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["链接","预览","查看结果"]
		}]
		"""

	When jobs删除百宝箱活动报名'活动报名-积分'
	When jobs删除百宝箱活动报名'活动报名-优惠券'
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-无奖励",
			"participant_count": 0,
			"prize_type": "无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["链接","预览","查看结果"]
		}]
		"""
