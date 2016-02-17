#watcher:wangli@weizoom.com,benchi@weizoom.com
#editor：王丽 2015.10.14

Feature: 更新图片分组
"""

	Jobs通过管理系统在商城中更新图片分组
"""

Background:
	Given jobs登录系统
	When jobs添加图片分组
		"""
		[{
			"name": "图片分组1",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "图片分组2",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou3.jpg"
			}]
		}, {
			"name": "图片分组3",
			"images": []
		}]
		"""
	Given bill登录系统
	When bill添加图片分组
		"""
		[{
			"name": "图片分组1",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "图片分组2",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou3.jpg"
			}]
		}, {
			"name": "图片分组3",
			"images": []
		}]
		"""

@mall2 @product @picture   @mall @mall.product @mall.product_model
Scenario:1 更新图片分组
	jobs更新图片分组的名称和图片后
	1. job的图片分组更新
	2. bill的图片分组不受影响
	
	Given jobs登录系统
	Then jobs能获取图片分组列表
		"""
		[{
			"name": "图片分组1",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "图片分组2",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou3.jpg"
			}]
		}, {
			"name": "图片分组3",
			"images": []
		}]
		"""
	When jobs更新图片分组'图片分组1'
		"""
		{
			"name": "图片分组1*",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/standard_static/test_resource_img/mian1.jpg"
			}]
		}
		"""
	Then jobs能获取图片分组列表
		"""
		[{
			"name": "图片分组1*",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/standard_static/test_resource_img/mian1.jpg"
			}]
		}, {
			"name": "图片分组2",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou3.jpg"
			}]
		}, {
			"name": "图片分组3",
			"images": []
		}]
		"""
	And jobs能获取图片分组'图片分组1*'
		"""
		{
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/standard_static/test_resource_img/mian1.jpg"
			}]
		}
		"""
	Given bill登录系统
	Then bill能获取图片分组列表
		"""
		[{
			"name": "图片分组1",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
			"name": "图片分组2",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou3.jpg"
			}]
		}, {
			"name": "图片分组3",
			"images": []
		}]
		"""
