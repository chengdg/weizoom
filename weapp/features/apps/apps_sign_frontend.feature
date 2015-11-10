#__author__ : "许韦"

Feature: Sign
    用户进行签到

Background:
    Given jobs登录系统
    When jobs添加优惠券规则
        """
        [{
            "name": "优惠券1",
            "money": 1.00,
            "limit_counts": "无限",
            "start_date": "2天前",
            "end_date": "今天",
            "coupon_id_prefix": "coupon1_id_"
        },{
            "name": "优惠券2",
            "money": 5.00,
            "limit_counts": "无限",
            "start_date": "今天",
            "end_date": "1天后",
            "coupon_id_prefix": "coupon2_id_"
        },{
            "name": "优惠券3",
            "money": 10.00,
            "limit_counts": "无限",
            "start_date": "2天前",
            "end_date": "2天后",
            "coupon_id_prefix": "coupon3_id_"
        }]
        """
@apps_sign @apps_sign_frontend @kuku
Scenario:1 用户浏览"签到活动1"
    Given jobs添加签到活动"签到活动1",并且保存
        """
        {
            "status":"off",
            "name": "签到活动1",
            "sign_describe":"签到赚积分！连续签到奖励更丰富哦！",
            "share_pic":"1.img",
            "share_describe": "签到送好礼！",
            "reply_content":"每日签到获得2积分和优惠券1一张,连续签到3天获得5积分和优惠券1一张,连续签到5天获得7积分和优惠券1一张",
            "reply_keyword":
                [{
                    "rule": "精确",
                    "key_word": "12"
                },{
                    "rule":"模糊",
                    "key_word": "123"
                }],

            "sign_settings":
                [{
                    "sign_in": "1",
                    "integral": "2",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                },{
                    "sign_in": "3",
                    "integral": "5",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                },{
                    "sign_in": "5",
                    "integral": "7",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                }]
        }
        """
    And jobs更新签到活动的状态
        """
        {
            "name":"签到活动1",
            "statis": "on"
        }
        """
    When bill关注jobs的公众号
    When bill访问jobs的webapp
    When bill的会员积分"0"
    When bill进入jobs的签到页面
    Then bill获取"签到活动1"内容
        """
        {
            "user_name":"bill",
            "integral_account":"0",
            "prize_item":
                {
                    "integral":"2",
                    "coupon_name":"优惠券1"
                },
            "sign_item":
            {
                "sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
                "sign_rule":"1.每日签到,获得2积分奖励优惠券1一张,2.连续签到至3天,获得5积分奖励优惠券1一张,3.连续签到至5天,获得7积分奖励优惠券1一张"
            }
        }
        """
@apps_sign @apps_sign_frontend @kuku @kuki
Scenario:1 用户回复精确关键字、完全匹配模糊关键字、不完全匹配模糊关键字签到
    Given jobs添加"签到活动1"
        """
        {
            "status":"off",
            "name": "签到活动1",
            "sign_describe":"签到赚积分！连续签到奖励更丰富哦！",
            "share_pic":"1.img",
            "share_describe": "签到送好礼！",
            "reply_content":"每日签到获得2积分,连续签到3天获得5积分,连续签到5天获得7积分",
            "reply_keyword":
                [{
                    "rule": "精确",
                    "key_word": "12"
                },{
                    "rule":"模糊",
                    "key_word": "123"
                }],

            "sign_settings":
                [{
                    "sign_in": "1",
                    "integral": "2"
                },{
                    "sign_in": "3",
                    "integral": "5"
                },{
                    "sign_in": "5",
                    "integral": "7"
                }]
        }
        """
    And jobs更新签到活动的状态
        """
        {
            "name":"签到活动1",
            "status": "on"
        }
        """
    When bill关注jobs的公众号
    When bill访问jobs的webapp
    Then bill在jobs的webapp中拥有'0'会员积分
