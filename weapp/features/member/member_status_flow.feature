Feature: 用户状态流
	测试在各种场景下与用户状态相关的各种数据的状态迁移

Background:
	Given jobs登录系统
	And 开启手动清除cookie模式

@mall2 @crm @member @member.status_flow
Scenario:1 直接关注单个公众号
	bill关注jobs的公众号

	When 清空浏览器
	Then 浏览器cookie包含"[]"
	And bill不是jobs的会员
	When bill关注jobs的公众号
	Then 浏览器cookie包含"[]"
	And bill已是jobs的会员
	When bill访问jobs的webapp
	Then 浏览器cookie包含"[sct, uuid]"
	When bill获得db中在jobs公众号中的sct为'sct_in_db'
	When bill获得db中在jobs公众号中的uuid为'uuid_in_db'
	Then 浏览器cookie等于
		"""
		{"sct":"sct_in_db", "uuid":"uuid_in_db"}
		"""
	And bill在jobs中的social_account与member已关联


@mall2 @crm @member @member.status_flow
Scenario:2 关注多个公众号，访问多个公众号的微站
	bill先关注jobs的公众号，再关注tom的公众号

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得db中在jobs公众号中的sct为'sct_to_jobs_in_db'
	When bill获得db中在jobs公众号中的uuid为'uuid_to_jobs_in_db'
	Then 浏览器cookie等于
		"""
		{"sct":"sct_to_jobs_in_db", "uuid":"uuid_to_jobs_in_db"}
		"""
	And bill不是tom的会员
	When bill关注tom的公众号
	Then bill已是tom的会员
	Then 浏览器cookie等于
		"""
		{"sct":"sct_to_jobs_in_db", "uuid":"uuid_to_jobs_in_db"}
		"""
	When bill访问tom的webapp
	When bill获得db中在tom公众号中的sct为'sct_to_tom_in_db'
	When bill获得db中在tom公众号中的uuid为'uuid_to_tom_in_db'
	Then 浏览器cookie等于
		"""
		{"sct":"sct_to_tom_in_db", "uuid":"uuid_to_tom_in_db"}
		"""
	When bill访问jobs的webapp
	Then 浏览器cookie等于
		"""
		{"sct":"sct_to_jobs_in_db", "uuid":"uuid_to_jobs_in_db"}
		"""
	When bill访问tom的webapp
	Then 浏览器cookie等于
		"""
		{"sct":"sct_to_tom_in_db", "uuid":"uuid_to_tom_in_db"}
		"""
	
@mall2 @crm @member @member.status_flow
Scenario:3 会员向朋友圈分享链接
	bill关注jobs的公众号

	When 清空浏览器
	When bill关注jobs的公众号
	When bill关注tom的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈
	Then bill分享的链接中的fmt为bill在jobs中的mt
	When bill访问tom的webapp
	When bill把tom的微站链接分享到朋友圈
	Then bill分享的链接中的fmt为bill在tom中的mt


@mall2 @crm @member @member.status_flow
Scenario:4 bill分享，tom关注，tom点击，tom访问webapp
	bill关注jobs的公众号

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈
	When bill获得db中在jobs公众号中的mt为'mt_{bill_jobs}'

	When 清空浏览器
	When tom关注jobs的公众号
	When tom点击bill分享链接
	When tom获得db中在jobs公众号中的uuid为'uuid_{tom_jobs}_in_db'
	Then 浏览器cookie等于
		"""
		{"fmt":"mt_{bill_jobs}", "uuid":"!uuid_{tom_jobs}_in_db"}
		"""
	When tom访问jobs的webapp
	When tom获得db中在jobs公众号中的uuid为'uuid_{tom_jobs}_in_db'
	When tom获得db中在jobs公众号中的sct为'sct_{tom_jobs}_in_db'
	Then 浏览器cookie等于
		"""
		{"fmt":"mt_{bill_jobs}", "uuid":"uuid_{tom_jobs}_in_db", "sct":"sct_{tom_jobs}_in_db"}
		"""

	When tom把jobs的微站链接分享到朋友圈
	Then tom分享的链接中的fmt为tom在jobs中的mt



@mall2 @crm @member @member.status_flow
Scenario:5 bill分享，tom关注，tom访问webapp，tom点击
	bill关注jobs的公众号

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈
	When bill获得db中在jobs公众号中的mt为'mt_{bill_jobs}'
	Then bill分享的链接中的fmt为bill在jobs中的mt

	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom点击bill分享链接
	When tom获得db中在jobs公众号中的uuid为'uuid_{tom_jobs}_in_db'
	When tom获得db中在jobs公众号中的sct为'sct_{tom_jobs}_in_db'
	Then 浏览器cookie等于
		"""
		{"fmt":"mt_{bill_jobs}", "uuid":"uuid_{tom_jobs}_in_db", "sct":"sct_{tom_jobs}_in_db"}
		"""


