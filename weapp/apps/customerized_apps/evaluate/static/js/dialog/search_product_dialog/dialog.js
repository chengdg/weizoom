/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.evaluate');
W.dialog.app.evaluate.SearchProductDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),
	
	templates: {
		dialogTmpl: '#app-evaluate-searchProductDialog-dialog-tmpl'
	},
	
	onInitialize: function(options) {
		this.table = this.$('[data-ui-role="advanced-table"]').data('view');
	},
	
	beforeShow: function(options) {
		this.product_name = options.product_name;
		this.bar_code = options.bar_code;
		this.table.reset();
	},
	
	onShow: function(options) {
	},
	
	afterShow: function(options) {
		this.table.reload({"product_name": this.product_name,"bar_code": this.bar_code});
	},
	
	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});
