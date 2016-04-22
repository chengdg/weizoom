#author: 王丽
#editor: 张三香 2015.10.16
#editor: 冯雪静 2016.3.29
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
			【会员等级】：此会员在本店铺的会员等级
			【消费金额】：计算此会员“已完成”的订单总金额包含（微众卡+现金）
			【积分】：此会员现在拥有的本店铺的积分数
			【来源】：此会员的来源（推广扫码、会员分享、直接关注）
			【推荐人】：此好友的推荐人的昵称（本店铺的会员），直接关注的此项为"无"；昵称有外链接，点击重新打开新页面此会员的"会员详情"
			【时间】：两者直接创建好友关系的时间
		（2）分页展示，每页8条数据
		（3）左下角显示"共XX条记录"
	3、传播能力
		包括二维码引流、会员分享引流、购买转化、转化率
"""
Background:
	Given jobs登录系统
	And 开启手动清除cookie模式

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

		#bill带来的传播能力数据创建
		When 清空浏览器
		When bill访问jobs的webapp
		When bill进入推广扫描链接

		When 清空浏览器
		When tom1扫描bill的推广二维码关注jobs公众号
		When 休眠1秒

		When 清空浏览器
		When tom2扫描bill的推广二维码关注jobs公众号
		When 休眠1秒

		When 清空浏览器
		When tom3扫描bill的推广二维码关注jobs公众号
		When 休眠1秒

		When 清空浏览器
		When tom4扫描bill的推广二维码关注jobs公众号
		When 休眠1秒



	When 微信用户批量消费jobs的商品
		| order_id | date | consumer | product | payment | pay_type | postage*| price* | paid_amount*| alipay*| wechat*| cash*|    action    | order_status*|
		|   0001   | 今天 | bill01   | 商品1,1 | 支付    | 支付宝   | 10      |  100   | 110         | 110    | 0      | 0    |              | 待发货       |
		|   0002   | 今天 | bill01   | 商品1,1 | 支付    | 微信支付 | 10      |  100   | 110         | 0      | 110    | 0    | jobs,发货    | 已发货       |
		|   0003   | 今天 | bill01   | 商品1,1 | 支付    | 货到付款 | 10      |  100   | 110         | 0      | 0      | 110  | jobs,完成    | 已完成       |
		|   0004   | 今天 | bill01   | 商品1,1 | 支付    | 货到付款 | 10      |  100   | 110         | 0      | 0      | 110  | jobs,取消    | 已取消       |
		|   0005   | 今天 | bill13   | 商品1,1 |         | 微信支付 | 10      |  100   | 110         | 0      | 0      | 0    |              | 待支付       |
		|   0006   | 今天 | bill13   | 商品1,1 | 支付    | 微信支付 | 10      |  100   | 110         | 0      | 110    | 0    | jobs,发货    | 已发货       |
		|   0007   | 今天 | bill13   | 商品1,1 | 支付    | 支付宝   | 10      |  100   | 110         | 110    | 0      | 0    | jobs,完成    | 已完成       |
		|   0008   | 今天 | bill13   | 商品1,1 | 支付    | 支付宝   | 10      |  100   | 110         | 110    | 0      | 0    | jobs,完成退款| 退款成功     |
		|   0009   | 今天 | tom1     | 商品1,1 | 支付    | 微信支付 | 10      |  100   | 110         | 0      | 110    | 0    | jobs,发货    | 已发货       |
		|   0010   | 今天 | tom2     | 商品1,1 | 支付    | 支付宝   | 10      |  100   | 110         | 110    | 0      | 0    | jobs,完成    | 已完成       |
		|   0011   | 今天 | tom3     | 商品1,1 | 支付    | 支付宝   | 10      |  100   | 110         | 110    | 0      | 0    | jobs,完成退款| 退款成功     |


Scenario:3 (传播能力)会员统计
	1.二维码引流会员数量
	2.分享链接引流会员数量
	3.购买转化会员数量
	4.转化率（购买转化数量/引流会员数量）百分比保留两位小数如：1/3等于33.33%

	Given jobs登录系统
	Then jobs获得'bill'的传播能力
		"""
		{
			"scan_qrcode_new_member": 4,
			"share_link_new_member": 6,
			"buy_transform_new_member": 2,
			"transform_rate": "20%"
		}
		"""


Scenario:4 (传播能力)会员的分享链接引流会员列表

	Given jobs登录系统
	#购买次数和金额按照订单“已完成”状态计算（金额包括：微众卡金额+现金）
	Then jobs获得'bill'分享链接引流会员统计
		"""
		{
			"new_members":6,
			"ordered_members":1,
			"pay_money":110.00
		}
		"""
	Then jobs获得'bill'分享链接引流会员列表
		|  member  | member_rank | pay_times | pay_money |  integral  |  Source  | attention_time |
		|  bill0013| 普通会员    |           |    0      |     0      | 会员分享 |      今天      |
		|  bill0011| 普通会员    |           |    0      |     0      | 会员分享 |      今天      |
		|  bill13  | 普通会员    |     1     |    110    |     0      | 会员分享 |      今天      |
		|  bill11  | 普通会员    |           |    0      |     70     | 会员分享 |      今天      |
		|  bill3   | 普通会员    |           |    0      |     0      | 会员分享 |      今天      |
		|  bill1   | 普通会员    |           |    0      |     50     | 会员分享 |      今天      |
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs访问'bill'分享链接引流会员页
	Then jobs获得'bill'分享链接引流会员列表显示共3页
	When jobs浏览分享链接引流会员列表第1页
	Then jobs获得'bill'分享链接引流会员列表
		|  member  | member_rank | pay_money |  integral  |  Source  | attention_time |
		|  bill0013| 普通会员    |    0      |     0      | 会员分享 |      今天      |
		|  bill0011| 普通会员    |    0      |     0      | 会员分享 |      今天      |


Scenario:5 (传播能力)会员的二维码引流会员列表

	Given jobs登录系统
	Then jobs获得'bill'二维码引流会员统计
		"""
		{
			"new_members":4,
			"ordered_members":1,
			"pay_money":110.00
		}
		"""
	Then jobs获得'bill'二维码引流会员列表
		|  member  | member_rank | pay_times | pay_money |  integral  |  Source  | attention_time |
		|  tom4    | 普通会员    |           |    0      |     0      | 推广扫码 |      今天      |
		|  tom3    | 普通会员    |           |    0      |     0      | 推广扫码 |      今天      |
		|  tom2    | 普通会员    |     1     |    110    |     0      | 推广扫码 |      今天      |
		|  tom1    | 普通会员    |           |    0      |     0      | 推广扫码 |      今天      |

	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs访问'bill'二维码引流会员页
	Then jobs获得'bill'二维码引流会员列表显示共2页
	When jobs浏览二维码引流会员列表第1页
	Then jobs获得'bill'二维码引流会员列表
		|  member  | member_rank | pay_times | pay_money |  integral  |  Source  | attention_time |
		|  tom4    | 普通会员    |           |    0      |     0      | 推广扫码 |      今天      |
		|  tom3    | 普通会员    |           |    0      |     0      | 推广扫码 |      今天      |



Scenario:6 (传播能力)会员的购买转化会员列表

	Given jobs登录系统
	Then jobs获得'bill'购买转化会员统计
		"""
		{
			"ordered_members":2,
			"pay_money":220.00
		}
		"""
	Then jobs获得'bill'购买转化会员列表
		|  member  | member_rank | pay_times | pay_money |  integral  |  Source  | attention_time |
		|  tom2    | 普通会员    |     1     |    110    |     0      | 推广扫码 |      今天      |
		|  bill13  | 普通会员    |     1     |    110    |     0      | 会员分享 |      今天      |

	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs访问'bill'购买转化会员页
	Then jobs获得'bill'购买转化会员列表显示共1页
	When jobs浏览购买转化会员列表第1页
	Then jobs获得'bill'购买转化会员列表
		|  member  | member_rank | pay_times | pay_money |  integral  |  Source  | attention_time |
		|  tom2    | 普通会员    |     1     |    110    |     0      | 推广扫码 |      今天      |
		|  bill13  | 普通会员    |     1     |    110    |     0      | 会员分享 |      今天      |