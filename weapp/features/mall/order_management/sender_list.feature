# watcher: tianfengmin@weizoom.com, benchi@weizoom.com
# __author__ : "田丰敏" 

Feature: 发件人信息列表
"""
	发件人信息列表：发件人姓名、发件人电话、所在地区、详细地址、邮政编码、操作（编辑、删除、默认）
	备注：
		1、第一次进入发件人信息页面，发件人信息列表为空，可通过“新增地址”链接跳转到“添加新地址”表单页面
		2、发件人信息列表中只有一个地址时，标注为默认地址，再次增加新地址后，默认地址为新增加的地址；发件人信息列表按照创建时间倒序排列；默认地址可手动修改
		3、可对已添加的发件人信息做编辑、删除的操作，删除所有发件人信息后，列表为空
	
		打印快递单检查点：
			1、选择需要打印的一个或多个订单后，点击“打印快递单”，出现弹窗，可选择快递模板，快递目前只支持部分：四通一达（申通、圆通、中通、百世汇通、韵达）、顺丰、EMS、德邦、宅急送
			2、如果未提前设置发件人信息，打印快递单时，可弹层提示“请先设置发件人信息”；如果已有默认地址，打印快递单时，直接使用默认地址
			3、打印快递单时，若收货人信息相同（收货人姓名、收货人电话、收货人地址相同），合并打印一张发货单
			4、打印快递单时，订单自动标记为已发货，且自动填充物流信息

		添加新地址表单检查点：
			1、表单包含：发件人（必填）、所在地区（必填）、详细地址（必填）、邮政编码、发件人电话（必填）、公司名称、备注
			2、发件人电话有位数、号段等校验

		手机端检查点：
			1、打印发货单，后台订单状态和物流信息自动修改后，手机端信息同步
			2、可查看物流信息，暂无物流信息时，显示为“商家正在通知快递公司揽件”，有物流信息则展示物流信息
"""
@mall2
Scenario:1 发件人信息列表

	#jobs首次进入发件人信息列表，列表为空
	Given jobs登录系统
	Then jobs能获得发件人信息列表
		"""
		[]
		"""

	#添加一个新的地址，自动为默认地址
	When jobs添加发件人新地址
		"""
		[{
			"sender_name": "一先生",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"sender_tel": "15612345678",
			"company_name": "某某技术有限公司",
			"remarks": "谢谢"
		}]
		"""
	Then jobs能获得发件人信息列表
		"""
		[{
			"sender_name": "一先生",
			"sender_tel": "15612345678",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "true"
		}]
		"""

	#再添加两个地址，“三先生”自动为默认地址
	When jobs添加发件人新地址
		"""
		[{
			"sender_name": "二先生",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"sender_tel": "15612345678"
		},{
			"sender_name": "三先生",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"sender_tel": "15612345678"		
		}]
		"""
	Then jobs能获得发件人信息列表
		"""
		[{
			"sender_name": "三先生",
			"sender_tel": "15612345678",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "true"
		},{
			"sender_name": "二先生",
			"sender_tel": "15612345678",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "",
			"is_selected": "false"
		},{
			"sender_name": "一先生",
			"sender_tel": "15612345678",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "false"
		}]
		"""

	#编辑地址“一先生”的电话为“15688888888”
	When jobs编辑'一先生'地址信息
		"""
		[{
			"sender_name": "一先生",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"sender_tel": "15688888888",
			"company_name": "某某技术有限公司",
			"remarks": "谢谢"
		}]
		"""
	Then jobs能获得发件人信息列表
		"""
		[{
			"sender_name": "三先生",
			"sender_tel": "15612345678",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "true"
		},{
			"sender_name": "二先生",
			"sender_tel": "15612345678",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "",
			"is_selected": "false"
		},{
			"sender_name": "一先生",
			"sender_tel": "15688888888",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "false"
		}]
		"""

	#手动修改“二先生”为默认地址
	When jobs设置'二先生'为默认地址
	Then jobs能获得发件人信息列表
		"""
		[{
			"sender_name": "三先生",
			"sender_tel": "15612345678",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "false"
		},{
			"sender_name": "二先生",
			"sender_tel": "15612345678",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "",
			"is_selected": "true"
		},{
			"sender_name": "一先生",
			"sender_tel": "15688888888",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "false"
		}]
		"""

	#删除默认地址“二先生”的信息，“三先生”成为默认地址
	When jobs'删除'地址'二先生'
	Then jobs能获得发件人信息列表
		"""
		[{
			"sender_name": "三先生",
			"sender_tel": "15612345678",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "true"
		},{
			"sender_name": "一先生",
			"sender_tel": "15688888888",
			"area": "北京 北京市 海淀区",
			"sender_address": "海淀科技大厦301",
			"code": "111111",
			"is_selected": "false"
		}]
		"""

	#删除所有地址信息
	When jobs'删除'地址'三先生'
	When jobs'删除'地址'一先生'
	Then jobs能获得发件人信息列表
		"""
		[]
		"""