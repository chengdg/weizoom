#author：新新
@func:termite2.views.custom_module
Feature: 自定义模块列表

Background:
	Given jobs登录系统
	#按添加的模块倒序排序(包括修改)

@termite2 @termite2.custom_module
Scenario:列表初始化
	#名称 最近应用在 操作列
	#列表为空
	Given jobs未添加模块
	Then jobs获取模块列表
	"""
		[]
	"""

	#已添加模块列表显示
	Given jobs已添加模块
	"""
		[{
			"name": "模块1"
		},{
			"name": "模块2"
		}]
	"""
	Then jobs获取模块列表	
	"""
		[{
			"name": "模块2"
		},{
			"name": "模块1"
		}]
	"""

@termite2 @termite2.custom_module
Scenario:已有模块新建模块
	#已有模块,新建模块后,列表中显示(名称 最近应用在 操作列)
	Given jobs已添加模块
		"""
		[{
			"name": "模块1"
		},{
			"name": "模块2"
		}]
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块2"
		},{
			"name": "模块1"
		}]
		"""
	
	When jobs添加模块
		"""
		{
			"name": "模块3"
		}
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块3"
		},{
			"name": "模块2"
		},{
			"name": "模块1"
		}]
		"""

@termite2 @termite2.custom_module
Scenario:未有模块新建模块
		#未添加任何模块,新建模块后列表显示
	Given jobs未添加模块
	Then jobs获取模块列表
	"""
		[]
	"""
	When jobs添加模块
		"""
		{
			"name": "模块2"
		}
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块2"
		}]
		"""

@termite2 @termite2.custom_module
Scenario:删除
	#删除提示并且被删除的模块消息一列消失
	Given jobs已添加模块
		"""
		[{
			"name": "模块1"
		},{
			"name": "模块2"
		}]
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块2"
		},{
			"name": "模块1"
		}]
		"""
	
	When jobs删除模块
		"""
		{
			"name": "模块1"
		}
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块2"
		}]
		"""
	
@termite2 @termite2.custom_module
Scenario:改名
	#改名后,成功显示修改后的名称
	Given jobs已添加模块
		"""
		[{
			"name": "模块1"
		},{
			"name": "模块2"
		}]
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块2"
		},{
			"name": "模块1"
		}]
		"""
	When jobs修改'模块1'的名称
		"""
		{
			"name": "模块3"
		}
		"""

	Then jobs获取模块列表
		"""
		[{
			"name": "模块3"
		},{
			"name": "模块2"
		}]
		"""

	###验证名称不可重复
	When jobs修改'模块3'的名称
		"""
		{
			"name": "模块2"
		}
		"""

	Then jobs获取模块列表
		"""
		[{
			"name": "模块3"
		},{
			"name": "模块2"
		}]
		"""

@termite2 @termite2.custom_module
Scenario:分页
	Given jobs已添加模块
		"""
		[{
			"name": "模块1"
		},{
			"name": "模块2"
		},{
			"name": "模块3"
		},{
			"name": "模块4"
		},{
			"name": "模块5"
		},{
			"name": "模块6"
		},{
			"name": "模块7"
		}]
		"""
	And jobs已设置分页条件
		"""
		{
			"page_count":3
		}
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块7"
		},{
			"name": "模块6"
		},{
			"name": "模块5"
		}]
		"""

	
	And jobs获取模块列表显示共'3'页
	When jobs浏览'第3页'
	Then jobs获取模块列表
		"""
		[{
			"name": "模块1"
		}]
		"""
	When jobs浏览'上一页'
	Then jobs获取模块列表
		"""
		[{
			"name": "模块4"
		},{
			"name": "模块3"
		},{
			"name": "模块2"
		}]
		"""
	When jobs浏览'下一页'
	Then jobs获取模块列表
		"""
		[{
			"name": "模块1"
		}]
		"""
	

@termite2 @termite2.custom_module
Scenario:搜索
	Given jobs已添加模块
		"""
		[{
			"name": "模块1"
		},{
			"name": "模块2"
		},{
			"name": "模块3"
		},{
			"name": "模块4"
		}]
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块4"
		},{
			"name": "模块3"
		},{
			"name": "模块2"
		},{
			"name": "模块1"
		}]
		"""
	
	When jobs按照模块名称搜索
		"""
		{
			"search": "1"
		}
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块1"
		}]
		"""
	When jobs按照模块名称搜索
		"""
		{
			"search": "模块"
		}
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块4"
		},{
			"name": "模块3"
		},{
			"name": "模块2"
		},{
			"name": "模块1"
		}]
		"""

	When jobs按照模块名称搜索
		"""
		{
			"search": "模块2"
		}
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块2"
		}]
		"""

	When jobs按照模块名称搜索
		"""
		{
			"search": "模2"
		}
		"""
	Then jobs获取模块列表
		"""
		[]
		"""
		
	When jobs按照模块名称搜索
		"""
		{
			"search": ""
		}
		"""
	Then jobs获取模块列表
		"""
		[{
			"name": "模块4"
		},{
			"name": "模块3"
		},{
			"name": "模块2"
		},{
			"name": "模块1"
		}]
		"""



