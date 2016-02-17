#watcher:fengxuejing@weizoom.com,benchi@weizoom.com
Feature:配置邮费配置
	Jobs能通过管理系统为管理商城添加的"邮费配置"

@ui @ui-mall @ui-mall.postage
Scenario: 添加邮费配置
	Jobs添加多个"邮费配置"后
	1. 能获取倒序排列的邮费配置

	Given jobs登录系统:ui
	When jobs添加邮费配置:ui
		"""
		[{
               "added_weight" : 1,
               "added_weight_price" : 6,
               "first_weight" : 40,
               "first_weight_price" : 4,
               "is_enable_added_weight" : true,
               "name" : "圆通"
		},{
               "first_weight" : 41,
               "first_weight_price" : 5,
               "name" : "顺丰"
          }]	
		"""
	Then jobs能获取添加的邮费配置:ui
		"""
		[{
               "name" : "免运费",
               "content": ""
		}, {
               "name" : "圆通",
               "content": "首重40.0公斤 【4.0元】， 续重1公斤 【6元】"
		}, {
               "name" : "顺丰",
               "content": "首重41.0公斤 【5.0元】， 无续重"
        }]
		"""
	Given bill登录系统:ui
	Then bill能获取添加的邮费配置:ui
		"""
		[{
               "name" : "免运费",
               "content": ""
		}]
		"""
