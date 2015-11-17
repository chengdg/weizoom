#_author_:王丽 2015.11.16

Feature: 会员分析-会员概况-推广扫码排行榜
"""

	对店铺的会员进行不同维度的分析

	说明：整个会员的统计只统计真实会员，没有注册直接下单的不统计

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

	二、推广扫码排行Top10
		备注：包含状态为‘关注’和‘已取消’的在查询区间内新增的会员
		1、【排行】：从1到10
		2、【昵称】：会员昵称
		3、【推荐人数】：=∑会员.个数[(会员.加入时间 in 查询区间) and (会员.来源 = ‘推广扫码’) and (会员是扫当前会员的推广扫码关注)]

			备注：（1）发起推广扫码的会员的发起时间必须在查询区间内
			（2）发起推广扫码的时间以二维码生成的时间为准
			（3）只包含会员发起的，不包含商家发起的

	三、分享链接排行Top10
		1、【排行】：从1到10
		2、【昵称】：会员昵称
		3、【引导关注人数】：=∑会员.个数[(会员.加入时间 in 查询区间) and (会员.来源 = ‘会员分享’) and (会员是通过当前会员的分享链接关注)]

			备注：发起分享链接的会员的发起时间，以此链接第一次被点击时间为准
""" 

Background:
	Given jobs登录系统

	#推广扫码新增会员
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
		#bill的扫码会员
			When 清空浏览器
			When bill关注jobs的公众号于'2015-10-01'
			When bill访问jobs的webapp
			When bill进入推广扫描链接

			When bill1扫描bill的推广二维码关注jobs公众号
			When bill2扫描bill的推广二维码关注jobs公众号
			When bill3扫描bill的推广二维码关注jobs公众号
			When bill4扫描bill的推广二维码关注jobs公众号

		#tom的扫码会员-扫码关注后再取消关注要计数
			When 清空浏览器
			When tom关注jobs的公众号于'2015-10-02'
			When tom访问jobs的webapp
			When tom进入推广扫描链接

			When tom1扫描tom的推广二维码关注jobs公众号
			When tom2扫描tom的推广二维码关注jobs公众号
			When tom3扫描tom的推广二维码关注jobs公众号

			When tom2取消关注jobs的公众号

		#jack的扫码会员-之前关注后取消关注之后再扫码关注不计数
			When 清空浏览器
			When jack关注jobs的公众号于'2015-10-03'
			When jack访问jobs的webapp
			When jack进入推广扫描链接

			When jack1扫描jack的推广二维码关注jobs公众号
			When jack2扫描jack的推广二维码关注jobs公众号

			When jack3关注jobs的公众号于'2015-10-04'
			When jack3取消关注jobs的公众号

			When jack3扫描jack的推广二维码关注jobs公众号

		#marry的扫码会员-扫码了tom的推广扫码，再扫marry的推广扫码不计数
			When 清空浏览器
			When tom进入推广扫描链接
			When marry1扫描tom的推广二维码关注jobs公众号

			When 清空浏览器
			When marry关注jobs的公众号于'2015-10-04'
			When marry访问jobs的webapp
			When marry进入推广扫描链接

			When marry1取消关注jobs的公众号
			When marry1扫描marry的推广二维码关注jobs公众号

			When marry2扫描marry的推广二维码关注jobs公众号

@mall2 @bi @memberAnalysis 
Scenario: 1  会员概况：推广扫码排行Top10
	Given jobs登录系统
	When jobs设置筛选日期
		"""
		{
			"start_date":"今天",
			"end_date":"今天"
		}
		"""
		
	Then jobs获得推广扫码排行Top10
		| rank | username | followers |
		|   1  |   tom    |     4     |
		|   2  |   bill   |     4     |
		|   3  |   jack   |     2     |
		|   4  |   marry  |     1     |
	