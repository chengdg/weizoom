/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.survey');
W.dialog.app.survey.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),
	
	templates: {
		dialogTmpl: '#app-survey-viewParticipanceDataDialog-dialog-tmpl'
	},
	getTemplate: function() {
        return "<span style=\"font-size:16px;font-weight:bold;\">\"{{ webapp_user_name }}\"填写的内容</span>\
		    <table class=\"table table-bordered xb-noTdBorder xb-noBottom xb-noBorder mb10\" style=\"\
		    border-bottom:0;\">\
                {{#each items }}\
                    <tr>\
                        <td style=\"text-align:right;width:10%; padding-left: 30px;\">{{item_name}}：</td>\
                        <td style=\"text-align:left;\">{{item_value}}</td>\
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
				app: 'apps/survey',
				resource: 'survey_participance',
				scope: this,
				args: {
					id: this.activityId
				},
				success: function(data) {
					this.$dialog.find('.modal-body').text(data);
					var template = Handlebars.compile(that.getTemplate());
					$('.xui-app_survey-Dialog .modal-body').html(template(data));

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
