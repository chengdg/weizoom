#_author_:王丽

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
"""
Background:
	Given jobs登录系统

	And 已添加会员分组
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
Scenario:1 选择当前页的部分会员，选择"给选中的人添加分组";包含了给已经有分组的批量添加分组;批量调整分组的下来列表
	
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	Then jobs获取会员列表显示共3页

	#批量调整分组的下来列表
		When jobs添加分组"给选中的人添加分组"

		Then jobs获得分组列表
			"""
			[{
				"name": "会员分组1"
			},{
				"name": "会员分组2"
			},{
				"name": "会员分组3"
			},{
				"name": "会员分组4"
			},{
				"name": "会员分组5"
			}]	
			"""

		When jobs添加分组"给筛选出来的所有人添加分组"

		Then jobs获得分组列表
			"""
			[{
				"name": "会员分组1"
			},{
				"name": "会员分组2"
			},{
				"name": "会员分组3"
			},{
				"name": "会员分组4"
			},{
				"name": "会员分组5"
			}]	
			"""

	#选择当前页的部分会员，选择"给选中的人添加分组"
		#选择第1页部分会员批量添加分组
			When jobs选择第1页会员
				| member_name   | attention_time 	| member_source | grouping |
				| tom 			| 2014-9-4 8:00:00 	| 推广扫码      |          |

			When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"会员分组1"
				}]
				"""

			Then jobs获得批量添加分组会员
				| member_name   | attention_time 	| member_source | grouping  |
				| tom 			| 2014-9-4 8:00:00 	| 推广扫码      | 会员分组1 |

		#选择第3页部分会员批量添加分组
			When jobs选择第3页会员
				| member_name   | attention_time 	| member_source | grouping  |
				| bill1         | 2014-6-6 8:00:00  | 直接关注      |           |
				| bill3         | 2014-6-4 8:00:00  | 直接关注      |           |

			When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"会员分组2"
				}]
				"""

			Then jobs获得批量添加分组会员
				| member_name   | attention_time 	| member_source | grouping   |
				| bill1         | 2014-6-6 8:00:00  | 直接关注      | 会员分组2  |
				| bill3         | 2014-6-4 8:00:00  | 直接关注      | 会员分组2  |

	#包含了给已经有分组的批量添加分组
		#选择第1页部分已有分组会员批量添加分组
			When jobs选择第1页会员
				| member_name   | attention_time 	| member_source | grouping   |
				| bill1         | 2014-6-6 8:00:00  | 直接关注      | 会员分组2  |
				| bill3         | 2014-6-4 8:00:00  | 直接关注      | 会员分组2  |

			When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"会员分组3"
				}]
				"""

			Then jobs获得批量添加分组会员
				| member_name   | attention_time 	| member_source |       grouping       |
				| bill1         | 2014-6-6 8:00:00  | 直接关注      | 会员分组2;会员分组3  |
				| bill3         | 2014-6-4 8:00:00  | 直接关注      | 会员分组2;会员分组3  |

@member @memberList
Scenario:2 选择当前页的全部会员，选择"给选中的人添加分组"
	
	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	Then jobs获取会员列表显示共3页

	#选择第1页全部会员批量添加分组
		When jobs选择第1页会员
			| member_name   | attention_time 	| member_source | grouping  |
			| bill 			| 2014-9-5 8:00:00  | 直接关注      |           |
			| tom 			| 2014-9-4 8:00:00 	| 推广扫码      |           |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      |           |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给选中的人添加分组",
				"grouping":"会员分组3"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source | grouping  |
			| bill 			| 2014-9-5 8:00:00  | 直接关注      | 会员分组3 |
			| tom 			| 2014-9-4 8:00:00 	| 推广扫码      | 会员分组3 |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组3 |

	#选择第2页全部会员批量添加分组
		When jobs选择第2页会员
			| member_name   | attention_time 	| member_source | grouping  |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      |           |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      |           |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      |           |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给选中的人添加分组",
				"grouping":"会员分组4"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source |  grouping  |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      |  会员分组4 |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      |  会员分组4 |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      |  会员分组4 |

