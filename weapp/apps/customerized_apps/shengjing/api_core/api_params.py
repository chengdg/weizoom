# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from django.conf import settings

class ShengjingAPIParams(object):
	"""
	盛景接口的相关参数
	"""

	def __init__(self):
		pass

	# 测试接口接口url
	TEST_URL = 'http://218.240.128.124:8080/ESignIn/Switches'

	# 正式接口
	URL = 'http://218.240.128.124:8081/ESignIn/Switches'
	
	def api_url(self):
		if settings.MODE == 'deploy':
			return self.URL
		else:
			return self.TEST_URL

	"""
	访问接口参数
	"""
	# 必须
	PARAM = 'Param'

	# 必须  三个接口Method
	# 值为调用的“命令字”，区分大小写，各具体接口命令字大小写需遵守本文档规范。
	METHOD = 'Method'

	# 必须 	版本号 目前1.0
	# 值为接口的当前版本，目前固定为“1.0”
	VERSION='Version'

	# 访问者唯一ID，另外说明。
	APPID = 'AppID'

	# 必须
	PARAMS = 'Params'

	# 必须 	
	# 访问者提交的验证Key。当前访问者调用“获取会话身份接口”WhoAmI获得的会话令牌SessionID，然后依据SessionID生成Key
	APPKEY = 'Key'

	# 当前学员的手机号码
	PARAM_MPHONE = 'MPhone'

	# String	报名课程
	COURSE = 'Course'

	# String	报名人
	STUDENT ='Student'

	# String	所属公司
	CUSTOMER = 'Customer'

	# Integer	参课人数
	NUMBER = 'Number'

	# String	报名时间
	BOOKED_TIME = 'BookedTime'

	# String	报名时间
	Captcha = 'Captcha'

	# String	公司名称
	COMPANY_NAME = 'company_name'

	# Integer	状态
	STATUS = 'status'

	# 当前学员的手机号码
	PHONE_NUMBER = 'phone_number'

	# webapp_user_id
	WEBAPP_USER_ID = 'webapp_user_id'

	# id
	ID = 'id'


	"""
	接口返回参数
	"""
	# 数值型数据
	# 返回代码，判断接口调用是否成功的依据。
	# (1)0，访问成功；
	# (2)-1，特别错误代码，当前用户没有权限；
	# (3)其它错误代码
	CODE = 'Code'

	# 数值型数据
	# 为当前的记录总数（非获取列表访问时为1）
	RECORD = 'Record'

	# 数值型数据
	# 为当前的页总数（非获取列表访问时忽略）
	PAGES = 'Pages'

	# 字符型数据
	# (1)"Code"为0时，本项值为返回的提示信息；
	# (2)"Code"为-1是，本项值为“权限不足。”；
	# (3)"Code"为其它错误代码时，本项为错误信息；
	INFO = 'Info'


	WATCHDOG_TYPE_SHENGJING = 'SHENGJING'