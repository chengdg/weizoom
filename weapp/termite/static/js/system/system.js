/*
Copyright (c) 2011-2012 Weizoom Inc
*/
W = {
	registry: {},
	common: {model:{}},
	mall: {},
	question: {},
	util: {},
	debug: {},
	uirole: {}
}

W.registerUIRole = function(selector, initializer) {
	W.uirole[selector] = initializer;	
}
W.initUIRole = function() {
	console.log("in W.initUIRole()");
	if (W.design && W.design.isInFrame) {
		//当viper页面在frame中时，启动ui-role的初始化动作
		var task = new W.DelayedTask(function() {
			_.each(W.uirole, function(initializer, selector) {
				var $uiViews = $(selector);
				if ($uiViews.length > 0) {
					xlog("[W] init ui role: '" + selector + "'");
					$uiViews.each(initializer);
				}
			});

			var task2 = new W.DelayedTask(function() {
				W.Broadcaster.trigger('component:resize', this);	
			}, this);
			task2.delay(500);			
		}, this);
		task.delay(100);
	}
}
$(document).ready(function(event) {
	W.initUIRole();
});

function ensureNS(ns) {
	var items = ns.split('.');
	var obj = window;
	for (var i = 0; i < items.length; ++i) {
		var item = items[i];
        if (!obj.hasOwnProperty(item)) {
            obj[item] = {}
        }
        obj = obj[item];
	}
}

W.loadJSON = function(id) {
	var selector = '#__json-'+id;
	var text = $.trim($(selector).text());
	return $.parseJSON(text);
}

W.getImgOriginalSize = function(path, callback) {
	var img = new Image();
	img.src = path;
	var width = 0;
	var height = 0;
	if(img.complete){
		width = img.width;
		height = img.height;
		callback(width, height);
    	img = null;
	}else{
    	img.onload = function(){
    	    width = img.width;
			height = img.height;
			callback(width, height);
        	img = null;
        }
    };
}

W.debug.logBaselineTime = new Date().getTime();
function xlog(msg) {
	if (window.console) {
		var delta = new Date().getTime() - W.debug.logBaselineTime;
		window.console.info(delta + '>. ');
		window.console.info(msg);
	}
}

function xwarn(msg) {
	if (window.console) {
		var delta = new Date().getTime() - W.debug.logBaselineTime;
		window.console.warn(delta + '>. ');
		window.console.warn(msg);
	}
}

function xerror(msg) {
	if (window.console) {
		var delta = new Date().getTime() - W.debug.logBaselineTime;
		window.console.error(delta + '>. ');
		window.console.error(msg);
	}
}

/**
 * parseUrl: 简单解析url，解析结果为:
 *  baseUrl: ?部分之前的url
 *  query: query string的array
 */
function parseUrl(url) {
	var result = {baseUrl:'', query:{}}
	var pos = url.indexOf('?');
	if (pos === -1) {
		result.baseUrl = url;
		return result;
	}

	result.baseUrl = url.substring(0, pos);

	var queryString = url.substring(pos+1);
	var querys = queryString.split('&');
	var count = querys.length;
	for (var i = 0; i < count; ++i) {
		var query = querys[i];
		var items = query.split('=');
		result.query[items[0]] = items[1];
	}

	return result;
}
W.parseUrl = parseUrl;


/*按扭LOADING*/
$.fn.bottonLoading = function (options) {
	console.log("in $.fn.bottonLoading()");
	var el = this;
	if(!el.find('span.img').length) {
		el.prepend('<span class="img"></span>');
	}
	switch(options.status) {
	case 'show':
		el.addClass('submitting');
		el.attr('disabled', true);
		break;
	case 'hide':
		el.removeClass('submitting');
		el.attr('disabled', false);
		break;
	}
}

$.fn.serializeObject = function(options) {
	var $form = $(this);
	var datas = $form.serializeArray();
	var obj = {};
	for (var i = 0; i < datas.length; ++i) {
		var data = datas[i];
		obj[data.name] = data.value;
	}

	return obj;
}


/**
 * @class W.DelayedTask
 *
 */
W.DelayedTask = function(fn, scope, args) {
    var me = this,
        id,
        call = function() {
            clearInterval(id);
            id = null;
            fn.apply(scope, args || []);
        };

    /**
     * Cancels any pending timeout and queues a new one
     * @param {Number} delay The milliseconds to delay
     * @param {Function} newFn (optional) Overrides function passed to constructor
     * @param {Object} newScope (optional) Overrides scope passed to constructor. Remember that if no scope
     * is specified, <code>this</code> will refer to the browser window.
     * @param {Array} newArgs (optional) Overrides args passed to constructor
     */
    this.delay = function(delay, newFn, newScope, newArgs) {
        me.cancel();
        fn = newFn || fn;
        scope = newScope || scope;
        args = newArgs || args;
        id = setInterval(call, delay);
    };

    /**
     * Cancel the last queued timeout
     */
    this.cancel = function(){
        if (id) {
            clearInterval(id);
            id = null;
        }
    };
};


// 系统错误码
W.SUCCESS = 200;