@mall2 @crm @member @member.status_flow
Scenario:6 bill分享，-tom点击，tom关注, tom访问webapp
	bill关注jobs的公众号

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈
	When bill获得db中在jobs公众号中的mt为'mt_{bill_jobs}'

	When 清空浏览器
	When tom点击bill分享链接
	Then tom在jobs公众号中有uuid对应的webapp_user
	Then 浏览器cookie包含"[fmt, uuid]"
	Then 浏览器cookie等于
		"""
		{"fmt":"mt_{bill_jobs}"}
		"""
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom获得db中在jobs公众号中的uuid为'uuid_{tom_jobs}_in_db'
	When tom获得db中在jobs公众号中的sct为'sct_{tom_jobs}_in_db'
	Then 浏览器cookie等于
		"""
		{"fmt":"mt_{bill_jobs}", "uuid":"uuid_{tom_jobs}_in_db", "sct":"sct_{tom_jobs}_in_db"}
		"""
	Then tom在jobs公众号中有mt对应的webapp_user


@mall2 @crm @member @member.status_flow
Scenario:7 bill分享，-tom点击并分享，nokia关注, nokia访问webapp, nokia点击
	bill关注jobs的公众号

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈
	When bill获得db中在jobs公众号中的mt为'mt_{bill_jobs}'

	When 清空浏览器
	When tom点击bill分享链接
	When tom把jobs的微站链接分享到朋友圈
	Then tom分享的链接中的fmt为空

	When 清空浏览器
	When nokia关注jobs的公众号
	When nokia访问jobs的webapp
	Then 浏览器cookie包含"[sct]"
	When nokia点击tom分享链接
	Then nokia当前链接中的fmt为nokia在jobs中的mt


@mall2 @crm @member @member.status_flow
Scenario:8 bill分享，-tom点击并分享，nokia关注, nokia点击, nokia访问webapp
	bill关注jobs的公众号

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈

	When 清空浏览器
	When tom点击bill分享链接
	When tom把jobs的微站链接分享到朋友圈
	Then tom分享的链接中的fmt为空

	When 清空浏览器
	When nokia关注jobs的公众号
	When nokia点击tom分享链接
	Then nokia当前链接中的fmt为空
	Then 浏览器cookie包含"[!fmt, !sct, uuid]"
	When nokia访问jobs的webapp
	Then 浏览器cookie包含"[sct, uuid]"
	Then nokia当前链接中的fmt为nokia在jobs中的mt


@mall2 @crm @member @member.status_flow
Scenario:9 bill分享，-tom点击并分享，nokia点击, nokia关注, nokia访问webapp
	bill关注jobs的公众号

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill把jobs的微站链接分享到朋友圈

	When 清空浏览器
	When tom点击bill分享链接
	When tom把jobs的微站链接分享到朋友圈
	Then tom分享的链接中的fmt为空

	When 清空浏览器
	When nokia点击tom分享链接
	Then nokia当前链接中的fmt为空
	Then 浏览器cookie包含"[!fmt, !sct, uuid]"
	When nokia关注jobs的公众号
	When nokia访问jobs的webapp
	Then 浏览器cookie包含"[sct, uuid]"
	Then nokia当前链接中的fmt为nokia在jobs中的mt


@mall2 @crm @member @member.status_flow
Scenario:10 在多个会员分享公众号的链接中切换

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得db中在jobs公众号中的mt为'mt_{bill_jobs}'
	When bill把jobs的微站链接'bill_jobs_shared_url'分享到朋友圈

	When 清空浏览器
	When tom关注guo的公众号
	When tom访问guo的webapp
	When tom获得db中在guo公众号中的mt为'mt_{tom_guo}'
	When tom把guo的微站链接'tom_guo_shared_url'分享到朋友圈

	When 清空浏览器
	When nokia点击bill分享链接'bill_jobs_shared_url'
	Then 浏览器cookie等于
		"""
		{"fmt":"mt_{bill_jobs}"}
		"""
	When nokia点击tom分享链接'tom_guo_shared_url'
	Then 浏览器cookie等于
		"""
		{"fmt":"mt_{tom_guo}"}
		"""


@mall2 @crm @member @member.status_flow
Scenario:11 同一个会员在不同设备上访问同一个公众号
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp

	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp
	Then bill在jobs公众号中有1个webapp_user


@mall2 @crm @member @member.status_flow
Scenario:12 同一个会员在不同设备上访问同一个公众号
	When 清空浏览器
	When bill关注jobs的公众号
	When bill访问jobs的webapp

	When 清空浏览器
	When tom关注jobs的公众号
	When tom访问jobs的webapp
	When tom把jobs的微站链接'tom_jobs_shared_url'分享到朋友圈

	When 清空浏览器
	When bill点击tom分享链接'tom_jobs_shared_url'
	When bill访问jobs的webapp
	Then 浏览器cookie包含"[sct]"
	Then bill在jobs公众号中有2个webapp_user
	