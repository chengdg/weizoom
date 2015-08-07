/*
Copyright (c) 2011-2012 Weizoom Inc
*/
__STRIPPER_TAG__
/**
 * 对话框
 */
ensureNS('W.dialog.app.{{app_name}}');
W.dialog.app.{{app_name}}.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),
	__STRIPPER_TAG__
	templates: {
		dialogTmpl: '#app-{{app_name}}-viewParticipanceDataDialog-dialog-tmpl'
	},
	__STRIPPER_TAG__
	onInitialize: function(options) {
	
	},
	__STRIPPER_TAG__
	beforeShow: function(options) {

	},
	__STRIPPER_TAG__
	onShow: function(options) {
		this.activityId = options.activityId;
	},
	__STRIPPER_TAG__
	afterShow: function(options) {
		if (this.activityId) {
			W.getApi().call({
				app: 'apps/{{app_name}}',
				resource: '{{participance_resource_name}}',
				scope: this,
				args: {
					id: this.activityId
				},
				success: function(data) {
					this.$dialog.find('.modal-body').text(data);
				},
				error: function(resp) {

				}
			})
		}
	},
	__STRIPPER_TAG__
	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});