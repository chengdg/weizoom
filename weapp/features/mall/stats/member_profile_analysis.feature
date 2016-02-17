#watcher:wangli@weizoom.com,benchi@weizoom.com
#_author_:王丽
#editor:王丽  2015.10.19

Feature: 会员分析-会员概况-基础数据、会员来源
"""
	对店铺的会员进行不同维度的分析

	说明：1）整个会员的统计只统计真实会员，没有注册直接下单的不统计
		2）有效订单：订单状态为 待发货、已发货、已完成的订单

	一、查询条件

		1、刷选日期
			1）开始日期和结束日期都为空；选择开始结束日期，精确到日期
			2）开始日期或者结束日期，只有一个为空，给出系统提示“请填写XX日期”
			3）默认为‘今天’，筛选日期：‘今天’到‘今天’
			4）包含筛选日期的开始和结束的边界值
			5）手工设置筛选日期，点击查询后，‘快速查询’的所有项都处于‘未选中状态’
		2、快速查看
		    1）今天：查询的当前日期，例如，今天是2015-6-16，筛选日期是：2015-6-16到2015-6-16
		    2）昨天：查询的前一天，例如，今天是2015-6-16，筛选日期是：2015-6-15到2015-6-15
			3）最近7天；包含今天，向前7天；例如，今天是2015-6-16，筛选日期是：2015-6-10到2015-6-16
			4）最近30天；包含今天，向前30天；例如，今天是2015-6-16，筛选日期是：2015-5-19到2015-6-16
			5）最近90天；包含今天，向前90天；例如，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
			6）全部：筛选日期更新到：2013.1.1到今天

	二、基础数据
		1、【会员总数】：当前时间系统中状态为‘关注’和‘已取消’的会员数总和。

			备注：状态的值，反应的是当前状态的会员总数，和查询区间没有关系

			数字做成超链接：点击打开新页，跳转到会员管理

			"？"说明弹窗：已关注和已取消关注的会员总数

		2、【取消关注会员】：=当前时间系统中状态为‘已取消’的会员数总和 

			备注：状态的值，反应的是当前状态的‘已取消’会员总数，和查询区间没有关系

			"？"说明弹窗：已取消关注的会员总数

			需求变更：删除【取消关注会员】字段；增加【关注会员】字段

			【关注会员】：当前时间系统中状态为‘关注’的会员数总和 

			备注：状态的值，反应的是当前状态的‘关注’会员总数，和查询区间没有关系

			数字做成超链接：点击打开新页，跳转到会员管理

			"？"说明弹窗：当前关注的会员总数

		3、【新增会员】：=∑会员.个数[【加入时间】 in 查询区间]

			备注：不包含之前注册成会员，又取消关注了，在查询区间内又重新关注的会员

			"？"说明弹窗：新增关注的会员去重人数

		4、【手机绑定会员】：手机绑定的会员的手机绑定时间在查询区间内的手机绑定会员数

			"？"说明弹窗：新增手机绑定会员数

		5、【下单会员】：=∑订单.买家个数[(订单.下单时间 in 查询区间) and (订单.来源 ='本店') and (订单.订单状态 in {待发货、已发货、已完成})]   

			备注：‘下单时间’在查询区间内的有效订单的买家个数，重复的会员不重复累加

			"？"说明弹窗：下单的会员数

		6、【会员复购率】：=∑(复购会员数/【下单会员】)*100% 
			1）复购会员数=∑订单.买家个数[(订单.下单时间 in 查询区间) and (订单.来源 ='本店') and (订单.订单状态 in {待发货、已发货、已完成})
						and (订单.订单编号[(订单.买家=该订单.买家) and (订单.下单时间<该订单.下单时间) 
										and (订单.订单状态 in {待发货、已发货、已完成}) and (订单.来源 ='本店')].exist) 
						]
				备注：满足下面条件的订单的买家个数总和；（1）下单时间在查询区间内的有效订单（1）订单的买家在该订单下单时间之前有‘有效订单’	

			2）【下单会员】：=∑订单.买家个数[(订单.下单时间 in 查询区间) and (订单.来源 ='本店') and (订单.订单状态 in {待发货、已发货、已完成})]

			备注：1）注意买家在查询区间内发生两次购买，第一次购买为初次购买;
					第二次购买统为复购。
				2）之前是会员,购买商品，有'有效订单'，现在取消关注购买的，订单有效，这样的也是复购

			"？"说明弹窗：时间段内，再次购买人数/总购买人数x100%

	三、会员来源
		1、【发起扫码会员】：在查询区间内发起‘有效扫码’的会员数
			‘有效扫码’：发起推广扫码或者带参数二维码，扫码并关注成为会员的第一个会员的关注时间在查询区间内

			备注：本会员发起的扫码，只有扫码人关注成为会员才是有效的

			"？"说明弹窗：发起推广扫码的会员数

		2、【发起分享链接会员】：在查询区间内发起‘有效分享链接’的会员数
			‘有效分享链接’：发起分享链接的并且此链接被第一次点击的时间在查询区间

			"？"说明弹窗：发起分享链接的会员数

		3、【扫码新增会员】：=∑会员.个数[(会员.加入时间 in 查询区间) and (会员.来源 = ‘推广扫码’)]

			备注：在查询区间内通过扫码新增的会员数，包含推广扫码和带参数二维码

			"？"说明弹窗：通过扫码新关注的会员数（包括推广扫码、带参数二维码）

		4、【直接关注】：=∑会员.个数[(会员.加入时间 in 查询区间) and (会员.来源 = ‘直接关注’)]

			备注：在查询区间内通过直接关注新增的会员数

			"？"说明弹窗：直接关注的会员数

		5、【分享链接新增会员】：∑会员.个数[(会员.加入时间 in 查询区间) and (会员.来源 = ‘会员分享’)]

			备注：在查询区间内通过分享链接新增的会员数

			"？"说明弹窗：通过分享链接新关注的会员数

		6、【会员推荐率】：(【发起扫码会员】+ 【发起分享链接会员】)/查询结束时间点时系统的会员总数 * 100%
			1）【发起扫码会员】：在查询区间内发起‘有效扫码’的会员数
			2）【发起分享链接会员】：在查询区间内发起‘有效分享链接’的会员数
			3）查询结束时间点时系统的会员总数
				例如：筛选日期：2015-5-1到2015-5-22
					查询结束时间点时系统的会员总数=∑会员.个数[会员.加入时间 < 2015-5-23 00:00]

			"？"说明弹窗：时间段内，发起推荐会员数/会员总数x100%
"""

