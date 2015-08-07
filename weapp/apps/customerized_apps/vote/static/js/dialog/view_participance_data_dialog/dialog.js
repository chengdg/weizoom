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
		dialogTmpl: '#app-vote-viewParticipanceDataDialog-dialog-tmpl'
	},

	getTemplate: function() {
        return "<h2>\"{{ webapp_user_name }}\"填写的内容</h2>\
		    <table class=\"table table-bordered\">\
                {{#each items }}\
                    <tr>\
                        <td>{{item_name}}</td>\
                        <td>{{item_value}}</td>\
                    </tr>\
                {{/each }}\
            </table>\
            "
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
					var template = Handlebars.compile(that.getTemplate());
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
