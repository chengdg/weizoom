#watcher:zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_:张三香

Feature:销售分析-商品概况分析

	"""
		一、查询条件
			1、刷选日期
				1）开始日期和结束日期都为空；选择开始结束日期，精确到日期
				2）开始日期或者结束日期，只有一个为空，给出系统提示“请填写XX日期”
				3）默认为‘今天’，筛选日期：‘今天’到‘今天’
				   需求变更，默认为"最近7天"，筛选日期：‘7天前’到‘今天’
				4）包含筛选日期的开始和结束的边界值
				5）手工设置筛选日期，点击查询后，‘快速查询’的所有项都处于‘未选中状态’
			2、快速查看
			    1）今天：查询的当前日期，例如，今天是2015-6-16，筛选日期是：2015-6-16到2015-6-16
			    2）昨天：查询的前一天，例如，今天是2015-6-16，筛选日期是：2015-6-15到2015-6-15
				3）最近7天；包含今天，向前7天；例如，今天是2015-6-16，筛选日期是：2015-6-10到2015-6-16
				4）最近30天；包含今天，向前30天；例如，今天是2015-6-16，筛选日期是：2015-5-19到2015-6-16
				5）最近90天；包含今天，向前90天；例如，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
				6）全部：筛选日期更新到：2013.1.1到今天

		二、商品概况
		    1、【购买总人数】=查询区间内，所有购买过商品的人数

		    '？'说明窗提示:购买商品的总人数

		      备注：购买总人数包括会员（关注和取消关注）和非会员，非会员购买时，uesr_id不同才累加
		            现在系统：非会员的身份就等同于取消关注状态的会员
		            1）会员购买商品1
	                2）已跑路会员购买商品1
	                3）非会员购买商品1：
	                   非会员a从链接1购买商品1
	                   非会员a从链接1购买商品1
	                   非会员a从链接2购买商品1
	                   非会员b从链接2购买商品1
		            只计算有效订单，即订单状态为待发货、已发货、已完成的订单

			2、【下单单量】=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) and (订单.来源='本店')]

			   
			   '？'说明窗提示:当前所选时段内该店铺已发货、待发货、已完成的订单数之和

			3、【总成交件数】=∑订单.商品件数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)
											and (订单.来源='本店')]
		        
		        '？'说明窗提示:当前所选时段内所有成交订单内商品总件数

		三、下单单量排行top10
		    下单单量排行柱状图
		    1、【排名】：从1到10
			2、【商品名称】：商品的名称
			3、【次数】：查询区间内，商品被下单的次数

	         备注：只统计‘有效订单’，即订单状态为待发货、已发货、已完成的订单

			横轴：从1到10
			纵轴：下单次数
			鼠标滑动显示下单次数，例如"50次"	 
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
Scenario:1 获取默认查询最近7天的商品概况分析
    Given jobs登录系统
    When jobs访问商品概况分析
    Then jobs获得筛选日期
        """
        [{
            "option":"最近7天",
            "begin_date":"7天前",
            "end_date":"今天"
        }]
        """
		Then jobs获得商品概况数据
		|    item           | quantity |
		|   购买总人数      |    3     |
		|   下单单量        |    4     |
		|   总成交件数      |    5     |

    And jobs获得下单单量排行top10
        |ranking  |name   |count  |  
        |1        |商品2  |3      |
		|2        |商品1  |2      | 

@stats @ui
Scenario:2  商品概况分析：快速查询切换筛选日期

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