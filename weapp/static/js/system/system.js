/*
Copyright (c) 2011-2012 Weizoom Inc
*/
(function() {
	var Dropdown = $.fn.dropdown.Constructor;
	var old_toggle = Dropdown.prototype.toggle;
	Dropdown.prototype.toggle = function(e) {
		$('.open').removeClass('open').find('input').val('');
		old_toggle.call(this, e);
		e.stopPropagation();
		e.preventDefault();
	}
	$('html').on('click.dropdown.data-api', function (e) {
		$('.open').find('input').val('');
		$('.open').find('li').show();
	})
})();

W = {
	registry: {},
	common: {model:{}},
	mall: {},
	material:{},
	marketTools:{},
	question: {},
	customerMenu:{},
	util: {},
	uirole: {},
	ueditor: {},
	member: {}
}

/**
 * W.registerUIRole: 每一个widget(view)，通过该函数向W中注册一个ui role，由W负责统一初始化
 *   selector: ui role的selector
 *   initializer: 初始化函数
 */
W.registerUIRole = function(selector, initializer) {
	W.uirole[selector] = initializer;	
}
W.createWidgets = function($node) {
	if (!$node) {
		$node = $;
	}
	_.each(W.uirole, function(initializer, selector) {
		var $uiViews = $node.find(selector);
		if ($uiViews.length > 0) {
			xlog("[W] init ui role: '" + selector + "'");
			$uiViews.each(function() {
				var $uiView = $(this);
				if ($uiView.data('view')) {
					return;
				} else {
					initializer.call(this);
				}
			});
		}
	});
}
$(document).ready(function(event) {
	_.each(W.uirole, function(initializer, selector) {
		var $uiViews = $(selector);
		if ($uiViews.length > 0) {
			xlog("[W] init ui role: '" + selector + "'");
			$uiViews.each(initializer);
		}
	});
});

W.loadJSON = function(id) {
	var text = $.trim($('#__json-'+id).text());
	return $.parseJSON(text);
}

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

function xlog(msg) {
	if (window.console) {
		window.console.info(msg);
	}
}

function xwarn(msg) {
	if (window.console) {
		window.console.warn(msg);
	}
}

function xerror(msg) {
	if (window.console) {
		window.console.error(msg);
	}
}

W.ueditor.handleSelectLinkTarget = function(callback) {
	W.dialog.showDialog('W.dialog.workbench.SelectLinkTargetDialog', {
		currentLinkTarget: '',
        success: function(data) {
            callback(data);
        }
	});
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
W.ERR_DUPLICATE_PATTERN = 601;