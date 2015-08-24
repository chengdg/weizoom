#_author_:zhangsx

Feature:员工管理-新建部门 、重命名、删除
"""
1.部门名称不能为空
2.部门名称不允许重复
3.重命名部门
4.删除部门：
a.部门下无员工时允许删除
b.部门下存在员工时不允许删除，只有将员工全部删除后方可删除
"""

Scenario:1新建部门
    Given jobs登录系统
    When jobs新建部门
        """
        [{
            "department_name":"部门a"
        }]
        """
    Then jobs展示区左侧显示部门信息
        """
        [{
            "department_name":"部门a"
        }]
        """
    And jobs展示区右侧显示部门的员工信息
        """
        [{
            "reminder":"还没有员工，请添加",
            "employees":
        [{
            "account_name":"",
            "employee_name":"",
            "deparment_name":""，
            "roles":"",
            "is_active":""
        }]
        }]
        """

#部门名为空
    When jobs新建部门
        """
        [{
        "department_name":""
        }]
        """
    
    Then jobs提示错误信息'部门名不能为空'

#部门名重复
    When jobs新建部门
        """
        [{
            "department_name":"部门a"
        }]
        """
 Then jobs提示错误信息'部门名不能重复'

#重命名
    When jobs修改部门
        """
        [{
            "department_name":"部门aa"
        }]
        """
    Then jobs展示区左侧显示部门信息
        """
        [{
            "department_name":"部门aa"
        }]
        """
    And jobs展示区右侧显示部门的员工信息
        """
        [{
            "reminder":"还没有员工，请添加",
            "employees":
        [{
            "account_name":"",
            "employee_name":"",
            "department_name":"",
            "roles":"",
            "is_active":""
        }]
        }]
        """

#删除
    #验证无员工删除部门
        When jobs新建部门
            """
            [{
                "department_name":"部门aa2"
            }]
            """
        Then jobs展示区左侧显示部门信息
            """
            [
                {"department_name":"部门aa2"},
                {"department_name":"部门aa"},
            ]
            """
        When jobs删除部门'部门aa'
        #Then jobs弹出提示信息
        And jobs确认删除
        Then jobs展示区左侧显示部门信息
            """
            [{
                "department_name":"部门aa2"
            }]
            """
        #验证有员工删除部门
        Given jobs已添加角色信息
            """
            [{
                {"role_name":"商品"},
                {"role_name":"促销"},
                {"role_name":"配置"},
                {"role_name":"权限"}
            }]
            """
        And jobs已新建员工
            """
            [{
                "reminder":"",
                "employees":
                [{
                    "account_name":"ceshi03",
                    "employee_name":"张03",
                    "department_name":"部门aa2",
                    "roles":"商品",
                    "is_active":"停用"
                },{
                    "account_name":"ceshi02",
                    "employee_name":"张02",
                    "department_name":"部门aa2",
                    "roles":"促销",
                    "is_active":"停用"
                },{
                    "account_name":"ceshi01",
                    "employee_name":"张01",
                    "department_name":"部门aa2",
                    "roles":"配置",
                    "is_active":"停用"
                }]
            }]
            """
        When jobs删除部门'部门aa2'
        Then jobs提示错误信息'请将部门内所有员工删除后再删除部门'
        When jobs已删除员工'ceshi03,ceshi02,ceshi01'
        Then jobs展示区左侧显示部门信息
        """
        [{
            "department_name":"部门aa2"
        }]
        """
        And jobs展示区右侧显示部门的员工信息
        """
        [{
            "reminder":"还没有员工，请添加",
            "employees":
            [{
                "account_name":"",
                "employee_name":"",
                "department_name":"",
                "roles":"",
                "is_active":""
            }]
        }]
        """
        When jobs删除部门'部门aa2'
        #Then jobs弹出提示信息
        And jobs确认删除
        Then jobs展示区左侧显示部门信息
        """
        [{
            "department_name":""
        }]
        """


