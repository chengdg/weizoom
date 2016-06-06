/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.evaluate');
W.dialog.app.evaluate.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),
	
	templates: {
		dialogTmpl: '#app-evaluate-viewParticipanceDataDialog-dialog-tmpl'
	},

	onInitialize: function(options) {
		//创建富文本编辑器
        var editor = new W.view.common.RichTextEditor({
            el: 'textarea',
            type: 'text',
            width:837,
            height:100,
            pasteplain: true
        });
		editor.render();
	},
	
	beforeShow: function(options) {
	},
	
	onShow: function(options) {
		this.activityId = options.activityId;
	},
	
	afterShow: function(options) {	
		if (this.activityId) {
			W.getApi().call({
				app: 'apps/evaluate',
				resource: 'evaluate_participance',
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
	
	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});
