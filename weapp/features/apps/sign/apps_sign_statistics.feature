# __author__ : 王丽 2015-11-25

Feature: 签到-后台签到统计
"""
	列表展示参与签到活动的会员的相关参与信息
	1 列表展示签到的会员，默认按照会员的"最后一次签到时间"倒叙排列；
		可以按照"第一次签到"、"最后一次签到"、"累计次数"、"连续次数"、"最高连续次数"、"奖励总积分"字段进行手动排序
	2【会员】：该会员的头像和会员昵称，会员昵称全部显示，不折行
	3【第一次签到】：该会员第一次签到的时间；精确到秒（例：2015/11/25 10:25:21）
	4【最后一次签到】：该会员最后一次签到的时间；精确到秒（例：2015/11/25 10:25:21）
	5【累计次数】：该会员累计签到的次数
	6【连续次数】：该会员目前最后一次的连续签到天数
	7【最高连续次数】：该会员连续签到天数最大值
	8【奖励总积分】：该会员签到获得的总积分数
	9【优惠券奖励】：该会员最近三次获得优惠券奖励的优惠券名称
"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 10.00,
			"limit_counts": "无限",
			"start_date": "1天前",
			"end_date": "3天后",
			"coupon_id_prefix": "coupon1_id_"
		},{
			"name": "优惠券2",
			"money": 20.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon2_id_"
		},{
			"name": "优惠券M",
			"money": 20.00,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""
	Given jobs添加签到活动"签到活动1",并且保存
		"""
		{
			"status": "off",
			"name": "签到活动1",
			"sign_describe": "签到赚积分！连续签到奖励更丰富哦！",
			"share_pic": "1.jpg",
			"share_describe": "签到送好礼！",
			"reply_content": "每日签到获得20积分,连续签到奖励更丰富哦！",
			"reply_keyword":
				[{
					"rule": "精确",
					"key_word": "签到"
				}],
			"sign_settings":
				[{
					"sign_in": "0",
					"integral": "20"
				},{
					"sign_in":"2",
					"send_coupon":"优惠券M"
				},{
					"sign_in":"3",
					"send_coupon":"优惠券1"
				},{
					"sign_in":"5",
					"integral": "10",
					"send_coupon":"优惠券2"
				}]
		}
		"""
	When jobs更新签到活动的状态
		"""
		{
			"name":"签到活动1",
			"status": "on"
		}
		"""

	Given bill关注jobs的公众号
	And tom关注jobs的公众号
	And marry关注jobs的公众号
	And jack关注jobs的公众号
	And nokia关注jobs的公众号

	#会员签到

	#bill先连续签到5次，终止一天，再连续签到3次
		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-01 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-02 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-03 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-04 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-05 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-07 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-08 10:30:00'

		When 清空浏览器
		When bill访问jobs的webapp
		When bill在微信中向jobs的公众号发送消息'签到'于'2015-10-09 10:30:00'

	#tom先签到1次，终止一天，再连续签到2次
		When 清空浏览器
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'签到'于'2015-10-03 10:30:00'

		When 清空浏览器
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'签到'于'2015-10-05 10:30:00'

		When 清空浏览器
		When tom访问jobs的webapp
		When tom在微信中向jobs的公众号发送消息'签到'于'2015-10-06 10:30:00'

	#marry先签到1次，终止一天，再连续签到3次, 再终止两天，再签到一次
		When 清空浏览器
		When marry访问jobs的webapp
		When marry在微信中向jobs的公众号发送消息'签到'于'2015-10-04 10:30:00'

		When 清空浏览器
		When marry访问jobs的webapp
		When marry在微信中向jobs的公众号发送消息'签到'于'2015-10-06 10:30:00'

		When 清空浏览器
		When marry访问jobs的webapp
		When marry在微信中向jobs的公众号发送消息'签到'于'2015-10-07 10:30:00'

		When 清空浏览器
		When marry访问jobs的webapp
		When marry在微信中向jobs的公众号发送消息'签到'于'2015-10-08 10:30:00'

		When 清空浏览器
		When marry访问jobs的webapp
		When marry在微信中向jobs的公众号发送消息'签到'于'2015-10-11 10:30:00'

	#jack签到1次
		When 清空浏览器
		When jack访问jobs的webapp
		When jack在微信中向jobs的公众号发送消息'签到'于'2015-10-12 10:30:00'

	#nokia签到1次,终止两天，再签到一次
		When 清空浏览器
		When nokia访问jobs的webapp
		When nokia在微信中向jobs的公众号发送消息'签到'于'2015-10-10 10:30:00'

		When 清空浏览器
		When nokia访问jobs的webapp
		When nokia在微信中向jobs的公众号发送消息'签到'于'2015-10-13 10:30:00'

@mall2 @apps_sign @apps_sign_backend @sign_statistics
Scenario:1 会员签到统计列表
	Given jobs登录系统

	Then jobs获得会员签到统计列表
		| name |     first_sign      |       last_sign     | total_sign | continuous_sign | max_continuous_sign | integral |       coupon            |
		| nokia| 2015/10/10 10:30:00 | 2015/10/13 10:30:00 |      2     |         1       |         0           |     40   |                         |
		| jack | 2015/10/12 10:30:00 | 2015/10/12 10:30:00 |      1     |         1       |         0           |     20   |                         |
		| marry| 2015/10/04 10:30:00 | 2015/10/11 10:30:00 |      5     |         1       |         3           |     60   | 优惠券1<br>优惠券M         |
		| bill | 2015/10/01 10:30:00 | 2015/10/09 10:30:00 |      8     |         3       |         5           |     70   | 优惠券1<br>优惠券M<br>优惠券2 |
		| tom  | 2015/10/03 10:30:00 | 2015/10/06 10:30:00 |      3     |         2       |         2           |     40   | 优惠券M                 |

@mall2 @apps_sign @apps_sign_backend @sign_statistics
Scenario:2 会员签到统计列表分页
	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	#列表共3页
	When jobs访问签到统计第'1'页
	Then jobs获得会员签到统计列表
		| name |     first_sign      |       last_sign     | total_sign | continuous_sign | max_continuous_sign | integral |       coupon            |
		| nokia| 2015/10/10 10:30:00 | 2015/10/13 10:30:00 |      2     |         1       |         0           |     40   |                         |
		| jack | 2015/10/12 10:30:00 | 2015/10/12 10:30:00 |      1     |         1       |         0           |     20   |                         |
  	When jobs访问签到统计列表下一页
	Then jobs获得会员签到统计列表
		| name |     first_sign      |       last_sign     | total_sign | continuous_sign | max_continuous_sign | integral |       coupon            |
		| marry| 2015/10/04 10:30:00 | 2015/10/11 10:30:00 |      5     |         1       |         3           |     60   | 优惠券1<br>优惠券M         |
		| bill | 2015/10/01 10:30:00 | 2015/10/09 10:30:00 |      8     |         3       |         5           |     70   | 优惠券1<br>优惠券M<br>优惠券2 |
  	When jobs访问签到统计第'3'页
	Then jobs获得会员签到统计列表
		| name |     first_sign      |       last_sign     | total_sign | continuous_sign | max_continuous_sign | integral |       coupon            |
		| tom  | 2015/10/03 10:30:00 | 2015/10/06 10:30:00 |      3     |         2       |         2           |     40   | 优惠券M                 |
	When jobs访问签到统计列表上一页
	Then jobs获得会员签到统计列表
		| name |     first_sign      |       last_sign     | total_sign | continuous_sign | max_continuous_sign | integral |       coupon            |
		| marry| 2015/10/04 10:30:00 | 2015/10/11 10:30:00 |      5     |         1       |         3           |     60   | 优惠券1<br>优惠券M         |
		| bill | 2015/10/01 10:30:00 | 2015/10/09 10:30:00 |      8     |         3       |         5           |     70   | 优惠券1<br>优惠券M<br>优惠券2 |
