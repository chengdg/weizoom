#watcher:wangli@weizoom.com,benchi@weizoom.com
#_author_:王丽
#editor:王丽  2015.10.19
#editor:王丽  2015.11.16

Feature: 会员分析-会员概况-分享链接排行榜
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
	And 开启手动清除cookie模式

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

@mall2 @bi @memberAnalysis  @stats @stats.member @wip.member_rank
Scenario: 1  会员概况：分享链接排行Top10
	Given jobs登录系统
	When jobs设置筛选日期
		"""
		{
			"start_date":"今天",
			"end_date":"今天"
		}
		"""
		
	Then jobs获得分享链接排行Top10
		| rank | username | followers |
		|   1  |   bill   |     6     |
		|   2  |   marry2 |     2     |
		|   3  |   marry  |     2     |

