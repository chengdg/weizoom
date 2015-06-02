Feature:盛景后台课程编辑增加非学员可见按钮开关
@ignore
@apps.shengjing.shengjing_course 
Scenario: jobs在后台添加课程编辑选择非学员可见
	Given jobs登录系统

	When jobs添加盛景课程
	"""
	[{
		"non_participants": "非学员可报名",
		"name":"1_盛景课程"
	}]
	"""

	Then jobs能获取盛景课程列表
	"""
	[{
		"name":"1_盛景课程"
	}]
	"""

	And jobs能获取课程1_盛景课程的详情
	"""
	[{
		"non_participants": "非学员可报名"
	}]
	"""

@ignore
Scenario:bill在webapp可以课程报名列表可以报名
	Give bill是非盛景学员
		bill登录webapp
	jobs在后台课程编辑选择'非学员可见'
	When bill点击课程报名
	Then 验证bill报名成功
	"""
			[{
				"status": "己报名"
			}]
	"""