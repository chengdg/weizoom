#_author_:王丽
#editor:张三香 2015.10.15

Feature: 会员管理-批量添加到分组
"""
	会员管理的列表中对会员进行批量添加分组

	1、在会员列表的左下角添加"添加分组"，
	   点击"添加分组"下拉两个选项：（1）"给选中的人添加分组（2）"给筛选出来的所有人添加分组"
	2、选择"给选中的人添加分组"和"给筛选出来的所有人添加分组"弹出添加分组的窗体
		列表方式（按照创建分组的创建顺序）显示会员分组中的所有分组，单项选择
	3、添加分组，即将条件范围内的所有人添加到修改后的分组中，依然保有之前会员的分组
	4、只能选择当前页的会员，不能够选择多页会员，"给选中的人添加分组"，
	5、添加分组的各种情况的处理
		（1）操作：选择当前页的部分会员，选择"给选中的人添加分组"
			结果：给选中的人添加分组
		（2）操作：选择当前页的全部会员，选择"给选中的人添加分组"
			结果：给选中的人添加分组
		（3）操作：没有选中会员，选择"给选中的人添加分组"
			结果：不给任何人添加分组
		（4）操作：选择当前页的部分会员，选择"给筛选出来的所有人添加分组"
			结果：给筛选出来的所有人添加分组
		（5）操作：选择当前页的全部会员，选择"给筛选出来的所有人添加分组"
			结果：给筛选出来的所有人添加分组
		（6）操作：没有选中会员，选择"给筛选出来的所有人添加分组"
			结果：给筛选出来的所有人添加分组

	# __author__ : "王丽"
	2015-9新增需求
	1、会员分组默认有个分组："未分组"，不能修改（没有修改框）、不能删除（没有删除按钮）
	2、新增会员和调整没有分组的会员，默认进入"未分组"
"""
Background:
	Given jobs登录系统

	And jobs已添加会员分组
		"""
		{
			"tag_id_1": "会员分组1",
			"tag_id_2": "会员分组2",
			"tag_id_3": "会员分组3",
			"tag_id_4": "会员分组4",
			"tag_id_5": "会员分组5"
		}
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
Scenario:1 选择当前页的部分会员，选择"给选中的人添加分组";包含了给已经有分组的批量添加分组;批量调整分组的下拉列表
	Given jobs登录系统
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	#选择当前页的部分会员，选择"给选中的人添加分组"
		#选择第1页部分会员批量添加分组
			When jobs访问会员列表第1页
			Then jobs可以获得会员列表
				| member| member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
				| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
				| tom   |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
				| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

			When jobs选择会员
				| member_name | member_rank |    tags     |
				|     tom     |   普通会员  | 未分组      |

			When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"会员分组1"
				}]
				"""

			When jobs访问会员列表第1页
			Then jobs可以获得会员列表
				| member| member_rank |    tags     |
				| bill  |   普通会员  | 未分组      |
				| tom   |   普通会员  | 会员分组1   |
				| marry |   普通会员  | 未分组      |

		#选择第3页部分会员批量添加分组
			When jobs访问会员列表第3页
			Then jobs可以获得会员列表
				| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
				| bill1 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-06    | 直接关注 | 未分组      |
				| bill2 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-05    | 推广扫码 | 未分组      |
				| bill3 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-04    | 直接关注 | 未分组      |

			When jobs选择会员
				| member_name  | member_rank |    tags     |
				| bill1        |   普通会员  | 未分组      |
				| bill3        |   普通会员  | 未分组      |

			When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"会员分组2"
				}]
				"""

			When jobs访问会员列表第3页
			Then jobs可以获得会员列表
				| name  | member_rank |    tags     |
				| bill1 |   普通会员  | 会员分组2   |
				| bill2 |   普通会员  | 未分组      |
				| bill3 |   普通会员  | 会员分组2   |

	#包含了给已经有分组的批量添加分组
		#选择第3页部分已有分组会员批量添加分组
			When jobs访问会员列表第3页
			Then jobs可以获得会员列表
				| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
				| bill1 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-06    | 直接关注 | 会员分组2   |
				| bill2 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-05    | 推广扫码 | 未分组      |
				| bill3 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-04    | 直接关注 | 会员分组2   |

			When jobs选择会员
				| member_name  | member_rank |    tags     |
				| bill1        |   普通会员  | 会员分组2   |
				| bill3        |   普通会员  | 会员分组2   |

			When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"会员分组3"
				}]
				"""
			When jobs访问会员列表第3页
			Then jobs可以获得会员列表
				| name  | member_rank |        tags        |
				| bill1 |   普通会员  | 会员分组2,会员分组3|
				| bill2 |   普通会员  | 未分组             |
				| bill3 |   普通会员  | 会员分组2,会员分组3|

