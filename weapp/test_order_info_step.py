1、先访问gaia的order/orders接口，每500条访问一次，并把拿到的数据整理到一个文件中
2、查看线上最大的订单ID和最小的订单ID,修改update_order_info.py, 确认无误后，执行python update_order_info.py 更新数据库
3、把第一步拿到的数据整体复制粘贴到test_order_info_step.py中的 "s=[]" 的地方,给s赋值为拿到的数据
4、执行python  test_order_info_step.py,如果中间有不匹配的记录的话会报出以下信息：
      '========================'+条数
      '========failed  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'+订单ID
5、完成
