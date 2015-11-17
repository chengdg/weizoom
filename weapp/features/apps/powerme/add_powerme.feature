#_author_:张三香 2015.11.16

Feature: 新建微助力
"""
	说明：
	活动名称：必填项，字数不超过30个字
	活动时间：必填项
	显示倒计时：勾选则在活动页面显示倒计时:图标:xx天xx时xx分xx秒
	活动描述：非必填项，字数不超过30个字
	参与活动回复语:必填项，需再微信-自动回复中创建该关键词
	用户识别二维码：非必填项,此处若空缺，则使用公众号二维码代替
	分享图标：必填项,建议图片长宽100px*100px，正方形图片
	顶部背景图片:必填项,图片格式jpg/png, 图片宽度640px, 高度自定义, 请上传风格与背景配色协调的图片
	背景配色：冬日暖阳，玫瑰茜红，热带橙色
	活动规则：非必填项，字数不超过300字
"""
Background:
	Given jobs登录系统
	When jobs已添加单图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
		}]
		"""
	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"规则1",
			"keyword": [{
					"keyword": "微助力1",
					"type": "equal"
				}],
			"keyword_reply": [{
					 "reply_content":"关键字回复内容1",
					 "reply_type":"text"
				}]
		},{
			"rules_name":"规则2",
			"keyword": [{
					"keyword": "微助力2",
					"type": "equal"
				}],
			"keyword_reply": [{
					"reply_type":"text_picture",
					"reply_content":"图文1"
		}]
		"""

@apps @powerme
Scenario:1 新建微助力,用户识别二维码为空
	Given jobs登录系统
	When jobs新建微助力
		"""
		[{
			"name":"微助力活动1",
			"start_date":"今天",
			"end_date":"3天后",
			"is_show_countdown":"true",
			"reply":"微助力1",
			"desc":"微助力活动描述",
			"qr_code":"",
			"share_pic":"1.jpg",
			"background_pic":"11.jpg",
			"background_color":"冬日暖阳",
			"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打"
		}]
		"""
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动1",
			"start_date":"今天",
			"end_date":"3天后",
			"status":"进行中",
			"parti_person_cnt":0,
			"actions": ["查看","预览","复制链接","关闭"]
		}]
		"""

@apps @powerme
Scenario:2 新建微助力,用户识别二维码非空
	Given jobs登录系统
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "微助力二维码",
			"create_time": "今天",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "立即参加"
		}]
		"""
	When jobs新建微助力
		"""
		[{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"is_show_countdown":"false",
			"reply":"微助力2",
			"desc":"微助力活动描述",
			"qr_code":"微助力二维码",
			"share_pic":"1.jpg",
			"background_pic":"11.jpg",
			"background_color":"热带橙色",
			"rules":"按上按上打算四大的撒的撒<br />撒打算的撒的撒大声地<br />按上打算打算<br />阿萨德按上打"
		}]
		"""
	Then jobs获得微助力活动列表
		"""
		[{
			"name":"微助力活动2",
			"start_date":"明天",
			"end_date":"3天后",
			"status":"未开始",
			"parti_person_cnt":0,
			"actions": ["查看","预览","复制链接","关闭"]
		}]
		"""