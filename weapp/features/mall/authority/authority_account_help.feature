#_author_:zhangsx

Feature:权限管理-账号帮助
  1.账号帮助页为用户提供如何进行权限管理的简略引导说明
  2.操作步骤：3个自上而下TAB选项卡，引导用户如何快捷创建子账号

#按顺序切换操作步骤TAB选项卡（第一步、第二步、第三步）
Scenario:1 权限管理-账号帮助
    用户能在账号帮助页查看快捷创建子账号的引导说明
    Given jobs登录系统
    When jobs访问账号帮助
    Then jobs展示区左侧焦点定位在第'一'个选项卡第'一'步
    And jobs展示区右侧显示第'一'步对应图标和描述信息
    """
    [{
        "icon_id":1,
        "introduction":
        [{
          "step_name":"设置角色",
          "description":"根据后台使用者职责，配置拥有不同权限的角色，使网站后台管理工作安全，高效！"
        }]
    }]
    """
    When jobs切换第'二'个选项卡第'二'步
    Then jobs展示区左侧焦点定位在第'二'个选项卡第'二'步
    And jobs展示区右侧显示第'二'步对应图标和描述信息
      """
      [{
        "icon_id":2,
        "introduction":
        [{
          "step_name":"创建部门",
          "description":"创建部门，使组织架构一目了然！"
        }]
      }]
      """
    When jobs切换第'三'个选项卡第'三'步
    Then jobs展示区左侧焦点定位在第'三'个选项卡第'三'步
    And jobs展示区右侧显示第'三'步对应图标和描述信息
      """
      [{
        "icon_id":3,
        "introduction":
        [{
          "step_name":"员工账号",
          "description":"为每个部门录入员工信息，同事为员工创建专属子账号，一人一号掌控员工权限和操作记录。"
        }]
      }]
      """

#向下切换操作步骤TAB选项卡，第一步切换至第三步
Scenario:2 向下切换操作步骤TAB选项卡，第一步切换至第三步
    Give jobs登录系统
    And jobs展示区左侧焦点已定位在第'一'个选项卡第'一'步
    And jobs展示区右侧已显示第'一'步对应图标和描述信息
      """
      [{
        "icon_id":1,
        "introduction":
        [{
          "step_name":"设置角色",
          "description":"根据后台使用者职责，配置拥有不同权限的角色，使网站后台管理工作安全，高效！"
        }]
      }]
      """
    When jobs切换第'三'个选项卡第'三'步
    Then jobs展示区左侧焦点定位在第'三'个选项卡第'三'步
    And jobs展示区右侧显示第'三'步对应图标和描述信息
      """
      [{
        "icon_id":3,
        "introduction":
        [{
          "step_name":"员工账号",
          "description":"为每个部门录入员工信息，同事为员工创建专属子账号，一人一号掌控员工权限和操作记录。"
        }]
      }]
      """

#向上切换操作步骤TAB选项卡，第三步切换至第二步
Scenario:3 向上切换操作步骤TAB选项卡，第三步切换至第二步
    Give jobs登录系统
    And jobs展示区左侧焦点已定位在第'三'个选项卡第'三'步
    And jobs展示区右侧已显示第'三'步对应图标和描述信息
      """
      [{
        "icon_id":3,
        "introduction":[{
        "step_name":"员工账号",
        "description":"为每个部门录入员工信息，同事为员工创建专属子账号，一人
        一号掌控员工权限和操作记录。"
        }]
      }]
      """
    When jobs切换第'二'个选项卡'第二步'
    Then jobs展示区左侧焦点定位在第'二'个选项卡'第二步'
    And jobs展示区右侧显示第'二'步对应图标和描述信息
      """
      [{
        "icon_id":2,
        "introduction":
        [{
          "step_name":"创建部门",
          "description":"创建部门，使组织架构一目了然！"
        }]
      }]
      """

#向上切换操作步骤TAB选项卡，第三步切换至第一步
Scenario:4 向上切换操作步骤TAB选项卡，第三步切换至第一步
    Give jobs登录系统
    And jobs展示区左侧焦点已定位在第'三'个选项卡第'三'步
    And jobs展示区右侧已显示第'三'步对应图标和描述信息
      """
      [{
        "icon_id":3,
        "introduction":
        [{
          "step_name":"员工账号",
          "description":"为每个部门录入员工信息，同事为员工创建专属子账号，一人一号掌控员工权限和操作记录。"
        }]
      }]
      """
    When jobs切换第'一'个选项卡第'一'步
    Then jobs展示区左侧焦点定位在第'一'个选项卡第'一'步
    And jobs展示区右侧显示第'一'步对应图标和描述信息
      """
      [{
        "icon_id":1,
        "introduction":
        [{
          "step_name":"设置角色",
          "description":"根据后台使用者职责，配置拥有不同权限的角色，使网站后台管理工作安全，高效！"
        }]
      }]
      """
