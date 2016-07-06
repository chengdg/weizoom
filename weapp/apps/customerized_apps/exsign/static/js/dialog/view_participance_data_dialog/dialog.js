/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.exsign');
W.dialog.app.exsign.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),

	templates: {
		dialogTmpl: '#app-exsign-viewParticipanceDataDialog-dialog-tmpl'
	},
	getTemplate: function() {
			$('#app-exsign-viewParticipanceDataDialog-dialog-tmpl').template('app-exsign-viewDetails-tmpl');
			return "app-exsign-viewParticipanceDataDialog-dialog-tmpl";
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
		this.memberId = options.memberId;
		this.belongTo = options.belongTo

		var _this = this;
		if (!_this.table) {
				_this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
		}
		_this.table.curPage = 1;
		_this.table.reload({"member_id": this.memberId,"belong_to": this.belongTo});
	},

	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});
