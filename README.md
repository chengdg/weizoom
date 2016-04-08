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
1. 执行 `rebuild.bat`，初始化数据库
1. 启动 `start_bundle_server.bat`
1. 启动 `start_service.bat | bunyan`
1. 访问 `http://127.0.0.1:4180/account/login/`
1. 以 `manager:test`登陆系统