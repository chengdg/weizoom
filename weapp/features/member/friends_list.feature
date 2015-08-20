#_author_:王丽

Feature: 会员管理-好友关系列表
"""
	会员管理下的会员列表，【好友数】不为零，即当前会员有好友，点击好友数，弹出好友列表窗体
	好友列表窗体
	1、"推荐关注"页签
		当前会员推荐关注本店铺成为店铺会员的好友列表，按照[关注时间]倒序排列
		（1）推荐关注好友列表展示字段
			【会员】：推荐关注的好友的头像和昵称、会员等级，昵称有外链接，点击重新打开新页面此会员的"会员详情"
			【消费金额】：此会员在本店铺提交并成功支付的订单的"实付金额"的总和
			【积分】：此会员现在拥有的本店铺的积分数
			【来源】：此会员的来源（推广扫码、会员分享）
			【时间】：两者直接创建好友关系的时间
		（2）分页展示，每页8条数据
		（3）左下角显示"共XX条记录"
	2、"好友列表"页签
		当前会员的好友的列表（包含推荐关注的好友），按照[关注时间]倒序排列
		（1）好友列表展示字段
			【会员】：此好友的头像和昵称、会员等级，昵称有外链接，点击重新打开新页面此会员的"会员详情"
			【消费金额】：此会员在本店铺提交并成功支付的订单的"实付金额"的总和
			【积分】：此会员现在拥有的本店铺的积分数
			【来源】：此会员的来源（推广扫码、会员分享、直接关注）
			【推荐人】：此好友的推荐人的昵称（本店铺的会员），直接关注的此项为"无"；昵称有外链接，点击重新打开新页面此会员的"会员详情"
			【时间】：两者直接创建好友关系的时间
		（2）分页展示，每页8条数据
		（3）左下角显示"共XX条记录"
"""
Background:
	Given jobs登录系统
	And 开启手动清除cookie模式

	And jobs添加会员等级
		"""
		[{
			"name": "普通会员",
			"upgrade": "手动升级",
			"shop_discount": "10"
		},{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"shop_discount": "9"
		},{
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "8"
		},{
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "7"
		}]
		"""

	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"postage": 10,
			"price": 100.00,
			"weight": 5.0,
			"stock_type": "无限"
		}]
		"""

	When jobs添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345", 
			"weixin_partner_id": "22345", 
			"weixin_partner_key": "32345", 
			"weixin_sign": "42345"
		},{
			"type": "支付宝",
			"description": "我的支付宝支付",
			"is_active": "启用"
		}]
		"""

	#以bill为基础创建数据
		When 清空浏览器
		When bill关注jobs的公众号于'2015-5-1'
		When bill访问jobs的webapp
		When bill把jobs的微站链接分享到朋友圈

	#会员分享
		#建立好友关系传播情景,A-->(E,F,G)
			#bill1点击bill的分享链接,bill1关注jobs,访问jobs的webapp; bill1是bill推荐来的下级好友，来源是"会员分享"
			When 清空浏览器
			When bill1点击bill分享链接
			When bill1关注jobs的公众号
			When bill1访问jobs的webapp

			#bill2关注jobs,访问jobs的webapp,点击bill的分享链接; bill2是bill的好友，来源是"直接关注"
			When 清空浏览器
			When bill2关注jobs的公众号
			When bill2访问jobs的webapp
			When bill2点击bill分享链接

			#bill3关注jobs,点击bill的分享链接,访问jobs的webapp; bill3是bill推荐来的下级好友，来源是"会员分享"
			When 清空浏览器
			When bill3关注jobs的公众号
			When bill3点击bill分享链接
			When bill3访问jobs的webapp

		#建立好友关系传播情景,A-->B-->(E,F,G)

			#marry关注jobs的公众账号，访问jobs的webapp，点击bill的分享链接，marry分享bill的分享链接到朋友圈；marry是bill的好友，来源是"直接关注"
				When 清空浏览器
				When marry关注jobs的公众号
				When marry访问jobs的webapp
				When marry点击bill分享链接
				When marry分享bill分享jobs的微站链接到朋友圈

			#bill01点击marry的分享链接，关注jobs的公众账号，访问jobs的webapp；bill01是marry推荐的下级好友，来源是"会员分享"
				When 清空浏览器
				When bill01点击marry分享链接
				When bill01关注jobs的公众号
				When bill01访问jobs的webapp

			#bill02关注jobs的公众账号，访问jobs的webapp，点击marry的分享链接；bill02是marry的好友，来源是"直接关注"
				When 清空浏览器
				When bill02关注jobs的公众号
				When bill02访问jobs的webapp
				When bill02点击marry分享链接

			#bill03关注jobs的公众账号，点击marry的分享链接，访问jobs的webapp；bill03是marry推荐的下级好友，来源是"会员分享"
				When 清空浏览器
				When bill03关注jobs的公众号
				When bill03点击marry分享链接
				When bill03访问jobs的webapp

		#建立好友关系传播情景,A-->C-->(E,F,G)

			#jack1点击bill的分享链接，jack1分享bill的分享链接到朋友圈
				When 清空浏览器
				When jack1点击bill分享链接
				When jack1分享bill分享jobs的微站链接到朋友圈

			#bill11点击jack1的分享链接，关注jobs的公众账号，访问jobs的weapp；bill11是bill推荐的下级好友，来源是"会员分享"
				When 清空浏览器
				When bill11点击jack1分享链接
				When bill11关注jobs的公众号
				When bill11访问jobs的webapp

			#bill12关注jobs的公众账号，访问jobs的webapp，点击jack1的分享链接；bill12是bill的好友，来源是"直接关注"
				When 清空浏览器
				When bill12关注jobs的公众号
				When bill12访问jobs的webapp
				When bill12点击jack1分享链接

			#bill13关注jobs的公众账号，点击jack1的分享链接，访问jobs的webapp；bill13是bill推荐的下级好友，来源是"会员分享"
				When 清空浏览器
				When bill13关注jobs的公众号
				When bill13点击jack1分享链接
				When bill13访问jobs的webapp

		#建立好友关系传播情景,A-->C-->B-->(E,F,G)

			#jack1点击bill的分享链接，jack1分享bill的分享链接到朋友圈
				When 清空浏览器
				When jack1点击bill分享链接
				When jack1分享bill分享jobs的微站链接到朋友圈

			#marry2关注jobs的公众账号，访问jobs的webapp，点击jack1的分享链接；marry2是bill的好友，来源是"直接关注"
				When 清空浏览器
				When marry2关注jobs的公众号
				When marry2访问jobs的webapp
				When marry2点击jack1分享链接
				When marry2分享jack1分享jobs的微站链接到朋友圈

			#bill01点击marry2的分享链接，关注jobs的公众账号，访问jobs的webapp；bill001是marry2推荐的下级好友，来源是"会员分享"
				When 清空浏览器
				When bill001点击marry2分享链接
				When bill001关注jobs的公众号
				When bill001访问jobs的webapp

			#bill002关注jobs的公众账号，访问jobs的webapp，点击marry2的分享链接；bill002是marry2的好友，来源是"直接关注"
				When 清空浏览器
				When bill002关注jobs的公众号
				When bill002访问jobs的webapp
				When bill002点击marry2分享链接

			#bill003关注jobs的公众账号，点击marry2的分享链接，访问jobs的webapp，bill003是marry2推荐的下级好友，来源是"会员分享"
				When 清空浏览器
				When bill003关注jobs的公众号
				When bill003点击marry2分享链接
				When bill003访问jobs的webapp

		#建立好友关系传播情景,A-->C-->D-->(E,F,G)

			#jack2点击bill的分享链接，jack2分享bill的分享链接到朋友圈
				When 清空浏览器
				When jack2点击bill分享链接
				When jack2分享bill分享jobs的微站链接到朋友圈

			#jack3点击jack2的分享链接，jack3分享jack2的分享链接到朋友圈
				When 清空浏览器
				When jack3点击jack2分享链接
				When jack3分享jack2分享jobs的微站链接到朋友圈
			
			#bill0011点击jack3的分享链接，关注jobs的公众账号，访问jobs的webapp；bill0011是bill推荐的下级好友，来源是"会员分享"
				When 清空浏览器
				When bill0011点击jack3分享链接
				When bill0011关注jobs的公众号
				When bill0011访问jobs的webapp

			#bill0012关注jobs的公众账号，访问jobs的weapp，点击jack3的分享链接；bill0012是bill好友，来源是"直接关注"
				When 清空浏览器
				When bill0012关注jobs的公众号
				When bill0012访问jobs的webapp
				When bill0012点击jack3分享链接

			#bill0013关注jobs的公众账号，点击jack3的分享链接，访问jobs的weapp；bill0013是bill推荐的下级好友，来源是"会员分享"
				When 清空浏览器
				When bill0013关注jobs的公众号
				When bill0013点击jack3分享链接
				When bill0013访问jobs的webapp

		When 清空浏览器
		When bill01点击bill分享链接

		When 清空浏览器
		When bill001点击bill分享链接

	#会员获取jobs的积分

		When bill1访问jobs的webapp
		When bill1获得jobs的50会员积分
		Then bill1在jobs的webapp中拥有50会员积分

		When bill01访问jobs的webapp
		When bill01获得jobs的60会员积分
		Then bill01在jobs的webapp中拥有60会员积分

		When bill11访问jobs的webapp
		When bill11获得jobs的70会员积分
		Then bill11在jobs的webapp中拥有70会员积分

		When bill001访问jobs的webapp
		When bill001获得jobs的80会员积分
		Then bill001在jobs的webapp中拥有80会员积分

	#调整会员等级
		When jobs调整会员等级
			"""
			[{
				"name":"bill1",
				"member_rank":"铜牌会员"
			},{
				"name":"bill01",
				"member_rank":"银牌会员"
			},{
				"name":"bill11",
				"member_rank":"金牌会员"
			}]
			"""

	When 微信用户批量消费jobs的商品
		| date | consumer | type  |businessman| product | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action     |  order_status   |
		| 今天 | bill01   | 购买  | jobs      | 商品1,1 | 支付    | 支付宝         | 10      |    100   | 		   |        | 110         |              | 110    | 0      | 0    | jobs,支付       |  待发货         |
		| 今天 | bill01   | 购买  | jobs      | 商品1,1 | 支付    | 微信支付       | 10      |    100   | 		   |        | 110         |              | 0      | 110    | 0    | jobs,发货       |  已发货         |
		| 今天 | bill01   | 购买  | jobs      | 商品1,1 | 支付    | 货到付款       | 10      |    100   | 		   |        | 110         |              | 0      | 0      | 110  | jobs,完成       |  已完成         |
		| 今天 | bill01   | 购买  | jobs      | 商品1,1 | 支付    | 货到付款       | 10      |    100   | 		   |        | 110         |              | 0      | 0      | 110  | jobs,取消       |  已取消         |
		| 今天 | bill13   | 购买  | jobs      | 商品1,1 | 未支付  | 微信支付       | 10      |    100   | 		   |        | 110         |              | 0      | 0      | 0    | jobs,无操作     |  待支付         |
		| 今天 | bill13   | 购买  | jobs      | 商品1,1 | 支付    | 微信支付       | 10      |    100   | 		   |        | 110         |              | 0      | 110    | 0    | jobs,发货       |  已发货         |
		| 今天 | bill13   | 购买  | jobs      | 商品1,1 | 支付    | 支付宝         | 10      |    100   | 		   |        | 110         |              | 110    | 0      | 0    | jobs,退款       |  退款中         |
		| 今天 | bill13   | 购买  | jobs      | 商品1,1 | 支付    | 货到付款       | 10      |    100   | 		   |        | 110         |              | 0      | 0      | 110  | jobs,完成退款   |  退款成功       |

