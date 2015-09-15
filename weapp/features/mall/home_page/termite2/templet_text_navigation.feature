#_author_:王丽
#_edit_:新新

Feature:自定义模块——【基础模块】文本导航-页面
	1、文本导航模块新建时，默认有一个文本导航
	2、‘导航名称’和‘链接到’都是必填的
	3、文本导航的‘导航名称’字数不能超过30字
	4、文本导航的‘导航名称’，自适应，可单行显示的单行显示，不可单行显示的用‘...’的方式单行显示
	5、新添加的文本导航，默认在最后一个，可以无限添加文本导航
	6、文本导航可以删除，最后必须保留一个，当只有一个文本导航的时候，该文本导航不能删除
	7、文本导航的链接，“从微站选择”当选择的链接的名称过长时用省略号截取显示，保证链接名称、修改、图标在同一行，不折行

Background:
	Given jobs登录系统
	And jobs已添加模块
		"""
		[	
			{"modle_name": "富文本"},
			{"modle_name": "商品"},
			{"modle_name": "商品列表"},
			{"modle_name": "图片广告"},
			{"modle_name": "公告"},
			{"modle_name": "标题"},
			{"modle_name": "文本导航"},
			{"modle_name": "图片导航"},
			{"modle_name": "辅助空白"},
			{"modle_name": "橱窗"}
		]
		"""

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

	#删除文本导航模块,弹出删除确认提示窗体
		When jobs删除文本导航模块
		Then jobs删除确认
		Then jobs展示区文本导航模块删除
		And  jobs编辑区编辑窗体关闭