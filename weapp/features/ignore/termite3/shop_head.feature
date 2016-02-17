#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

Feature: 自定义模块-店铺头


#图片非必填，背景色默认为蓝色

Scenario:1 商城店铺头
	When jobs登录系统
	And jobs添加店铺头信息
	"""
		[{
			"background_picture": "图片1",
			"shop_logo": "logo1",
			"background_color": "blue",
			"shop_name": "店铺1"
		}]
	"""

#若添加图片和背景色，则图片会覆盖背景色
	Then 展示区显示'店铺头'
	"""
		[{
			"background_picture": "图片1",
			"shop_logo": "logo1",
			"shop_name": "店铺1"
		}]
	"""
	When jobs删除'图片1'
	Then 展示区显示'店铺头'
	"""
		[{
			"shop_logo": "logo1",
			"background_color": "blue",
			"shop_name": "店铺1"
		}]
	"""

Scenario:2个性模板店铺头
	When jobs登录系统
	And jobs添加店铺头信息
	"""
		[{
			"background_picture": "图片1",
			"shop_name": "店铺1"
		}]
	"""
	Then 展示区显示'店铺头'
	"""
		[{
			"background_picture": "图片1",
			"shop_name": "店铺1"
		}]
	"""
	When jobs删除'图片1'
	Then 展示区显示'店铺头'
	"""
		[{
			"shop_name": "店铺1"
		}]
	"""

#店铺名称字数限制为15个字，一行显示，超出显示...
#重置背景色，是将背景色重置为默认颜色
Scenario:3 验证
	When jobs登录系统
	And jobs添加店铺头信息
	"""
		[{
			"shop_logo": "logo1",
			"background_color": "red",
			"shop_name": "店铺名称超过15个字"
		}]
	"""
	Then jobs编辑区提示错误信息'店铺名称最多可输入15个字'
	And jobs展示区显示'店铺头'
	"""
		[{
			"shop_logo": "logo1",
			"background_color": "red",
			"shop_name": "店铺名称前15个字"
		}]
	"""
	When jobs重置背景色
	Then jobs展示区显示'店铺头'
	"""
		[{
			"shop_logo": "logo1",
			"background_color": "blue",
			"shop_name": "店铺名称前15个字"
		}]
	"""






