#watcher:fengxuejing@weizoom.com,benchi@weizoom.com

# @func:market_tools.tools.activity.views.list_activity_members
# Feature: Get Joined Activity Members
	# Jobs能通过管理系统获取己参加"活动报名"的人员列表
# 	
# Background:
	# Given jobs登录系统
	# And jobs已添加'活动报名'
		# """
		# [{
			# "name": "活动1",
			# "is_non_member": "不可参加",
			# "is_enable_offline_sign": "启用",
		# },{
			# "name": "活动2",
			# "is_non_member": "可参加",
			# "is_enable_offline_sign": "不启用",
		# }]
		# """
	# And 己关注jobs的会员
	    # """
	    # [{
	        # "name": "xxx",
	    # }]
	    # """
# 
# @weapp.market_tools.activity
# Scenario: 获取己参加"活动报名"下的用户列表
	# Jobs添加"活动报名"后，能获取参加该活动下的人员列表,列表按报名顺序倒序排列
# 
	# Given jobs登录系统
	# When 'xxx'参加'活动1'
	# Then jobs获取参加'活动1'人员列表
	    # """
	    # [{
	    	# "name": "xxx"
	    # }]
	    # """
	# When 'xxx'参加'活动2'
	# Then jobs获取参加'活动2'人员列表
	    # """
	    # [{
	    	# "name": "xxx"
	    # }]
	    # """	
	# When 非会员'yyy'参加'活动2'
	# Then jobs获取参加'活动2'人员列表
	    # """
	    # [{
	    	# "name": "xxx",
	    # },{
	    	# "name": "yyy",
	    # }]
	    # """	
# 		
