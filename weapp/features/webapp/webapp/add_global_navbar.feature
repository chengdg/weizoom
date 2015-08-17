Feature: 添加webapp中的全局导航
	jobs能为webapp添加全局导航

Background:
	Given jobs登录系统
	And bill关注jobs的公众号
	
@webapp @webapp.webapp @webapp.global_navbar
Scenario: 添加全局导航
	jobs添加全局导航后
	1. jobs能在获得全局导航
	2. bill能在webapp上看到该全局导航

	Given jobs登录系统
	When jobs添加webapp的全局导航
		"""
		[{
			"name": "文章",
			"url": "url1"
		}, {
			"name": "商城",
			"items": [{
				"name": "个人中心",
				"url": "url2"
			}, {
				"name": "购物车",
				"url": "url3"
			}]
		}]
		"""	
	Then jobs能获得webapp的全局导航
		"""
		[{
			"name": "文章",
			"url": "url1"
		}, {
			"name": "商城",
			"items": [{
				"name": "个人中心",
				"url": "url2"
			}, {
				"name": "购物车",
				"url": "url3"
			}]
		}]
		"""	
	When bill访问jobs的webapp
	Then bill能看到jobs的webapp中的全局导航
		"""
		[{
			"name": "文章",
			"url": "url1"
		}, {
			"name": "商城",
			"items": [{
				"name": "个人中心",
				"url": "url2"
			}, {
				"name": "购物车",
				"url": "url3"
			}]
		}]
 		"""