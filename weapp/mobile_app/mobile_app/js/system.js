
//全局工具对象
var W = {
	active : false,	//W是否具有plus能力，默认没有，调用init后置为true
	timeout : 60*1000
};

/**
 * 滚动到底部
 * wrapCSS ： 承载内容的元素css定位，暂时只有id
 */
W.scrollToBottom = function(wrapCSS){
	var scrollHeight = document.getElementById(wrapCSS).clientHeight;
	document.body.scrollTop = scrollHeight;
};

W.init = function(){
	W.active = true;
	/**跨域请求
 * url : 请求地址
 * successCallback : 成功后回调函数
 * 		其参数为响应的JSON对象
 * errorCallback : 失败后回调函数，没有参数
 */
	W.getJsonP = function(url,successCallback,errorCallback){
		if(!plus){
			return;
		}
		var callbackTimer = null;
		var xhr=new plus.net.XMLHttpRequest();
		xhr.onreadystatechange = function(){
			if(xhr.readyState == 4){
				if(xhr.status == 200){
					successCallback(JSON.parse(xhr.responseText));
				}else{
					if(typeof(errorCallback) == 'function')errorCallback();
				}
				window.clearTimeout(callbackTimer);
				callbackTimer = null;
			}
		}
		xhr.open("GET",url);
		xhr.send();
		callbackTimer = window.setTimeout(function(){
			xhr = W.abortJsonP(xhr);
			(typeof(errorCallback) == 'function')?(function(){
				errorCallback();
			}()) : (function(){
				mui.toast('网络错误，请重试...');
			}());
			callbackTimer = null;
		},W.timeout)
		return xhr;
	};
	/**
	 * 中止跨域请求
	 * xhr ： XHR对象
	 * return 返回null，以便回收xhr
	 */
	W.abortJsonP = function(xhr){
		if(!xhr)return null;
		xhr.abort();
		return null;
	};
};

function listenBackButton(){
		//返回键处理
		//处理逻辑：2秒内，连续两次按返回键，则退出应用；
		var first = null;
		mui.back = function() {
			//首次按键，提示‘再按一次退出应用’
			if (!first) {
				first = new Date().getTime();
				mui.toast('再按一次退出应用');
				setTimeout(function() {
					first = null;
				}, 1000);
			} else {
				if (new Date().getTime() - first < 2000) {
					//清除通知
					plus.push.clear();
					plus.runtime.quit();
				}
			}
		};
}

//检查更新
function login_check_new() {
		$.getJSON(HOST_URL + 'mobile_app/api/version/check/?version_id='+VERSION_ID+'&callback=?',
			function(data){
			if (data.code == 200){
				plus.storage.setItem('newVersion',data.version+'');
				plus.storage.setItem('is_update',data.is_update+'');
				}else{
					mui.toast("检查更新失败");
				}
			});
	}