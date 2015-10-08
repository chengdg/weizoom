#_author_:王丽

Feature:推广扫码
"""
	在系统中【推广扫码】建立推广扫码规则，在系统可以设置链接的地方，将此链接分享给系统中会员，
	会员打开链接得到一个带有会员自己信息的店铺公众账号的二维码，会员邀请其他的微信用户扫此二维码，
	关注店铺的公众账号，并成为店铺的会员，这样推广的会员就会得到【推广扫码】模块设置的对应的奖励

	1、【推广扫码】设置
		（1）奖品类型：
			【无】：没有任何奖励
			【优惠券】：下拉选择本店铺状态为"进行中""未开始"的优惠券
			【积分】：输入相应的积分奖励数值；输入的积分必须是整数
		（2）页面描述：显示在手机端页面，二维码下面
						文本编辑框（多功能）：文本编辑框，有添加链接，
						添加链接的列表：微页面、商品及分组、店铺主页、会员主页、
										营销推广、推广扫码、我的订单
"""

Background:
	Given jobs登录系统

	When jobs已添加关键词自动回复规则
		"""
		[{
			"rules_name":"推广扫码",
			"keyword": [{
					"keyword": "我的推广码",
					"type": "equal"
				}],
			"keyword_reply": [{
					 "reply_content":"推广扫码链接",
					 "reply_type":"text"
				}]
		}]
		"""

Scenario:1 无奖励

	Given jobs登录系统

	When jobs创建推广扫码
		"""
		{
			"prize_type":"无",
			"page_description":"无奖励，页面描述文本"
		}
		"""
	Then jobs获得推广扫码
		"""
		{
			"prize_type":"无",
			"page_description":"无奖励，页面描述文本"
		}
		"""

	#推广扫码验证
	When 清空浏览器
	When bill关注jobs的公众号
	When bill在微信中向jobs的公众号发送消息'我的推广码'
	Then bill收到自动回复'推广扫码链接'

	When bill进入链接'推广扫码链接'
	Then bill获得'bill'的推广码
		"""
		{
			"spreading_code":"bill的推广码",
			"page_description":"无奖励，页面描述文本"
		}
		"""

	When tom扫码'bill'的推广码关注jobs的公众号

	Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |   今天            | 直接关注 |             |
			| tom   |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |   今天            | 推广扫码 |             |

Scenario:2 积分奖励

	Given jobs登录系统

	When jobs创建推广扫码
		"""
		{
			"prize_type":"积分",
			"integral":10,
			"page_description":"积分奖励，页面描述文本"
		}
		"""
	Then jobs获得推广扫码
		"""
		{
			"prize_type":"积分",
			"integral":10,
			"page_description":"积分奖励，页面描述文本"
		}
		"""

	#推广扫码验证
	When 清空浏览器
	When bill关注jobs的公众号
	When bill在微信中向jobs的公众号发送消息'我的推广码'
	Then bill收到自动回复'推广扫码链接'

	When bill进入链接'推广扫码链接'
	Then bill获得'bill'的推广码
		"""
		{
			"spreading_code":"bill的推广码",
			"page_description":"积分奖励，页面描述文本"
		}
		"""

	When tom扫码'bill'的推广码关注jobs的公众号

	Given jobs登录系统
	Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       1      |     10   |   0.00    |    0.00    |      0    |   今天            | 直接关注 |             |
			| tom   |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |   今天            | 推广扫码 |             |

Scenario:3 优惠券奖励

	Given jobs登录系统

	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 2,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

	When jobs创建推广扫码
		"""
		{
			"prize_type":"优惠券",
			"coupon":优惠券1,
			"page_description":"优惠券奖励，页面描述文本"
		}
		"""
	Then jobs获得推广扫码
		"""
		{
			"prize_type":"积分",
			"coupon":优惠券1,
			"page_description":"优惠券奖励，页面描述文本"
		}
		"""

	#推广扫码验证
	When 清空浏览器
	When bill关注jobs的公众号
	When bill在微信中向jobs的公众号发送消息'我的推广码'
	Then bill收到自动回复'推广扫码链接'

	When bill进入链接'推广扫码链接'
	Then bill获得'bill'的推广码
		"""
		{
			"spreading_code":"bill的推广码",
			"page_description":"优惠券奖励，页面描述文本"
		}
		"""

	When tom扫码'bill'的推广码关注jobs的公众号

	Given jobs登录系统
	Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times |   attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |   今天            | 直接关注 |             |
			| tom   |   普通会员  |       1      |     0    |   0.00    |    0.00    |      0    |   今天            | 推广扫码 |             |

	Then jobs能获得优惠券'优惠券1'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 100.00,
				"status": "未使用",
				"consumer": "",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 100.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""
	