/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.sign');
W.dialog.app.sign.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),

	templates: {
		dialogTmpl: '#app-sign-viewParticipanceDataDialog-dialog-tmpl'
	},
	getTemplate: function() {
			$('#app-sign-viewParticipanceDataDialog-dialog-tmpl').template('app-sign-viewDetails-tmpl');
			return "app-sign-viewParticipanceDataDialog-dialog-tmpl";
	},

	onInitialize: function(options) {
		this.table = this.$('[data-ui-role="advanced-table"]').data('view');
	},
	beforeShow: function(options) {
		this.memberId = options.memberId;
		this.belongTo = options.belongTo;
		this.table.reset();
	},

	onShow: function(options) {
	},

	afterShow: function(options) {
		this.table.reload({"member_id": this.memberId,"belong_to": this.belongTo});
	},

	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});
