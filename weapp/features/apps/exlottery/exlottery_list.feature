#_author_:江秋丽 2016.07.13


Feature: 微信专项抽奖码库列表
	"""
	微信专项抽奖码库列表
		查询条件:
			抽奖码:默认为空,模糊匹配查询
			使用人:默认为空,模糊匹配查询
		列表字段:
			【抽奖码】:显示随机生成以'el'开头的10位数字、字母组合
			【使用人】:使用抽奖码的用户名称
			【使用时间】:用户使用抽奖码的时间
			【获奖等级】:配置的奖品等级
			【奖品名称】:用户抽中的奖品名称
			【操作】:【导出】
			排序：按照抽奖码使用时间倒序排列,每页最多显示10条数据
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
	"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 50,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "优惠券2",
			"money": 50.00,
			"count": 50,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "5天后",
			"coupon_id_prefix": "coupon2_id_"
		}, {
			"name": "优惠券3",
			"money": 30.00,
			"count": 50,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "5天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}]
	"""
	When jobs已添加单图文
	"""
		[{
			"title":"百事抽奖活动单图文",
			"cover": [{
				"url": "6.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"百事抽奖",
			"content":"百事抽奖",
			"jump_url":"专项抽奖"
		}]
	"""
	When jobs已添加关键词自动回复规则
	"""
		[{
			"rules_name":"抽奖规则",
			"keyword":
				[{
					"keyword": "百事抽奖",
					"type": "equal"
				}],
			"keyword_reply":
				[{
					"reply_content":"百事抽奖活动单图文",
					"reply_type":"text_picture"
				}]
		}]
	"""
	When jobs新建专项抽奖活动
	"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"desc":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"#0000FF",
			"start_date":"今天",
			"end_date":"2天后",
#			"reduce_integral":0,
#			"send_integral":0,
			"win_rate":"100%",
			"lottory_code_num":5,
			"is_repeat_win":"否",			
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":0,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":0,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"4.jpg"
			}]
		}]
	"""
	
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18","el2f5e754g","el58fe24rf","elm8v6uj41","elmn782f2r"]
	"""
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入专项抽奖活动页面
	Then bill在专项抽奖活动首页获得验证码'tudf'
	When bill在专项抽奖活动首页中输入验证码'tudf'
	When bill在专项抽奖活动首页中输入抽奖码'el8s539t18'
	When bill点击'立即抽奖'进入专项抽奖活动内容页
	When bill参加专项抽奖活动'专项抽奖'
	Then bill获得专项抽奖结果
	"""
		{
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		}
	"""

	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入专项抽奖活动页面
	Then bill在专项抽奖活动首页获得验证码'tudf'
	When bill在专项抽奖活动首页中输入验证码'tudf'
	When bill在专项抽奖活动首页中输入抽奖码'elm8v6uj41'
    When bill点击'立即抽奖'进入专项抽奖活动内容页
	When bill参加专项抽奖活动'专项抽奖'
	Then bill获得专项抽奖结果
	"""
		{
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		}
	"""
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入专项抽奖活动页面
	Then bill在专项抽奖活动首页获得验证码'tudf'
	When bill在专项抽奖活动首页中输入验证码'tudf'
	When bill在专项抽奖活动首页中输入抽奖码'el58fe24rf'
	When bill点击'立即抽奖'进入专项抽奖活动内容页
	When bill参加专项抽奖活动'专项抽奖'
	Then bill获得专项抽奖结果
	"""
		{
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		}
	"""

@mall2 @apps @apps_exlottery @exlottery_code_list
Scenario:1 微信专项抽奖活动码库查询
	Given jobs登录系统
	#空查询
	When jobs设置'专项抽奖'码库列表查询条件
	"""
		{}
	"""
	Then jobs能获得'专项抽奖'码库列表
	"""
		[{
			"lottery_code":"el58fe24rf",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		},{
			"lottery_code":"elm8v6uj41",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		},{
			"lottery_code":"el8s539t18",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		},{
			"lottery_code":"el2f5e754g",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		},{
			"lottery_code":"elmn782f2r",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		}]
	"""
	#按照抽奖码查询
	When jobs设置'专项抽奖'码库列表查询条件
	"""
		{
			"lottery_code":"el2f5e754g"
		}
	"""
	Then jobs能获得'专项抽奖'码库列表
	"""
		[{
			"lottery_code":"el2f5e754g",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		}]
	"""
	#按照使用人查询
	When jobs设置'专项抽奖'码库列表查询条件
	"""
		{
			"user":"bill"
		}
	"""
	Then jobs能获得'专项抽奖'码库列表
	"""
		[{
			"lottery_code":"el58fe24rf",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		},{
			"lottery_code":"elm8v6uj41",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		},{
			"lottery_code":"el8s539t18",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		}]
	"""

@mall2 @apps @apps_exlottery @exlottery_code_list
Scenario:2 微信专项抽奖活动码库列表分页
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	#Then jobs获得微信专项抽奖活动'专项抽奖'码库列表共'3'页
	When jobs访问'专项抽奖'码库列表第'1'页
	Then jobs能获得'专项抽奖'码库列表
	"""
		[{
			"lottery_code":"el58fe24rf",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		},{
			"lottery_code":"elm8v6uj41",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		}]
	"""
	When jobs访问'专项抽奖'码库列表下一页
	Then jobs能获得'专项抽奖'码库列表
	"""
		[{
			"lottery_code":"el8s539t18",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		},{
			"lottery_code":"el2f5e754g",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		}]
	"""
	When jobs访问'专项抽奖'码库列表第'3'页
	Then jobs能获得'专项抽奖'码库列表
	"""
		[{
			"lottery_code":"elmn782f2r",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		}]
	"""
	When jobs访问'专项抽奖'码库列表上一页
	Then jobs能获得'专项抽奖'码库列表
		"""
		[{
			"lottery_code":"el8s539t18",
			"user":"bill",
			"use_date":"今天",
			"prize_grade":"一等奖",
			"prize_name":"100积分"
		},{
			"lottery_code":"el2f5e754g",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		}]
		"""