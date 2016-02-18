/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * News编辑器
 * @class
 */
ensureNS('W.view.weixin')
W.view.weixin.NewsView = Backbone.View.extend({
	el: '',

	events: {
		
	},

	getTemplate: function() {
		$('#weixin-news-view-tmpl-src').template('weixin-news-view-tmpl');
		return 'weixin-news-view-tmpl';
	},

	initialize: function(options) {
		this.material = options.material;
		this.template = this.getTemplate();
	},

	render: function() {
		return $.tmpl(this.template, {material: this.material});
	}
});