#_author_:张三香

Feature: 会员分析-会员概况

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
    And jobs设定会员积分策略
        """
        {
            "integral_each_yuan":10
        }
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
    And jobs开通使用微众卡权限
    And jobs添加支付方式
        """
        [{
            "type": "微众卡支付",
            "description": "我的微众卡支付",
            "is_active": "启用"
        }]
        """
    Given jobs已创建微众卡
        """
        {
            "cards":[{
                "id":"0000001",
                "password":"1234567",
                "status":"未使用",
                "price":110.00
            },{
                "id":"0000002",
                "password":"1234567",
                "status":"未使用",
                "price":90.00
            }]
        }
        """
    
    When jobs添加商品规格
        """
        [{
            "name": "颜色",
            "type": "文字",
            "values": [{
                "name": "黑色"
            },{
                "name": "白色"
            }]
        }]
        """
    And jobs已添加商品
        """
        [{
            "name": "商品1",
            "promotion_title": "促销商品1",
            "category": "分类1",
            "postage": 10,
            "detail": "商品1详情",
            "swipe_images": [{
                "url": "/standard_static/test_resource_img/hangzhou1.jpg"
            }],
            "model": {
                "models": {
                    "standard": {
                        "price": 100.00,
                        "weight": 5.0,
                        "stock_type": "无限"
                    }
                }
            },
            "synchronized_mall":"是"
        }, {
            "name": "商品2",
            "promotion_title": "促销商品2",
            "category": "分类1",
            "postage": 15,
            "detail": "商品2详情",
            "swipe_images": [{
                "url": "/standard_static/test_resource_img/hangzhou1.jpg"
            }],
            "is_enable_model": "启用规格",
            "model": {
                "models": {
                    "黑色": {
                        "price": 100.00,
                        "weight": 5.0,
                        "stock_type": "无限"
                    },
                    "白色": {
                        "price": 100.00,
                        "weight": 5.0,
                        "stock_type": "无限"
                    }
                }
            },
            "synchronized_mall":"是"
        }]
        """

    And jobs创建积分应用活动
        """
        [{
            "name": "商品1积分应用",
            "start_date": "2014-08-01",
            "end_date": "10天后",
            "product_name": "商品1",
            "is_permanant_active": "true",
            "rules": [{
                "member_grade": "全部会员",
                "discount": 70,
                "discount_money": 70.00
            }]
        }, {
            "name": "商品2积分应用",
            "start_date": "2014-08-01",
            "end_date": "10天后",
            "product_name": "商品2",
            "is_permanant_active": "true",
            "rules": [{
                "member_grade": "全部会员",
                "discount": 70,
                "discount_money": 70.00
            }]
        }]
        """

    And jobs添加优惠券规则
        """
        [{
            "name": "全体券1",
            "money": 10,
            "start_date": "2014-08-01",
            "end_date": "10天后",
            "coupon_id_prefix": "coupon1_id_"
        }]
        """

    When jack关注jobs的公众号于'2014-07-01'
    When tom关注jobs的公众号于'2014-07-02'
    When marry关注jobs的公众号于'2014-07-03'

    #取消关注
    When marry取消关注jobs的公众号

    When 微信用户批量消费jobs的商品
        | order_id |    date    | consumer |    product   | payment | pay_type       |postage*|price*|integral | product_integral |       coupon         | paid_amount* |  weizoom_card     | alipay* | wechat* | cash* |   action      | order_status*  |
        |   0001   | 2014-08-05 |   jack   | 商品1,1      |         |    支付宝      |   10   | 100  |  300    |       200        |                      |     90       |                   |   90    |    0    |   0   |               |    待支付      |
        |   0002   | 8天前      |   tom    | 商品1,1      |         |    支付宝      |   10   | 100  |  200    |       200        |                      |     90       |                   |   90    |    0    |   0   |  jobs,取消    |    已取消      |
        |   0003   | 7天前      |   tom    | 商品2,黑色,2 |   支付  |    微信支付    |   15   | 100  |   0     |        0         | 全体券1,coupon1_id_1 |     205      |                   |    0    |   205   |   0   |  jobs,发货    |    已发货      |
        |   0004   | 6天前      |   tom    | 商品2,白色,1 |   支付  |    货到付款    |   15   | 100  |   0     |        0         | 全体券1,coupon1_id_2 |     105      |  0000002,1234567  |    0    |    0    |  105  |  jobs,完成    |    已完成      |
        |   0005   | 2天前      |  marry   | 商品1,1      |   支付  |    支付宝      |   10   | 100  |  200    |       200        |                      |     90       |                   |   90    |    0    |   0   |  jobs,退款    |    退款中      |
        |   0006   | 今天       |  marry   | 商品1,1      |   支付  |    支付宝      |   10   | 100  |  200    |       200        |                      |     90       |                   |   90    |    0    |   0   |  jobs,完成退款|   退款成功     |
        |   0007   | 今天       |   -tom3  | 商品1,1      |   支付  |    货到付款    |   10   | 100  |   0     |        0         |                      |     110      |                   |    0    |    0    |   110 |               |    已发货      |
        |   0008   | 今天       |   -tom4  | 商品1,1      |   支付  |    支付宝      |   10   | 100  |   0     |        0         |                      |     110      |                   |    0    |    0    |   110 |               |    待发货      |

@stats @ui
Scenario:1 获取默认查询最近7天的会员概况
    Given jobs登录系统
    When jobs访问会员分析
    Then jobs获得筛选日期
        """
        [{
            "option":"最近7天",
            "begin_date":"7天前",
            "end_date":"今天"
        }]
        """
	Then jobs能获得基础数据和会员来源数据
		| item              | quantity|
		| 会员总数          | 7    |
		| 关注会员          | 5    |
		| 新增会员          | 7    |
		| 手机绑定会员      | 0    |
		| 下单会员          | 3    |
		| 会员复购率        | 33.33%|
		| 发起扫码会员      | 0    |
		| 发起分享链接会员  | 2    |
		| 扫码新增会员      | 0    |
		| 直接关注          | 5    |
		| 分享链接新增会员  | 2    |
		| 会员推荐率        | 28.57%|

	Then jobs获得会员增长趋势数据
		|      date     | new_member_count |  bought_member_count |
		|    2015-5-1   |         2        |           1          |
		|    2015-5-2   |         2        |           0          |
		|    2015-5-3   |         4        |           0          |
		|    2015-5-4   |         1        |           0          |
		|    2015-5-5   |         0        |           1          |
		|    2015-5-6   |         2        |           3          |
		|    2015-5-7   |         2        |           0          |
		|    2015-5-8   |         1        |           0          |
		|    2015-5-9   |         2        |           0          |
		|    2015-5-10  |         1        |           0          |

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

	Then job获得会员详细数据
		|    date    |  new_member  | mobile_phone_member | launch_share_link_member | share_link_new_member | launch_spreading_code_member | spreading_code_new_member | order_member |
		|    今天    |      4       |          0          |            2             |           2           |               0              |              0            |       3      |
		|   1天前    |      1       |          0          |            0             |           0           |               0              |              0            |       2      |
		|   2天前    |      1       |          0          |            0             |           0           |               0              |              0            |       1      |

@stats @ui
Scenario:2  会员概况：快速查询切换筛选日期

    Given jobs登录系统

    #备注：今天，今天是2015-6-16，筛选日期：2015-6-16到2015-6-16
    When jobs选中'今天'
    Then jobs获得筛选日期
        """
        [{
            "option":"今天",
            "begin_date":"今天",
            "end_date":"今天"
        }]
        """

    #备注：昨天，今天是2015-6-16，筛选日期：2015-6-15到2015-6-15
    When jobs选中'昨天'
    Then jobs获得筛选日期
        """
        [{
            "option":"昨天",
            "begin_date":"昨天",
            "end_date":"昨天"
        }]
        """

    #备注：最近7天，今天是2015-6-16，筛选日期：2015-6-10到2015-6-16
    When jobs选中'最近7天'
    Then jobs获得筛选日期
        """
        [{
            "option":"最近7天",
            "begin_date":"7天前",
            "end_date":"今天"
        }]
        """

    #备注：最近30天，今天是2015-6-16，筛选日期：2015-5-19到2015-6-16
    When jobs选中'最近30天'
    Then jobs获得筛选日期
        """
        [{
            "option":"最近30天",
            "begin_date":"30天前",
            "end_date":"今天"
        }]
        """

    #备注：最近90天，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
    When jobs选中'最近90天'
    Then jobs获得筛选日期
        """
        [{
            "option":"最近90天",
            "begin_date":"90天前",
            "end_date":"今天"
        }]
        """

    #备注：全部，今天是2015-6-16，筛选日期：2013-1-1到2015-6-16
    When jobs选中'全部'
    Then jobs获得筛选日期
        """
        [{
            "option":"全部",
            "begin_date":"2014-01-01",
            "end_date":"今天"
        }]
        """