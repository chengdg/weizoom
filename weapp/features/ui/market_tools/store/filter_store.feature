# __author__ : "崔帅帅"
@func:market_tools.tools.store
Feature:在webapp中浏览门店列表
	bill能在webapp中按照地区看到jobs添加的门店列表

Background:
	Given jobs登录系统
	Given jobs已经添加门店信息
		"""
		[{
			"name": "门店1",
			"city": "北京"
		},{
			"name": "门店2",
			"city": "南京"
		}]
		"""
	And bill关注jobs的公众号

@weapp.market_tools.store.l
Scenario: 按所在地浏览全部门店列表
	jobs添加门店后
	bill能在webapp中看到jobs添加的门店

	When bill访问jobs的webapp
	And bill浏览jobs的webapp中'北京'地区内的门店列表
	Then bill获得webapp中所在地为'北京'的门店
	"""
	[{
		"name":"门店1",
		"city":"北京"
	}]
	"""
