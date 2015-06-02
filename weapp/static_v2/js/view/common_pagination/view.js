/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 分页的View
 * @class isHasDetailedPage 是否是"详细分页"模块
 * @class isHasJumpPage 是否有"跳转页"功能
 * @event goto - 点击翻页链接时，触发，参数为page
 *
 * TODO: 处理query string
 */
ensureNS('W.view.common');
W.view.common.PaginationView = Backbone.View.extend({	
	getTemplate: function() {
		$('#pagination-view-box-tmpl-src').template('pagination-view-tmpl');
		return 'pagination-view-tmpl';
	},

	events: {
		'click a': 'gotoPage',
		'keypress .xa-gotoPage': 'gotoPage',
		'keyup input:text': 'onKeyUp'
	},
	
	isDisplayInfo: true,

	initialize: function(options) {
		this.$el = $(this.el);
		this.templateName = this.getTemplate();
		this.isHasDetailedPage = options.isHasDetailedPage || false;
		this.isHasJumpPage = options.isHasJumpPage || false;
		this.pageinfo = options.pageinfo || null;
		this.pageRegex = /page=(\d)+/g
	},

	render: function() {
		this.show()
	},

	setPageInfo: function(pageinfo) {
		this.pageinfo = pageinfo;
	},

	show: function() {
		if (!this.pageinfo) {
			this.pageinfo = {max_page:-1}
		}

		var context = _.extend({}, this.pageinfo, {
			isHasDetailedPage: this.isHasDetailedPage,
			isHasJumpPage: this.isHasJumpPage
		});
		var pagination_dom = $.tmpl(this.templateName, context);
		this.$el.html(pagination_dom).show();

		if (!this.pageinfo || (this.pageinfo && !this.pageinfo.has_next)) {
			if(this.isDisplayInfo) {
				//最后一页，显示提示信息
				this.$('#lastPageHint').show();
			}
		}
		return this;
	},

	hide: function() {
		this.$el.html('').hide();
	},
	
	/**
	 * 在页码框中输入的响应函数
	 */
	onKeyUp: function(event) {
		var $el = $(event.target);
		var value = $el.val();
		if(!Number(value)) {
			$el.val('');
		}
		else if(Number(value) > this.pageinfo.max_page) {
			$el.val(this.pageinfo.max_page);
		}
		else {
		
		}
		return false;
	},

	/**
	 * 翻页响应函数，在以下两种情况下会进行翻页
	 * 1. 点击页码链接
	 * 2. 点击Go按钮
	 */
	gotoPage: function(event) {
		var $el = $(event.target);
		var page;
		if(event.keyCode == 13) {
			page = $('input', this.el).val();
		}else {
			if($el.parents('li').hasClass('disabled')) {
				return false;
			}
			page = $(event.target).attr('page');
		}
		if(page.indexOf('#') === 0) {
			return false;
		}

		if (page) {
			this.trigger('goto', page);
		}

		event.stopPropagation();
		event.preventDefault();
	},

	/**
	 * 根据page获得新的target url
	 */
	getTargetUrl: function(page) {
		var url = window.location.href;
		var beg = url.indexOf('page=', 0);
		if (beg == -1) {
			if (url.indexOf('?') != -1) {
				return url + '&page=' + page;
			} else {
				return url + '?page=' + page;
			}
		} else {
			var target = 'page='+page;
			return url.replace(this.pageRegex, target);
		}
	} 
});