#    When bill回复关键字
#        | key_word | rule |
#        | 12       | 精确 |
#        | 123      | 模糊 |
#        | 1234     | 模糊 |
#
#    Then bill获得系统回复的消息
#        """
#        {
#            "prize_item":
#                {
#                    "serial_count":"1",
#                    "integral":"2"
#                },
#            "reply":
#                {
#                    "content":"每日签到获得2积分,连续签到3天获得5积分,连续签到5天获得7积分"
#                }
#            "url_id_2":url2
#        }
#        """
#    When bill访问系统回复的"url2"
#    Then bill获取"签到活动1"内容
#        """
#        {
#            "user_name":"bill",
#            "integral_account":"2",
#            "serial_count":"1",
#            "prize_item":
#                {
#                    "serial_count_next":"3",
#                    "integral":"5"
#                }
#        }
#        """
@apps_sign @apps_sign_frontend
Scenario:3 用户回复完全不匹配关键字签到
    Given jobs添加"签到活动1"
        """
        {
            "status":"off",
            "name": "签到活动1",
            "sign_describe":"签到赚积分！连续签到奖励更丰富哦！",

            "share_pic":"1.img",
            "share_describe": "签到送好礼！",
            "reply_content":"每日签到获得优惠券1一张",
            "reply_keyword":
                [{
                    "rule": "精确",
                    "key_word": "12"
                },{
                    "rule":"模糊",
                    "key_word": "123"
                }],

            "sign_settings":
                [{
                    "sign_in": "1",
                    "send_coupon": "优惠券1",
                    "prize_counts":50
                }]
        }
        """
    And jobs开启签到活动"签到活动1"
        """
        {
            "name":"签到活动1",
            "enable": true
        }
        """
    When bill关注jobs的公众号
    When bill访问jobs的webapp
    When bill的会员积分"0"
    When bill回复关键字"1"
    Then bill没有获得系统回复的消息
    When jobs设置"签到活动1"状态
        """
        {
            "name":"签到活动1",
            "status":"关闭"
        }
        """
    And bill回复关键字"1"
    Then bill没有获得系统回复的消息

@apps_sign @apps_sign_frontend
Scenario Outline: 4 签到活动结束后用户回复精确关键字、完全匹配模糊关键字、不完全匹配模糊关键字签到
    Given jobs添加"签到活动1"
        """
        {
            "status":"off",
            "name": "签到活动1",
            "sign_describe":"签到赚积分！连续签到奖励更丰富哦！",

            "share_pic":"1.img",
            "share_describe": "签到送好礼！",
            "reply_content":"每日签到获得2积分和优惠券1一张
                    连续签到3天获得5积分",
            "reply_keyword":
                [{
                    "rule": "精确",
                    "key_word": "78"
                },{
                    "rule":"模糊",
                    "key_word": "abc"
                }],

            "sign_settings":
                [{
                    "sign_in": "1",
                    "integral": "2"
                    "send_coupon": "优惠券1"
                },{
                    "sign_in": "3",
                    "integral": "5"
                }]
        }
        """
    And jobs设置"签到活动1"状态
        """
        {
            "name":"签到活动1",
            "status":"关闭"
        }
        """
    When bill关注jobs的公众号
    When bill访问jobs的webapp
    When bill的会员积分"0"
    When bill回复关键字
        | key_word | rule |
        | 78       | 精确 |
        | abc      | 模糊 |
        | abcd     | 模糊 |

    Then bill获得系统自动回复的消息"签到活动还未开始。"

