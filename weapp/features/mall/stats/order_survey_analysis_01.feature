#_author_:三香  2016.05.10

Feature: 销售概况-订单概况
    """
        补充2016.05.10
            同步订单中的数据计入到数据罗盘中
                1、经营报告中的以下字段，统计同步订单的数据
                    成交金额、成交订单、购买总人数、客单价
                2、销售分析-订单概况分析
                    成交金额、客单价、成交商品、支付金额饼图
                3、销售分析-商品概况分析
                    购买总人数、下单单量、成交总件数、商品销售排行次数

        对店铺的订单进行不同维度的数据统计分析，订单的订单来源为'本店'和‘商城’

    """

Background:
    #说明：toms代表微众商城，jobs代表商户
    #jobs的基础数据设置

    Given jobs登录系统
    And jobs设定会员积分策略
        """
        {
            "be_member_increase_count":400,
            "integral_each_yuan": 10
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
            },{
                "id":"0000003",
                "password":"1234567",
                "status":"未使用",
                "price":100.00
            },{
                "id":"0000004",
                "password":"1234567",
                "status":"未使用",
                "price":50.00
            }]
        }
        """

    And jobs已添加商品
        """
        [{
            "name": "商品1",
            "postage": 10.00,
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
            "postage": 15.00,
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
        }]
        """

    When jobs创建积分应用活动
        """
        [{
            "name": "商品1积分应用",
            "start_date": "2014-8-1",
            "end_date": "10天后",
            "product_name": "商品1",
            "is_permanant_active": "true",
            "rules": [{
                "member_grade": "全部",
                "discount": 20,
                "discount_money": 20.00
            }]
        }, {
            "name": "商品2积分应用",
            "start_date": "2014-8-1",
            "end_date": "10天后",
            "product_name": "商品2",
            "is_permanant_active": "true",
            "rules": [{
                "member_grade": "全部",
                "discount": 20,
                "discount_money": 20.00
            }]
        }]
        """
    And jobs添加优惠券规则
        """
        [{
            "name": "全体券1",
            "money": 10.00,
            "start_date": "2014-8-1",
            "end_date": "10天后",
            "coupon_id_prefix": "coupon1_id_"
        }]
        """

    When jobs批量获取微信用户关注
        | member_name | attention_time    | member_source |    extra   |
        | bill        | 2014-8-5 8:00:00  | 直接关注      | -          |
        | tom         | 2014-9-1 8:00:00  | 推广扫码      | 渠道扫码01 |
        | marry       | 2014-9-1 10:00:00 | 会员分享      | bill       |
        | tom1        | 2014-9-1 8:00:00  | 会员分享      | bill       |
        | tom2        | 2014-9-3 8:00:00  | 会员分享      | bill       |
        | tom3        | 2014-6-1 8:00:00  | 推广扫码      | 渠道扫码01 |

        #在查询区间之前有有效订单；
        #在查询区间之前有无效订单；
        #在查询区间之前无订单；
        #三种有效订单类型：待发货、已发货、已完成
        #无效订单类型：待支付、已取消、退款中、退款完成
        #三种支付方式：支付宝、微信支付、货到付款
        #优惠期扣：微众卡、优惠券、积分、微众卡+优惠券、微众卡+积分
    When 微信用户批量消费jobs的商品
        | order_id |   date   | consumer | product  | payment | pay_type | postage*   | price*    | product_integral |       coupon         | paid_amount*   |  weizoom_card   | alipay*   | wechat*   | cash*   |   action    | order_status*|
        |   0001   | 2014-8-5 | bill     | 商品1,1  | 支付    | 支付宝   | 10.00      | 100.00    |                  |                      | 110.00         | 0000001,1234567 | 0.00      | 0.00      | 0.00    |             | 待发货       |
        |   0002   | 2014-8-6 | tom      | 商品2,2  |         |          | 15.00      | 100.00    |                  |                      | 215.00         |                 | 0.00      | 0.00      | 0.00    |  jobs,取消  | 已取消       |    
        |   0003   | 2014-9-1 | bill     | 商品2,2  | 支付    | 支付宝   | 15.00      | 100.00    |                  |                      | 215.00         | 0000002,1234567 | 125.00    | 0.00      | 0.00    |             | 待发货       |
        |   0004   | 2014-9-2 | tom      | 商品1,1  | 支付    | 微信支付 | 10.00      | 100.00    |                  |                      | 110.00         |                 | 0.00      | 110.00    | 0.00    |  jobs,发货  | 已发货       |
        |   0005   | 2014-9-3 | marry    | 商品1,1  | 支付    | 货到付款 | 10.00      | 100.00    |                  |                      | 110.00         |                 | 0.00      | 0.00      | 110.00  |             | 待发货       |
        |   0006   | 2014-9-3 | tom1     | 商品1,1  |         |          | 10.00      | 100.00    |                  |                      | 110.00         |                 | 0.00      | 0.00      | 0.00    |  jobs,取消  | 已取消       |
        |   0007   | 2014-9-4 | bill     | 商品1,1  | 支付    | 货到付款 | 10.00      | 100.00    |                  |                      | 110.00         |                 | 0.00      | 0.00      | 110.00  |             | 待发货       |
        |   0008   | 2014-9-4 | marry    | 商品1,1  | 支付    | 支付宝   | 10.00      | 100.00    | 200              |                      | 90.00          |                 | 90.00     | 0.00      | 0.00    |  jobs,发货  | 已发货       |
        |   0009   | 2014-9-5 | bill     | 商品1,2  | 支付    | 微信支付 | 10.00      | 100.00    |                  | 全体券1,coupon1_id_1 | 200.00         | 0000003,1234567 | 0.00      | 100.00    | 0.00    |             | 待发货       |
        |   0010   | 2014-9-5 | marry    | 商品1,1  | 支付    | 微信支付 | 10.00      | 100.00    | 200              |                      | 90.00          |                 | 0.00      | 0.00      | 0.00    |  jobs,退款  | 退款中       |
        |   0011   | 2014-9-6 | tom      | 商品1,1  | 支付    | 支付宝   | 10.00      | 100.00    |                  | 全体券1,coupon1_id_2 | 100.00         |                 | 100.00    | 0.00      | 0.00    |  jobs,完成  | 已完成       |
        |   0012   | 2014-9-7 | tom1     | 商品2,1  | 支付    | 微信支付 | 15.00      | 100.00    | 200              |                      | 95.00          |                 | 0.00      | 95.00     | 0.00    |  jobs,完成  | 已完成       |
        |   0013   | 2014-9-8 | tom2     | 商品1,1  | 支付    | 支付宝   | 10.00      | 100.00    |                  | 全体券1,coupon1_id_3 | 100.00         |                 | 100.00    | 0.00      | 0.00    |  jobs,完成  | 已完成       |
        |   0014   | 2014-9-9 | tom3     | 商品2,1  | 支付    | 微信支付 | 15.00      | 100.00    | 200              |                      | 95.00          | 0000004,1234567 | 0.00      | 45.00     | 0.00    |  jobs,完成  | 已完成       |
        |   0017   | 今天     | bill     | 商品2,1  |         |          | 15.00      | 100.00    | 200              |                      | 95.00          |                 | 0.00      | 0.00      | 0.00    |             | 待支付       |

