# __author__ : "wangli"
Feature: jobs粉丝管理中的粉丝添加备注
			1在粉丝管理的粉丝列表中对某个粉丝加备注
			1)表示给当前的粉丝加备注2)加完备注后备注信息显示在粉丝昵称前，原粉丝昵称用“()”包起来
			3在已有备注下，加备注，相当于替换原有的备注信息
	
Background:
	Given jobs登录系统
	And jobs已获取粉丝列表
	"""
		[{
			"fans_nickname": "fans_1",
			"fans_remark":"",
			"attention_time": "2015-4-30 20:06:43",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""
	When jobs在"全部分组"选项卡下给"fans_1"修改备注信息
		"""
		[{
			"fans_remark": "fans_1备注修改"
			
		}]
		"""
	Then jobs成功获取'所有信息'列表
	"""
		[{
			"fans_nickname": "fans_1备注修改(fans_1)",
			"fans_remark":"fans_1备注修改",
			"attention_time": "2015-4-30 20:06:43",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
	"""

@new_weixin.message
Scenario: 2给已有备注的粉丝加备注，相当于替换原有的备注
	Given jobs登录系统
	And jobs已获取"fans_1"
	"""
		[{
			"fans_nickname": "fans_1",
			"fans_remark":"",
			"attention_time": "2015-4-30 20:06:43",
	    	"last_message_time": "2015-04-20 15:50:07",
		}]
	"""
	When jobs给"fans_1"添加备注信息
		"""
		[{
			"fans_remark":"fans_1备注",
			
		}]
		"""
	
	Then jobs成功获取"fans_1"列表
	"""
		{[{
			"fans_nickname": "fans_1备注(fans_1)",
			"fans_remark":"fans_1备注",
			"attention_time": "2015-4-30 20:06:43",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		}
	"""

	When jobs获取"fans_1"原有备注信息
		"""
		[{
			"remark": "fans_1备注"
			
		}]
		"""
	Then jobs给"fans_1"修改备注信息
		"""
		[{
			"remark": "fans_1备注-------备注修改"
			
		}]
		"""

	Then jobs成功获取"fans_1"列表
	"""
	{
	[{
			"fans_nickname": "fans_1备注-------备注修改(fans_1)",
			"fans_remark":"fans_1备注-------备注修改",
			"attention_time": "2015-4-30 20:06:43",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		}
	"""

	@new_weixin.message
	Scenario: 3给已有备注的粉丝加空格备注，相当于清空备注
	Given jobs登录系统
	And jobs已获取"fans_1"
	"""
		[{
			"fans_nickname": "fans_1",
			"fans_remark":"",
			"attention_time": "2015-4-30 20:06:43",
	    	"last_message_time": "2015-04-20 15:50:07",
		}]
	"""
	When jobs给"fans_1"添加备注信息
		"""
		[{
			"fans_remark":"fans_1备注",
			
		}]
		"""
	
	Then jobs成功获取"fans_1"列表
	"""
		[{
			"fans_nickname": "fans_1备注(fans_1)",
			"fans_remark":"fans_1备注",
			"attention_time": "2015-4-30 20:06:43",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		
	"""

	When jobs获取"fans_1"原有备注信息
		"""
		[{
			"remark": "fans_1备注"
			
		}]
		"""
	Then jobs给"fans_1"修改备注信息
		"""
		[{
			"remark": "    "
			
		}]
		"""

	Then jobs成功获取"fans_1"列表
	"""
	{
	[{
			"fans_nickname": "fans_1",
			"fans_remark":"   ",
			"attention_time": "2015-4-30 20:06:43",
	    	"last_message_time": "2015-04-20 15:50:07",
	    	"user_icon": "http://wx.qlogo.cn/mmopen/u83HrgfsuWXdb82iaCNl0vibGdEc1tib22ORvSBpwBW6VQthuweHP4Vp3kCCh1Sr3n39ogfxAhL7XlXxZYgG4e0Ig/0"
		}]
		}
	"""