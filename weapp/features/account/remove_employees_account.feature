# __author__ : "崔帅帅"
Feature:Remove employees account
	Jobs能通过管理系统删除员工子账号

Background:
	Given jobs已有的员工账号
		"""
		[{
			"employees_account" : "001@jobs",
			"remark":"第一个账号"
		},{
			"employees_account" : "002@jobs",
			"remark" :""
		},{
			"employees_account" : "003@jobs",
			"remark" :"第三个账号"
		}]
		"""
@account_subuser
Scenario: 删除员工账号
	Jobs删除"员工账号"
	When jobs删除员工账号003@jobs
		"""
		[{
			"employees_account" : "003@jobs",
			"remark" :"第三个账号"
		}]	
		"""
	Then jobs能获取添加的员工账号
		"""
		[{
			"employees_account" : "001@jobs",
			"remark" :"第一个账号"
		},{
			"employees_account" : "002@jobs",
			"remark" : ""
		}]
		"""