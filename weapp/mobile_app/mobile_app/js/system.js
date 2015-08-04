
//全局工具对象

/**
 * 调用原生js选择器方法查找dom元素
 * @param {String} selector css选择器字符串，如'.xa-item input'
 * @param {DOM Object} context dom对象，作为选择器的上下文
 */
var W = function(selector, context){
	context = context || document;
	if(/\s?./.test(selector)){
		return context.querySelector(selector);
	}else if(/^#/.test(selector)){
		return document.getElementById(selector.substr(1));
	}else{
		return context.getElementsByTagName(selector);
	}
}

/**
 * 扩展对象 用src扩展target
 * @param target 目标
 * @param src 源
 * @returns target
 */
W.extendObj = function(target,src){
	for(var i in src){
		if(src.hasOwnProperty(i) && !target[i]){
			target[i] = src[i];
		}
	}
	return target;
};

W.extendObj(W, {
	active : false,	//W是否具有plus能力，默认没有，调用init后置为true
	timeout : 60*1000,
	/**
	 * 滚动到底部
	 * wrapCSS ： 承载内容的元素css定位，暂时只有id
	 */
	scrollToBottom : function(wrapCSS){
		var scrollHeight = document.getElementById(wrapCSS).clientHeight;
		document.body.scrollTop = scrollHeight;
	},

});



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
/**
 * 回调
 * @param {Object} callback
 */
W.next = new function(){
	if(!W.messageAPI){
		window.addEventListener('message', function(e){
			W.messageAPI = true;
			var source = e.source;
            if ((source === window || source === null) && e.data === 'chart_is_ready') {
                e.stopPropagation();
//	                callback();
            }
		}, false);
	}
	window.postMessage('chart_is_ready', '*');
	return function(fn){
		//TODO 未完成
	}
}

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