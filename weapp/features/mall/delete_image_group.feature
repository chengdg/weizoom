Feature: 删除图片分组
	Jobs通过管理系统在商城中删除图片分组

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

@mall @mall.product @mall.product_model @mall2
Scenario: 删除图片分组
	jobs删除图片分组后
	1. jobs的图片分组发生变化
	2. bill的图片分组不变
	
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
	When jobs删除图片分组'图片分组1'
	Then jobs能获取图片分组列表
		"""
		[{
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
