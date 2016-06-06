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
		// if (this.product_review_id) {
		// 	W.getApi().call({
		// 		app: 'apps/evaluates',
		// 		resource: 'evaluates',
		// 		scope: this,
		// 		args: {
		// 			id: this.product_review_id
		// 		},
		// 		success: function(data) {
					
		// 		},
		// 		error: function(resp) {
		// 		}
		// 	})
		// }
		var source = $("#app-evaluate-viewParticipanceResultDialog-dialog-tmpl").html();
		var template = Handlebars.compile(source);
		var context = {datetime: "2016/03/03",content: "This is my first post!",product_name:"PS4"};
		var html = template(context);
		$('.xui-modal-content').html(html);

		$(".xa-modify").click(function(event){
            var $el = $(event.currentTarget);
            var status = $el.attr("data-status");
            W.getApi().call({
                app: 'apps/evaluate',
                resource: 'evaluate_participance',
                method: 'post',
                args: {
                    product_review_id: this.product_review_id,
                    status: status
                },
                success: function(){
                    W.showHint('success', '操作成功');
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
