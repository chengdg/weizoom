Feature: Add Article
	Jobs能通过管理系统在文章管理中添加"文章"

Background:
	Given jobs登录系统
	When jobs已添加了文章分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""

@cms @cms.article
Scenario: 添加文章
	Jobs添加文章后，能获取它添加的文章
	
	When jobs添加文章
		"""
		[{
			"category" : "分类1",
			"content" :	"<p>内容1<br/></p>",
			"summary" : "摘要1",
			"title" : "文章1"
		}, {
			"category" : "分类2",
			"content" :	"<p>内容2<br/></p>",
			"summary" : "摘要2",
			"title" : "文章2"
		}]	
		"""
	Then jobs能获取文章'文章1'
		"""
		{
			"category" : "分类1",
			"content" :	"<p>内容1<br/></p>",
			"summary" : "摘要1",
			"title" : "文章1"
		}
		"""
	And jobs能获取文章'文章2'
		"""
		{
			"category" : "分类2",
			"content" :	"<p>内容2<br/></p>",
			"summary" : "摘要2",
			"title" : "文章2"
		}
		"""
	Given bill登录系统
	Then bill能获取文章列表
		"""
		[]
		"""


@cms @cms.article
Scenario: 添加文章按倒序排列
	Jobs添加多个文章后，"文章列表"会按照添加的顺序倒序排列
	
	When jobs添加文章
		"""
		[{
			"title": "文章1"
		}, {
			"title": "文章2"
		}, {
			"title": "文章3"
		}]	
		"""
	Then jobs能获取文章列表
		"""
		[{
			"title": "文章3"
		}, {
			"title": "文章2"
		}, {
			"title": "文章1"
		}]
		"""
	Given bill登录系统
	Then bill能获取文章列表
		"""
		[]
		"""