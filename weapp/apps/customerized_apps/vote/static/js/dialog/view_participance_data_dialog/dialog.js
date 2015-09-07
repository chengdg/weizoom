/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.vote');
W.dialog.app.vote.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),
	
	templates: {
		dialogTmpl: '#app-vote-viewParticipanceDataDialog-dialog-tmpl',
		resultTmpl: '#app-vote-viewParticipanceResultDialog-dialog-tmpl'
	},
	onInitialize: function(options) {
	},
	
	beforeShow: function(options) {
	},
	
	onShow: function(options) {
		this.activityId = options.activityId;
	},
	
	afterShow: function(options) {
		var that = this;
		if (this.activityId) {
			W.getApi().call({
				app: 'apps/vote',
				resource: 'vote_participance',
				scope: this,
				args: {
					id: this.activityId
				},
				success: function(data) {
					this.$dialog.find('.modal-body').text(data);
					var template = Handlebars.compile($(that.templates['resultTmpl']).html());
					$('.xui-app_vote-Dialog .modal-body').html(template(data));
				},
				error: function(resp) {
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
