# FAQ #

### 问：如何rebuild本地环境？ ###

**答**：如下步骤操作（即执行rebuild.bat）
```
cd init_db 
mysql -u weapp --password=weizoom weapp < rebuild_database.sql
cd ..
python manage.py clean_mongo
python manage.py syncdb --noinput
cd init_db
mysql -u weapp --password=weizoom weapp < loc.sql
cd ..
python manage.py markettool2app
python manage.py init_permissions
```

### 问：如何更新线上数据库结构？ ###

**答**：执行如下操作：

1. 导出老版本数据库SQL
```
mysqldump -d -u xxx -p weapp > old.sql
```

2. 导出最新数据库SQL
```
rebuild.bat
mysqldump -d -u xxx -p weapp > new.sql
```

3. 比对新老数据库，生成更新SQL：
```
python manage.py sqldiff --old old.sql --new new.sql
```

4. 更新线上数据库：
```
mysql -u xxx -p weapp < migrate.sql
```

### 问：如何启动前端模拟器？ ###

**答**：执行如下步骤：

1. 启动 MySQL，Redis，MongoDB，Nginx。

2. 执行：
```
rebuild.bat
behave -kt @full_init
```

3. 启动 web server：
```
python manage.py runserver 0.0.0.0:8000
```

4. 打开浏览器： `http://dev.weapp.com/simulator/2/`  
> 说明：需要将 `dev.weapp.com` 映射到本机地址。即在 hosts 文件中加入：
> ```
> 127.0.0.1       dev.weapp.com
> ```


5. 用 **bill** 登录，选 **jobs**。


### 问：如何进行WAPI的BDD测试？ ###

**答**：执行
```
behave -k -t @wapi
```



# 集成测试 #

* [Weapp每日BDD测试](http://192.168.1.21:8081/jenkins/view/bdd/job/weapp_2.0_trunk_bdd_everyday/)

# 积分测试用例

```
水晶虾仁
	红色 S：10.00
	红色 M：9.10
热干面
	1.5
东坡肘子
	11.12
武昌鱼
	11.0

（水晶虾仁+热干面）满3减0.5	
水晶虾仁积分活动：普通会员 10%，金牌会员100%


东坡肘子 限时抢购1.1
东坡肘子积分活动：普通会员100%

武昌鱼 买赠
武昌鱼积分活动：普通会员100%

5积分=1元
用户50积分

1. 购买水晶虾仁（红色 M），5积分抵扣1元
1. 购买水晶虾仁（红色 M）+热干面，5积分抵扣1元
1. 购买水晶虾仁（红色 M），升级bill为金牌会员，50积分抵扣10元（积分金额等于商品金额）
1. 购买2个热干面，15积分抵扣3元（积分金额大于商品金额）

热干面积分活动：普通会员 100%
1. 购买水晶虾仁（红色 M）+热干面，13积分抵扣2.5元
1. 购买水晶虾仁（红色 M）+水晶虾仁（2个黄色 M）+热干面，22积分抵扣4.32元

1. 购买水晶虾仁（红色 M）+水晶虾仁（2个黄色 M）+热干面，2个东坡肘子，前者22积分抵扣4.32元，后者11积分抵扣2.2元

1. 购买水晶虾仁（红色 M）+水晶虾仁（2个黄色 M），2个武昌鱼
	1. 先抵扣水晶虾仁，水晶虾仁15积分抵扣2.82元，武昌鱼35积分抵扣7元
	2. 先抵扣武昌鱼，武昌鱼50积分抵扣10元
```

