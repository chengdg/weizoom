/*
收货地址相关
*/

// 获得url中get查询参数
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



/*
weapp特有部分
*/

var getWoid = function(){
    var urlParm = document.location.search;
    if(urlParm.indexOf('woid=')>=0){
        return getParam('woid');
    } else if(urlParm.indexOf('webapp_owner_id=')>=0){
        return getParam('webapp_owner_id');
    }else{
        return $.cookie('current_token').split('____')[0]
    }
};


var urlFilter = function(url){
	return url.replace(/&/g, '%26')
};


var getRedirectUrlQueryString = function(){
    var woid = getWoid();
    // 入口是图文
    var sign = getParam('sign');
    if(sign == 'material_news'){
        return 'woid='+woid+'&module=mall&model=address&action=list&sign=material_news';
    }

    // 参数中包含
    var redirect_url_query_string = getParam('redirect_url_query_string');
    if(redirect_url_query_string){
        if(redirect_url_query_string.indexOf('user_center')>0){
            return 'woid='+woid+'&module=mall&model=address&action=list&sign=material_news';
        }
        return redirect_url_query_string;
    }

    // 当前页面的参数
    if(getParam('product_ids')||getParam('product_id')){
        return window.location.search;
    }

    // 前一页的参数
    strs = document.referrer.split("/?");
    if(strs.length>1){
        return strs[1]
    }

    return '#'
};

var JSAnalysis = function(analysis_name,content,woid){
    if(woid === undefined){
        woid = getWoid();
    }
    W.getApi().call({
    app: 'webapp',
    api: 'project_api/call',
    method: 'post',
    args: {
        woid: woid,
        module: 'mall',
        target_api: 'js_analysis/log',
        analysis_name: analysis_name,
        content: content
        }

    });
};


// webStorage可用性探针
var webStorageProbe = function () {
    var content = '';
    try{
        if (localStorage.mallWebStorageOk == 1) {
            return
        } else {
            localStorage.mallWebStorageOk = 1;
        }
    }catch(e){
        content += e;
    }
    try{
        sessionStorage.getItem('10086');
    }catch(e){
        content += '\n'+e
    }
    if (content != '') {
        JSAnalysis('webStorageProbe', content);
    }

};

/*
收货地址相关
*/

var shipInfosConfig = {
    'cacheTime': 1000*20
};


var initShipInofs = function(){
    var lastUpdate;
    function shipInfoAnalysis(){
        var s = sessionStorage;
        var content = '';
        // mallShipSessionFlag会话标志，辨别当前是第一次运行还是会话中的运行
        if(!s.mallShipSessionFlag){
            s.mallShipSessionFlag = 1
        }else{
            if(now.getTime() - lastUpdate > shipInfosConfig.cacheTime && lastUpdate > 0){
                content = '单个会话超过5分钟触发更新';
            }
        }
        if(content){
            alert(10086)
            JSAnalysis('shipInfoAnalysis',content)
        }
    }
    if(localStorage.ship_infos_updated_at){
        lastUpdate = localStorage.ship_infos_updated_at;
    }
    else {
        lastUpdate = 0
    }
    var now = new Date();
    var woid = getWoid();
    if (now.getTime() - lastUpdate > shipInfosConfig.cacheTime || $.cookie('current_token')!=localStorage.ship_infos_token) {
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'get',
            args: {
                woid: woid,
                module: 'mall',
                target_api: 'address/list'
            },
            success: function(data) {
                var ship_infos = data.ship_infos;
                var infos = {};
                for(var i in ship_infos){
                    infos[ship_infos[i].ship_id] = ship_infos[i]
                }
                localStorage.ship_infos=JSON.stringify(infos);
                localStorage.ship_infos_updated_at = new Date().getTime();
                localStorage.ship_infos_token = $.cookie('current_token');
                shipInfoAnalysis();
            },
            error: function(resp) {
            }
        });
    }
};
