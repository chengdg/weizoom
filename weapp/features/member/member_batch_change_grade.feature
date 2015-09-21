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
		| member_name   | attention_time       | member_source |
		| bill3         | 2014-06-04 08:00:00  | 直接关注      |
		| bill2         | 2014-06-05 08:00:00  | 推广扫码      |
		| bill1         | 2014-06-06 08:00:00  | 直接关注      |
		| tom3          | 2014-06-07 08:00:00  | 会员分享      |
		| tom2 			| 2014-09-01 08:00:00  | 会员分享      |
		| tom1 			| 2014-09-02 08:00:00  | 会员分享      |
		| marry 	    | 2014-09-03 10:00:00  | 会员分享      |
		| tom 			| 2014-09-04 08:00:00  | 推广扫码      |
		| bill 			| 2014-09-05 08:00:00  | 直接关注      |

@mall2 @member @memberList
Scenario:1 选择当前页的部分会员，选择"给选中的人修改等级"
	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	#Then jobs获取会员列表显示共3页

	#选择第1页部分会员批量修改等级
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| member| member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |
			| tom          |   普通会员  |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给选中的人修改等级",
				"member_rank":"银牌会员"
			}]
			"""
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

	#选择第3页部分会员批量修改等级
		When jobs访问会员列表第3页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill1 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-06    | 直接关注 | 未分组      |
			| bill2 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-05    | 推广扫码 | 未分组      |
			| bill3 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-04    | 直接关注 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |
			| bill1        |   普通会员  |
			| bill3        |   普通会员  |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给选中的人修改等级",
				"member_rank":"铜牌会员"
			}]
			"""

		When jobs访问会员列表第3页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill1 |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-06    | 直接关注 | 未分组      |
			| bill2 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-05    | 推广扫码 | 未分组      |
			| bill3 |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-04    | 直接关注 | 未分组      |

