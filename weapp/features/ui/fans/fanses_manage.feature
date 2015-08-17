Feature: 粉丝管理的列表

Background:
	Given jobs登录系统
	#And jobs添加粉丝

Scenario: 浏览粉丝列表
	jobs登录之后访问"高级管理"->"粉丝管理"，浏览粉丝列表

	Given jobs登录系统
	When 粉丝diana关注了jobs的公众号
	And jobs访问粉丝管理页面
	Then 粉丝页面上有diana的信息

Scenario: 编辑粉丝备注名
	在粉丝管理页面编辑粉丝的备注名称

	Given 粉丝diana关注了jobs公众号
	And jobs登录了系统
	When jobs访问粉丝管理页面
	Then 在粉丝页面上diana的备注名为''
	When jobs编辑了diana的备注名为'戴安娜'
	Then 在粉丝页面上diana的备注名为'戴安娜'

Scenario: 取消关注的粉丝显示为'已跑路'
	
	Given 粉丝frank关注了jobs公众号
	And jobs登录了系统
	When 粉丝frank取消关注jobs公众号
	Then 在粉丝页面上frank头像上显示'已跑路'


Scenario: 修改分组
	Given 粉丝diana关注了jobs公众号
	And jobs登录系统
	Given 粉丝分组有
		"""
		[{
			"name": "未分组"
		}, {
			"name": "铁杆粉丝"
		}, {
			"name": "木杆粉丝"
		}]
		"""
	When jobs访问粉丝管理页面
	Then '未分组'粉丝组中有diana
	Then '铁杆粉丝'粉丝组中没有diana
	Then '木杆粉丝'粉丝组中没有diana
	When jobs修改diana的分组为'铁杆粉丝'
	Then '未分组'粉丝组中没有diana
	Then '铁杆粉丝'粉丝组中有diana
	Then '木杆粉丝'粉丝组中没有diana


@mall2 @weixin2 @weixin2.fans
Scenario: 粉丝列表中添加分组
	在【粉丝管理】粉丝列表中添加分组

	Given jobs登录系统
	When jobs创建分组
	"""
	[{
		"category_name": "新分组1"
	}]
	"""
	Then jobs看到分组列表中有'新分组1'
	Then jobs能看到的分组名列表
	"""
	[{
		"category_name": "全部分组"
	}, {
		"category_name": "未分组"
	}, {
		"category_name": "新分组1"
	}]
	"""


@mall2 @weixin2 @weixin2.fans
Scenario: 粉丝列表中添加分组，添加重名的分组
	在【粉丝管理】粉丝列表中添加分组

	Given jobs登录系统
	When jobs创建分组
		"""
		[{
			"category_name": "重复分组名"
		}, {
			"category_name": "重复分组名"
		}]
		"""
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "重复分组名"
		}]
		"""

Scenario: 分组显示顺序
	一个一个添加分组，看显示列表的顺序

Scenario: 删除一个粉丝分组


@weixin2 @weixin2.fans @wip.fan_category
Scenario: 修改粉丝分类的名称

	Given jobs登录系统
	When jobs创建分组
		"""
		[{
			"category_name": "已有分组"
		}]
		"""
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}]
		"""
	When jobs添加一个分组
		"""
		{
			"category_name": "修改前分组名"
		}
		"""
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}, {
			"category_name": "修改前分组名"
		}]
		"""
	When jobs修改刚添加的分组名为'修改后分组名'
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}, {
			"category_name": "修改后分组名"
		}]
		"""

Scenario:  正常修改分组

Scenario: 修改成不存在的分组

Scenario: 修改成"未分组"

Scenario: 获取分组列表

Scenario: 改分组名称，与已有的重名

@weixin2.fans @wip.fan_category
Scenario: 创建名为"未分组"的分组
	不允许创建"未分组"的分组

	Given jobs登录系统
	When jobs创建分组
	#清除现有分组数据
		"""
		[{
			"category_name": "已有分组"
		}]
		"""	
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}]
		"""
	When jobs添加一个分组
		"""
		{
			"category_name": "未分组"
		}
		"""
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}]
		"""


@weixin2.fans @wip.fan_category
Scenario: 将分组名更名为"未分组"
	不允许更名为"未分组"

	Given jobs登录系统
	When jobs创建分组
	#清除现有分组数据
		"""
		[{
			"category_name": "已有分组"
		}]
		"""	
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}]
		"""
	When jobs添加一个分组
		"""
		{
			"category_name": "未分类"
		}
		"""
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}, {
			"category_name": "未分类"
		}]
		"""
	When jobs修改刚添加的分组名为'未分组'
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}, {
			"category_name": "未分类"
		}]
		"""

@weixin2.fans @wip.fan_category
Scenario: 分组名长度超过6

	Given jobs登录系统
	When jobs创建分组
	#清除现有分组数据
		"""
		[{
			"category_name": "已有分组"
		}]
		"""	
	Then jobs能看到的分组名列表
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}]
		"""
	When jobs添加一个分组
		# 添加长度为7的
		"""
		{
			"category_name": "一二三四五六七"
		}
		"""
	Then jobs能看到的分组名列表
		# 看不到此分组
		"""
		[{
			"category_name": "全部分组"
		}, {
			"category_name": "未分组"
		}, {
			"category_name": "已有分组"
		}]
		"""

#Scenario: 批量修改分组
#Scenario: 分页