@mall2 @member @memberList
Scenario:2 选择当前页的全部会员，选择"给选中的人添加分组"
	Given jobs登录系统
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

	#选择第1页全部会员批量添加分组
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| member| member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name | member_rank |    tags     |
			| bill        |   普通会员  | 未分组      |
			| tom         |   普通会员  | 未分组      |
			| marry       |   普通会员  | 未分组      |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给选中的人添加分组",
				"grouping":"会员分组3"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| member| member_rank |    tags     |
			| bill  |   普通会员  | 会员分组3   |
			| tom   |   普通会员  | 会员分组3   |
			| marry |   普通会员  | 会员分组3   |

	#选择第2页全部会员批量添加分组
		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom1  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |
			| tom3  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |    tags     |
			| tom1         |   普通会员  | 未分组      |
			| tom2         |   普通会员  | 未分组      |
			| tom3         |   普通会员  | 未分组      |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给选中的人添加分组",
				"grouping":"会员分组4"
			}]
			"""

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |   tags     |
			| tom1  |   普通会员  | 会员分组4  |
			| tom2  |   普通会员  | 会员分组4  |
			| tom3  |   普通会员  | 会员分组4  |

@mall2 @member @memberList
Scenario:3 没有选中会员，选择"给选中的人添加分组"
	Given jobs登录系统
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

	#进入第1页，不选择任何会员
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| member| member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

		When jobs选择会员
			| member| member_rank |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给选中的人添加分组",
				"grouping":"会员分组5"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| member| member_rank |    tags     |
			| bill  |   普通会员  | 未分组      |
			| tom   |   普通会员  | 未分组      |
			| marry |   普通会员  | 未分组      |

@mall2 @member @memberList
Scenario:4 选择当前页的部分会员，选择"给筛选出来的所有人添加分组";包含了给已经有分组的批量添加分组
	Given jobs登录系统
	Given jobs设置分页查询参数
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

	#选择第1页部分会员批量添加分组
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |    tags     |
			| tom1         |   普通会员  | 未分组      |
			| tom2         |   普通会员  | 未分组      |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组1"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| marry |   普通会员  | 会员分组1   |
			| tom1  |   普通会员  | 会员分组1   |
			| tom2  |   普通会员  | 会员分组1   |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| tom3  |   普通会员  | 会员分组1   |

	#选择第2页部分会员批量添加分组
		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| tom3  |   普通会员  | 会员分组1   |

		When jobs选择会员
			| member_name  | member_rank |    tags     |
			| tom3         |   普通会员  |  会员分组1  |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组2"
			}]
			"""
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank |        tags         |
			| marry |   普通会员  | 会员分组1,会员分组2 |
			| tom1  |   普通会员  | 会员分组1,会员分组2 |
			| tom2  |   普通会员  | 会员分组1,会员分组2 |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |        tags         |
			| tom3  |   普通会员  | 会员分组1,会员分组2 |

@mall2 @member @memberList
Scenario:5 选择当前页的全部会员，选择"给筛选出来的所有人添加分组"包含了给已经有分组的批量添加分组
	Given jobs登录系统
	Given jobs设置分页查询参数
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

	#选择第1页全部会员批量添加分组
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |    tags     |
			| marry        |   普通会员  | 未分组      |
			| tom1         |   普通会员  | 未分组      |
			| tom2         |   普通会员  | 未分组      |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组2"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| marry |   普通会员  | 会员分组2   |
			| tom1  |   普通会员  | 会员分组2   |
			| tom2  |   普通会员  | 会员分组2   |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| tom3  |   普通会员  | 会员分组2   |

@mall2 @member @memberList
Scenario:6 没有选中会员，选择"给筛选出来的所有人添加分组"包含了给已经有分组的批量添加分组
	Given jobs登录系统
	Given jobs设置分页查询参数
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

	#没有选择任何会员批量添加分组
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |
			| tom1  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组4"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| marry |   普通会员  | 会员分组4   |
			| tom1  |   普通会员  | 会员分组4   |
			| tom2  |   普通会员  | 会员分组4   |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| tom3  |   普通会员  | 会员分组4   |

