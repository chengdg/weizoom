# __author__ : 许韦

Feature: 新建微助力
	"""
		用户通微助力活动参与获得助力值和帮助好友增加助力值
		1.【活动名称】:必填项，不超过30个字符
		2.【活动时间】:必填项
		3.显示倒计时:勾选则在活动页面显示倒计时：图标：xx天xx时xx分xx秒
		4.【活动描述】:非必填项，不超过30个字符
		5.【参与活动回复语】:必填项，不超过5个字符，需在微信-自动回复创建该关键词
		6.【用户识别二维码】：非必填项，此处若空缺，则使用公众号二维码代替
		7.【分享图标】：必填项，建议图片长宽100px*100px，正方形图片
		8.【顶部背景图】：必填项，图片格式jpg/png, 图片宽度640px, 高度自定义, 请上传风格与背景配色协调的图片
		9.【背景配色】：冬日暖阳、玫瑰茜红、热带橙色
		10.【活动规则】：非必填项，不超过500个字符

	"""
Background:
	Given jobs登录系统
  	And jobs添加会员分组
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
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "感谢您的的参与，为好友助力成功！"
		}]
		"""
@apps @apps_powerme @apps_powerme_backend @kuki
Scenario:1 新建微助力，用户识别二维码为空
	Given jobs登录系统
	When jobs新建微助力活动
		"""
		[{
			"name":"微助力活动1",
			"start_date":"今天",
			"end_date":"3天后",
			"is_show_countdown":"true",
			"desc":"微助力活动描述",
			"reply":"微助力活动",
			"qr_code":"",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"冬日暖阳",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		}]
		"""
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"start_date":"今天",
			"end_date":"3天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","关闭"]
		}]
		"""

@apps @apps_powerme @apps_powerme_backend
Scenario:2 新建微助力，用户识别二维码非空
	Given jobs登录系统
	When jobs新建微助力活动
		"""
		[{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"is_show_countdown":"false",
			"desc":"微助力活动描述",
			"reply":"微助力活动",
			"qr_code":"带参数二维码1",
			"share_pic":"1.jpg",
			"background_pic":"2.jpg",
			"background_color":"热带橙色",
			"rules":"获奖条件必须要排名在100名以内<br />获奖名单将在什么时间点公布<br />奖品都有哪些内容<br />奖励的领取方式"
		}]
		"""
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"status":"未开始",
			"participant_count":0,
			"actions": ["查看","预览","复制链接","关闭"]
		}]
		"""