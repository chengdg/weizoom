# __author__ : "冯雪静"

Feature: 删除红包
	Jobs能通过管理系统删除"分享红包"
	
Background:
	Given jobs登录系统
	And jobs已添加分享红包
		"""
		[{
			"name": "分享红包1",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""

Scenario: 1 开启分享红包
	jobs成功创建红包后，是关闭状态，可以进行开启操作
	1.分享红包列表中只允许一个红包是开启状态


	Given jobs登录系统
	Then jobs能获取红包列表
		"""
		[{
			"name": "分享红包1",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""
	When jobs开启分享红包'分享红包1'
	Then jobs能获取红包列表
		"""
		[{
			"name": "分享红包1",
			"status": "开启",
			"actions": ["关闭","查看"]
		}, {
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""
	When jobs开启分享红包'分享红包2'
	Then jobs获得错误提示'请先关闭开启活动'
	Then jobs能获取红包列表
		"""
		[{
			"name": "分享红包1",
			"status": "开启",
			"actions": ["关闭","查看"]
		}, {
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""
	

Scenario: 2 删除分享红包
	jobs成功创建红包后，是关闭状态，可以进行删除操作
	1.开启红包后不可以进行删除操作

	Given jobs登录系统
	Then jobs能获取红包列表
		"""
		[{
			"name": "分享红包1",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""
	When jobs删除分享红包'分享红包1'
	Then jobs能获取红包列表
		"""
		[{
			"name": "分享红包2",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}, {
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""
	When jobs开启分享红包'分享红包2'
	Then jobs能获取红包列表
		"""
		[{
			"name": "分享红包2",
			"status": "开启",
			"actions": ["关闭","查看"]
		}, {
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""
	#开启红包后不可删除
	When jobs删除分享红包'分享红包2'
	Then jobs能获取红包列表
		"""
		[{
			"name": "分享红包2",
			"status": "开启",
			"actions": ["关闭","查看"]
		}, {
			"name": "分享红包3",
			"status": "关闭",
			"actions": ["开启","删除","查看"]
		}]
		"""

		
