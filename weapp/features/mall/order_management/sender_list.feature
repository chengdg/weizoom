# watcher: tianfengmin@weizoom.com, benchi@weizoom.com
# __author__ : "田丰敏" 

Feature: 发件人信息列表
"""
	发件人信息列表：发件人姓名、发件人电话、所在地区、详细地址、邮政编码、操作（编辑、删除）
	备注：
		1、第一次进入收件人信息页面，收件人信息列表为空，可通过“新增地址”链接跳转到“添加新地址”表单页面
		2、发件人信息列表中只有一个地址时，标注为默认地址，再次增加新地址后，默认地址为新增加的地址；发件人信息列表按照创建时间倒序排列；默认地址可手动修改
		3、可对已添加的发件人信息做编辑、删除的操作，删除所有发件人信息后，列表为空
	
"""

Scenario:1 发件人信息列表

	#jobs首次进入发件人信息列表，列表为空
	Given jobs登录系统
	Then jobs能获得收件人信息列表
		"""
		[]
		"""

	#添加一个新的地址，自动为默认地址
	When jobs添加发件人新地址
		"""
		{
			"sender_name": "一先生",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"sender_tel": "15612345678",
			"company_name": "某某技术有限公司",
			"remarks": "谢谢"
		}
	Then jobs能获得发件人信息列表
		"""
		{
			"sender_name": "一先生",
			"sender_tel": "15612345678",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "true",
			"actions": ["编辑","删除"]
		}
		"""

	#再添加两个个地址，“三先生”自动为默认地址
	When jobs添加发件人新地址
		"""
		[{
			"sender_name": "二先生",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"sender_tel": "15612345678"
		},{
			"sender_name": "三先生",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"sender_tel": "15612345678"		
		}]
	Then jobs能获得发件人信息列表
		"""
		[{
			"sender_name": "三先生",
			"sender_tel": "15612345678",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "true",
			"actions": ["编辑","删除"]
		},{
			"sender_name": "二先生",
			"sender_tel": "15612345678",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "",
			"is_selected": "false",
			"actions": ["编辑","删除","默认"]
		},{
			"sender_name": "一先生",
			"sender_tel": "15612345678",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "false",
			"actions": ["编辑","删除","默认"]
		}]
		"""

	#编辑地址“一先生”的电话为“15688888888”
	When jobs编辑'一先生'地址信息
		"""
		{
			"sender_name": "一先生",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"sender_tel": "15688888888",
			"company_name": "某某技术有限公司",
			"remarks": "谢谢"
		}
		"""
	Then jobs能获得发件人信息列表
		"""
		[{
			"sender_name": "三先生",
			"sender_tel": "15612345678",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "true",
			"actions": ["编辑","删除"]
		},{
			"sender_name": "二先生",
			"sender_tel": "15612345678",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "",
			"is_selected": "false",
			"actions": ["编辑","删除","默认"]
		},{
			"sender_name": "一先生",
			"sender_tel": "15688888888",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "false",
			"actions": ["编辑","删除","默认"]
		}]
		"""

	#手动修改“二先生”为默认地址
	When jobs设置'二先生'为默认地址
	Then jobs能获得发件人信息列表
		"""
		[{
			"sender_name": "三先生",
			"sender_tel": "15612345678",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "false",
			"actions": ["编辑","删除","默认"]
		},{
			"sender_name": "二先生",
			"sender_tel": "15612345678",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "",
			"is_selected": "true",
			"actions": ["编辑","删除"]
		},{
			"sender_name": "一先生",
			"sender_tel": "15688888888",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "false",
			"actions": ["编辑","删除","默认"]
		}]
		"""

	#删除默认地址“二先生”的信息，“一先生”成为默认地址
	When jobs'删除'地址'三先生'
	When jobs'删除'地址'二先生'
	Then jobs能获得发件人信息列表
		"""
		{
			"sender_name": "一先生",
			"sender_tel": "15688888888",
			"area": "北京北京市海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "true",
			"actions": ["编辑","删除"]
		}
		"""

	#删除默认地址“一先生”的信息
	When jobs'删除'地址'一先生'
	Then jobs能获得发件人信息列表
		"""
		[]
		"""