Background:
	Given jobs登录系统
	And 开启手动清除cookie模式

	When jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.0,
			"weight": 5,
			"postage": 10.0,
			"stock_type": "无限"
		},{
			"name": "商品2",
			"price": 100.0,
			"weight": 5,
			"postage": 15.0,
			"stock_type": "无限"
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}, {
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""

	When 清空浏览器
	When bill1关注jobs的公众号
	When bill1访问jobs的webapp
	When bill1把jobs的微站链接分享到朋友圈
	
	When 清空浏览器
	When bill2点击bill1分享链接
	When bill2关注jobs的公众号
	When bill2访问jobs的webapp
	When bill2把jobs的微站链接分享到朋友圈

	When 清空浏览器
	When bill3点击bill2分享链接
	When bill3关注jobs的公众号
	When bill3访问jobs的webapp

	When 清空浏览器
	When bill4关注jobs的公众号
	When bill5关注jobs的公众号
	When bill6关注jobs的公众号
	When bill7关注jobs的公众号

	When bill6取消关注jobs的公众号
	When bill7取消关注jobs的公众号

	When 微信用户批量消费jobs的商品
		| order_id | date | consumer | product  | payment | pay_type | postage*| price*   | paid_amount*| alipay*| wechat*| cash*|    action     |  order_status*  |
		|  0001    | 昨天 | bill1    | 商品1,1  | 支付    | 微信支付 | 10      | 100      | 110         | 0      |  110   | 0    | jobs,完成     |    已完成       |
		|  0002    | 今天 | bill3    | 商品1,1  |         | 支付宝   | 10      | 100      | 110         | 0      |    0   | 0    |               |    待支付       |
		|  0003    | 今天 | bill1    | 商品2,1  |         | 微信支付 | 15      | 100      | 115         | 0      |    0   | 0    | jobs,取消     |    已取消       |
		|  0004    | 今天 | bill4    | 商品1,1  | 支付    | 货到付款 | 10      | 100      | 110         | 0      |    0   | 110  | jobs,发货     |    已发货       |
		|  0005    | 今天 | bill1    | 商品1,1  | 支付    | 微信支付 | 10      | 100      | 110         | 0      |    0   | 0    | jobs,退款     |    退款中       |
		|  0006    | 今天 | bill2    | 商品1,1  | 支付    | 支付宝   | 10      | 100      | 110         | 0      |    0   | 0    | jobs,完成退款 |    退款成功     |
		|  0007    | 今天 | bill1    | 商品2,1  | 支付    | 微信支付 | 15      | 100      | 115         | 0      |   115  | 0    | jobs,完成     |    已完成       |
		|  0008    | 今天 | -lili    | 商品2,2  | 支付    | 支付宝   | 15      | 100      | 215         | 215    |    0   | 0    | jobs,发货     |    已发货       |

@mall2 @bi @memberAnalysis   @stats @stats.membe
Scenario: 1  会员概况：基础数据和会员来源数据
	Given jobs登录系统
	When jobs设置筛选日期
		"""
		{
			"start_date":"今天",
			"end_date":"今天"
		}
		"""

	Then jobs能获得基础数据和会员来源数据
		| item              | quantity |
		| 会员总数          |    7     |
		| 关注会员          |    5     |
		| 新增会员          |    7     |
		| 手机绑定会员      |    0     |
		| 下单会员          |    3     |
		| 会员复购率        |   33.33% |
		| 发起扫码会员      |    0     |
		| 发起分享链接会员  |    2     |
		| 扫码新增会员      |    0     |
		| 直接关注          |    5     |
		| 分享链接新增会员  |    2     |
		| 会员推荐率        |   28.57% |
