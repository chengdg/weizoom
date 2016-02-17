#_author_:张三香 2015.11.23

Feature:更新微助力活动
	"""
		1 编辑微助力活动:只能编辑'未开始'状态的，'进行中'和'已结束'状态的不能进行编辑

		2 删除微助力活动:只能删除'已结束'状态的，'未开始'和'进行中'的不能进行删除

		3 关闭微助力活动:'未开始'和'进行中'状态的活动可以进行关闭

	"""

Background:
	Given jobs登录系统
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		},{
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}]
		"""
	When jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1"
		}
		"""
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码1",
			"create_time": "2015-10-10 10:20:30",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "分组1",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "感谢您的的参与，为好友助力成功！"
		}]
		"""
	When jobs新建微助力活动
		"""
		[{
			"name":"微助力活动1",
			"start_date":"3天前",
			"end_date":"昨天",
			"is_show_countdown":"false",
			"desc":"微助力活动描述1",
			"reply":"微助力活动",
			"qr_code":"带参数二维码1",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"冬日暖阳",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		},{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"is_show_countdown":"ture",
			"desc":"微助力活动描述2",
			"reply":"微助力活动",
			"qr_code":"",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"玫瑰茜红",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		},{
			"name":"微助力活动3",
			"start_date":"今天",
			"end_date":"3天后",
			"is_show_countdown":"false",
			"desc":"微助力活动描述3",
			"reply":"微助力活动",
			"qr_code":"",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"热带橙色",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		}]
		"""

@mall2 @apps @apps_powerme @apps_powerme_backend @update_powerme
Scenario:1 编辑'未开始'的微助力活动
	Given jobs登录系统
	When jobs编辑微助力活动'微助力活动2'
		"""
		[{
			"name":"微助力活动02",
			"start_date":"今天",
			"end_date":"2天后",
			"is_show_countdown":"false",
			"desc":"微助力活动描述02",
			"reply":"微助力活动02",
			"qr_code":"带参数二维码1",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"热带橙色",
			"rules":"1获奖条件必须要排名在100名以内<br />2获奖名单将在什么时间点公布<br />3奖品都有哪些内容<br />奖励的领取方式"
		}]
		"""
	Then jobs获得微助力活动'微助力活动02'
		"""
		[{
			"name":"微助力活动02",
			"start_date":"今天",
			"end_date":"2天后",
			"is_show_countdown":"false",
			"desc":"微助力活动描述02",
			"reply":"微助力活动02",
			"qr_code":"带参数二维码1",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"热带橙色",
			"rules":"1获奖条件必须要排名在100名以内<br />2获奖名单将在什么时间点公布<br />3奖品都有哪些内容<br />奖励的领取方式"
		}]
		"""
	And jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动3",
			"start_date":"今天",
			"end_date":"3天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","关闭"]
		},{
			"name":"微助力活动02",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","关闭"]
		},{
			"name":"微助力活动1",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","删除"]
		}]
		"""

@mall2 @apps @apps_powerme @apps_powerme_backend @update_powerme
Scenario:2 删除'已结束'的微助力活动
	Given jobs登录系统
	When jobs删除微助力活动'微助力活动1'
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动3",
			"start_date":"今天",
			"end_date":"3天后",
			"status":"进行中",
			"participant_count":0,
			"actions":  ["查看","预览","复制链接","关闭"]
		},{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"status":"未开始",
			"participant_count":0,
			"actions":  ["查看","预览","复制链接","关闭"]
		}]
		"""

@mall2 @apps @apps_powerme @apps_powerme_backend @update_powerme
Scenario:3 关闭'未开始'或'进行中'的微助力活动
	Given jobs登录系统
	#关闭'未开始'状态的微助力活动
	When jobs关闭微助力活动'微助力活动2'
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动3",
			"start_date":"今天",
			"end_date":"3天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","关闭"]
		},{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"今天",
			"status":"已结束",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","删除"]
		},{
			"name":"微助力活动1",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","删除"]
		}]
		"""
	#关闭'进行中'状态的微助力活动
	When jobs关闭微助力活动'微助力活动3'
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动3",
			"start_date":"今天",
			"end_date":"今天",
			"status":"已结束",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","删除"]
		},{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"今天",
			"status":"已结束",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","删除"]
		},{
			"name":"微助力活动1",
			"start_date":"3天前",
			"end_date":"昨天",
			"status":"已结束",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","删除"]
		}]
		"""