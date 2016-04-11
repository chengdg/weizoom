**weizoom_card**

# FAQ

### 如何准备NodeJS环境？ ###

如果没有安装cnpm，安装cnpm：
```
npm install -g cnpm --registry=https://registry.npm.taobao.org 
```

安装必要的包：
```
cnpm install supervisor -g
cnpm install -g bunyan
cnpm install
```

### 如何在本地开发调试？ ###

答：初次搭建环境，按如下步骤：
1. 在mysql中创建`card`数据库: `create database card`;
1. 将`card`数据库授权给`card`用户：`grant all on card.* to 'card'@localhost identified by 'weizoom'`
1. 增加 `hosts 127.0.0.1 db.card.com`
1. 执行 `rebuild.bat`，初始化数据库
1. 启动 `start_bundle_server.bat`
1. 启动 `start_service.bat | bunyan`
1. 访问 `http://127.0.0.1:4180/account/login/`
1. 以 `manager:test`登陆系统

### 如何进行BDD测试？ ###

答：初次搭建环境，按如下步骤：
1. bdd相关文件放在features目录下：每一个app的feature文件放在独立目录下，如card，所有的step实现放在steps目录下，数据库清理文件放在clean目录下。
1. 运行 behave -k 测试所有；运行behave -k -t @wip 测试wip标签（安装pip install behave）