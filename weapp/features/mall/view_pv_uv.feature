Feature: 访问PV与UV信息
	jobs通过管理系统能获得PV和UV信息

Background:
	Given jobs登录系统
	Given bill关注jobs的公众号
	Given tom关注jobs的公众号


@mall @mall.outline 
Scenario: 获得页面访问信息
	多个用户访问jobs的微站后，jobs能获得pv和uv信息

	When 微信用户批量访问jobs的webapp
		| date  	 | user     | 
		| 7天前      | -nokia   |
		| 7天前      | bill     |
		| 7天前      | tom      |
		| 7天前      | bill     |
		| 7天前      | tom      |
		| 6天前      | bill     |
		| 5天前      | bill     |
		| 5天前      | bill     |
		| 5天前      | bill     |
		| 5天前      | tom      |
		| 4天前      | bill     |
		| 4天前      | bill     |
		| 4天前      | tom      |
		| 4天前      | -tom1    |
		| 3天前      | tom      |
		| 3天前      | tom      |
		| 3天前      | tom      |
		| 1天前      | -nokia   |
		| 1天前      | tom      |
		| 1天前      | tom      |
		| 1天前      | bill     |
		| 今天       | bill     |
		| 今天       | bill     |
		| 今天       | bill     |
	Given jobs登录系统
	Then jobs能获取'7天'页面访问趋势
		| date  	 | pv | uv |
		| 7天前      | 5  | 3  |
		| 6天前      | 1  | 1  |
		| 5天前      | 4  | 2  |
		| 4天前      | 4  | 3  |
		| 3天前      | 3  | 1  |
		| 2天前      | 0  | 0  |
		| 1天前      | 4  | 3  |
		| 今天       | 3  | 1  |