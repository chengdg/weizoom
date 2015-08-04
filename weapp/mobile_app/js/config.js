/**
 * 配置文件
*/

// 数据来源地址
var HOST_URL = "http://weapp.weizoom.com/";

var USER_ID = 0;

//版本号
var VERSION_ID = '1.6';

//消息自动更新的频率
var message_auto_update_time = 10 * 1000;

//消息列表的当前页
var message_list_curr_page = 1;
var message_count_per_page = 10;

//消息历史的当前页面
var message_history_curr_page = 1;
var message_history_per_page = 10;

//订单列表每页订单数
var order_count_curr_page = 1;
var order_count_per_page = 10;

//最大加载页数
var max_message_list_loaded_count = 10;
var max_message_history_loaded_count = 10;
var max_order_list_loaded_count = 10;

var ACCOUNTS = [{'id':216,'name':'微众商城'},{'id':185,'name':'纽仕兰'},{'id':102,'name':'米奇尔'}];
var isManager = false;
var isSystemMenager = false;
// 系统管理员用户名与密码，需与get_login方法内校验一致
var SYSTEMUSERNAME = 'system';
var STSTEMPW = 'weizoom';

$.os.android = false;
$.os.androidICS = false;
$.os.ios = false;
$.os.ios7 = false;

$.ui.slideSideMenu = false;


//统计每页数
var page = 1;
var count_per_page = 10;
