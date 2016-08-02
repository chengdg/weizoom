#author: 邓成龙 2016-08-02

Feature:分销会员结算页返现状态转换
		1.无状态,默认状态,没有申请的时候
		2.正在返现中,当前台用户申请返现时
		3.已完成/切换为无状态,管理返现完成时切换到当前状态,系统自动转为无状态

Background:
	Given jobs登录系统

	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2"
		}
		"""
	And jobs已添加多图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"单条图文1文本内容"
		},{
			"title":"图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou2.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"单条图文2文本内容"
		}]
		"""
	And bigs关注jobs的公众号于'2015-10-01'
	And bill关注jobs的公众号于'2015-10-01 10:00:00'
	And tom关注jobs的公众号于'2015-10-02'
	Given jobs登录系统
	When jobs新建渠道分销二维码
		"""
		[{
			"code_name": "渠道分销二维码-默认设置",
			"relation_member": "bigs",
			"distribution_prize_type": "佣金",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":50.00,
			"is_seven_day_settlement_standard":"false",
			"tags": "未分组",
			"prize_type": "无",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本",
			"create_time": "2015-10-10 10:20:30"
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type":"货到付款"
		},{
			"type":"微信支付"
		},{
			"type":"支付宝"
		}]
		"""

	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 50.00
		},{
			"name": "商品2",
			"price": 100.00
		}]
		"""

	#扫码关注成为会员
		When 清空浏览器
		And jack扫描带参数二维码"带参数二维码-默认设置"于2015-08-10 10:00:00
		And jack访问jobs的webapp

		When 清空浏览器
		And nokia扫描带参数二维码"带参数二维码-默认设置"于2015-08-11 10:00:00
		And nokia访问jobs的webapp

		When 清空浏览器
		And marry扫描带参数二维码"带参数二维码-默认设置"于2015-08-12 10:00:00
		And marry访问jobs的webapp

	#已关注或者取消关注的会员，扫码
		When bill扫描带参数二维码"带参数二维码-默认设置"于2015-08-10 10:00:00

		And tom扫描带参数二维码"带参数二维码-默认设置"于2015-08-10 11:00:00
		And tom关注jobs的公众号

	#会员购买
		When 微信用户批量消费jobs的商品
			"""
			{
				"wx_name":"jack",
				"order_id": "002",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1
				}]
			}
			"""
		When jack完成订单"002"
@mall2 @apps @senior @processing_applications
Scenario:1 分销会员结算页等待审核状态
	
		When jack访问jobs的webapp
		When bigs申请返现于2015-08-12 10:00:00
		Given jobs登录系统
		
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":10.00,
				"cash_back_state":"等待审核"
			}]
			"""

@mall2 @apps @senior @processing_applications
Scenario:2 分销会员结算页正在返现状态
	
		When jack访问jobs的webapp
		When bigs申请返现
		Given jobs登录系统
		When jobs更改返现状态为"正在返现"
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":10.00,
				"cash_back_state":"正在返现"
			}]
			"""
@mall2 @apps @senior @processing_applications
Scenario:3 分销会员结算页已完成/切换为无状态
	
		When jack访问jobs的webapp
		When bigs申请返现
		Given jobs登录系统
		When jobs更改返现状态为"已完成/切换为无状态"
		Then jobs获得分销会员结算列表
			"""
			[{
				"relation_member": "bigs",
				"submit_time":"2015-08-12 10:00:00",
				"current_transaction_amount":100.00,
				"commission_return_standard":50.00,
				"commission_return_rate":"10",
				"already_reward":10.00,
				"cash_back_amount":10.00,
				"cash_back_state":"无状态"
			}]
			"""
