#author：师帅
@func:termite2.views.custom_module
Feature: 微页面列表

Background:
	Given jobs登录系统
	#按添加的模块倒序排序(包括修改)
	And jobs已添加微页面
		"""
		[{
			"name": "微页面1",
			"create_time": "2015-09-28 17:00"
		},{
			"name": "微页面2",
			"create_time": "2015-09-28 08:00"
		},{
			"name": "微页面3",
			"create_time": "2015-09-27 08:00"
		},{
			"name": "微页面4",
			"create_time": "2015-09-27 15:00"
		}]
		"""
	Then jobs能获取微页面列表
		"""
		[{
			"name": "空白页面"
		},{
			"name": "微页面1",
			"create_time": "2015-09-28 17:00"
		},{
			"name": "微页面2",
			"create_time": "2015-09-28 08:00"
		},{
			"name": "微页面4",
			"create_time": "2015-09-27 15:00"
		},{
			"name": "微页面3",
			"create_time": "2015-09-27 08:00"
		}]
		"""

@mall2  @termite2
Scenario:1已有模块新建模块
	#已有模块,新建模块后,列表中显示(名称 最近应用在 操作列)
	Given jobs登录系统
	And jobs已添加微页面
		"""
		[{
			"name": "微页面标题1",
			"create_time": "2015-09-28 17:48"
		}]
		"""
	Then jobs能获取微页面列表
		"""
		[{
			"name": "空白页面"
		},{
			"name": "微页面标题1",
			"create_time": "2015-09-28 17:48"
		},{
			"name": "微页面1",
			"create_time": "2015-09-28 17:00"
		},{
			"name": "微页面2",
			"create_time": "2015-09-28 08:00"
		},{
			"name": "微页面4",
			"create_time": "2015-09-27 15:00"
		},{
			"name": "微页面3",
			"create_time": "2015-09-27 08:00"
		}]
		"""



@mall2  @termite2
Scenario:2删除
	#删除提示并且被删除的模块消息一列消失
	When jobs删除微页面'微页面2'
	Then jobs能获取微页面列表
		"""
		[{
			"name": "空白页面"
		},{
			"name": "微页面1",
			"create_time": "2015-09-28 17:00"
		},{
			"name": "微页面4",
			"create_time": "2015-09-27 15:00"
		},{
			"name": "微页面3",
			"create_time": "2015-09-27 08:00"
		}]
		"""

	
@mall2  @termite2
Scenario:3改名
	#改名后,成功显示修改后的名称
	When jobs修改微页面标题'微页面1'
		"""
		{
			"name": "微页面123"
		}
		"""
	Then jobs能获取微页面列表
		"""
		[{
			"name": "空白页面"
		},{
			"name": "微页面123",
			"create_time": "2015-09-28 17:00"
		},{
			"name": "微页面2",
			"create_time": "2015-09-28 08:00"
		},{
			"name": "微页面4",
			"create_time": "2015-09-27 15:00"
		},{
			"name": "微页面3",
			"create_time": "2015-09-27 08:00"
		}]
		"""
	#命名可以重复
	When jobs修改微页面标题'微页面2'
		"""
		{
			"name": "微页面3"
		}
		"""
	Then jobs能获取微页面列表
		"""
		[{
			"name": "空白页面"
		},{
			"name": "微页面123",
			"create_time": "2015-09-28 17:00"
		},{
			"name": "微页面3",
			"create_time": "2015-09-28 08:00"
		},{
			"name": "微页面4",
			"create_time": "2015-09-27 15:00"
		},{
			"name": "微页面3",
			"create_time": "2015-09-27 08:00"
		}]
		"""

@mall2  @termite2
Scenario: 4设置主页
	When jobs设置主页'微页面3'
	Then jobs能获取微页面列表
		"""
		[{
			"name": "微页面3",
			"create_time": "2015-09-27 08:00"
		},{
			"name": "空白页面"
		},{
			"name": "微页面1",
			"create_time": "2015-09-28 17:00"
		},{
			"name": "微页面2",
			"create_time": "2015-09-28 08:00"
		},{
			"name": "微页面4",
			"create_time": "2015-09-27 15:00"
		}]
		"""


