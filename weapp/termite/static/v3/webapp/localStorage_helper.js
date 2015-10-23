
// 获得get查询参数
var getParam = function (name) {
    var search = document.location.search;
    var pattern = new RegExp("[?&]" + name + "\=([^&]+)", "g");
    var matcher = pattern.exec(search);
    var items = null;
    if (null != matcher) {
        try {
            items = decodeURIComponent(decodeURIComponent(matcher[1]));
        } catch (e) {
            try {
                items = decodeURIComponent(matcher[1]);
            } catch (e) {
                items = matcher[1];
            }
        }
    }
    return items;
};

// 深拷贝JSON
var deepCopyJSON = function(obj){
    return JSON.parse(JSON.stringify(obj));
};

// 创建createdAt属性，为1970 年 1 月 1 日至今的毫秒数
var setCreatedAt = function(obj){
    now = new Date();
    obj.createdAt = now.getTime();
    return obj;
};
//var getLocalStorageJsonList = function (name) {
//    var list = localStorage.name;
//    list = list.split('|');
//
//};


