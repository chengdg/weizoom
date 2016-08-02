#author: 邓成龙 2016-08-01

Feature:渠道分销-列表查询
"""
	渠道分销二维码列表
	1 【二维码名称】：渠道分销二维码的名称
	2 【关联会员】：设置的"关联会员"的会员名称；
					(1)点击会员名称，跳转到此会员的会员详情页
					(2)鼠标移动到会员名称上显示："关联时间"和"取消关联时间",精确到秒（多次关联和取消关联的，显示最后一次的时间）；
	3 【关注数量】：通过扫码关注会员的数量；
					(1)扫码新增会员数量
				
	4 【总交易金额】:关注此二维码的会员的订单的"下单时间"在此会员的"扫码时间"之后的，
						所有有效订单（待发货、已发货、已完成）的实付金额之和

	5 【返现金额】:达到此金额额度则可以提现
	6 【关注奖励】：设置的扫此二位码获得的奖励
					(1)【扫码奖励】设置为"无奖励"：无奖励
					(2)【扫码奖励】设置为"积分"10：[积分]10
					(3)【扫码奖励】设置为"优惠券"优惠券名称：[优惠券]优惠券名称
	7 【分销奖励】：设置的扫此二位码代言人获得的奖励
					(1)【扫码奖励】设置为"无奖励"：无奖励
					(2)【扫码奖励】设置为"佣金",返现金额
				
	8 【创建时间】：此二维码规则的创建时间，精确到秒；默认按照创建时间倒叙排列
	
	9 【二维码操作】：显示"查看二维码"；点击新页面打开此二维码的二维码图片

	10 渠道分销二维码列表的"查询"，可以按照渠道分销二维码的名称进行模糊匹配查询，查询条件为空时，查询全部

	11 渠道分销二维码列表的"分页"，每20条记录一页

"""

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
			"distribution_prize_type": "无",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":500.00,
			"is_seven_day_settlement_standard":"false",
			"tags": "未分组",
			"prize_type": "无",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本",
			"create_time": "2015-10-10 10:20:30"
		},{
			"code_name": "渠道分销二维码-积分奖励",
			"relation_member": "bill",
			"distribution_prize_type": "佣金",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":500.00,
			"is_seven_day_settlement_standard":"false",
			"tags": "分组1",
			"prize_type": "积分",
			"integral": 10,
			"reply_type": "图文",
			"scan_code_reply": "图文1",
			"create_time": "2015-10-11 10:20:30"
		},{
			"code_name": "渠道分销二维码-优惠券奖励",
			"relation_member": "tom",
			"distribution_prize_type": "佣金",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":500.00,
			"is_seven_day_settlement_standard":"true",
			"tags": "分组2",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"reply_type": "图文",
			"scan_code_reply": "图文2",
			"create_time": "2015-10-12 10:20:30"
		}]
		"""
@mall2 @apps @senior @channel_distribution
Scenario:1 渠道分销二维码的查看
	Given jobs登录系统

		Then jobs获得渠道分销二维码列表
			"""
			[{
				"code_name": "渠道分销二维码-优惠券奖励",
				"relation_member": "tom",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "[优惠券]优惠券1",
				"distribution_prize":"无",
				"create_time": "2015-10-12 10:20:30"
			},{
				"code_name": "渠道分销二维码-积分奖励",
				"relation_member": "bill",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "[积分]10",
				"distribution_prize":"佣金",
				"create_time": "2015-10-11 10:20:30"
			},{
				"code_name": "渠道分销二维码-默认设置",
				"relation_member": "bigs",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "无",
				"distribution_prize":"佣金",
				"create_time": "2015-10-10 10:20:30"
			}]
			"""


@mall2 @apps @senior @channel_distribution
Scenario:2 渠道分销二维码的查询
	Given jobs登录系统

	#空查询
		When jobs设置渠道分销二维码查询条件
			"""
			{
				"code_name": ""
			}
			"""
		Then jobs获得渠道分销二维码列表
			"""
			[{
				"code_name": "渠道分销二维码-优惠券奖励",
				"relation_member": "tom",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "[优惠券]优惠券1",
				"distribution_prize":"无",
				"create_time": "2015-10-12 10:20:30"
			},{
				"code_name": "渠道分销二维码-积分奖励",
				"relation_member": "bill",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "[积分]10",
				"distribution_prize":"佣金",
				"create_time": "2015-10-11 10:20:30"
			},{
				"code_name": "渠道分销二维码-默认设置",
				"relation_member": "bigs",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "无",
				"distribution_prize":"佣金",
				"create_time": "2015-10-10 10:20:30"
			}]
			"""

	#模糊匹配查询
		When jobs设置渠道分销二维码查询条件
			"""
			{
				"code_name": "积分"
			}
			"""
		Then jobs获得渠道分销二维码列表
			"""
			[{
				"code_name": "渠道分销二维码-积分奖励",
				"relation_member": "bill",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "[积分]10",
				"distribution_prize":"佣金",
				"create_time": "2015-10-11 10:20:30"
			}]
			"""

	#精确匹配查询
		When jobs设置渠道分销二维码查询条件
			"""
			{
				"code_name": "渠道分销二维码-优惠券奖励"
			}
			"""
		Then jobs获得渠道分销二维码列表
			"""
			[{
				"code_name": "渠道分销二维码-优惠券奖励",
				"relation_member": "tom",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "[优惠券]优惠券1",
				"distribution_prize":"无",
				"create_time": "2015-10-12 10:20:30"
			}]
			"""

	#无查询结果查询
		When jobs设置渠道分销二维码查询条件
			"""
			{
				"code_name": "我们"
			}
			"""
		Then jobs获得渠道分销二维码列表
			"""
			[]
			"""

@mall2 @apps @senior @channel_distribution
Scenario:3 渠道分销二维码的分页
	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":1
		}
		"""
	#Then jobs获得渠道分销二维码列表共'3'页

	When jobs访问渠道分销二维码列表第'1'页
	Then jobs获得渠道分销二维码列表
		"""
		[{
				"code_name": "渠道分销二维码-优惠券奖励",
				"relation_member": "tom",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "[优惠券]优惠券1",
				"distribution_prize":"无",
				"create_time": "2015-10-12 10:20:30"
		}]
		"""
	When jobs访问渠道分销二维码列表下一页
	Then jobs获得渠道分销二维码列表
		"""
		[{
				"code_name": "渠道分销二维码-积分奖励",
				"relation_member": "bill",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "[积分]10",
				"distribution_prize":"佣金",
				"create_time": "2015-10-11 10:20:30"
		}]
		"""
	When jobs访问渠道分销二维码列表第'3'页
	Then jobs获得渠道分销二维码列表
		"""
		[{
				"code_name": "渠道分销二维码-默认设置",
				"relation_member": "bigs",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "无",
				"distribution_prize":"佣金",
				"create_time": "2015-10-10 10:20:30"
		}]
		"""
	When jobs访问渠道分销二维码列表上一页
	Then jobs获得渠道分销二维码列表
		"""
		[{
				"code_name": "渠道分销二维码-积分奖励",
				"relation_member": "bill",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "[积分]10",
				"distribution_prize":"佣金",
				"create_time": "2015-10-11 10:20:30"
		}]
		"""