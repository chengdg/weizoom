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
		dialogTmpl: '#app-evaluate-viewParticipanceDataDialog-dialog-tmpl',
		resultTmpl: '#app-evaluate-viewParticipanceResultDialog-dialog-tmpl'
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
		this.product_review_id = options.product_review_id;
	},
	
	afterShow: function(options) {
		if (this.product_review_id) {
			W.getApi().call({
				app: 'apps/evaluate',
				resource: 'evaluate_review',
				scope: this,
				args: {
					id: this.product_review_id
				},
				success: function(data) {
					var context = data.items;
					console.log(context);
					var source = $("#app-evaluate-viewParticipanceResultDialog-dialog-tmpl").html();
					var template = Handlebars.compile(source);					
					var html = template(context);
					$('.xui-modal-content').html(html);
				},
				error: function(resp) {
					console.log('error');
				}
			})
		}

		var _this = this;
		$(".xa-modify").click(function(event){
            var $el = $(event.currentTarget);
            var status = $el.attr("data-status");
            W.getApi().call({
                app: 'apps/evaluate',
                resource: 'evaluate_review',
                method: 'post',
				scope: this,
                args: {
                    product_review_id: _this.product_review_id,
                    status: status
                },
                success: function(){
                    W.showHint('success', '操作成功');
					var table = $('[data-ui-role="advanced-table"]').data('view');
					table.reload();
                },
                error: function(){
                    W.showHint('error', '操作失败');
                }
            })
        })	
	},
	
	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});