@mall2 @member @memberList
Scenario:2 选择当前页的全部会员，选择"给选中的人修改等级"

	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

	#选择第1页全部会员批量修改等级
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |
			| bill         |   普通会员  |
			| tom          |   普通会员  |
			| marry        |   普通会员  |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给选中的人修改等级",
				"member_rank":"银牌会员"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

	#选择第2页全部会员批量修改等级
		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom1  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |
			| tom3  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |
			| tom1         |   普通会员  |
			| tom2         |   普通会员  |
			| tom3         |   普通会员  |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给选中的人修改等级",
				"member_rank":"金牌会员"
			}]
			"""

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom1  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |
			| tom3  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

@mall2 @member @memberList
Scenario:3 没有选中会员，选择"给选中的人修改等级"

	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

	#进入第1页，不选择任何会员
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给选中的人修改等级",
				"member_rank":"银牌会员"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

@mall2 @member @memberList
Scenario:4 选择当前页的部分会员，选择"给筛选出来的所有人修改等级"

	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	When jobs设置会员查询条件
		"""
		[{
			"source":"会员分享"
		}]
		"""
	#Then jobs获取会员列表显示共2页

	#选择第1页部分会员批量修改等级
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |
			| tom1         |   普通会员  |
			| tom2         |   普通会员  |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给筛选出来的所有人修改等级",
				"member_rank":"银牌会员"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom3  |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

	#选择第2页部分会员批量修改等级
		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom3  |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |
			| tom3         |   银牌会员  |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给筛选出来的所有人修改等级",
				"member_rank":"金牌会员"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom3  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

@mall2 @member @memberList
Scenario:5 选择当前页的全部会员，选择"给筛选出来的所有人修改等级"

	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	When jobs设置会员查询条件
		"""
		[{
			"source":"会员分享"
		}]
		"""
	#Then jobs获取会员列表显示共2页

	#选择第1页全部会员批量修改等级
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |
			| marry        |   普通会员  |
			| tom1         |   普通会员  |
			| tom2         |   普通会员  |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给筛选出来的所有人修改等级",
				"member_rank":"铜牌会员"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom3  |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

	#选择第2页全部会员批量修改等级

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom3  |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |
			| tom3         |   铜牌会员  |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给筛选出来的所有人修改等级",
				"member_rank":"金牌会员"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom3  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

@mall2 @member @memberList
Scenario:6 没有选中会员，选择"给筛选出来的所有人修改等级"

	Given jobs登录系统
	And jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	When jobs设置会员查询条件
		"""
		[{
			"source":"会员分享"
		}]
		"""
	#Then jobs获取会员列表显示共2页

	#没有选择任何会员批量修改等级
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |

		When jobs批量修改等级
			"""
			[{
				"modification_method":"给筛选出来的所有人修改等级",
				"member_rank":"银牌会员"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom3  |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

@mall2 @member @memberList
Scenario:7 批量修改会员等级后，在会员详情和会员的个人中心，会员等级都是修改后的等级，会员在购买有会员价商品时可以享受会员价

	Given jobs登录系统
	#设置分页
		Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

	#支付方式
		And jobs已添加支付方式
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
		}]
		"""

	#添加会员价商品
		And jobs已添加商品
		"""
		[{
			"name": "商品8",
			"is_member_product": "on",
			"price": 100.00
		}]
		"""

	#修改会员等级

		When jobs更新"bill"的会员等级
			"""
			{
				"name": "bill",
				"member_rank": "金牌会员"
			}
			"""

	#修改会员等级前购买会员价商品，按照现在的等级价购买

		#会员bill购买商品，金牌会员，按照70%价格购买
			When bill访问jobs的webapp
			And bill购买jobs的商品
				"""
				{
					"ship_name": "bill",
					"ship_tel": "12345678911",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦",
					"products": [{
						"name": "商品8",
						"count": 1
					}]
				}
				"""
			Then bill成功创建订单
				"""
				{
					"status": "待支付",
					"ship_name": "bill",
					"ship_tel": "12345678911",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦",
					"final_price": 70.00,
					"products": [{
						"name": "商品8",
						"price": 70.00,
						"count": 1
					}]
				}
				"""

		#会员bill3购买商品，普通会员，按照100%价格购买
			When bill3访问jobs的webapp
			And bill3购买jobs的商品
				"""
				{
					"ship_name": "bill3",
					"ship_tel": "12345678912",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦2",
					"products": [{
						"name": "商品8",
						"count": 1
					}]
				}
				"""
			Then bill3成功创建订单
				"""
				{
					"status": "待支付",
					"ship_name": "bill3",
					"ship_tel": "12345678912",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦2",
					"final_price": 100.00,
					"products": [{
						"name": "商品8",
						"price": 100.00,
						"count": 1
					}]
				}
				"""

	#批量修改会员等级，选择"给选中的人修改等级"

		#选择第3页部分会员批量修改等级
			Given jobs登录系统
			When jobs访问会员列表第3页
			Then jobs可以获得会员列表
				| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
				| bill1 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-06    | 直接关注 | 未分组      |
				| bill2 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-05    | 推广扫码 | 未分组      |
				| bill3 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-04    | 直接关注 | 未分组      |

			When jobs选择会员
				| member_name  | member_rank |
				| bill3        |   普通会员  |

			When jobs批量修改等级
				"""
				[{
					"modification_method":"给选中的人修改等级",
					"member_rank":"银牌会员"
				}]
				"""

			When jobs访问会员列表第3页
			Then jobs可以获得会员列表
				| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
				| bill1 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-06    | 直接关注 | 未分组      |
				| bill2 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-05    | 推广扫码 | 未分组      |
				| bill3 |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-04    | 直接关注 | 未分组      |

	#修改会员等级后购买会员价商品，按照修改后的等级价购买

		#会员bill3购买商品，银牌会员，按照80%价格购买
			When bill3访问jobs的webapp
			And bill3购买jobs的商品
				"""
				{
					"ship_name": "bill3",
					"ship_tel": "12345678913",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦3",
					"products": [{
						"name": "商品8",
						"count": 1
					}]
				}
				"""
			Then bill3成功创建订单
				"""
				{
					"status": "待支付",
					"ship_name": "bill3",
					"ship_tel": "12345678913",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦3",
					"final_price": 80.00,
					"products": [{
						"name": "商品8",
						"price": 80.00,
						"count": 1
					}]
				}
				"""

	#批量修改会员等级，选择"给筛选出来的所有人修改等级"
		Given jobs登录系统
		When jobs设置会员查询条件
			"""
			[{
				"source":"直接关注"
			}]
			"""
		#不选择任何会员，直接批量修改等级
			When jobs访问会员列表第1页
			Then jobs可以获得会员列表
				| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
				| bill  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
				| bill1 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-06    | 直接关注 | 未分组      |
				| bill3 |   银牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-04    | 直接关注 | 未分组      |

			When jobs选择会员
				| member_name  | member_rank |

			When jobs批量修改等级
				"""
				[{
					"modification_method":"给筛选出来的所有人修改等级",
					"member_rank":"铜牌会员"
				}]
				"""

			When jobs访问会员列表第1页
			Then jobs可以获得会员列表
				| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
				| bill  |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
				| bill1 |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-06    | 直接关注 | 未分组      |
				| bill3 |   铜牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-04    | 直接关注 | 未分组      |

	#修改会员等级后购买会员价商品，按照修改后的等级价购买

		#会员bill购买商品，铜牌会员，按照90%价格购买
			When bill访问jobs的webapp
			And bill购买jobs的商品
				"""
				{
					"ship_name": "bill",
					"ship_tel": "12345678911",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦",
					"products": [{
						"name": "商品8",
						"count": 1
					}]
				}
				"""
			Then bill成功创建订单
				"""
				{
					"status": "待支付",
					"ship_name": "bill",
					"ship_tel": "12345678911",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦",
					"final_price": 90.00,
					"products": [{
						"name": "商品8",
						"price": 90.00,
						"count": 1
					}]
				}
				"""

		#会员bill3购买商品，铜牌会员，按照90%价格购买
			When bill3访问jobs的webapp
			And bill3购买jobs的商品
				"""
				{
					"ship_name": "bill3",
					"ship_tel": "12345678913",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦3",
					"products": [{
						"name": "商品8",
						"count": 1
					}]
				}
				"""
			Then bill3成功创建订单
				"""
				{
					"status": "待支付",
					"ship_name": "bill3",
					"ship_tel": "12345678913",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦3",
					"final_price": 90.00,
					"products": [{
						"name": "商品8",
						"price": 90.00,
						"count": 1
					}]
				}
				"""
