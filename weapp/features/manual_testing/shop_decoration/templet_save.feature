#watcher:wangli@weizoom.com,wangxinrui@weizoom.com,benchi@weizoom.com
#_author_:王丽
#_edit_:新新

Feature: 自定义模块编辑-保存
	保存时，做如下两个校验
	1、校验自定义模块中的下面这些规则
		（1）富文本：最多只能输入10000字	
		（2）图片广告：	1、标题最多只能输入20个字符
						2、链接到必填‘链接地址不能为空’
						3、图片必填‘请添加一张图片’
		（3）标题：	1、标题名必填“标题名不能为空”
					2、标题名最大长度为30个字
					3、副标题最大长度为50个字
		（4）文本导航：1、导航名称是必填项‘导航名称不能为空’
						2、链接到必填‘链接地址不能为空’
						3、导航名称不得超过30个字数
		（5）图片导航：1、描述文字最多5个字符
					    2、四张图片必填，请添加一张图片
						3、链接到必填‘链接地址不能为空’
		（6）橱窗	1、标题名：最多可输入15个字
					2、内容区标题：最多可输入15个字
					3、内容区说明：最多输入50个字
					4、链接到必填‘链接地址不能为空’
					5、图片必填‘请添加一张图片’
	2、自定义模块第一次保存，弹窗填写自定义模块名称，模块名称有如下规则
			（1）模块名称不能为空
			（2）空格忽略，认为为空
			（3）去掉首尾空格
			（4）模块名称与现有系统中的自定义模块的名称可以重复


#1.保存时和预览一样，需要校验
#2.校验顺序从上到下一次校验
#3.保存后页面跳转到微页面列表页
