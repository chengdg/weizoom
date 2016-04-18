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
		dialogTmpl: '#app-shvote-viewParticipanceDataDialog-dialog-tmpl',
		resultTmpl: '#app-shvote-viewParticipanceResultDialog-dialog-tmpl'
	},
	
	onInitialize: function(options) {
	},
	
	beforeShow: function(options) {
	},
	
	onShow: function(options) {
		this.playerId = options.playerId;
	},
	
	afterShow: function(options) {
		var that = this;
		if (this.playerId) {
			W.getApi().call({
				app: 'apps/shvote',
				resource: 'shvote_participance',
				scope: this,
				args: {
					id: this.playerId
				},
				success: function(data) {
					this.$dialog.find('.modal-body').text(data);
					var template = Handlebars.compile($(that.templates['resultTmpl']).html());
					$('.xui-app_shvote-Dialog .modal-body').html(template(data));
				},
				error: function(resp) {
					W.showHint('error', resp.errMsg);
				}
			})
		}
	},
	
	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});