@member @memberList
Scenario:3 没有选中会员，选择"给选中的人添加分组"

	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	Then jobs获取会员列表显示共3页

	#进入第1页，不选择任何会员
		When jobs批量添加分组
			"""
			[{
				"modification_method":"给选中的人添加分组",
				"grouping":"会员分组5"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source |  grouping |

@member @memberList
Scenario:4 选择当前页的部分会员，选择"给筛选出来的所有人添加分组";包含了给已经有分组的批量添加分组

	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	When jobs设置查询条件
		"""
		[{
			"member_source":"会员分享"
		}]
		"""
	Then jobs获取会员列表显示共2页

	#选择第1页部分会员批量添加分组
		When jobs选择第1页会员
			| member_name   | attention_time 	| member_source | grouping  |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      |           |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      |           |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组1"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source | grouping  |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组1 |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      | 会员分组1 |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      | 会员分组1 |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组1 |

	#选择第2页部分会员批量添加分组
		When jobs选择第1页会员
			| member_name   | attention_time 	| member_source | grouping  |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组1 |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组2"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source |     grouping        |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组1;会员分组2 |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      | 会员分组1;会员分组2 |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      | 会员分组1;会员分组2 |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组1;会员分组2 |

@member @memberList
Scenario:5 选择当前页的全部会员，选择"给筛选出来的所有人添加分组"包含了给已经有分组的批量添加分组

	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	When jobs设置查询条件
		"""
		[{
			"member_source":"会员分享"
		}]
		"""
	Then jobs获取会员列表显示共2页

	#选择第1页全部会员批量添加分组
		When jobs选择第1页会员
			| member_name   | attention_time 	| member_source | grouping  |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      |           |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      |           |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      |           |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组2"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source | grouping  |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组2 |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      | 会员分组2 |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      | 会员分组2 |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组2 |

	#选择第2页全部会员批量添加分组
		When jobs选择第1页会员
			| member_name   | attention_time 	| member_source | grouping  |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组2 |

		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组3"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source |       grouping      |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组2;会员分组3 |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      | 会员分组2;会员分组3 |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      | 会员分组2;会员分组3 |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组2;会员分组3 |

@member @memberList
Scenario:6 没有选中会员，选择"给筛选出来的所有人添加分组"包含了给已经有分组的批量添加分组

	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	When jobs设置查询条件
		"""
		[{
			"member_source":"会员分享"
		}]
		"""
	Then jobs获取会员列表显示共2页

	#没有选择任何会员批量添加分组
		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组4"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source | grouping  |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组4 |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      | 会员分组4 |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      | 会员分组4 |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组4 |

	#没有选择任何会员批量添加分组
		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组5"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source |       grouping      |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组4;会员分组5 |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      | 会员分组4;会员分组5 |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      | 会员分组4;会员分组5 |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组4;会员分组5 |

@member @memberList
Scenario:7 筛选条件为“分组”的筛选结果时，批量调整分组

	Given jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""
	Then jobs获取会员列表显示共3页

	#没有选择任何会员批量添加分组
		When jobs批量添加分组
			"""
			[{
				"modification_method":"给筛选出来的所有人添加分组",
				"grouping":"会员分组4"
			}]
			"""

		Then jobs获得批量添加分组会员
			| member_name   | attention_time 	| member_source | grouping  |
			| bill 			| 2014-9-5 8:00:00  | 直接关注      | 会员分组4 |
			| tom 			| 2014-9-4 8:00:00 	| 推广扫码      | 会员分组4 |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组4 |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      | 会员分组4 |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      | 会员分组4 |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组4 |
			| bill1         | 2014-6-6 8:00:00  | 直接关注      | 会员分组4 |
			| bill2         | 2014-6-5 8:00:00  | 推广扫码      | 会员分组4 |
			| bill3         | 2014-6-4 8:00:00  | 直接关注      | 会员分组4 |

	#以分组为筛选条件，给筛选结果批量调整分组
		When jobs设置查询条件
			"""
			[{
				"member_grouping":"会员分组4"
			}]
			"""
		Then jobs获取会员列表显示共3页

		#选择第1页全部会员批量添加分组
			When jobs选择第1页会员
				| member_name   | attention_time 	| member_source | grouping  |
				| bill 			| 2014-9-5 8:00:00  | 直接关注      | 会员分组4 |
				| tom 			| 2014-9-4 8:00:00 	| 推广扫码      | 会员分组4 |
				| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组4 |

			When jobs批量添加分组
				"""
				[{
					"modification_method":"给选中的人添加分组",
					"grouping":"会员分组5"
				}]
				"""

			Then jobs获得批量添加分组会员
				| member_name   | attention_time 	| member_source |       grouping      |
				| bill 			| 2014-9-5 8:00:00  | 直接关注      | 会员分组4;会员分组5 |
				| tom 			| 2014-9-4 8:00:00 	| 推广扫码      | 会员分组4;会员分组5 |
				| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组4;会员分组5 |

	#校验批量调整分组后，查询结果

		Then jobs获取会员列表显示共3页

		Then jobs获得会员列表
			| member_name   | attention_time 	| member_source |       grouping      |
			| bill 			| 2014-9-5 8:00:00  | 直接关注      | 会员分组4;会员分组5 |
			| tom 			| 2014-9-4 8:00:00 	| 推广扫码      | 会员分组4;会员分组5 |
			| marry 	    | 2014-9-3 10:00:00 | 会员分享      | 会员分组4;会员分组5 |
			| tom1 			| 2014-9-2 8:00:00  | 会员分享      | 会员分组4           |
			| tom2 			| 2014-9-1 8:00:00  | 会员分享      | 会员分组4           |
			| tom3          | 2014-6-7 8:00:00  | 会员分享      | 会员分组4           |
			| bill1         | 2014-6-6 8:00:00  | 直接关注      | 会员分组4           |
			| bill2         | 2014-6-5 8:00:00  | 推广扫码      | 会员分组4           |
			| bill3         | 2014-6-4 8:00:00  | 直接关注      | 会员分组4           |





