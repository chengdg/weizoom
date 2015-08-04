@func:apps.shengjing.order
Feature:盛景定制化需求订单查询

Background:
	Given bill是企业决策人绑定盛景CRM
	AND bill是非企业决策人绑定盛景CRM
	
@apps @apps.shengjing @apps.shengjing.order  @ignore
Scenario: 账单查询
	1、bill(企业决策人)绑定CRM后能够查看账单信息
	2、tom(非企业决策人)绑定CRM后不能查看账单信息

	Given bill所属公司
		"""
			["A公司", "B公司", "C公司"]
		"""
	And bill拥有人次卡
		"""
			[{
				"company": "A公司",
				"order_time": "2014年06月01日",
				"person_times": 10,
				"study_times": 3,
				"surplus_times": 7,
				"bill_status": "已开",
				"status": "正在使用",
				"course_info": {
					"name": "经营哲学与智慧(第2期)",
					"study_time": "2014年06月01日",
					"students": ["李佳", "王华", "李聂安"]
				}
			},{
				"company": "A公司",
				"order_time": "2014年06月01日",
				"person_times": 10,
				"study_times": 3,
				"surplus_times": 7,
				"bill_status": "未开",
				"status": "已使用",
				"course_info": {
					"name": "经营哲学与智慧(第2期)",
					"study_time": "2014年06月01日",
					"students": ["李佳", "王华", "李聂安"]
				}
			}]
		"""
	And bill拥有时间卡
		"""
			[{
				"company": "A公司",
				"order_time": "2014年06月01日",
				"valid_time": "2014年09月01日",
				"study_times": 3,
				"surplus_times": 7,
				"bill_status": "已开",
				"status": "正在使用",
				"course_info": {
					"name": "经营哲学与智慧(第2期)",
					"study_time": "2014年06月01日",
					"students": ["李佳", "王华", "李聂安"]
				}
			},{
				"company": "A公司",
				"valid_time": "2014年09月01日",
				"person_times": 10,
				"study_times": 3,
				"surplus_times": 7,
				"bill_status": "未开",
				"status": "已使用",
				"course_info": {
					"name": "经营哲学与智慧(第2期)",
					"study_time": "2014年06月01日",
					"students": ["李佳", "王华", "李聂安"]
				}
			}]
		"""
	When bill访问正在使用的账单明细
	Then bill可以看到账单明细
	"""
		{
			"person_card": [{
				"company": "A公司",
				"order_time": "2014年06月01日",
				"person_times": 10,
				"study_times": 3,
				"surplus_times": 7,
				"bill_status": "已开",
				"status": "正在使用",
				"course_info": {
					"name": "经营哲学与智慧(第2期)",
					"study_time": "2014年06月01日",
					"students": ["李佳", "王华", "李聂安"]
				}
			}],
			"time_card": [{
				"company": "A公司",
				"order_time": "2014年06月01日",
				"valid_time": "2014年09月01日",
				"study_times": 3,
				"surplus_times": 7,
				"bill_status": "已开",
				"status": "正在使用",
				"course_info": {
					"name": "经营哲学与智慧(第2期)",
					"study_time": "2014年06月01日",
					"students": ["李佳", "王华", "李聂安"]
				}
			}],
			"companys": ["A公司", "B公司", "C公司"]
		}
	"""
	When bill访问已使用的账单明细
	Then bill可以看到账单明细
	"""
		{
			"person_card": [{
				"company": "A公司",
				"order_time": "2014年06月01日",
				"person_times": 10,
				"study_times": 3,
				"surplus_times": 7,
				"bill_status": "未开",
				"status": "已使用",
				"course_info": {
					"name": "经营哲学与智慧(第2期)",
					"study_time": "2014年06月01日",
					"students": ["李佳", "王华", "李聂安"]
				}
			}],
			"time_card": [{
				"company": "A公司",
				"valid_time": "2014年09月01日",
				"person_times": 10,
				"study_times": 3,
				"surplus_times": 7,
				"bill_status": "未开",
				"status": "已使用",
				"course_info": {
					"name": "经营哲学与智慧(第2期)",
					"study_time": "2014年06月01日",
					"students": ["李佳", "王华", "李聂安"]
				}
			}],
			"companys": ["A公司", "B公司", "C公司"]
		}
	"""