@apps_sign @apps_sign_frontend
Scenario:5 用户一天内连续两次签到
    Given jobs添加"签到活动1"
        """
        {
            "name":"签到活动1",
            "sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
            "share":
                {
                    "img": 1.img,
                    "desc":"签到送好礼！"
                },
            "key_word":
                [{
                    "keyword": "签到",
                    "type": "equal"
                },{
                    "keyword": "123",
                        "type": "like"
                }],
            "reply":
                {
                    "content":
                    "每日签到获得优惠券1一张
                    连续签到3天获得优惠券2一张
                    连续签到5天获得优惠券3一张",
                    "reply_type":"text"
                },
            "prize_settings":
                [{
                    "serial_count":"1",
                    "coupon_name":"优惠券1"
                },{

                    "serial_count":"3",
                    "coupon_name":"优惠券2"
                },{
                    "serial_count":5",
                    "coupon_name":"优惠券3"
                }]
        }
        """
    And jobs设置"签到活动1"状态
        """
        {
            "name":"签到活动1",
            "status":"开启"
        }
        """
    When bill关注jobs的公众号
    When bill访问jobs的weapp
    When bill的会员积分"0"
    When bill回复关键字
        | key_word | rule |
        | 签到     | 精确 |
        | 123      | 模糊 |
        | 1234     | 模糊 |

    Then bill获得系统回复的消息
        """
        {
            "prize_item":
                {
                    "serial_count":"1",
                    "coupon_name":[优惠券1]
                },
            "url_id_1":url1,
            "reply":
                {
                    "content":
                    "每日签到获得优惠券1一张
                    连续签到3天获得优惠券2一张
                    连续签到5天获得优惠券3一张",
                    "reply_type":"text"
                },
            "url_id_2":url2
        }
        """
    When bill访问系统回复的"url1"
    Then bill获得"优惠券1"
        """
        {
            "name": "优惠券1",
            "money": 1.00,
            "limit_counts": "无限",
            "start_date": "2天前",
            "end_date": "今天",
            "coupon_id_prefix": "coupon1_id_"
        }
        """
    When bill访问系统回复的"url2"
    Then bill获取"签到活动1"内容
        """
        {
            "user_name":"bill",
            "integral_account":"0",
            "serial_count":"1",
            "prize_item":
                {
                    "serial_count_next":"3",
                    "coupon_name":"优惠券2"
                }
        }
        """
    When bill退出jobs的weapp
    When bill再次访问jobs的weapp
    When bill回复关键字
    Then bill获得系统回复的消息
        """
        {
            "reply":"
            亲，今天您已经签到过了哦，
            明天再来吧！",
            "url_id_2":"url2"
        }
        """
    When bill访问系统回复的"url2"
    Then bill获取"签到活动1"内容
        """
        {
            "user_name":"bill",
            "integral_account":"0",
            "serial_count":"1",
            "prize_item":
                {
                    "serial_count_next":"3",
                    "coupon_name":"优惠券2"
                }
        }
        """
