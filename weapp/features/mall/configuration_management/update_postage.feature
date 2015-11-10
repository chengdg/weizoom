#author: 冯雪静
#editor: 张三香 2015.10.16

Feature:更新运费配置
	Jobs能通过管理系统为管理商城更新已添加的"邮费配置"

Background:
	Given jobs登录系统 
	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}, {
			"name" : "圆通",
			"first_weight":1,
			"first_weight_price":10.00
		}]
		"""

@mall2 @configuration @postaSet   @mall @mall.postage
Scenario:1 更新邮费配置
	Jobs更新"邮费配置"
	1. jobs能获得更新后的邮费配置

	Given jobs登录系统
	When jobs修改'顺丰'运费配置
		"""
		{
			"name" : "顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00,
			"special_area": [{
				"to_the":"北京市",
				"first_weight_price":20.00,
				"added_weight_price":10.00
			},{
				"to_the":"上海市,重庆市,江苏省",
				"first_weight_price":30.00,
				"added_weight_price":20.00
			}]
		}
		"""
	When jobs修改'圆通'运费配置
		"""
		{
			"name" : "圆通",
			"first_weight":1,
			"first_weight_price":10.0,
			"special_area": [{
				"to_the":"上海市",
				"first_weight_price":40.00
			},{
				"to_the":"江苏省",
				"first_weight_price":30.00
			}]
		}
		"""
	Then jobs能获取'顺丰'运费配置
		"""
		{
			"name" : "顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00,
			"special_area": [{
				"to_the":"北京",
				"first_weight_price":20.00,
				"added_weight_price":10.00
			},{
				"to_the":"上海, 重庆, 江苏",
				"first_weight_price":30.00,
				"added_weight_price":20.00
			}]
		}	
		"""
	And jobs能获取'圆通'运费配置
		"""
		{
			"name" : "圆通",
			"first_weight":1,
			"first_weight_price":10.0,
			"special_area": [{
				"to_the":"上海",
				"first_weight_price":40.00
			}, {
				"to_the":"江苏",
				"first_weight_price":30.00
			}]
		}	
		"""

