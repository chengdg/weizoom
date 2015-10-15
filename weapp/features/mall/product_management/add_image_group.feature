#editor:王丽 2015.10.14

Feature: 添加图片分组
"""

	Jobs通过管理系统在商城中添加图片及图片分组
"""

Background:
	Given jobs登录系统

@mall2 @product @picture   @mall @mall.product @mall.image_group
Scenario:1 添加图片分组
	Jobs添加图片分组后
	1. jobs能获取图片分组
	2. bill不能获取图片分组
	3. 多个图片分组按添加顺序排列

	When jobs添加图片分组
		"""
		{
			"name": "图片分组1",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""
	And jobs添加图片分组
		"""
		{
			"name": "图片分组2",
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou3.jpg"
			}]
		}
		"""
	And jobs添加图片分组
		"""
		{
			"name": "图片分组3",
			"images": []
		}
		"""
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
	And jobs能获取图片分组'图片分组1'
		"""
		{
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"path": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""
	And jobs能获取图片分组'图片分组2'
		"""
		{
			"images": [{
				"path": "/standard_static/test_resource_img/hangzhou3.jpg"
			}]
		}
		"""
	And jobs能获取图片分组'图片分组3'
		"""
		{
			"images": []
		}
		"""
	Given bill登录系统
	Then bill能获取图片分组列表
		"""
		[]
		"""
