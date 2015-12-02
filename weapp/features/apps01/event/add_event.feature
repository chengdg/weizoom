#_author_:王丽 2015.12.02

Feature: 应用和营销-活动报名
"""
	后台创建报名活动，前台会员确认参与活动报名，对参与活动的会员进行统计

	1 创建活动报名-活动信息
		【标题】：活动名称，必填；不能超过35个字符，超出部分自动截掉
		【副标题】：活动副标题；不能超过30个字符，超出部分自动截掉
		【内容】：富文本，可以添加连接：商品及分组、店铺主页、会员主页、购物车、营销推广、推广扫码、我的订单、签到
		【有效时间】：点击选择日期时间
		【活动权限】：两个选项："无需关注即可参与"和"必须关注才可参与"；默认"必须关注才可参与"
		【活动奖励】：三个选项：无奖励、积分、优惠券；优惠券可以选择到状态为"进行中"的所有优惠券
	2 创建活动报名-报名填写项设置
		1）默认有三项勾选：姓名、手机、邮箱；必填
		2）可选择勾选项：姓名、手机、邮箱、QQ、职位、住址
		3）点击"添加"按钮，在后面追加项目，设置"填写项"和"是否必填"；"是否必填"默认"否"
"""
		
@apps @event
Scenario:1 新建活动报名-无奖励
	Given jobs登录系统
	When jobs新建活动报名
		"""
		{
			"title":"活动报名-无奖励",
			"subtitle":"活动报名-副标题-无奖励",
			"content":"内容描述-无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"right":"必须关注才可参与",
			"prize_type": "无奖励",
			"items_select":[{
						"item_name":"姓名",
						"is_selected":true
					},{
						"item_name":"手机",
						"is_selected":true
					},{
						"item_name":"邮箱",
						"is_selected":true
					},{
						"item_name":"QQ",
						"is_selected":true
					},{
						"item_name":"职位",
						"is_selected":false
					},{
						"item_name":"住址",
						"is_selected":false
					}],
			"items_add":[{
						"item_name":"其他",
						"is_required":"false"
					}]
		}
		"""
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-无奖励",
			"part_num": 0,
			"prize_type": "无奖励",
			"start_date":"明天",
			"end_date":"2天后",
			"status":"未开始",
			"actions": ["预览","查看结果"]
		}]
		"""

@apps @event
Scenario:2 新建活动报名-积分
	Given jobs登录系统
	When jobs新建活动报名
		"""
		{
			"title":"活动报名-积分",
			"subtitle":"活动报名-副标题-积分",
			"content":"内容描述-积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"right":"必须关注才可参与",
			"prize_type": "积分",
			"integral": 50,
			"items_select":[{
						"item_name":"姓名",
						"is_selected":true
					},{
						"item_name":"手机",
						"is_selected":true
					},{
						"item_name":"邮箱",
						"is_selected":false
					},{
						"item_name":"QQ",
						"is_selected":false
					},{
						"item_name":"职位",
						"is_selected":false
					},{
						"item_name":"住址",
						"is_selected":false
					}],
			"items_add":[{
						"item_name":"店铺类型",
						"is_required":"true"
					},{
						"item_name":"开店时间",
						"is_required":"true"
					}]
		}
		"""
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-积分",
			"part_num": 0,
			"prize_type": "积分",
			"start_date":"1天前",
			"end_date":"2天后",
			"status":"进行中",
			"actions": ["关闭","预览","查看结果"]
		}]
		"""

@apps @event
Scenario:3 新建活动报名-优惠券
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
		{
			"title":"活动报名-优惠券",
			"subtitle":"活动报名-副标题-优惠券",
			"content":"内容描述-优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"right":"无需关注即可参与",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"items_select":[{
						"item_name":"姓名",
						"is_selected":true
					},{
						"item_name":"手机",
						"is_selected":true
					},{
						"item_name":"邮箱",
						"is_selected":false
					},{
						"item_name":"QQ",
						"is_selected":false
					},{
						"item_name":"职位",
						"is_selected":false
					},{
						"item_name":"住址",
						"is_selected":true
					}],
			"items_add":[{
						"item_name":"店铺类型",
						"is_required":"true"
					},{
						"item_name":"开店时间",
						"is_required":"true"
					}]
		}
		"""
	Then jobs获得活动报名列表
		"""
		[{
			"name":"活动报名-优惠券",
			"part_num": 0,
			"prize_type": "优惠券",
			"start_date":"3天前",
			"end_date":"1天前",
			"status":"已结束",
			"actions": ["删除","预览","查看结果"]
		}]
		"""
