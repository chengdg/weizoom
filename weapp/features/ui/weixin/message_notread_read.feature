# __author__ : "新新"


Feature:未读消息为已读

"""
	1.给选中的会员标为已读"选中的消息标为已读"
	2.全选中针对当前页
	3.批量标为已读"全部未读消息标为已读"
	#选中消息标记为已读：仅针对当前页面
	#全部未读消息标记为已读：针对所有未读消息
"""
	Background：
	Given jobs登录系统

	#jobs查看bill的未读消息，未读一条

		When bill关注jobs的公众号
		When bill在模拟器中给jobs发送消息'bill发送一条文本消息，未读'

	#jobs查看bill的未读消息，未读两条

		When bill1关注jobs的公众号
		When bill1在模拟器中给jobs发送消息'bill1发送一条文本消息，未读'
		When bill1在模拟器中给jobs发送消息'bill1_图片.png'

	#jobs查看bill的未读消息，未读十条

		When bill2关注jobs的公众号
		When bill2在模拟器中给jobs发送消息'bill2发送一条文本消息，未读'
		When bill2在模拟器中给jobs发送消息'bill2发送二条文本消息，未读'
		When bill2在模拟器中给jobs发送消息'bill2发送三条文本消息，未读'
		When bill2在模拟器中给jobs发送消息'bill2发送四条文本消息，未读'
		When bill2在模拟器中给jobs发送消息'bill2发送五条文本消息，未读'
		When bill2在模拟器中给jobs发送消息'bill2发送六条文本消息，未读'
		When bill2在模拟器中给jobs发送消息'bill2发送七条文本消息，未读'
		When bill2在模拟器中给jobs发送消息'bill2发送八条文本消息，未读'
		When bill2在模拟器中给jobs发送消息'bill2发送九条文本消息，未读'
		When bill2在模拟器中给jobs发送消息'bill2发送十条文本消息，未读'


	#会员按发送时间倒序显示
	#列表按会员发送时间倒序显示
	Then jobs获得实时消息"未读信息"列表
		"""
		[{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 10,
			"fans_name": "bill2",
			"inf_content": "bill2发送十条文本消息，未读",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 2,
			"fans_name": "bill1",
			"inf_content": "bill1_图片.png",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		},{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 1,
			"fans_name": "bill",
			"inf_content": "bill发送一条文本消息，未读",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		"""

Scenario:1 给选中的会员标为已读"选中的消息标为已读

	Given jobs登录系统
	When jobs选中的消息标为已读:ui
	"""
		[{
			"name": bill
		},{
			"name": bill1
		}]
	"""
	Then jobs获得实时消息"未读信息"列表:ui
		"""
		[{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 10,
			"fans_name": "bill2",
			"inf_content": "bill2发送十条文本消息，未读",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		"""
Scenario:2 全选中针对当前页

	Given jobs登录系统
	When jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs选中的消息标为已读:ui
	#选中第一页的全选
		"""
		[{
			"name": [全选]
		}]
		"""
	Then jobs获得实时消息"未读信息"列表:ui
		"""
		[{
			"have_read": false,
			"have_replied": false,
			"remark": "",
			"start": false,
			"unread_count": 1,
			"fans_name": "bill",
			"inf_content": "bill发送一条文本消息，未读",
			"last_message_time": "今天",
			"latest_reply_time": "",
			"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		"""
Scenario:3 批量标为已读"全部未读消息标为已读"

	Given jobs登录系统
	When jobs设置分页查询参数
		"""
		{
			"count_per_page":2
		}
		"""
	When jobs选中的消息标为已读:ui
		"""
		[{
			"name": [全部]
		}]
		"""

	Then jobs获得实时消息"未读信息"列表:ui
		"""
		[]
		"""
	

	

