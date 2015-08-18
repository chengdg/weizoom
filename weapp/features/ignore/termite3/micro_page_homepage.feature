#author：师帅
Feature: 微页面-设为主页

#project1为主页面
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

Scenario:1对设为主页微页面进行操作
#编辑操作
	When jobs对微页面列表'project1'进行'编辑'操作
	Then jobs进入'project1'编辑页面

#链接操作
	When jobs对微页面列表'project1'进行'链接'操作
	Then jobs弹出链接地址
	And jobs对链接进行'复制'操作

#对主页查看二维码
	When jobs对微页面列表'project1'进行'二维码'操作
	Then jobs弹出'project1'的二维码信息

#预览操作
	When jobs对微页面列表'project1'进行'预览'操作
	Then jobs对'project1'进行预览