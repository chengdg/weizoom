#_author_:王丽

Feature: 会员管理-批量修改等级
"""
	会员管理的列表中对会员的等级进行批量修改

	1、在会员列表的左下角添加"修改等级"，
	   点击"修改等级"下拉两个选项：（1）"给选中的人修改等级"（2）"给筛选出来的所有人修改等级"
	2、选择"给选中的人修改等级"和"给筛选出来的所有人修改等级"弹出修改等级的窗体
		列表方式显示会员等级中的所有等级，单项选择
	3、只能选择当前页的会员，不能够选择多页会员，"给选中的人修改等级"
	4、修改等级的各种情况的处理
		（1）操作：选择当前页的部分会员，选择"给选中的人修改等级"
			结果：给选中的人修改等级
		（2）操作：选择当前页的全部会员，选择"给选中的人修改等级"
			结果：给选中的人修改等级
		（3）操作：没有选中会员，选择"给选中的人修改等级"
			结果：不给任何人修改等级
		（4）操作：选择当前页的部分会员，选择"给筛选出来的所有人修改等级"
			结果：给筛选出来的所有人修改等级
		（5）操作：选择当前页的全部会员，选择"给筛选出来的所有人修改等级"
			结果：给筛选出来的所有人修改等级
		（6）操作：没有选中会员，选择"给筛选出来的所有人修改等级"
			结果：给筛选出来的所有人修改等级
"""

Background:
	Given jobs登录系统

	And jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		},{
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""

	When jobs批量获取微信用户关注
		| member_name   | attention_time 	| member_source |
		| bill 			| 2014-9-5 8:00:00  | 直接关注      |
		| tom 			| 2014-9-4 8:00:00 	| 推广扫码      |
		| marry 	    | 2014-9-3 10:00:00 | 会员分享      |
		| tom1 			| 2014-9-2 8:00:00  | 会员分享      |
		| tom2 			| 2014-9-1 8:00:00  | 会员分享      |
		| tom3          | 2014-6-7 8:00:00  | 会员分享      |
		| bill1         | 2014-6-6 8:00:00  | 直接关注      |
		| bill2         | 2014-6-5 8:00:00  | 推广扫码      |
		| bill3         | 2014-6-4 8:00:00  | 直接关注      |

@member @memberList
Scenario:1 选择当前页的部分会员，选择"给选中的人修改等级"
	
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

	#选择第1页部分会员批量修改等级
		When jobs访问会员列表第1页
		Then jobs获得第1页会员列表
			| member_name   | attention_time 	| member_source |     member_rank   |
			| bill 			| 2014-9-5 8:00:00 	| 直接关注      |      普通会员     |
			| tom 			| 2014-9-4 8:00:00 	| 推广扫码      |      普通会员     |
			| marry 		| 2014-9-3 10:00:00 | 会员分享      |      普通会员     |

		When jobs选择会员
			| member_name   | attention_time 	| member_source |     member_rank   |
			| tom 			| 2014-9-4 8:00:00 	| 推广扫码      |      普通会员     |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给选中的人修改等级",
				"member_rank":"银牌会员"
			}]
			"""
		When jobs访问会员列表第1页
		Then jobs获得第1页会员列表
			| member_name   | attention_time 	| member_source |     member_rank   |
			| bill 			| 2014-9-5 8:00:00 	| 直接关注      |      普通会员     |
			| tom 			| 2014-9-4 8:00:00 	| 推广扫码      |      银牌会员     |
			| marry 		| 2014-9-3 10:00:00 | 会员分享      |      普通会员     |
		When jobs访问会员列表第2页
		Then jobs获得第2页会员列表
			| member_name   | attention_time 	| member_source |     member_rank   |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      |      普通会员     |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      |      普通会员     |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      |      普通会员     |
		When jobs访问会员列表第3页
		Then jobs获得第3页会员列表
			| member_name   | attention_time 	| member_source |     member_rank   |
			| bill1         | 2014-6-6 8:00:00  | 直接关注      |      普通会员     |
			| bill2         | 2014-6-5 8:00:00  | 推广扫码      |      普通会员     |
			| bill3         | 2014-6-4 8:00:00  | 直接关注      |      普通会员     |

	#选择第3页部分会员批量修改等级
		When jobs访问会员列表第3页
		Then jobs获得第3页会员列表
			| member_name   | attention_time 	| member_source |     member_rank   |
			| bill1         | 2014-6-6 8:00:00  | 直接关注      |      普通会员     |
			| bill2         | 2014-6-5 8:00:00  | 推广扫码      |      普通会员     |
			| bill3         | 2014-6-4 8:00:00  | 直接关注      |      普通会员     |
		When jobs选择会员
			| member_name   | attention_time 	| member_source |     member_rank   |
			| bill1         | 2014-6-6 8:00:00  | 直接关注      |      普通会员     |
			| bill3         | 2014-6-4 8:00:00  | 直接关注      |      普通会员     |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给选中的人修改等级",
				"member_rank":"铜牌会员"
			}]
			"""
		When jobs访问会员列表第1页
		Then jobs获得第1页会员列表
			| member_name   | attention_time 	| member_source |     member_rank   |
			| bill 			| 2014-9-5 8:00:00 	| 直接关注      |      普通会员     |
			| tom 			| 2014-9-4 8:00:00 	| 推广扫码      |      银牌会员     |
			| marry 		| 2014-9-3 10:00:00 | 会员分享      |      普通会员     |
		When jobs访问会员列表第2页
		Then jobs获得第2页会员列表
			| member_name   | attention_time 	| member_source |     member_rank   |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      |      普通会员     |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      |      普通会员     |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      |      普通会员     |
		Then jobs获得第3页会员列表
			| member_name   | attention_time 	| member_source |     member_rank   |
			| bill1         | 2014-6-6 8:00:00  | 直接关注      |      铜牌会员     |
			| bill2         | 2014-6-5 8:00:00  | 推广扫码      |      普通会员     |
			| bill3         | 2014-6-4 8:00:00  | 直接关注      |      铜牌会员     |
			