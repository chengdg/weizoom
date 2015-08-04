# __author__ : '崔帅帅'

@func:webapp.modules.mall.views.list_products
Feature:微众商城商品页面增加现金支付功能
	用户能够在微众商城进入商户的现金支付页面

Background:
	Given bill登录系统	
	And bill已添加商品
		"""
		[{
			"name": "商品1",
			"is_commit": "是"
		}, {
			"name": "商品2",
			"is_commit": "是"
		},{
			"name": "商品3",
			"is_commit": "是"
		}]
		"""
	And jobs登录系统
	And jobs已审核bill的'商品1'
	And jobs已审核bill的'商品2'
	And jobs已审核bill的'商品3'
	And tom关注jobs的公共号

@ignore
@mall.attention_interface @ignore
Scenario:访问已配置好地址已审核的商品	
	1.tom通过webapp访问'商品1'详情页
	2.nokia通过tom分享的链接访问'商品1'详情页
	When bill配置现金支付地址
		"""
		{
			"url":'http://mp.weixin.qq.com'
		}
		"""
	Then tom在'商品1'的详情页能看到可点击'现金支付'的按钮
	Then nokia在'商品1'的详情页能看到可点击'现金支付'的按钮


@mall.attention_interface @ignore
Scenario:访问没有配置好地址但已审核的商品
	1.tom通过webapp访问'商品2'详情页
	2.nokia通过tom分享的链接访问'商品2'详情页

	When bill配置现金支付
		"""
		{
			"url":''
		}
		"""
	Then tom在'商品2'的详情页不能看到可点击'关注店铺'的按钮
	Then nokia在'商品2'的详情页不能看到可点击'关注店铺'的按钮


@mall.attention_interface @ignore
Scenario:访问配置非微信图文的现金支付地址但已审核的商品
	1.tom通过webapp访问'商品3'详情页
	2.nokia通过tom分享的链接访问'商品3'详情页
	
	When bill配置引导现金支付地址
		"""
		{
			"url":'http://www.baidu.com'
		}
		"""
	Then tom在'商品3'的详情页不能看到可点击'现金支付'的按钮
	Then nokia在'商品3'的详情页不能看到可点击'现金支付'的按钮

