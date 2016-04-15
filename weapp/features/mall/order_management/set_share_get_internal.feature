#watcher: benchi@weizoom.com, wangli@weizoom.com
#_author_:张三香 2016.04.14

Feature:后台设置'订单提交成功后提示分享赚积分'功能
	"""
		1、'订单-订单设置'，订单设置页面添加配置'订单提交成功后提示分享赚积分'功能；
		2、勾选时，显示如下配置项信息，不勾选时不显示：
			a.'上传弹层背景图片' 格式：建议jpg,png 尺寸:500*680 不超过1M
			b.'选择要分享的图文':
				b1.选择分享图文时，弹窗仅显示'单图文'
				b2.该图文点击后仅显示'正文内容'
				b3.图文选择后可修改
			c.'分享图片':
				c1.建议尺寸90*90,仅支持jpg/png
				c2.点击'添加图片',弹窗显示'用过的图片/新图片'两个选项卡
			d.'分享描述'
		3.页面设置完成后点击【保存】才能生效
		4.设置完成后，将勾选取消并且保存成功，再次勾选时显示上次所输入内容

		5、下单成功后直接显示分享赚积分弹层（背景图、【去分享】、关闭X）
		6、点击弹层右上角的“x”，则关闭该弹层，并返回到订单支付结果页，并且页面右侧悬浮显示“分享赚积分”入口，点击该入口则显示分享赚积分弹层；
		7、点击弹层中的【去分享】按钮，跳转到设置的分享图文页面（默认进入时显示蒙版提示“点击这里可以分享给好友哦！”）
		8、将链接分享给好友或朋友圈后，点击时直接显示图文页面，不显示分享蒙版提示
		9、该功能后台开启后，手机端个人中心的订单列表页则显示“分享赚积分”的入口，若后台关闭该功能，则手机端的入口消失；
		10、手机端订单详情页不显示“分享赚积分”入口

	"""

Scenario:1 后台设置'订单提交成功后提示分享赚积分'功能
	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"integral_each_yuan":10,
			"click_shared_url_increase_count":11
		}
		"""
	When jobs已添加单图文
		"""
		[{
			"title":"单图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"单条图文1文本摘要",
			"content":"单条图文1文本内容"
		},{
			"title":"单图文2",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou3.jpg"
			}],
			"cover_in_the_text":"false",
			"summary":"单条图文2文本摘要",
			"content":"单条图文2文本内容",
			"jump_url":"www.baidu.com"
		}]
		"""
	When jobs已添加多图文
		"""
		[{
			"title":"多图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"单条图文1文本内容"
		}]
		"""
	When jobs设置订单提交成功后提示分享赚积分信息
		"""
		{
			"logo_pic":"1.jpg",
			"text_picture":"单图文1",
			"share_pic":"2.jpg",
			"share_description":"分享描述1"
		}
		"""
	Then jobs获得订单提交成功后提示分享赚积分信息
		"""
		{
			"logo_pic":"1.jpg",
			"text_picture":"单图文1",
			"share_pic":"2.jpg",
			"share_description":"分享描述1"
		}
		"""
	#修改配置信息
	When jobs设置订单提交成功后提示分享赚积分信息
		"""
		{
			"logo_pic":"11.jpg",
			"text_picture":"单图文2",
			"share_pic":"22.jpg",
			"share_description":"分享描述2"
		}
		"""
	Then jobs获得订单提交成功后提示分享赚积分信息
		"""
		{
			"logo_pic":"11.jpg",
			"text_picture":"单图文2",
			"share_pic":"22.jpg",
			"share_description":"分享描述2"
		}
		"""
