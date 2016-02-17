#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

Feature: 微页面-微页面列表

Background:
	Given jobs登录系统
	And jobs已获取微页面列表信息
	"""
		[{
			"name": "project1",
			"creat_time": "2015-6-19 12:00:00"
		}, {
			"name": "project2",
			"creat_time": "2015-6-18 12:00:00"
		}, {
			"name": "project3",
			"creat_time": "2015-6-17 12:00:00"
		}, {
			"name": "project4",
			"creat_time": "2015-6-16 12:00:00"
		}]
	"""
	And jobs已添加模块
		"""
		[	
			{"model_name": "富文本"},
			{"model_name": "商品"},
			{"model_name": "商品列表"},
			{"model_name": "图片广告"},
			{"model_name": "公告"},
			{"model_name": "标题"},
			{"model_name": "文本导航"},
			{"model_name": "图片导航"},
			{"model_name": "辅助空白"},
			{"model_name": "橱窗"}
		]
		"""
	

Scenario:1微页面列表

#编辑操作
	When jobs对微页面列表'project1'进行'编辑'操作
	Then jobs进入'project1'编辑页面


#删除操作
	When jobs对微页面列表'project1'进行'删除'操作
	Then jobs弹出确认删除提示信息
	And jobs微页面列表显示
	"""
		[{
			"name": "project2",
			"creat_time": "2015-6-18 12:00:00"
		}, {
			"name": "project3",
			"creat_time": "2015-6-17 12:00:00"
		}, {
			"name": "project4",
			"creat_time": "2015-6-16 12:00:00"
		}]
	"""

#链接操作
	When jobs对微页面列表'project2'进行'链接'操作
	Then jobs弹出链接地址
	And jobs对链接进行'复制'操作


#预览操作
	When jobs对微页面列表'project2'进行'预览'操作
	Then jobs对'project2'进行预览


#设为主页
	When jobs对微页面列表'project4'进行'设为主页'操作
	Then jobs将'project4'设为主页
	And jobs将 'project4'的'设为主页'变为'店铺主页'
	And jobs微页面列表显示
	"""
		[{
			"name": "project4",
			"creat_time": "2015-6-16 12:00:00"
		}, {
			"name": "project2",
			"creat_time": "2015-6-18 12:00:00"
		}, {
			"name": "project3",
			"creat_time": "2015-6-17 12:00:00"
		}]
	"""
	When jobs对微页面列表'project2'进行'设为主页'操作
	Then jobs将'project2'设为主页
	And jobs将 'project2'的'设为主页'变为'店铺主页'
	And jobs微页面列表显示
	"""
		[{
			"name": "project2",
			"creat_time": "2015-6-18 12:00:00"
		}, {
			"name": "project3",
			"creat_time": "2015-6-17 12:00:00"
		}, {
			"name": "project4",
			"creat_time": "2015-6-16 12:00:00"
		}]
	"""
	
#修改店铺名称，修改店铺主页名称，则上面显示店铺名称实时刷新显示
	When jobs修改'project2'名称
	"""
		[{
			"name": "pro2"
		}]
	"""
	Then jobs微页面列表显示
	"""
		[{
			"name": "pro2",
			"creat_time": "2015-6-18 12:00:00"
		}, {
			"name": "project3",
			"creat_time": "2015-6-17 12:00:00"
		}, {
			"name": "project4",
			"creat_time": "2015-6-16 12:00:00"
		}]
	"""






	