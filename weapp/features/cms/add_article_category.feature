Feature: Add Article Category
	Jobs能通过管理系统为管理商城添加的"文章分类"

@cms.add_article_category
Scenario: 添加文章分类
	Jobs添加一组"文章分类"后，"文章分类列表"会按照添加的顺序倒序排列

	Given jobs登录系统
	When jobs添加文章分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	Then jobs能获取文章分类列表
		"""
		[{
			"name": "分类3"
		}, {
			"name": "分类2"
		}, {
			"name": "分类1"
		}]
		"""
	And bill能获取文章分类列表
		"""
		[]
		"""