@apps_sign @apps_sign_frontend
Scenario:6 用户连续3天进行签到
    Given jobs添加"签到活动1"
        """
        {
            "name":"签到活动1",
            "sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
            "share":
                {
                    "img": 1.img,
                    "desc":"签到送好礼！"
                },
            "key_word":
                [{
                    "keyword": "a",
                    "type": "equal"
                },{
                    "keyword": "签到",
                        "type": "like"
                }],
            "reply":
                {
                    "content":
                    "每日签到获得2积分
                    连续签到3天获得优惠券1一张
                    连续签到5天获得10积分和优惠券2一张",
                    "reply_type":"text"
                },
            "prize_settings":
                [{
                    "serial_count":"1",
                    "integral":"2"
                },{
                    "serial_count":"3",
                    "coupon_name":"优惠券1"
                },{
                    "serial_count":5",
                    "integral":"10",
                    "coupon_name":"优惠券3"
                }]
        }
        """
    And jobs设置"签到活动1"状态
        """
        {
            "name":"签到活动1",
            "status":"开启"
        }
        """
    When bill关注jobs的公众号
    When bill访问jobs的weapp
    When bill的会员积分"0"
    When bill回复关键字
        | key_word | rule |
        | a        | 精确 |
        | 签到     | 模糊 |
        | 参加签到 | 模糊 |

    Then bill获得系统回复的消息
        """
        {
            "prize_item":
                {
                    "serial_count":"1",
                    "integral":"2"
                },
            "reply":
                {
                    "content":
                    "每日签到获得2积分
                    连续签到3天获得优惠券1一张
                    连续签到5天获得10积分和优惠券2一张",
                    "reply_type":"text"
                },
            "url_id_2":url2
        }
        """
    When bill访问系统回复的"url2"
    Then bill获取"签到活动1"内容
        """
        {
            "user_name":"bill",
            "integral_account":"2",
            "serial_count":"1",
            "prize_item":
                {
                    "serial_count_next":"3",
                    "coupon_name":"优惠券1"
                }
        }
        """
    When bill退出jobs的weapp
    When bill1天后访问jobs的weapp
    When bill进行签到
    Then bill获得系统回复的消息
        """
        {
            "prize_item":
                {
                    "serial_count":"2",
                    "integral":"2"
                },
            "reply":
                {
                    "content":
                    "每日签到获得2积分
                    连续签到3天获得优惠券1一张
                    连续签到5天获得10积分和优惠券2一张",
                    "reply_type":"text"
                },
            "url_id_2":url2
        }
        """
    When bill访问系统回复的"url2"
    Then bill获取"签到活动1"内容
        """
        {
            "user_name":"bill",
            "integral_account":"4",
            "serial_count":"2",
            "prize_item":
                {
                    "serial_count_next":"3",
                    "coupon_name":"优惠券1"
                }
        }
        """
    When bill2天后访问jobs的weapp
    When bill进行签到
    Then bill获得系统回复的消息
        """
        {
            "prize_item":
                {
                    "serial_count":"3",
                    "coupon_name":"优惠券1"
                },
            "url_id_1":url1,
            "reply":
                {
                    "content":
                    "每日签到获得2积分
                    连续签到3天获得优惠券1一张
                    连续签到5天获得10积分和优惠券2一张",
                    "reply_type":"text"
                },
            "url_id_2":url2
        }
        """
    When bill访问系统回复的"url2"
    Then bill获取"签到活动1"内容
        """
        {
            "user_name":"bill",
            "integral_account":"4",
            "serial_count":"3",
            "coupom_name":"优惠券1",
            "prize_item":
                {
                    "serial_count_next":"5",
                    "integral":"10",
                    "coupon_name":"优惠券2"
                }
        }
        """
@apps_sign @apps_sign_frontend
Scenario:7 用户分享"签到活动1"到朋友圈
    Given jobs添加"签到活动1"
        """
        {
            "name":"签到活动1",
            "sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
            "share":
                {
                    "img": 1.img,
                    "desc":"签到送好礼！"
                },
            "key_word":
                [{
                    "keyword": "签到",
                    "type": "equal"
                },{
                    "keyword": "123",
                        "type": "like"
                }],
            "reply":
                {
                    "content":
                    "每日签到获得5积分和优惠券1一张
                    连续签到3天获得10积分和优惠券2一张
                    连续签到5天获得20积分和优惠券3一张",
                    "reply_type":"text"
                },
            "prize_settings":
                [{
                    "serial_count":"1",
                    "integral":"5",
                    "coupon_name":"优惠券1"
                },{

                    "serial_count":"3",
                    "integral":"10",
                    "coupon_name":"优惠券2"
                },{
                    "serial_count":5",
                    "integral":"20",
                    "coupon_name":"优惠券3"
                }]
        }
        """
    And jobs设置"签到活动1"状态
        """
        {
            "name":"签到活动1",
            "status":"开启"
        }
        """
    When bill浏览"签到活动1"
    And bill分享"签到活动1"到朋友圈
    Then bill发表分享链接"share"
        """
        {
            "img": 1.img,
            "desc":"签到送好礼！"
        }
        """
