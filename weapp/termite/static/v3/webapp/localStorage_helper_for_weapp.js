var getWoid = function(){
    return getParam('woid')
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


var initShipInofs = function(){
    localStorage.removeItem('ship_infos');

    W.getApi().call({
        app: 'webapp',
        api: 'project_api/call',
        method: 'get',
        args: {
            woid: W.webappOwnerId,
            module: 'mall',
            target_api: 'address/list',
        },
        success: function(data) {
            ship_infos = data.ship_infos;
            infos = {};
            for(i in ship_infos){
                infos[ship_infos[i].ship_id] = ship_infos[i]
            }
            localStorage.ship_infos=JSON.stringify(infos);
        },
        error: function(resp) {
        }
    });
};

