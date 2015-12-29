#_author_:张三香 2015.12.02

Feature:新建微信投票活动

@apps @vote
Scenario:1 新建微信投票活动,只添加'文本选项'模块,无奖励
	#活动权限-必须关注才可参与
	#奖励类型-无奖励
	#包含模块-2个文本选项模块
	#状态-进行中

	Given jobs登录系统
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票-文本选项",
			"subtitle":"微信投票01",
			"content":"微信投票文本选项内容",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type":"无奖励",
			"text_options":
				[{
					"title":"文本选项1",
					"single_or_multiple":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
						}]
				},{
					"title":"文本选项2",
					"single_or_multiple":"多选",
					"is_required":"否",
					"option":[{
							"options":"选项A"
						},{
							"options":"选项B"
						},{
							"options":"选项C"
						},{
							"options":"选项D"
						}]
				}]
		}]
		"""
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票-文本选项",
			"participant_count":0,
			"prize_type":"无奖励",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		}]
		"""

@apps @vote
Scenario:2 新建微信投票活动,只添加'图片选项'模块,无奖励
	#活动权限-必须关注才可参与
	#奖励类型-无奖励
	#包含模块-2个图片选项模块
	#状态-进行中

	Given jobs登录系统
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票-图片选项",
			"subtitle":"微信投票02",
			"content":"微信投票图片选项内容",
			"start_date":"今天",
			"end_date":"2天后",
			"permission":"必须关注才可参与",
			"prize_type":"无奖励",
			"pic_options":
				[{
					"title":"图片选项1",
					"single_or_multiple":"单选",
					"pic_show_type":"列表",
					"is_required":"是",
					"option":[{
						"options":{
							"pic":"1.jpg",
							"pic_desc":"图片描述1"
							},
						"options":{
							"pic":"2.jpg",
							"pic_desc":"图片描述2"
							},
						"options":{
							"pic":"3.jpg",
							"pic_desc":"图片描述3"
						}]
				},{
					"title":"图片选项2",
					"single_or_multiple":"多选",
					"pic_show_type":"表格",
					"is_required":"否",
					"option":[{
						"options":{
							"pic":"1.jpg",
							"pic_desc":"图片描述1"
							},
						"options":{
							"pic":"2.jpg",
							"pic_desc":"图片描述2"
							},
						"options":{
							"pic":"3.jpg",
							"pic_desc":"图片描述3"
						},
						"options":{
							"pic":"4.jpg",
							"pic_desc":"图片描述4"
						}]
				}]
		}]
		"""
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票-图片选项",
			"participant_count":0,
			"prize_type":"无奖励",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","链接","预览","统计","查看结果"]
		}]
		"""

@apps @vote
Scenario:3 新建微信投票活动,只添加'参与人信息'模块,积分奖励
	#活动权限-无需关注即可参与
	#奖励类型-积分
	#包含模块-1个参与人信息模块
	#状态-未开始

	Given jobs登录系统
	When jobs新建微信投票活动
		"""
		[{
			"title":"微信投票-参与人信息",
			"subtitle":"微信投票03",
			"content":"微信投票参与人信息内容",
			"start_date":"明天",
			"end_date":"2天后",
			"permission":"无需关注即可参与",
			"prize_type":"积分",
			"integral":20,
			"participate_info":[{
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
							"is_selected":"true"
						},{
							"item_name":"住址",
							"is_selected":"false"
						}],
				"items_add":[{
						"item_name":"填写项1",
						"is_required":"是"
					},{
						"item_name":"填写项2",
						"is_required":"否"
					}]
				}]
		}]
		"""
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"微信投票-参与人信息",
			"participant_count":0,
			"prize_type":"积分",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["删除","链接","预览","统计","查看结果"]
		}]
		"""

@apps @vote
Scenario:4 新建微信投票活动,添加多个模块,优惠券奖励
	#活动权限-必须关注才可参与
	#奖励类型-优惠券
	#包含模块-1个文本选项模块、1个图片选项模块和一个参与人信息模块
	#状态-已结束

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建微信投票活动
		"""
		[{
			"title":"多个模块微信投票",
			"subtitle":"微信投票04",
			"content":"多个模块微信投票内容",
			"start_date":"3天前",
			"end_date":"昨天",
			"permission":"必须关注才可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"text_options":
				[{
					"title":"选择题1",
					"single_or_multiple":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
						}]
				}],
			"pic_options":
				[{
					"title":"图片选项1",
					"single_or_multiple":"单选",
					"pic_show_type":"列表",
					"is_required":"是",
					"option":[{
						"options":{
							"pic":"1.jpg",
							"pic_desc":"图片描述1"
							},
						"options":{
							"pic":"2.jpg",
							"pic_desc":"图片描述2"
							},
						"options":{
							"pic":"3.jpg",
							"pic_desc":"图片描述3"
						}]
				}],
			"participate_info":[{
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
							"is_selected":"true"
						},{
							"item_name":"住址",
							"is_selected":"false"
						}],
				"items_add":[{
						"item_name":"填写项1",
						"is_required":"是"
					},{
						"item_name":"填写项2",
						"is_required":"否"
					}]
				}]
		}]
		"""
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"多个模块微信投票",
			"participant_count":0,
			"prize_type":"优惠券",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"actions": ["删除","链接","预览","统计","查看结果"]
		}]
		"""

@apps @vote
Scenario:5 新建微信投票活动,添加多个模块,优惠券奖励,标题相同
	#活动权限-必须关注才可参与
	#奖励类型-优惠券
	#包含模块-1个文本选项模块、1个图片选项模块和一个参与人信息模块
	#状态-进行中

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建微信投票活动
		"""
		[{
			"title":"多个模块微信投票",
			"subtitle":"微信投票05",
			"content":"多个模块微信投票内容",
			"start_date":"今天",
			"end_date":"明天",
			"permission":"必须关注才可参与",
			"prize_type":"优惠券",
			"coupon":"优惠券1",
			"text_options":
				[{
					"title":"相同的标题",
					"single_or_multiple":"单选",
					"is_required":"是",
					"option":[{
							"options":"1"
						},{
							"options":"2"
						},{
							"options":"3"
						},{
							"options":"4"
						}]
				}],
			"pic_options":
				[{
					"title":"相同的标题",
					"single_or_multiple":"单选",
					"pic_show_type":"列表",
					"is_required":"是",
					"option":[{
						"options":{
							"pic":"1.jpg",
							"pic_desc":"图片描述1"
							},
						"options":{
							"pic":"2.jpg",
							"pic_desc":"图片描述2"
							},
						"options":{
							"pic":"3.jpg",
							"pic_desc":"图片描述3"
						}]
				}],
			"participate_info":[{
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
							"is_selected":"true"
						},{
							"item_name":"住址",
							"is_selected":"false"
						}],
				"items_add":[{
						"item_name":"填写项1",
						"is_required":"是"
					},{
						"item_name":"填写项2",
						"is_required":"否"
					}]
				}]
		}]
		"""
	Then jobs获得微信投票活动列表
		"""
		[{
			"name":"多个模块微信投票",
			"participant_count":0,
			"prize_type":"优惠券",
			"start_date":"今天",
			"end_date":"明天",
			"status":"进行中",
			"actions": ["删除","链接","预览","统计","查看结果"]
		}]
		"""