@mall2 @member @memberList
Scenario:7 筛选条件为“分组”的筛选结果时，批量调整分组
	Given jobs登录系统
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

	#选择第1页全部会员批量添加分组
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| member| member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name | member_rank |    tags     |
			| bill        |   普通会员  | 未分组      |
			| tom         |   普通会员  | 未分组      |
			| marry       |   普通会员  | 未分组      |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组4"
			}]
			"""

		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| member| member_rank |    tags     |
			| bill  |   普通会员  | 会员分组4   |
			| tom   |   普通会员  | 会员分组4   |
			| marry |   普通会员  | 会员分组4   |

	#以分组为筛选条件，给筛选结果批量调整分组
		When jobs设置查询条件
			"""
			[{
				"member_grouping":"会员分组4"
			}]
			"""

		#选择第1页全部会员批量添加分组
			When jobs访问会员列表第1页
			Then jobs可以获得会员列表
				| member| member_rank |    tags     |
				| bill  |   普通会员  | 会员分组4   |
				| tom   |   普通会员  | 会员分组4   |
				| marry |   普通会员  | 会员分组4   |

			When jobs选择会员
				| member_name | member_rank |   tags      |
				| bill        |   普通会员  | 会员分组4   |
				| tom         |   普通会员  | 会员分组4   |
				| marry       |   普通会员  | 会员分组4   |

			When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"会员分组5"
				}]
				"""
			When jobs访问会员列表第1页
			Then jobs可以获得会员列表
				| member| member_rank |        tags         |
				| bill  |   普通会员  | 会员分组4,会员分组5 |
				| tom   |   普通会员  | 会员分组4,会员分组5 |
				| marry |   普通会员  | 会员分组4,会员分组5 |

@mall2 @member @memberList @meberGroup
Scenario:8 会员分组人数验证
	Given jobs登录系统
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

	#选择第1页全部会员批量添加分组
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| member| member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-05    | 直接关注 | 未分组      |
			| tom   |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-04    | 推广扫码 | 未分组      |
			| marry |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-03    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name | member_rank |    tags     |
			| bill        |   普通会员  | 未分组      |
			| tom         |   普通会员  | 未分组      |
			| marry       |   普通会员  | 未分组      |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给选中的人添加分组",
				"grouping":"会员分组3"
			}]
			"""
	#选择第2页全部会员批量添加分组
		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank | friend_count | integral | pay_money | unit_price | pay_times | attention_time  |  source  |    tags     |
			| tom1  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-02    | 会员分享 | 未分组      |
			| tom2  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-09-01    | 会员分享 | 未分组      |
			| tom3  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |   2014-06-07    | 会员分享 | 未分组      |

		When jobs选择会员
			| member_name  | member_rank |    tags     |
			| tom1         |   普通会员  | 未分组      |
			| tom2         |   普通会员  | 未分组      |
			| tom3         |   普通会员  | 未分组      |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给选中的人添加分组",
				"grouping":"会员分组4"
			}]
			"""
	#给筛选出来的所有人调分组
		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| tom1  |   普通会员  | 会员分组4   |
			| tom2  |   普通会员  | 会员分组4   |
			| tom3  |   普通会员  | 会员分组4   |

		When jobs选择会员
			| member_name  | member_rank |    tags     |
			| tom1         |   普通会员  |  会员分组4  |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组2"
			}]
			"""
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| member| member_rank |        tags         |
			| bill  |   普通会员  | 会员分组3,会员分组2 |
			| tom   |   普通会员  | 会员分组3,会员分组2 |
			| marry |   普通会员  | 会员分组3,会员分组2 |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |        tags         |
			| tom1  |   普通会员  | 会员分组4,会员分组2 |
			| tom2  |   普通会员  | 会员分组4,会员分组2 |
			| tom3  |   普通会员  | 会员分组4,会员分组2 |

		When jobs访问会员列表第3页
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| bill1 |   普通会员  | 会员分组2   |
			| bill2 |   普通会员  | 会员分组2   |
			| bill3 |   普通会员  | 会员分组2   |

		Then jobs能获取会员分组列表
			"""
			[{
				"name": "未分组",
				"group_membership":0
			},{
				"name": "会员分组1",
				"group_membership":0
			},{
				"name": "会员分组2",
				"group_membership":9
			},{
				"name": "会员分组3",
				"group_membership":3
			},{
				"name": "会员分组4",
				"group_membership":3
			},{
				"name": "会员分组5",
				"group_membership":0
			}]
			"""


