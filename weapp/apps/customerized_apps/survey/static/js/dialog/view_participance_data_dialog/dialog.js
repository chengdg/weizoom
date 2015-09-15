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
		dialogTmpl: '#app-survey-viewParticipanceDataDialog-dialog-tmpl',
		resultTmpl: '#app-survey-viewParticipanceResultDialog-dialog-tmpl'
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
					var template = Handlebars.compile($(that.templates['resultTmpl']).html());
					$('.xui-app_survey-Dialog .modal-body').html(template(data));


					var att_name = data.att_url.item_name;
					var att_array = data.att_url.item_value;
					var att_val = "";
					for(var i=0;i<att_array.length;i++){
						att_val = att_val+'<img class=\"xa-uploadimg\" src=\"'+att_array[i]+'\">'
					}
					var att_html = '<tr><td>'+att_name+':</td><td>'+att_val+'</td></tr>';
					$('.modal-body .table.table-bordered').append(att_html);


					$('img.xa-uploadimg').click(function(){
						var that = this;
						$('.xa-uploadimg_box').append($(that).clone(true));
						$('.xa-uploadimg_box').removeClass('inactive').addClass('active');
						$('img.xa-uploadimg').unbind();
					});

					$('.xa-uploadimg_box .xa-close_btn').click(function(){
						$('.xa-uploadimg_box').removeClass('active');
					})

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
