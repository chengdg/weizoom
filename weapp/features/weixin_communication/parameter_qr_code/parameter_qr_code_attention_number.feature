#watcher:wangli@weizoom.com,benchi@weizoom.com
#author: 王丽 2015-10-27

Feature:带参数二维码-列表-[关注数量]
"""
	带参数二维码-列表列表-[关注数量]
	1 【关注数量】：通过扫码关注会员的数量；
					(1)扫码新增会员数量（【已关注会员可参与】设置为"否"）
					(2)扫码新增会员数量+之前关注过的会员(包含当前为"关注"状态或者"取消关注"状态)
					扫码的会员数量（【已关注会员可参与】设置为"是"）
					(3)"已关注会员可参与"同一微信账号重复扫码[关注数量]累计一次
					(4)"已关注会员可参与"同一微信账号交替扫不同的码[关注数量]跳转
"""

Background:
	Given jobs登录系统
	#必须添加分组和等级数据库中才会有默认分组和等级
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}]
		"""
	And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1"
		}
		"""

@mall2 @senior @bandParameterCode
Scenario:1 带参数二维码[关注数量]-已关注会员不可参与
	#"已关注会员不可参与"的带参数二维码，已关注的会员扫码之后，关注数量不增加

	Given jobs登录系统

	#添加默认条件：无奖励、普通会员、未分组、否、无备注、否、扫码后回复文本
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "今天",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""
	#未关注微信账号扫码关注，关注数量增加
		When 清空浏览器
		When bill扫描带参数二维码"带参数二维码-默认设置"
		When bill访问jobs的webapp

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			}]
			"""
	#已关注会员扫码，关注数量不增加
		When 清空浏览器
		When tom关注jobs的公众号
		When tom访问jobs的webapp
		When tom扫描带参数二维码"带参数二维码-默认设置"

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			}]
			"""
	#取消关注的会员扫码，关注数量不增加
		When 清空浏览器
		When jack关注jobs的公众号
		When jack访问jobs的webapp
		When jack取消关注jobs的公众号

		When jack扫描带参数二维码"带参数二维码-默认设置"

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			}]
			"""

@mall2 @senior @bandParameterCode
Scenario:2 带参数二维码[关注数量]-已关注会员可参与
	#"已关注会员可参与"的带参数二维码，已关注的会员扫码之后，关注数量增加

	Given jobs登录系统

	#添加默认条件：无奖励、普通会员、未分组、是、无备注、否、扫码后回复文本
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "今天",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "true",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""
	#未关注微信账号扫码关注，关注数量增加
		When 清空浏览器
		When bill扫描带参数二维码"带参数二维码-默认设置"
		When bill访问jobs的webapp

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			}]
			"""
	#已关注会员扫码，关注数量不增加
		When 清空浏览器
		When tom关注jobs的公众号
		When tom访问jobs的webapp
		When tom扫描带参数二维码"带参数二维码-默认设置"

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 2
			}]
			"""
	#取消关注的会员扫码，关注数量不增加
		When 清空浏览器
		When jack关注jobs的公众号
		When jack访问jobs的webapp
		When jack取消关注jobs的公众号

		When jack扫描带参数二维码"带参数二维码-默认设置"

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 3
			}]
			"""

@mall2 @senior @bandParameterCode
Scenario:3 带参数二维码[关注数量]-"已关注会员可参与"同一微信账号重复扫码[关注数量]累计一次

	Given jobs登录系统

	#添加默认条件：无奖励、普通会员、未分组、是、无备注、否、扫码后回复文本
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "今天",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "true",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""
	#未关注微信账号扫码关注，关注数量增加
		When 清空浏览器
		When bill扫描带参数二维码"带参数二维码-默认设置"
		When bill访问jobs的webapp

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			}]
			"""
	#同一账号第二次扫描二维码，关注数量不累计
		#关注状态扫码
		When bill扫描带参数二维码"带参数二维码-默认设置"

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			}]
			"""
		#取消关注状态扫码
		When bill取消关注jobs的公众号
		When bill扫描带参数二维码"带参数二维码-默认设置"

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			}]
			"""

@mall2 @senior @bandParameterCode
Scenario:4 带参数二维码[关注数量]-"已关注会员可参与"同一微信账号交替扫不同的码[关注数量]跳转
	Given jobs登录系统

	#添加默认条件：无奖励、普通会员、未分组、是、无备注、否、扫码后回复文本
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "今天",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "true",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		},{
			"code_name": "带参数二维码-第二个二维码",
			"create_time": "今天",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "true",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""
	#未关注微信账号扫码关注，关注数量增加
		When 清空浏览器
		When bill扫描带参数二维码"带参数二维码-默认设置"
		When bill访问jobs的webapp

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			},{
				"code_name": "带参数二维码-第二个二维码",
				"attention_number": 0
			}]
			"""
	#已关注会员扫另一个二维码，关注数量跳转
		#关注状态扫码
		When bill扫描带参数二维码"带参数二维码-第二个二维码"

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 0
			},{
				"code_name": "带参数二维码-第二个二维码",
				"attention_number": 1
			}]
			"""
		#取消关注状态扫码
		When bill取消关注jobs的公众号
		When bill扫描带参数二维码"带参数二维码-默认设置"

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			},{
				"code_name": "带参数二维码-第二个二维码",
				"attention_number": 0
			}]
			"""

@mall2 @senior @bandParameterCode
Scenario:5 带参数二维码[关注数量]-扫码会员取消关注不影响[关注数量]
	#"已关注会员不可参与"的带参数二维码，会员扫码之后，关注数量增加，
	#扫码会员取消关注不影响[关注数量]，关注数量不减少

	Given jobs登录系统

	#添加默认条件：无奖励、普通会员、未分组、否、无备注、否、扫码后回复文本
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "今天",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "false",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""
	#未关注微信账号扫码关注，关注数量增加
		When 清空浏览器
		When bill扫描带参数二维码"带参数二维码-默认设置"
		When bill访问jobs的webapp

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			}]
			"""
	#扫码关注的会员取消关注，关注数量不减少
		When bill取消关注jobs的公众号

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 1
			}]
			"""

@mall2 @senior @bandParameterCode
Scenario:6 带参数二维码[关注数量]-代言人扫自己的二维码，此二维码的【关注数量】不增加
	Given jobs登录系统

	When bill关注jobs的公众号于'2015-10-12 08:00:00'

	Given jobs登录系统
	#添加默认条件：无奖励、普通会员、未分组、否、无备注、是、扫码后回复文本
	When jobs添加带参数二维码
		"""
		[{
			"code_name": "带参数二维码-默认设置",
			"create_time": "2015-10-12 08:00:00",
			"prize_type": "无奖励",
			"member_rank": "普通会员",
			"tags": "未分组",
			"is_attention_in": "false",
			"remarks": "",
			"is_relation_member": "true",
			"relation_time": "2015-10-13 08:00:00",
			"relation_member": "bill",
			"title": "星级代言人",
			"code_description": "星级代言人二维码描述",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本"
		}]
		"""
	#代言人（二维码关联会员）扫自己的二维码，关注数量不增加
		When 清空浏览器
		When bill扫描带参数二维码"带参数二维码-默认设置"

		Given jobs登录系统
		Then jobs获得带参数二维码列表
			"""
			[{
				"code_name": "带参数二维码-默认设置",
				"attention_number": 0
			}]
			"""
