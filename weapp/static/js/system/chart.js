/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/*
 * 封装对open flash chart的安装和初始化
 */

/**
 * 创建Single Chart对象
 * @param jqObj
 * @param jsonUrl
 * @param showSidebar
 */
W.SingleTitleChart = Backbone.View.extend({
	events: {
	
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.tmpl = this.getTemplate();

		this.id = options.id
		this.title = options.title;
		this.dataUrl = options.dataUrl.replace(/%26/g, '&'); //用于获取json数据的url
		this.width = options.width || 700;
		this.height = options.height || 250;
		this.args = options.args || {};

		//将url中的query string解析出来
		this.urlInfo = this.parseUrl(this.dataUrl);
		this.urlInfo.params = this.args;
	},

	render: function() {
		this.$el.html($.tmpl(this.tmpl, {
			id: this.id,
			title: this.title
		}));

		this.install(this.args);
	},

	getTemplate: function() {
		$('#single-title-chart-tmpl-src').template('single-title-chart-tmpl');
        return 'single-title-chart-tmpl';
	},
	
	switchTab: function(div, activeLink){
		div.find('li.active').removeClass('active');
		activeLink.parent().addClass('active');
	},

	/**
	 * 在页面中寻找flash对象
	 * @param movieName
	 */
	findSWF: function(movieName) {
		if (navigator.appName.indexOf("Microsoft") !== -1) {
			return window[movieName];
		}
		else {
			return document[movieName];
		}
	},

	
	/**
	 * 得到获取json数据的url
	 */
	getUrl: function(params) {
		// 构造完整的url
		var urlParams = this.urlInfo.params;
		//覆盖已有参数
		_.each(params, function(value, key) {
			urlParams[key] = value;
		});
		//构造url
		var queryString = '?';
		_.each(urlParams, function(value, key) {
			queryString += (key+'='+value+'&');
		});
		var url = this.urlInfo.url
		if (queryString.length > 1) {
			url += queryString
		}
		return url.substr(0, url.length-1);
	},
	
	/**
	 * 加载json数据
	 */
	loadJson: function(params){
		var url = this.getUrl(params);

		var chart = this;
		$.get(url, function(data){
			xlog('data is received for ' + chart.topId);
			if (jQuery.trim(data) == "{}") {
				//如果返回的是空json，则意味着没有数据，直接退出
				return;
			}
			
			data = JSON.stringify(data);
			var swf = chart.findSWF(chart.id + 'ChartFlash');
			swf.load(data);

			/*
			if (data.indexOf(chart.seperator) == -1) {
				var swf = findSWF(chart.id + 'ChartFlash');
				swf.load(data);
				chart.$(".chart_sidebar").html('');
			}
			else {
				var items = data.split(chart.seperator);
				if (2 != items.length) {
					alert('加载数据失败，请刷新页面');
					return;
				}
				else {
					var chartJson = items[0];
					var siteList = items[1];
					var swf = findSWF(chart.id + 'ChartFlash');
					swf.load(chartJson);
					if (chart.shouldShowSidebar) {
						chart.$(".chart_sidebar").html(siteList);
					}
				}
			}
			*/
		});
	},
	
	/**
	 * 将url解析为以下两部分:
	 * 1. path
	 * 2. query string
	 */
	parseUrl: function(url) {
		var pos = url.indexOf('?');
		var urlInfo = {};
		var items = url.split('?');
		urlInfo.url = items[0];
		urlInfo.params = {};
		if (items.length > 1) {
			items = items[1].split('&');
			var count = items.length;
			for (var i = 0; i < count; ++i) {
				var item = items[i];
				var kv = item.split('=');
				urlInfo.params[kv[0]] = kv[1];
			}
		}
		return urlInfo;
	},
	
	// init: function(args){
	// 	var chart = this;
	// 	this.jqObj.find('.chartTitle a').each(function(event) {
	// 		$(this).click(function(event){
	// 			try {
	// 				var link = $(this);
	// 				var ul = link.parent().parent();
	// 				chart.switchTab(ul, link);
					
	// 				chart.loadJson({days: link.attr('href')});
	// 			}
	// 			catch(e) {
	// 				xlog(e);
	// 			}
	// 			event.stopPropagation();
	// 			event.preventDefault();
	// 		});
	// 	});

	// 	//从jsonUrl中解析出url
	// 	this.urlInfo = this.parseUrl(this.jsonUrl);
	// 	this.urlInfo.params = args;
	// },
	
	install: function(args){
		xlog('install single title chart for ' + this.id);

		var dataUrl =  this.getUrl(args).replace(/\&/g, '%26');

		swfobject.embedSWF("/static/open-flash-chart.swf", 
			this.id + "ChartFlash", 
			this.width, 
			this.height, 
			"9.0.0", 
			"expressInstall.swf", {
				"data-file": dataUrl
			}, {
				wmode: 'transparent'
			}
		);
	}
});