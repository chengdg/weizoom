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

function getWoid(){
    var urlParm = document.location.search;
    if(urlParm.indexOf('woid=')>=0){
        return getParam('woid');
    } else if(urlParm.indexOf('webapp_owner_id=')>=0){
        return getParam('webapp_owner_id');
    }else{
        var cookies = $.cookie('current_token');
        if(cookies){
            return $.cookie('current_token').split('____')[0];
        } else{
            return '';
        }

    }
};

function addFmt(){
    return '&fmt=' + getParam('fmt')
}

var urlFilter = function(url){
	return url.replace(/&/g, '%26')
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