@apps_sign @apps_sign_frontend
Scenario:8 会员用户访问签到分享进行签到
    Given jobs添加"签到活动1"
        """
        {
            "name":"签到活动1",
            "sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
            "share":
                {
                    "img": 1.img,
                    "desc":"签到送好礼！"
                },
            "key_word":
                [{
                    "keyword": "签到",
                    "type": "equal"
                },{
                    "keyword": "123",
                        "type": "like"
                }],
            "reply":
                {
                    "content":
                    "每日签到获得5积分和优惠券1一张
                    连续签到3天获得10积分和优惠券2一张
                    连续签到5天获得20积分和优惠券3一张",
                    "reply_type":"text"
                },
            "prize_settings":
                [{
                    "serial_count":"1",
                    "integral":"5",
                    "coupon_name":"优惠券1"
                },{

                    "serial_count":"3",
                    "integral":"10",
                    "coupon_name":"优惠券2"
                },{
                    "serial_count":5",
                    "integral":"20",
                    "coupon_name":"优惠券3"
                }]
        }
        """
    And jobs设置"签到活动1"状态
        """
        {
            "name":"签到活动1",
            "status":"开启"
        }
        """
    When bill分享"签到活动1"到朋友圈
    When jack关注公众号jobs
    When jack的会员积分0
    When jack访问分享链接"share"
    Then jack获取"签到活动1"内容
        """
        {
            "user_name":"jack",
            "integral_account":"0",
            "prize_item":
                {
                    "integral":"5",
                    "coupon_name":"优惠券1"
                }
        }
        """
    When jack进行签到
    Then jack获取"签到活动1"内容
        """
        {
            "user_name":"jack",
            "integral_account":"5",
            "serial_count":"1",
            "coupom_name":"优惠券1",
            "prize_item":
                {
                    "serial_count_next":"3",
                    "integral":"10",
                    "coupon_name":"优惠券2"
                }
        }
        """
@apps_sign @apps_sign_frontend
Scenario:9 非会员用户访问签到分享进行签到
    Given jobs添加"签到活动1"
        """
        {
            "name":"签到活动1",
            "sign_desc":"签到赚积分！连续签到奖励更丰富哦！",
            "share":
                {
                    "img": 1.img,
                    "desc":"签到送好礼！"
                },
            "key_word":
                [{
                    "keyword": "签到",
                    "type": "equal"
                },{
                    "keyword": "123",
                        "type": "like"
                }],
            "reply":
                {
                    "content":
                    "每日签到获得优惠券1
                    连续签到2天获得优惠券2
                    连续签到3天获得30积分",
                    "reply_type":"text"
                },
            "prize_settings":
                [{
                    "serial_count":"1",
                    "coupon_name":"优惠券1"
                },{

                    "serial_count":"2",
                    "coupon_name":"优惠券2"
                },{
                    "serial_count":3",
                    "integral":"30"
                }]
        }
        """
    And jobs设置"签到活动1"状态
        """
        {
            "name":"签到活动1",
            "status":"开启"
        }
        """
    When bill分享"签到活动1"到朋友圈
    When jack没有关注公众号jobs
    When jack访问分享链接"share"
    Then jack获取"签到活动1"内容
        """
        {
            "user_name":"jack",
            "integral_account":"0",
            "prize_item":
                {
                    "coupon_name":"优惠券1",
                }
        }
        """
    When jack进行签到
    Then jack获取"二维码1"
        """
        {
            "img":2.img,
            "url_name":"识别图中二维码",
            "url":url3
        }
        """
    When jack访问"url3"
    When jack关注jobs的公众号
    When jack访问jobs的webapp
    When jack的会员积分0
    When jack访问分享链接"share"
    Then jack获取"签到活动1"内容
        """
        {
            "user_name":"jack",
            "integral_account":"0",
            "prize_item":
                {
                    "coupon_name":"优惠券1"
                }
        }
        """
    When jack进行签到
    Then jack获取"签到活动1"内容
        """
        {
            "user_name":"jack",
            "integral_account":"0",
            "serial_count":"1",
            "coupom_name":"优惠券1",
            "prize_item":
                {
                    "serial_count_next":"2",
                    "coupon_name":"优惠券2"
                }
        }
        """