Scenario:1 会员的好友列表和推荐关注列表

	Given jobs登录系统
	Then jobs获得bill的'推荐关注'
		|   fans   | consumption_amount |  integral  |  Source  |      time      |
		|  bill1   |        0           |     50     | 会员分享 |      今天      |
		|  bill3   |        0           |     0      | 会员分享 |      今天      |
		|  bill11  |        0           |     70     | 会员分享 |      今天      |
		|  bill13  |        330         |     0      | 会员分享 |      今天      |
		|  bill0011|        0           |     0      | 会员分享 |      今天      |
		|  bill0013|        0           |     0      | 会员分享 |      今天      |
	Then jobs获得bill的'推荐关注'记录数
		"""
		[{
			"record_count":6
		}]
		"""

	Then jobs获得bill的'好友列表'
		|   fans   | consumption_amount |  integral  |  Source  | recommended |      time      |
		|  bill1   |        0           |     50     | 会员分享 |    bill     |      今天      |
		|  bill2   |        0           |     0      | 直接关注 |    无       |      今天      |
		|  bill3   |        0           |     0      | 会员分享 |    bill     |      今天      |
		|  marry   |        0           |     0      | 直接关注 |    无       |      今天      |
		|  bill01  |        330         |     60     | 会员分享 |    marry    |      今天      |
		|  bill11  |        0           |     70     | 会员分享 |    bill     |      今天      |
		|  bill12  |        0           |     0      | 直接关注 |    无       |      今天      |
		|  bill13  |        330         |     0      | 会员分享 |    bill     |      今天      |
		|  marry2  |        0           |     0      | 直接关注 |    无       |      今天      |
		|  bill001 |        0           |     80     | 会员分享 |    marry2   |      今天      |
		|  bill0011|        0           |     0      | 会员分享 |    bill     |      今天      |
		|  bill0012|        0           |     0      | 直接关注 |    无       |      今天      |
		|  bill0013|        0           |     0      | 会员分享 |    bill     |      今天      |

	Then jobs获得bill的'好友列表'记录数
		"""
		[{
			"record_count":14
		}]
		"""

