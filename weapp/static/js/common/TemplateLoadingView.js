/*
Copyright (c) 2011-2012 Weizoom Inc
*/
W.TemplateLoadingView = function(options) {
	this.$el = $(options.el);
	this.url = options.url;
	this.args = options.args || {
		item_index: 0,
		count: 20
	};
	this.getTemplate = options.getTemplate || this.getTemplate;
	this.complete = options.complete || function() {};
	this.begin_load = options.begin_load || function() {};
	this.initialize();
}

W.TemplateLoadingView.prototype = {
	initialize: function() {
		this.render();
		this.tmplName = this.getTemplate();
		this.fetch();
		this.bindEvents();
	},
	
	bindEvents: function() {
		var _this = this;
		this.$el.delegate('a.tx_btnMore', 'click', function(event) {_this.fetch(event)});
	},
	
	fetch: function(event) {
		var _this = this;
		if(this.itemIndex) {
			this.args.item_index = this.itemIndex;
		}
		this.$el.alert({
			'info': '加载中...'
		})
		$.ajax({
			url: this.url,
			data: this.args,
			type: 'post',
			success: function(data) {
				_this.parse(data.data);
				if(data.code === 200) {
					xlog('fetch')
					_this.bindDisplayItems();
					_this.bindDisplayBtnMove();
				}
				else {
					_this.bindDisplayError();
				}
				_this.$el.alert({
					isShow: false
				})
			},
			error: function() {
				_this.bindDisplayError();
				_this.$el.alert({
					isShow: false
				})
			}
		})
	},
	
	bindDisplayBtnMove: function() {
		if(this.isHasMore) {
			if(!this.$more) {
				this.$el.append('<a href="javascript:void(0);" class="tx_btnMore" style="display:none;">更多...</a>');
				this.$more = this.$el.find('.tx_btnMore');
			}
			this.$more.show();
		}
		else {
			if(this.$more) {
				this.$more.hide();
			}
		}
	},
	
	render: function() {
		this.$el.html('<ul class="tx_content"></ul><div class="error-alert tx_error-alert" style="display:none;"><h3>没有相关信息</h3></div>');
		this.$content = this.$el.find('.tx_content');
		this.$error = this.$el.find('.tx_error-alert');
	},
	
	bindDisplayItems: function() {
		this.begin_load();
		var data = this.cacheData;
		if((!data.items || data.items && !data.items.length) && !this.hadLoading) {
			this.hadLoading = true;
			this.$error.show();
			return;
		}
		this.$content.append($.tmpl(this.tmplName, data));
		this.$content.find('a[data-role="button"]').buttonMarkup( "refresh" );
		this.complete();
	},
	
	bindDisplayError: function() {
		
	},
	
	parse: function(data) {
		this.cacheData = data;
		this.isHasMore = data.is_has_more;
		this.itemIndex = data.item_index;
	}
}