#补充：张三香 2016.05.10
#同步订单数据计入到数据罗盘的各个字段中
@mall2 @bi @salesAnalysis
Scenario:1 查询订单概况数据，包含自营平台同步的订单
    #jobs为普通商家、nokia为自营平台
    Given 添加jobs店铺名称为'jobs商家'
    Given 设置nokia为自营平台账号
    Given nokia登录系统
    Given nokia设定会员积分策略
        """
        {
            "integral_each_yuan": 1,
            "use_ceiling": 100,
            "be_member_increase_count": 300
        }
        """
    And nokia已添加支付方式
        """
        [{
            "type": "微信支付",
            "is_active": "启用"
        }, {
            "type": "支付宝",
            "is_active": "启用"
        }, {
            "type": "货到付款",
            "is_active": "启用"
        }]
        """
    When nokia开通使用微众卡权限
    When nokia添加支付方式
        """
        [{
            "type": "微众卡支付",
            "is_active": "启用"
        }]
        """
    Given nokia已添加供货商
        """
        [{
            "name": "供货商1",
            "responsible_person": "宝宝",
            "supplier_tel": "13811223344",
            "supplier_address": "北京市海淀区泰兴大厦",
            "remark": "备注卖花生油"
        }]
        """
    And nokia已添加商品
        """
        [{
            "supplier": "供货商1",
            "name": "nokia商品1",
            "price": 10.00,
            "purchase_price": 9.00,
            "weight": 1.0,
            "stock_type": "无限"
        }]
        """
    When nokia将商品池商品批量放入待售于'2016-05-10 10:30'
            """
            [
                "商品2",
                "商品1"
            ]
            """
    When nokia更新商品'商品2'
        """
        {
            "name":"jobs商品2",
            "supplier":"jobs商家",
            "purchase_price": 90.00,
            "is_member_product":"off",
            "model": {
                "models": {
                    "standard": {
                        "price": 200.00,
                        "user_code":"0102",
                        "weight":1.0,
                        "stock_type": "无限"
                    }
                }
            }
        }
        """
    When nokia更新商品'商品1'
        """
        {
            "name":"jobs商品1",
            "supplier":"jobs商家",
            "purchase_price": 80.00,
            "is_member_product":"off",
            "model": {
                "models": {
                    "standard": {
                        "price": 100.00,
                        "user_code":"0101",
                        "weight":1.0,
                        "stock_type": "无限"
                    }
                }
            }
        }
        """
    When nokia批量上架商品
        """
        ["jobs商品2","jobs商品1"]
        """
    When lily关注nokia的公众号
    When lily访问nokia的webapp
    #1001-微信支付-jobs商品1
        When lily购买nokia的商品
            """
            {
                "order_id":"1001",
                "pay_type":"微信支付",
                "products":[{
                    "name":"jobs商品1",
                    "count":1
                }]
            }
            """
        When lily使用支付方式'微信支付'进行支付订单'1001'
    #1002-支付宝-jobs商品1，jobs商品2
        When lily购买nokia的商品
            """
            {
                "order_id":"1002",
                "pay_type":"支付宝",
                "products":[{
                    "name":"jobs商品1",
                    "count":1
                },{
                    "name":"jobs商品2",
                    "count":1
                }]
            }
            """
        When lily使用支付方式'微信支付'进行支付订单'1002'
    #1003-货到付款-jobs商品1，nokia商品1
        When lily购买nokia的商品
            """
            {
                "order_id":"1003",
                "pay_type":"货到付款",
                "products":[{
                    "name":"jobs商品1",
                    "count":1
                },{
                    "name":"nokia商品1",
                    "count":1
                }]
            }
            """
    #1004-优惠抵扣-jobs商品2，nokia商品1
        When lily购买nokia的商品
            """
            {
                "order_id":"1004",
                "pay_type":"货到付款",
                "products":[{
                    "name":"jobs商品2",
                    "count":1
                },{
                    "name":"nokia商品1",
                    "count":1
                }],
                    "integral":210,
                    "integral_money": 210.00
            }
            """

    Given jobs登录系统
    When jobs设置筛选日期
        """
        {
            "start_date":"2014-9-1",
            "end_date":"今天"
        }
        """
    When jobs查询订单概况统计
    #订单概况
    Then jobs获得订单概况统计数据
        """
        {
            "成交订单": 14,
            "成交金额": 1705.00,
            "客单价": 121.79,
            "成交商品": 17,
            "优惠抵扣": 30.00
        }
        """

    #订单趋势
    Then jobs获得订单趋势统计数据
        """
        {
            "待发货":8,
            "已发货":2,
            "已完成":4
        }
        """
    Then jobs获得支付金额统计数据
        """
        {
            "支付宝":435.00,
            "微信支付":810.00,
            "货到付款":220.00,
            "微众卡支付":240.00
        }
        """





