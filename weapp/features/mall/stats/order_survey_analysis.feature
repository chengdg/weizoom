#_author_:王丽
#edit：张三香

Feature: 销售概况-订单概况
    对店铺的订单进行不同维度的数据统计分析，订单的订单来源为'本店'和‘商城’

    备注：
        名词解释
            已支付的订单：已支付订单和货到付款提交成功订单
            有效订单：订单状态为 待发货、已发货、已完成的订单
            订单.实付金额：=现金支付金额+微众卡支付金额；不包含优惠券和积分抵扣的金额，包含微众卡支付的金额；

    查询条件
        1、刷选日期
            1）开始日期和结束日期都为空；选择开始结束日期，精确到日期
            2）开始日期或者结束日期，只有一个为空，给出系统提示“请填写XX日期”
            3）默认为‘最近7天’，筛选日期：‘七天前’到‘今天’
            4）包含筛选日期的开始和结束的边界值
            5）手工设置筛选日期，点击查询后，‘快速查询’的所有项都处于‘未选中状态’，时间和选项匹配的，选项处于选中状态
        2、快速查看
            选择快速查看的选项后就直接查询
            1）今天：查询的当前日期，例如，今天是2015-6-16，筛选日期是：2015-6-16到2015-6-16
            2）昨天：查询的前一天，例如，今天是2015-6-16，筛选日期是：2015-6-15到2015-6-15
            3）最近7天；包含今天，向前7天；例如，今天是2015-6-16，筛选日期是：2015-6-10到2015-6-16
            4）最近30天；包含今天，向前30天；例如，今天是2015-6-16，筛选日期是：2015-5-19到2015-6-16
            5）最近90天；包含今天，向前90天；例如，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
            6）全部：筛选日期更新到：2013.1.1到今天

    订单概况
        1、【成交订单】=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)]

            "？"说明弹窗：当前所选时段内该店铺已发货、待发货、已完成的订单数之和

        2、【成交金额】=∑订单.实付金额[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)]

            "？"说明弹窗：当前所选时段内该店铺已支付订单和货到付款提交成功订单的总金额

        3、【客单价】=【成交金额】/【成交订单】

            备注：保留小数点后两位

            "？"说明弹窗：当前所选时段内平均每个订单的金额

        4、【成交商品】=∑订单.商品件数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)]

            "？"说明弹窗：当前所选时段内所有成交订单内商品总件数

            备注：注意一个订单包含多个商品和一个商品购买多件的情况

        5、【优惠抵扣】=∑订单.积分抵扣金额[(订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)] 
                            +∑订单.优惠券抵扣金额[(订单状态 in {待发货、已发货、已完成}) 
                                                    and (订单.下单时间 in 查询区间)] 

            "？"说明弹窗：当前所选时段内成交订单中使用积分或优惠券抵扣的总金额

        6、【总运费】=∑订单.运费金额[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)]

            "？"说明弹窗：当前所选时段内所有成交订单中总支付的运费金额

        备注：订单来源为本店的订单，支付方式只有三种：在线支付(微信支付、支付宝支付)、货到付款

        #虽然现在‘在线支付’只有支付宝、微信两种方式，为了增加可扩展性，修改为用整体减去‘货到付款’来得到‘在线支付’，
        #这样以后再增加了其他的在线支付方式也是不用再调整的
        
        #【在线付款订单】=∑订单.个数[(支付方式 in {'微信支付'、'支付宝支付'}) 
        #                                and (订单状态 in {待发货、已发货、已完成}) 
        #                                and (订单.下单时间 in 查询区间)]
        7、【在线付款订单】=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) 
                            -(∑订单.个数[(支付方式 in {'货到付款'}) 
                                        and (订单状态 in {待发货、已发货、已完成}) 
                                        and (订单.下单时间 in 查询区间)])

            "？"说明弹窗：当前所选时段内除货到付款之外的成交订单数

        #8、【在线付款订单金额】=∑订单.实付金额[(支付方式 in {'微信支付'、'支付宝支付'}) 
        #                                        and (订单状态 in {待发货、已发货、已完成}) 
        #                                        and (订单.下单时间 in 查询区间)]
        8、【在线付款订单金额】=∑订单.实付金额[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)]
                                -(∑订单.实付金额[(支付方式 in {'微信支付'、'支付宝支付'}) 
                                                and (订单状态 in {待发货、已发货、已完成}) 
                                                and (订单.下单时间 in 查询区间)])

            "？"说明弹窗：当前所选时段内除货到付款之外的成交订单金额

        9、【货到付款订单】=∑订单.个数[(支付方式 ='货到付款') and (订单状态 in {待发货、已发货、已完成}) 
                                        and (订单.下单时间 in 查询区间)]

            "？"说明弹窗：当前所选时段内使用货到付款方式的订单数

        10、【货到付款金额】=∑订单.货到付款金额[(支付方式 ='货到付款') and (订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]

            "？"说明弹窗：当前所选时段内使用货到付款方式的订单支付现金总计

    订单分析图表
        店铺内订单来源为'本店'，订单的'下单时间'在查询区间内的，有效订单(订单状态为：待发货、已发货、已完成)进行分析
        1、订单趋势
            店铺内订单来源为'本店'的，订单的'下单时间'在查询区间内的，订单不同状态的订单占比
            1）订单总量：=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)
                备注：待发货、已发货、已完成，订单的'下单时间'在查询区间内的订单数之和
            2）图形划过展开，展示内容为（该区域订单状态、订单量、订单量占比）
            3）点击详情跳转到，带入的查询条件
                【订单名称】：空；【订单编号】：空；【支付方式】：全部；【订单状态】：当前的图形对应的订单状态
                【复购筛选】：全部；【优惠抵扣】：全部；【仅显示微众卡抵扣订单】：否
        2、复购率
            店铺内订单，买家购买次数的统计分析
            1）订单总量：=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)]
            2）“初次购买”：在查询区间以前没有发生过购买，在查询区间内发生初次购买的用户订单数和其在总订单数占比
            3）“重复购买”：在该时间段以前发生过购买或者在该订单的订单时间之前发生过购买，在该时间段内又发生了购买的用户订单数和其在总订单数占比
                            满足下面条件的订单个数总和；（1）下单时间在查询区间内的‘有效订单’（1）订单的买家在该订单下单时间之前有‘有效订单’
            4）图形划过展开，展示内容为（该区域类型、订单量、订单量占比）
            5）点击详情跳转到，带入的查询条件
                【订单名称】：空；【订单编号】：空；【支付方式】：全部；【订单状态】：待发货、已发货、已完成
                【复购筛选】：当前的图形对应的类；【优惠抵扣】：全部；【仅显示微众卡抵扣订单】：否

            备注：1）注意买家在查询区间内发生两次购买，第一次购买为初次购买的统计到'初次购买';
                    第二次购买统计到'重复购买'。
                2）买家未知的订单按照内部的ID计算复购

        3、买家来源
            店铺内订单的'下单时间'在查询区间内的，"有效订单"的买家来源的占比
            1）订单总量：=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间)]
            2）“直接关注购买”：=∑订单.个数[(买家来源 ='直接关注') and (订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]
            3）“推广扫码关注购买”：=∑订单.个数[(买家来源 ='推广扫码') and (订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]
            4）“分享链接关注购买”：=∑订单.个数[(买家来源 ='分享链接') and (订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]
            5）“其他”：=∑订单.个数[(买家来源不确定) and (订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]
            6）图形划过展开，展示内容为（该区域类型、订单量、订单量占比）
            7）点击详情跳转到，带入的查询条件
                【订单名称】：空；【订单编号】：空；【支付方式】：全部；【订单状态】：待发货、已发货、已完成
                【复购筛选】：当前的图形对应的类；【优惠抵扣】：全部；【仅显示微众卡抵扣订单】：否

            备注：1）买家可能会先下订单再关注，即买家的'关注时间'晚于订单的'下单时间'，这种订单的归类到其他
                2）没有关注店铺公众账号，直接下的订单的归类到其他
                即：所有不能确定买家的都归类到其他

        4、支付金额
            店铺内订单的'下单时间'在查询区间内的，"有效订单"的支付方式的支付金额占比
            1）订单总金额：=∑订单.实付金额[(订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]
            2）支付宝支付金额:=∑订单.支付宝支付金额[(订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]
            3）微信支付金额:=∑订单.微信支付金额[(订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]
            4）货到付款支付金额:=∑订单.货到付款支付金额[(订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]
            5）微众卡支付金额:=∑订单.微众卡支付金额[(订单状态 in {待发货、已发货、已完成}) 
                                            and (订单.下单时间 in 查询区间)]
            6）图形划过展开，展示内容为（该区域类型、金额、金额占比）

            备注：金额维度的分析，没有点击详情进入订单明细分析界面的功能                    
        
        5、优惠抵扣
            店铺内订单的'下单时间'在查询区间内的，"有效订单"的优惠抵扣方式的订单占比
            1）订单总量：=∑订单.个数[(订单状态 in {待发货、已发货、已完成}) and (订单.下单时间 in 查询区间) 
                                     and (优惠抵扣使用 in {积分、优惠券、微众卡})]
            2）微众卡支付：=∑订单.个数[(订单.优惠抵扣 = {微众卡}) and (订单状态 in {待发货、已发货、已完成}) 
                                    and (订单.下单时间 in 查询区间)]
                （1）微众卡支付金额：=∑订单.微众卡支付金额[(订单.优惠抵扣 = {微众卡}) and (订单状态 in {待发货、已发货、已完成}) 
                                    and (订单.下单时间 in 查询区间)]
            3）积分抵扣：=∑订单.个数[(订单.优惠抵扣 = {积分抵扣}) and (订单状态 in {待发货、已发货、已完成}) 
                （1）积分抵扣金额：=∑订单.积分抵扣金额[(订单.优惠抵扣 = {积分抵扣}) and (订单状态 in {待发货、已发货、已完成}) 
                                    and (订单.下单时间 in 查询区间)]    
            4）优惠券：=∑订单.个数[(订单.优惠抵扣 = {优惠券}) and (订单状态 in {待发货、已发货、已完成}) 
                                    and (订单.下单时间 in 查询区间)]
                （1）优惠券金额：=∑订单.优惠券金额[(订单.优惠抵扣 = {优惠券}) and (订单状态 in {待发货、已发货、已完成}) 
                                    and (订单.下单时间 in 查询区间)]
            5）微众卡+积分：=∑订单.个数[(订单.优惠抵扣 = {微众卡+积分}) 
                                    and (订单状态 in {待发货、已发货、已完成}) 
                                    and (订单.下单时间 in 查询区间)]
                （1）(微众卡+积分)金额：=∑订单.(微众卡+积分)金额[(订单.优惠抵扣 = {微众卡+积分}) 
                                    and (订单状态 in {待发货、已发货、已完成}) 
                                    and (订单.下单时间 in 查询区间)]
            6）微众卡+优惠券：=∑订单.个数[(订单.优惠抵扣 = {微众卡+优惠券}) 
                                    and (订单状态 in {待发货、已发货、已完成}) 
                                    and (订单.下单时间 in 查询区间)]
                （1）(微众卡+优惠券)金额：=∑订单.(微众卡+优惠券)金额[(订单.优惠抵扣 = {微众卡+优惠券}) 
                                    and (订单状态 in {待发货、已发货、已完成}) 
                                    and (订单.下单时间 in 查询区间)]
             备注：目前的一个订单中不能同时使用‘积分’和‘优惠券’，这样我们的‘优惠抵扣’的图表的两项（积分+优惠券；微众卡+积分+优惠券）就不存在了


            9）图形划过展开，展示内容为（该区域类型、订单量、订单量占比、金额）
            10）点击详情跳转到，带入的查询条件
                【筛选日期】：当前‘订单概况’的筛选日期
                【订单名称】：空；【订单编号】：空；【支付方式】：全部；
                【订单状态】：待发货、已发货、已完成【复购筛选】：全部；
                【优惠抵扣】：当前的图形对应的优惠抵扣方式；【仅显示微众卡抵扣订单】：否

Background:
    #说明：toms代表微众商城，jobs代表商户
    #jobs的基础数据设置

    Given jobs登录系统
    When jobs设置未付款订单过期时间:
        """
        {
            "no_payment_order_expire_day":"1天"
        }
        """
    Given jobs已添加商品分类
        """
        [{
            "name": "分类1"
        }]
        """
    And jobs设定会员积分策略
        # 即: "integral_each_yuan": 10    
        """
        {
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
    Given jobs已添加商品
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
                        "freight":"10",
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
            "model": {
                "models": {
                    "standard": {
                        "price": 100.00,
                        "freight":"15",
                        "weight": 5.0,
                        "stock_type": "无限"
                    }
                }
            },
            "synchronized_mall":"是"
        }]

        """
    And jobs已创建微众卡
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
                "price":95.00
            },{
                "id":"0000005",
                "password":"1234567",
                "status":"未使用",
                "price":80.00
            },{
                "id":"0000006",
                "password":"1234567",
                "status":"未使用",
                "price":50.00
            },{
                "id":"0000007",
                "password":"1234567",
                "status":"未使用",
                "price":50.00
            }]
        }
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
                "discount": 70,
                "discount_money": 70.0
            }]
        }, {
            "name": "商品2积分应用",
            "start_date": "2014-8-1",
            "end_date": "10天后",
            "product_name": "商品2",
            "is_permanant_active": "true",
            "rules": [{
                "member_grade": "全部",
                "discount": 70,
                "discount_money": 70.0
            }]
        }]
        """
    And jobs添加优惠券规则
        """
        [{
            "name": "全体券1",
            "money": 10,
            "start_date": "2014-8-1",
            "end_date": "10天后",
            "coupon_id_prefix": "coupon1_id_"
        }]
        """
    # 暂时不起作用
    # Given jobs已添加'渠道扫码'营销活动
    #     """
    #     [{
    #         "setting_id": 0,
    #         "name": "渠道扫码01",
    #         "prize_info": "{\"id\":-1, \"name\": \"non-prize\", \"type\": \"积分\"}",
    #         "reply_type": 0,
    #         "reply_material_id": 0,
    #         "re_old_member": 1,
    #         "grade_id": 16,
    #         "remark": "备注1",
    #         "create_time":"2015-06-24 09:00:00"
    #     }]
    #     """

    #When 已有一批微信用户关注jobs
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
        | date       | consumer | type    |businessman|   product | payment | pay_type | freight |   price  | integral | product_integral |       coupon           | paid_amount | alipay | wechat | cash |   action    |  order_status   |
        | 2014-8-5   | bill     |  购买   | jobs      | 商品1,1   | 支付    | 支付宝   | 10      | 100      |     0    |                  |                        | 110         | 110    | 0      | 0    |             |  待发货         |
        | 2014-8-6   | tom      |  购买   | jobs      | 商品2,2   |         |          | 15      | 100      |     0    |                  |                        | 0           | 0      | 0      | 0    |  jobs,取消  |  已取消         |    
        | 2014-9-1   | bill     |  购买   | jobs      | 商品2,2   | 支付    | 支付宝   | 15      | 100      |     0    |                  |                        | 215         | 215    | 0      | 0    |             |  待发货         |
        | 2014-9-2   | tom      |  购买   | jobs      | 商品1,1   | 支付    | 微信支付 | 10      | 100      |     0    |                  |                        | 110         | 0      | 110    | 0    |  jobs,发货  |  已发货         |
        | 2014-9-3   | marry    |  购买   | jobs      | 商品1,1   | 支付    | 货到付款 | 10      | 100      |     0    |                  |                        | 110         | 0      | 0      | 110  |             |  待发货         |
        | 2014-9-3   | tom1     |  购买   | jobs      | 商品1,1   |         |          | 10      | 100      |     0    |                  |                        | 0           | 0      | 0      | 0    |  jobs,取消  |  已取消         |
        | 2014-9-4   | bill     |  购买   | jobs      | 商品1,1   | 支付    | 货到付款 | 10      | 100      |     0    |                  |                        | 110         | 0      | 0      | 0    |             |  待发货         |
        | 2014-9-4   | marry    |  购买   | jobs      | 商品1,1   | 支付    | 支付宝   | 10      | 100      |   200    | 200              |                        | 90          | 90     | 0      | 0    |  jobs,发货  |  已发货         |
        | 2014-9-5   | bill     |  购买   | jobs      | 商品1,2   | 支付    | 微信支付 | 10      | 100      |     0    |                  | 全体券1,coupon1_id_1   | 200         | 0      | 200    | 0    |             |  待发货         |
        | 2014-9-5   | marry    |  购买   | jobs      | 商品1,1   | 支付    | 微信支付 | 10      | 100      |   200    | 200              |                        | 90          | 0      | 0      | 0    |  jobs,退款  |  退款中         |
        | 2014-9-6   | tom      |  购买   | jobs      | 商品1,1   | 支付    | 支付宝   | 10      | 100      |     0    |                  | 全体券1,coupon1_id_2   | 100         | 0      | 0      | 0    |  jobs,完成  |  已完成         |
        | 2014-9-7   | tom1     |  购买   | jobs      | 商品2,1   | 支付    | 微信支付 | 15      | 100      |   200    | 200              |                        | 95          | 0      | 0      | 0    |  jobs,完成  |  已完成         |
        | 2014-9-8   | tom2     |  购买   | jobs      | 商品1,1   | 支付    | 支付宝   | 10      | 100      |     0    |                  | 全体券1,coupon1_id_3   | 100         | 20     | 0      | 0    |  jobs,完成  |  已完成         |
        | 2014-9-9   | tom3     |  购买   | jobs      | 商品2,1   | 支付    | 微信支付 | 15      | 100      |   200    | 200              |                        | 95          | 0      | 45     | 0    |  jobs,完成  |  已完成         |
        | 2014-9-10  | -tom4    |  购买   | jobs      | 商品2,1   | 支付    | 货到付款 | 15      | 100      |     0    |                  |                        | 115         | 0      | 0      | 65   |  jobs,完成  |  已完成         |
        | 2014-9-11  | -tom4    |  购买   | jobs      | 商品2,1   | 支付    | 微信支付 | 15      | 100      |     0    |                  |                        | 115         | 0      | 0      | 115  |jobs,完成退款| 退款成功        |
        | 今天       | bill     |  购买   | jobs      | 商品2,1   |         |          | 15      | 100      |   200    | 200              |                        | 95          | 0      | 0      | 0    |             |  待支付         |
        | 今天       | tom      |  购买   | jobs      | 商品2,1   | 支付    | 支付宝   | 15      | 100      |   200    | 200              |                        | 95          | 95     | 0      | 0    |  jobs,发货  |  已发货         |

@stats @stats.order_survey @mall2
Scenario: 1 订单概况数据，查询区间

    Given jobs登录系统

    When jobs设置筛选日期
        """
        {
            "start_date":"2014-9-1",
            "end_date":"2014-9-21"
        }
        """

    When jobs查询订单概况统计

    #订单概况
    Then jobs获得订单概况统计数据
        """
        {
            "成交订单": 11,
            "成交金额": 1340.00,
            "客单价": 121.82,
            "成交商品": 13,
            "优惠抵扣": 90.00,
            "总运费": 130.00,
            "在线支付金额": 1005.00,
            "货到付款金额": 335.00,
            "在线支付订单": 8,
            "货到付款订单": 3
        }
        """

    #订单趋势
    Then jobs获得订单趋势统计数据
        """
        {
            "待发货":4,
            "已发货":2,
            "已完成":5
        }
        """

    #复购率
    And jobs获得复购率统计数据
        """
        {
            "初次购买":6,
            "重复购买":5
        }
        """

    #买家来源
    And jobs获得买家来源统计数据
        """
        {
            "直接关注购买":3,
            "推广扫码关注购买":3,
            "分享链接关注购买":4,
            "其他":1
        }
        """

    #支付金额
    And jobs获得支付金额统计数据
        """
        {
            "支付宝":505.00,
            "微信支付":500.00,
            "货到付款":335.00,
            "微众卡支付":0.00
        }
        """

    #优惠抵扣
    And jobs获得优惠抵扣统计数据
        """
        {
            "微众卡支付.单量":0,
            "微众卡支付.金额":0.00,
            "积分抵扣.单量":3,
            "积分抵扣.金额":60.00,
            "优惠券.单量":3,
            "优惠券.金额":30.00,
            "微众卡+积分.单量":0,
            "微众卡+积分.金额":0.00,
            "微众卡+优惠券.单量":0,
            "微众卡+优惠券.金额":0.00,
            "优惠抵扣订单总数":6
        }
        """

@ignore
Scenario: 2 订单概况数据，查询区间

    Given jobs登录系统

    When jobs设置筛选日期
        """
        {
            "start_date":"2014-9-1",
            "end_date":"2014-9-21"
        }
        """

    When 查询订单概况统计

    #订单概况
        Then 获得订单概况统计数据
            """
            {
                "成交订单": 11,
                "成交金额": 1340.00,
                "客单价": 121.82,
                "成交商品": 13,
                "优惠抵扣": 90.00,
                "总运费": 130.00,
                "在线支付金额": 1165.00,
                "货到付款金额": 175.00
                "在线支付订单": 9,
                "货到付款订单": 2
            }
            """

    #订单趋势
        Then 获得订单趋势统计数据
            """
            {
                "待发货":4,
                "已发货":2,
                "已完成":5
            }
            """
            | order_status | order_quantity | proportion |
            |  待发货      |       4        |   36.36%   |
            |  已发货      |       2        |   18.18%   |
            |  已完成      |       5        |   45.45%   |

        #订单趋势详情

            #待发货
                When jobs进入'待发货'详情
                Then jobs获得查询条件
                """
                [{
                    "begin_date":"2014-9-1",
                    "end_date":"2014-9-21",
                    "product_name":"",
                    "order_number":"",
                    "payment_method":"",
                    "order_status":"待发货",
                    "re_purchase":"",
                    "preferential_deduction":"",
                    "only_weizoom_card":""
                }]
                """

                And jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品1     | 对应订单编号 |    10           |   10    |   200       |  微信支付      |  bill    | 2014-9-5 |  待发货      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  货到付款      |  bill    | 2014-9-4 |  待发货      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  货到付款      |  marry   | 2014-9-3 |  待发货      |
                    |    商品2     | 对应订单编号 |    0            |   15    |   215       |  支付宝        |  bill    | 2014-9-1 |  待发货      |        

            #已发货
                When jobs进入'已发货'详情
                Then jobs获得查询条件
                    """
                    [{
                        "begin_date":"2014-9-1",
                        "end_date":"2014-9-21",
                        "product_name":"",
                        "order_number":"",
                        "payment_method":"",
                        "order_status":"已发货",
                        "re_purchase":"",
                        "preferential_deduction":"",
                        "only_weizoom_card":""
                    }]
                    """
                And jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |    date    | order_status |
                    |    商品1     | 对应订单编号 |    20           |   10    |    90       |  微信支付      |  marry   | 2014-9-4   |  已发货      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2   |  已发货      |            

            #已完成
                When jobs进入'已完成'详情
                Then jobs获得查询条件
                    """
                    [{
                        "begin_date":"2014-9-1",
                        "end_date":"2014-9-21",
                        "product_name":"",
                        "order_number":"",
                        "payment_method":"",
                        "order_status":"已完成",
                        "re_purchase":"",
                        "preferential_deduction":"",
                        "only_weizoom_card":""
                    }]
                    """
                And jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   datet   | order_status |
                    |    商品2     | 对应订单编号 |    0            |   15    |   115       |  货到付款      |  tom4    | 2014-9-10 |  已完成      |
                    |    商品2     | 对应订单编号 |    20           |   15    |    95       |  微信支付      |  tom3    | 2014-9-9  |  已完成      |
                    |    商品1     | 对应订单编号 |    10           |   10    |    100      |  支付宝        |  tom2    | 2014-9-8  |  已完成      |
                    |    商品2     | 对应订单编号 |    20           |   15    |    95       |  微信支付      |  tom1    | 2014-9-7  |  已完成      |
                    |    商品1     | 对应订单编号 |    10           |   10    |    100      |  支付宝        |  tom     | 2014-9-6  |  已完成      |    

    #复购率
        And jobs获得复购率
            """
            {
                "初次购买":6,
                "重复购买":5
            }
            """

            |   item    | order_quantity | proportion |
            |  初次购买 |       6        |   54.55%   |
            |  重复购买 |       5        |   45.45%   |

        #复购详情
            #初次购买
                When jobs进入'初次购买'详情
                Then jobs获得查询条件
                    """
                    [{
                        "begin_date":"2014-9-1",
                        "end_date":"2014-9-21",
                        "product_name":"",
                        "order_number":"",
                        "payment_method":"",
                        "order_status":["待发货","已发货","已完成"],
                        "re_purchase":"初次购买",
                        "preferential_deduction":"",
                        "only_weizoom_card":"",
                        "buyers_source":""
                    }]
                    """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品2     | 对应订单编号 |    0            |   15    |   115       |  货到付款      |  未知    | 2014-9-10|  已完成      |
                    |    商品2     | 对应订单编号 |    20           |   15    |    95       |  微信支付      |  tom3    | 2014-9-9 |  已完成      |
                    |    商品1     | 对应订单编号 |    10           |   10    |    100      |  支付宝        |  tom2    | 2014-9-8 |  已完成      |
                    |    商品2     | 对应订单编号 |    20           |   15    |    95       |  微信支付      |  tom1    | 2014-9-7 |  已完成      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2 |  已发货      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  货到付款      |  marry   | 2014-9-3 |  待发货      |    

            #重复购买
                When jobs进入'重复购买'详情
                Then jobs获得查询条件
                    """
                    [{
                        "begin_date":"2014-9-1",
                        "end_date":"2014-9-21",
                        "product_name":"",
                        "order_number":"",
                        "payment_method":"",
                        "order_status":["待发货","已发货","已完成"],
                        "re_purchase":"重复购买",
                        "preferential_deduction":"",
                        "only_weizoom_card":"",
                        "buyers_source":""
                    }]
                    """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品1     | 对应订单编号 |    10           |   10    |    100      |  支付宝        |  tom     | 2014-9-6 |  已完成      |
                    |    商品1     | 对应订单编号 |    10           |   10    |   200       |  微信支付      |  bill    | 2014-9-5 |  待发货      |
                    |    商品1     | 对应订单编号 |    20           |   10    |    90       |  微信支付      |  marry   | 2014-9-4 |  已发货      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  货到付款      |  bill    | 2014-9-4 |  待发货      |
                    |    商品2     | 对应订单编号 |    0            |   15    |   215       |  支付宝        |  bill    | 2014-9-1 |  待发货      |    

    #买家来源
        And jobs获得买家来源
            """
            {
                "直接关注购买":3,
                "推广扫码关注购买":3,
                "分享链接关注购买":4,
                "其他":1
            }
            """
            |     item         |  order_quantity  |  proportion  |
            | 直接关注购买     |        3         |    27.27%    |
            | 推广扫码关注购买 |        3         |    27.27%    |
            | 分享链接关注购买 |        4         |    36.36%    |
            | 其他             |        1         |    9.09%     |

        #买家来源详情
            #直接关注购买
                When jobs进入'直接关注购买'详情
                Then jobs获得查询条件
                    """
                    [{
                        "begin_date":"2014-9-1",
                        "end_date":"2014-9-21",
                        "product_name":"",
                        "order_number":"",
                        "payment_method":"",
                        "order_status":["待发货","已发货","已完成"],
                        "re_purchase":"",
                        "preferential_deduction":"",
                        "only_weizoom_card":"",
                        "buyers_source":"直接关注购买"
                    }]
                    """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品1     | 对应订单编号 |    10           |   10    |   200       |  微信支付      |  bill    | 2014-9-5 |  待发货      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  货到付款      |  bill    | 2014-9-4 |  待发货      |
                    |    商品2     | 对应订单编号 |    0            |   15    |   215       |  支付宝        |  bill    | 2014-9-1 |  待发货      |    
                            
            #推广扫码关注购买
                When jobs进入'推广扫码关注购买'详情
                Then jobs获得查询条件
                """
                [{
                    "begin_date":"2014-9-1",
                    "end_date":"2014-9-21",
                    "product_name":"",
                    "order_number":"",
                    "payment_method":"",
                    "order_status":["待发货","已发货","已完成"],
                    "re_purchase":"",
                    "preferential_deduction":"",
                    "only_weizoom_card":"",
                    "buyers_source":"推广扫码关注购买"
                }]
                """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品2     | 对应订单编号 |    20           |   15    |    95       |  微信支付      |  tom3    | 2014-9-9 |  已完成      |
                    |    商品1     | 对应订单编号 |    10           |   10    |    100      |  支付宝        |  tom     | 2014-9-6 |  已完成      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  微信支付      |  tom     | 2014-9-2 |  已发货      |

            #分享链接关注购买
                When jobs进入'分享链接关注购买'详情
                Then jobs获得查询条件
                """
                [{
                    "begin_date":"2014-9-1",
                    "end_date":"2014-9-21",
                    "product_name":"",
                    "order_number":"",
                    "payment_method":"",
                    "order_status":["待发货","已发货","已完成"],
                    "re_purchase":"",
                    "preferential_deduction":"",
                    "only_weizoom_card":"",
                    "buyers_source":"分享链接关注购买"
                }]
                """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品1     | 对应订单编号 |    10           |   10    |    100      |  支付宝        |  tom2    | 2014-9-8 |  已完成      |
                    |    商品2     | 对应订单编号 |    20           |   15    |    95       |  微信支付      |  tom1    | 2014-9-7 |  已完成      |
                    |    商品1     | 对应订单编号 |    20           |   10    |    90       |  微信支付      |  marry   | 2014-9-4 |  已发货      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  货到付款      |  marry   | 2014-9-3 |  待发货      |    

            #其他
                When jobs进入'其他'详情
                Then jobs获得查询条件
                """
                [{
                    "begin_date":"2014-9-1",
                    "end_date":"2014-9-21",
                    "product_name":"",
                    "order_number":"",
                    "payment_method":"",
                    "order_status":["待发货","已发货","已完成"],
                    "re_purchase":"",
                    "preferential_deduction":"",
                    "only_weizoom_card":"",
                    "buyers_source":"其他"
                }]
                """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品2     | 对应订单编号 |    0            |   15    |   115       |  货到付款      |  未知    | 2014-9-10|  已完成      |

    #支付金额

        And jobs获得支付金额
            """
            {
                "支付宝":325,
                "微信支付":355,
                "货到付款":175,
                "微众卡支付":485
            }
            """
            |     item     |  sum_money  |  proportion  |    
            |    支付宝    |    325      |    19.40%    |
            |   微信支付   |    355      |    26.49%    |
            |   货到付款   |    175      |    13.06%    |
            |  微众卡支付  |    485      |    36.19%    |

    #优惠抵扣
        And jobs获得优惠抵扣
            """
            {
                "微众卡支付.单量":2,
                "微众卡支付.金额":165,
                "积分抵扣.单量":1,
                "积分抵扣.金额":20,
                "优惠券.单量":1,
                "优惠券.金额":10,
                "微众卡+积分.单量":2,
                "微众卡+积分.金额":185,
                "微众卡+优惠券.单量":2,
                "微众卡+优惠券.金额":200,
                "优惠抵扣订单总数":8
            }
            """
            |         item           |  order_quantity  |  proportion  |  sum_money  |
            |     微众卡支付         |      2           |     25%      |  165        |    
            |     积分抵扣           |      1           |   12.5%      |  20         |    
            |     优惠券             |      1           |   12.5%      |  10         |    
            |     微众卡+积分        |      2           |     25%      |  185        |    
            |     微众卡+优惠券      |      2           |   12.5%      |  200        |    

        #优惠抵扣详情
            #微众卡支付 
                When jobs进入'微众卡支付 '详情
                Then jobs获得查询条件
                """
                [{
                    "begin_date":"2014-9-1",
                    "end_date":"2014-9-21",
                    "product_name":"",
                    "order_number":"",
                    "payment_method":"",
                    "order_status":["待发货","已发货","已完成"],
                    "re_purchase":"",
                    "preferential_deduction":"微众卡支付",
                    "only_weizoom_card":"是",
                    "buyers_source":""
                }]
                """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品2     | 对应订单编号 |    0            |   15    |   115       |  货到付款      |  未知    | 2014-9-10|  已完成      |
                    |    商品1     | 对应订单编号 |    0            |   10    |   110       |  货到付款      |  bill    | 2014-9-4 |  待发货      |

            #积分抵扣 
                When jobs进入'积分抵扣 '详情
                Then jobs获得查询条件
                """
                [{
                    "begin_date":"2014-9-1",
                    "end_date":"2014-9-21",
                    "product_name":"",
                    "order_number":"",
                    "payment_method":"",
                    "order_status":["待发货","已发货","已完成"],
                    "re_purchase":"",
                    "preferential_deduction":"积分抵扣",
                    "only_weizoom_card":"",
                    "buyers_source":""
                }]
                """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品1     | 对应订单编号 |    20           |   10    |    90       |  微信支付      |  marry   | 2014-9-4 |  已发货      |

            #优惠券 
                When jobs进入'优惠券 '详情
                Then jobs获得查询条件
                """
                [{
                    "begin_date":"2014-9-1",
                    "end_date":"2014-9-21",
                    "product_name":"",
                    "order_number":"",
                    "payment_method":"",
                    "order_status":["待发货","已发货","已完成"],
                    "re_purchase":"",
                    "preferential_deduction":"优惠券",
                    "only_weizoom_card":"",
                    "buyers_source":""
                }]
                """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品1     | 对应订单编号 |    10           |   10    |   200       |  微信支付      |  bill    | 2014-9-5 |  待发货      |

            #微众卡+积分 
                When jobs进入'微众卡+积分 '详情
                Then jobs获得查询条件
                """
                [{
                    "begin_date":"2014-9-1",
                    "end_date":"2014-9-21",
                    "product_name":"",
                    "order_number":"",
                    "payment_method":"",
                    "order_status":["待发货","已发货","已完成"],
                    "re_purchase":"",
                    "preferential_deduction":"微众卡+积分",
                    "only_weizoom_card":"",
                    "buyers_source":""
                }]
                """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品2     | 对应订单编号 |    20           |   15    |    95       |  微信支付      |  tom3    | 2014-9-9 |  已完成      |
                    |    商品2     | 对应订单编号 |    20           |   15    |    95       |  微信支付      |  tom1    | 2014-9-7 |  已完成      |

            #微众卡+优惠券 
                When jobs进入'微众卡+优惠券 '详情
                Then jobs获得查询条件
                """
                [{
                    "begin_date":"2014-9-1",
                    "end_date":"2014-9-21",
                    "product_name":"",
                    "order_number":"",
                    "payment_method":"",
                    "order_status":["待发货","已发货","已完成"],
                    "re_purchase":"",
                    "preferential_deduction":"微众卡+优惠券",
                    "only_weizoom_card":"",
                    "buyers_source":""
                }]
                """
                Then jobs获得订单列表
                    | product_name | order_number | discount_amount | freight | paid_amount | payment_method | consumer |   date   | order_status |
                    |    商品1     | 对应订单编号 |    10           |   10    |    100      |  支付宝        |  tom2    | 2014-9-8 |  已完成      |
                    |    商品1     | 对应订单编号 |    10           |   10    |    100      |  支付宝        |  tom     | 2014-9-6 |  已完成      |

@ignore
Scenario: 3 订单概况数据，筛选日期，默认筛选日期当天；快速查询；重置

    #筛选日期设置至少有一个为空
        When jobs设置筛选日期
        """
        [{
            "begin_date":"2014-9-1",
            "end_date":""
        }]
        """
        Then jobs系统给出提示“请添加结束日期”

        When jobs设置筛选日期
        """
        [{
            "begin_date":"",
            "end_date":"2014-9-1"
        }]
        """
        Then jobs系统给出提示“请添加开始日期”

    #备注：昨天，今天是2015-6-16，筛选日期：2015-6-15到2015-6-15
        When jobs昨天
        Then jobs筛选日期
            """
            [{
                "begin_date":"昨天",
                "end_date":"昨天"
            }]
            """

    #备注：最近7天，今天是2015-6-16，筛选日期：2015-6-10到2015-6-16
        When jobs最近7天
        Then jobs筛选日期
            """
            [{
                "begin_date":"7天前",
                "end_date":"今天"
            }]
            """

    #备注：最近30天，今天是2015-6-16，筛选日期：2015-5-19到2015-6-16
        When jobs最近30天
        Then jobs筛选日期
            """
            [{
                "begin_date":"30天前",
                "end_date":"今天"
            }]
            """

    #备注：最近90天，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
            When jobs最近90天
            Then jobs筛选日期
                """
                [{
                    "begin_date":"90天前",
                    "end_date":"今天"
                }]
                """

    #重置
        When jobs设置筛选日期
        """
        [{
            "begin_date":"2014-9-1",
            "end_date":"2014-9-10"
        }]
        """
        When jobs重置

        Then jobs获得查询条件
        """
        [{
            "begin_date":"",
            "end_date":""
        }]
        """

@stats @wip.order_survey @mall2
Scenario: 4 订单概况数据,补充复购率对买家为‘未知’的订单的统计错误

    Given jobs登录系统

    When 微信用户批量消费jobs的商品
            | date       | consumer | type      |businessman|   product | payment | payment_method | freight |   price  | integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action       |  order_status   |
            | 今天       |   -tom4  | 购买      |    job    | 商品1,1   | 支付    | 支付宝         | 10      | 100      |          |        | 110         |              | 110    | 0      | 0    |      jobs,支付    |  待发货         |

    When jobs设置筛选日期
    """
    {
        "start_date":"今天",
        "end_date":"今天"
    }
    """

    When jobs查询订单概况统计

    #复购率
    Then jobs获得复购率统计数据
    """
    {
        "初次购买":1,
        "重复购买":1
    }
    """