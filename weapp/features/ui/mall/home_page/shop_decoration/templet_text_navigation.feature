#_author_:师帅
Feature:自定义模块——【基础模块】文本导航-页面

@ui
Scenario:文本导航模块，编辑、删除、字数校验

	#添加文本导航'可单行显示'
		When jobs添加文本导航
		"""
			[{
				"navigation_name":"导航名称小于30可单行显示",
				"navigation_link":"导航链接"
			}]
		"""
		Then jobs展示区显示'文本导航'
		"""
		[{
			"navigation_name":"导航名称小于30可单行显示"
		}]
		"""

	#修改之前的文本导航'不可单行显示'
		When jobs修改文本导航
		"""
			[{
				"navigation_name":"导航名称小于30不可单行显示...............................",
				"navigation_link":"导航链接"
			}]
		"""

	#显示不完整，多出的字，用'...'代替
		Then jobs展示区显示'文本导航'
		"""
		[{
			"navigation_name":"导航名称小于30不可单行显示..."
		}]
		"""

	#文本导航标题字数超出30个字限制
		When jobs修改文本导航
		"""
			[{
				"navigation_name":"修改后导航名称大于30不可单行显示...................."
			}]
		"""
		Then jobs展示区显示'文本导航'
		"""
		[{
			"navigation_name":"修改后导航名称大于30不可单行显示..."
		}]
		"""
		And jobs编辑区提示错误信息'导航名称最多可输入30个字'

	#删除文本导航
    
		When jobs添加文本导航
		"""
			[{
				"navigation_name":"文本导航1",
				"navigation_link":"导航链接1"

			},{
				"navigation_name":"文本导航2",
				"navigation_link":"导航链接2"
			},{
				"navigation_name":"文本导航3",
				"navigation_link":"导航链接3"
			}]
		"""
		Then jobs展示区显示'文本导航'
		"""
	    [{
	    	"navigation_name":"修改后导航名称大于30不可单行显示..."
	    },{
	    	"navigation_name":"文本导航1"
	    },{
	    	"navigation_name":"文本导航2"
	    },{
	    	"navigation_name":"文本导航3"
	    }]
	    """
	    And jobs编辑区'编辑窗体'
	    """
	    [{
	    	"navigation_name":"修改后导航名称大于30不可单行显示..."
	    },{
	    	"navigation_name":"文本导航1"
	    },{
	    	"navigation_name":"文本导航2"
	    },{
	    	"navigation_name":"文本导航3"
	    }]
	    """

	    #删除一个文本导航
			When jobs删除文本导航
			"""
			[{
				"navigation_name":"文本导航1"
			}]
			"""
			Then jobs展示区显示'文本导航'
			"""
		    [{
		    	"navigation_name":"修改后导航名称大于30不可单行显示..."
		    },{
		    	"navigation_name":"文本导航2"
		    },{
		    	"navigation_name":"文本导航3"
		    }]
		    """
			And  jobs编辑区'编辑窗体'
			"""
			[{
		    	"navigation_name":"修改后导航名称大于30不可单行显示..."
		    },{
		    	"navigation_name":"文本导航2"
		    },{
		    	"navigation_name":"文本导航3"
		    }]
			"""

		#删除多个文本导航
			When jobs删除文本导航
			"""
			[{
		    	"navigation_name":"修改后导航名称大于30不可单行显示..."
		    },{
		    	"navigation_name":"文本导航3"
		    }]
			"""
			Then jobs展示区显示'文本导航'
			"""
		    [{
		    	"navigation_name":"文本导航2"
		    }]
		    """
		    And jobs编辑区'编辑窗体'
		    """
		    [{
		    	"navigation_name":"文本导航2"
		    }]
		    """

	    #当只有一个文本导航的时候，该文本导航不能被删除
		When jobs删除文本导航
		"""
		[{
			"navigation_name":"文本导航2"
		}]
		"""
		Then jobs不能删除文本导航