#_author_:王丽

Feature: 会员分析-会员概况-推广扫码和分享链接排行榜

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

Background:
	Given jobs登录系统
	And 开启手动清除cookie模式

	When jobs添加商品
		"""
		[{
			"name": "商品1"
		}, {
			"name": "商品2"
		}, {
			"name": "商品3"
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

	#备注：1）关注时间：会员关注公众账号的时间，第一次关注和取消之后再关注的时间不同
	#      2）加入时间：会员第一次关注公众账号，注册成会员的时间，一个系统会员只有一个唯一的加入时间

	When 清空浏览器
	When bill1关注jobs的公众号
	When bill1访问jobs的webapp
	When bill1把jobs的微站链接分享到朋友圈
	
	# When 清空浏览器
	# When bill2点击bill1分享链接
	# When bill2关注jobs的公众号
	When bill2通过bill1分享链接关注jobs的公众号
	When bill2访问jobs的webapp
	When bill2把jobs的微站链接分享到朋友圈

	# When 清空浏览器
	# When bill3点击bill2分享链接
	# When bill3关注jobs的公众号
	When bill3通过bill2分享链接关注jobs的公众号
	When bill3访问jobs的webapp
	When bill3把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill4点击bill2分享链接
	#When bill4关注jobs的公众号
	When bill4通过bill2分享链接关注jobs的公众号
	When bill4访问jobs的webapp
	When bill4把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill5点击bill2分享链接
	#When bill5关注jobs的公众号
	When bill5通过bill2分享链接关注jobs的公众号
	When bill5访问jobs的webapp
	When bill5把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill6点击bill2分享链接
	#When bill6关注jobs的公众号
	When bill6通过bill2分享链接关注jobs的公众号
	When bill6访问jobs的webapp
	When bill6把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill7点击bill3分享链接
	#When bill7关注jobs的公众号
	When bill7通过bill3分享链接关注jobs的公众号
	When bill7访问jobs的webapp
	When bill7把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill8点击bill3分享链接
	#When bill8关注jobs的公众号
	When bill8通过bill3分享链接关注jobs的公众号
	When bill8访问jobs的webapp
	When bill8把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill9点击bill1分享链接
	#When bill9关注jobs的公众号
	When bill9通过bill1分享链接关注jobs的公众号
	When bill9访问jobs的webapp
	When bill9把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill10点击bill7分享链接
	#When bill10关注jobs的公众号
	When bill10通过bill7分享链接关注jobs的公众号
	When bill10访问jobs的webapp
	When bill10把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill11点击bill8分享链接
	#When bill11关注jobs的公众号
	When bill11通过bill8分享链接关注jobs的公众号
	When bill11访问jobs的webapp
	When bill11把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill12点击bill9分享链接
	#When bill12关注jobs的公众号
	When bill12通过bill9分享链接关注jobs的公众号
	When bill12访问jobs的webapp
	When bill12把jobs的微站链接分享到朋友圈

	#When 清空浏览器
	#When bill13点击bill7分享链接
	#When bill13关注jobs的公众号
	When bill13通过bill7分享链接关注jobs的公众号
	When bill13访问jobs的webapp

	#When 清空浏览器
	#When bill14点击bill6分享链接
	#When bill14关注jobs的公众号
	When bill14通过bill6分享链接关注jobs的公众号
	When bill14访问jobs的webapp

	#When 清空浏览器
	#When bill15点击bill5分享链接
	#When bill15关注jobs的公众号
	When bill15通过bill5分享链接关注jobs的公众号
	When bill15访问jobs的webapp

	#When 清空浏览器
	#When bill16点击bill5分享链接
	#When bill16关注jobs的公众号
	When bill16通过bill5分享链接关注jobs的公众号
	When bill16访问jobs的webapp

	When 清空浏览器
	When bill17关注jobs的公众号
	When bill17访问jobs的webapp

	When bill18关注jobs的公众号
	When bill18访问jobs的webapp

	When bill6取消关注jobs的公众号
	When bill7取消关注jobs的公众号

@stats @stats.member @wip.member_rank
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
		|  rank  |  username   | followers |
		|    1   |    bill2    |     4     |
		|    2   |    bill7    |     2     |
		|    3   |    bill5    |     2     |
		|    4   |    bill1    |     2     |
		|    5   |    bill3    |     2     |
		|    6   |    bill8    |     1     |
		|    7   |    bill9    |     1     |
		|    8   |    bill6    |     1     |
