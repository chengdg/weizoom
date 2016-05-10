/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.shvote');
W.dialog.app.shvote.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),
	
	templates: {
		dialogTmpl: '#app-shvote-viewParticipanceDataDialog-dialog-tmpl'
	},

	getTemplate: function() {
        $('#app-shvote-viewParticipanceDataDialog-dialog-tmpl').template('app-shvote-viewParticipanceResultDialog-dialog-tmpl');
        return "app-shvote-viewParticipanceDataDialog-dialog-tmpl";
    },

	onInitialize: function(options) {
		this.table = this.$('[data-ui-role="advanced-table"]').data('view');
	},
	
	beforeShow: function(options) {
		this.playerId = options.playerId;
        this.table.reset();
	},
	
	onShow: function(options) {
	},
	
	afterShow: function(options) {
		this.table.reload({"id": this.playerId});
	},
	
	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});
