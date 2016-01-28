/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.red_packet');
W.dialog.app.red_packet.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),
	
	templates: {
		dialogTmpl: '#app-red_packet-viewParticipanceDataDialog-dialog-tmpl'
	},
	
	onInitialize: function(options) {
	},
	
	beforeShow: function(options) {
	},
	
	onShow: function(options) {
		this.activityId = options.activityId;
	},
	
	afterShow: function(options) {
		if (this.activityId) {
			W.getApi().call({
				app: 'apps/red_packet',
				resource: 'red_packet_participance',
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

W.dialog.app.red_packet.ViewGrantResultDialog = W.dialog.Dialog.extend({
	events: _.extend({}, W.dialog.Dialog.prototype.events),

	templates: {
		dialogTmpl: '#app-red_packet-grant-result-dialog-tmpl'
	},

	onShow: function(options) {
		this.data = options.data;
	},

	afterShow: function(options) {
		var data = this.data;
		var html_str = "";
		for(var m_id in data){
			html_str += "<p>"+m_id+": "+data[m_id]+"</p>"
		}
		this.$dialog.find('.modal-body').html(html_str);
	}
});