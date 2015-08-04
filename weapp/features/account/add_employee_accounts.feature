# __author__ : "崔帅帅"
Feature:Add employee accounts
	Jobs能通过管理系统添加员工子账号

@account_subuser
Scenario: 添加员工账号
	Jobs添加"员工账号"
	Given jobs登录系统

	When jobs添加第一个员工账号
		"""
		[{
			"password" : "123456",
			"confirm_password" : "123456",
			"remark" :"第一个账号"
		}]	
		"""
	Then jobs能获取添加的员工账号
		"""
		[{
			"employees_account" : "001@jobs",
			"remark" :"第一个账号"
		}]
		"""

    When jobs添加第二个员工账号
		"""
		[{
			"password" : "12345",
			"confirm_password" : "12345",
			"remark" :""
		}]	
		"""
	Then jobs能获取添加的员工账号
		"""
		[{
			"employees_account" : "001@jobs",
			"remark" :"第一个账号"
		 },{
			"employees_account" : "002@jobs",
			"remark" :""  
		}]
		"""

	When jobs添加第三个员工账号
		"""
		[{ 
			"password" : "12345",
			"confirm_password" : "12345",
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
			"remark" :""  
		},{
			"employees_account" : "003@jobs",
			"remark" :"第三个账号"
		}]
		"""