Scenario:2 会员的好友列表和推荐关注列表分页

	Given jobs登录系统

	And jobs设置分页查询参数
	"""
	{
		"count_per_page":2
	}
	"""

	#推荐关注列表分页
		Then jobs获取'推荐关注'列表显示共3页
		When jobs浏览第1页
		Then jobs获得bill的'推荐关注'
			|   fans   | consumption_amount |  integral  |  Source  |      time      |
			|  bill1   |        0           |     50     | 会员分享 |      今天      |
			|  bill3   |        0           |     0      | 会员分享 |      今天      |
		When jobs浏览下一页
		Then jobs获得bill的'推荐关注'
			|   fans   | consumption_amount |  integral  |  Source  |      time      |
			|  bill11  |        0           |     70     | 会员分享 |      今天      |
			|  bill13  |        330         |     0      | 会员分享 |      今天      |
		When jobs浏览第3页
		Then jobs获得bill的'推荐关注'
			|   fans   | consumption_amount |  integral  |  Source  |      time      |
			|  bill0011|        0           |     0      | 会员分享 |      今天      |
			|  bill0013|        0           |     0      | 会员分享 |      今天      |
		When jobs浏览上一页
		Then jobs获得bill的'推荐关注'
			|   fans   | consumption_amount |  integral  |  Source  |      time      |
			|  bill11  |        0           |     70     | 会员分享 |      今天      |
			|  bill13  |        330         |     0      | 会员分享 |      今天      |

	#好友列表分页
		Then jobs获取'好友列表'列表显示共3页
		When jobs浏览第1页
		Then jobs获得bill的'好友列表'
			|   fans   | consumption_amount |  integral  |  Source  | recommended |      time      |
			|  bill1   |        0           |     50     | 会员分享 |    bill     |      今天      |
			|  bill2   |        0           |     0      | 直接关注 |    无       |      今天      |
		When jobs浏览下一页
		Then jobs获得bill的'好友列表'
			|   fans   | consumption_amount |  integral  |  Source  | recommended |      time      |
			|  bill3   |        0           |     0      | 会员分享 |    bill     |      今天      |
			|  marry   |        0           |     0      | 直接关注 |    无       |      今天      |
		When jobs浏览第3页
		Then jobs获得bill的'好友列表'
			|   fans   | consumption_amount |  integral  |  Source  | recommended |      time      |
			|  bill01  |        330         |     60     | 会员分享 |    marry    |      今天      |
			|  bill11  |        0           |     70     | 会员分享 |    bill     |      今天      |
		When jobs浏览上一页
		Then jobs获得bill的'好友列表'
			|   fans   | consumption_amount |  integral  |  Source  | recommended |      time      |
			|  bill3   |        0           |     0      | 会员分享 |    bill     |      今天      |
			|  marry   |        0           |     0      | 直接关注 |    无       |      今天      |

