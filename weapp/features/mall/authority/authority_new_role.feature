#_author_:zhangsx

Feature:角色管理-新建、重命名、删除
 1.点击“+新建”创建角色，下方新增可编辑文本框，里面文字为“新角色”
 2.角色名称不能为空
 3.角色名称不允许重复
 4.角色上限数为30
 5.重命名和删除角色

Scenario:角色管理-新建
  Given jobs登录系统
  When jobs新建角色
    """
    [{"role_name":"角色1"}]
    """
  Then jobs展示区左侧显示角色信息
    """
    [{"role_name":"角色1"}]
    """
  And jobs展示区右侧显示权限设置信息
    """
    [{
       #"button":"添加权限",
       "permissions":
          [{
             "type":"无"，
             "values":
                 [{
                     "name":"暂未给此角色添加权限"
                 }]

          }]
    }]
    """
#角色名为空
  When jobs新建角色
  """
  [{"role_name":""}]
  """
  Then jobs提示错误信息'角色名不能为空'

#角色名重复
  When jobs新建角色
    """
    [{"role_name":"角色2"}]
    """
  Then jobs展示区左侧显示角色信息
    """
    [{"role_name":"角色2"}]
    """
  And jobs展示区右侧显示权限设置信息
    """
    [{
       #"button":"添加权限",
       "permissions":
          [{
             "type":"无"，
             "values":
                 [{
                     "name":"暂未给此角色添加权限"
                 }]
          }]
    }]
    """
  When jobs新建角色
    """
    [{"role_name":"角色2"}]
    """
  Then jobs提示错误信息'角色名不能重复'

#重命名角色
  When jobs已修改角色
  """
  [
    {"role_name":"角色02"},
    {"role_name":"角色01"}
  ]
  """
  Then jobs获取角色信息
  """
   [
    {"role_name":"角色02"},
    {"role_name":"角色01"}
  ]
  """ 

#角色数上限为30
  Given jobs已添加角色信息
    """
    [
       {"role_name":"角色30"},
       {"role_name":"角色29"},
       {"role_name":"角色28"},
       {"role_name":"角色27"},
       {"role_name":"角色26"},
       {"role_name":"角色25"},
       {"role_name":"角色24"},
       {"role_name":"角色23"},
       {"role_name":"角色22"},
       {"role_name":"角色21"},
       {"role_name":"角色20"},
       {"role_name":"角色19"},
       {"role_name":"角色18"},
       {"role_name":"角色17"},
       {"role_name":"角色16"},
       {"role_name":"角色15"},
       {"role_name":"角色14"},
       {"role_name":"角色13"},
       {"role_name":"角色12"},
       {"role_name":"角色11"},
       {"role_name":"角色10"},
       {"role_name":"角色09"},
       {"role_name":"角色08"},
       {"role_name":"角色07"},
       {"role_name":"角色06"},
       {"role_name":"角色05"},
       {"role_name":"角色04"},
       {"role_name":"角色03"},
       {"role_name":"角色02"},
       {"role_name":"角色01"}
    ]
   """
  When jobs新建角色
    """
    [{"role_name":"角色31"}]
    """
  Then jobs提示错误信息'已达到角色最大限额(30)'

#删除角色(设置权限和未设置权限删除时一样，均可直接删除)
  #删除角色-未设置权限
   When jobs删除角色'角色30'
   #Then jobs弹出提示信息'确认删除该角色？'
   And jobs确认删除
   Then jobs展示区左侧显示角色信息
     """
      [
       {"role_name":"角色29"},
       {"role_name":"角色28"},
       {"role_name":"角色27"},
       {"role_name":"角色26"},
       {"role_name":"角色25"},
       {"role_name":"角色24"},
       {"role_name":"角色23"},
       {"role_name":"角色22"},
       {"role_name":"角色21"},
       {"role_name":"角色20"},
       {"role_name":"角色19"},
       {"role_name":"角色18"},
       {"role_name":"角色17"},
       {"role_name":"角色16"},
       {"role_name":"角色15"},
       {"role_name":"角色14"},
       {"role_name":"角色13"},
       {"role_name":"角色12"},
       {"role_name":"角色11"},
       {"role_name":"角色10"},
       {"role_name":"角色09"},
       {"role_name":"角色08"},
       {"role_name":"角色07"},
       {"role_name":"角色06"},
       {"role_name":"角色05"},
       {"role_name":"角色04"},
       {"role_name":"角色03"},
       {"role_name":"角色02"},
       {"role_name":"角色01"}     
     ]
     """
  #删除角色-已设置权限
  Given jobs已设置角色权限信息
     """
     [{
        "role_name":"角色29",
       #"button":"修改权限",
       "permissions":

          [{
             "type":"商品管理"，
             "values":
                 [{
                     "name":"添加新商品",
                     "name":"添加在售商品"
                 }]
          }]
     }]
     """
   When jobs删除角色'角色29'
   #Then jobs弹出提示信息'确认删除该角色？'
   And jobs确认删除
   Then jobs展示区左侧显示角色信息
     """
      [
       {"role_name":"角色28"},
       {"role_name":"角色27"},
       {"role_name":"角色26"},
       {"role_name":"角色25"},
       {"role_name":"角色24"},
       {"role_name":"角色23"},
       {"role_name":"角色22"},
       {"role_name":"角色21"},
       {"role_name":"角色20"},
       {"role_name":"角色19"},
       {"role_name":"角色18"},
       {"role_name":"角色17"},
       {"role_name":"角色16"},
       {"role_name":"角色15"},
       {"role_name":"角色14"},
       {"role_name":"角色13"},
       {"role_name":"角色12"},
       {"role_name":"角色11"},
       {"role_name":"角色10"},
       {"role_name":"角色09"},
       {"role_name":"角色08"},
       {"role_name":"角色07"},
       {"role_name":"角色06"},
       {"role_name":"角色05"},
       {"role_name":"角色04"},
       {"role_name":"角色03"},
       {"role_name":"角色02"},
       {"role_name":"角色01"}
     ]
     """
  





 
