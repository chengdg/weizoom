/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * Customer备注的编辑对话框
 */
W.EditRemarkCustomerDialog = W.DropBox.extend({
	SUCCESS_EVENT: 'submit_success',

	getTemplate: function() {
		$('#dialog-view-edit-remark-customer-tmpl-src').template('edit-remark-customer-dialog-tmpl');
		return 'edit-remark-customer-dialog-tmpl';
	},

	events: _.extend({}, W.Dialog.prototype.events, {
		'click .tx_submit': 'submit'
	}),

	initializePrivate: function(options) {
		this.tmplName = this.getTemplate();
		this.typeTextCount = 300;
	},

	submit: function() {
		var value = this.$textarea.val();

		if(value.length > this.typeTextCount) {
			this.$('.errorHint').html('长度已超出'+this.typeTextCount+'字符范围');
			return;
		}

		this.$submit.bottonLoading({status:'show'});
		var _this = this;

		W.getApi().call({
			app: 'customer',
			api: 'customer_remark/update',
			method: 'post',
			args: {
				id: this.customerId,
				remark: value
			},
			success: _.bind(function() {
				this.trigger(this.SUCCESS_EVENT, {info: value});
				_this.$submit.bottonLoading({status:'hide'});
				this.close();
			}, this),
			error: function() {
				alert('备注修改失败！');
				_this.$submit.bottonLoading({status:'hide'});
			}
		});
	},

	showPrivate: function(options) {
		this.title = 'bianji'
		this.render(options);
	},

	render: function(options) {
		options = options || {};
		this.customerId = options.customerId
		this.$content.html($.tmpl(this.tmplName, options));
		this.$submit = this.$('.tx_submit');
		this.$textarea = this.$('.tx_textarea');
		var value = this.$textarea.val();
		this.$textarea.val('');
		this.$textarea.focus().val(value);
		this.setPosition('down-left');
	}
}, W.TextareaMethod);

/**
 * 获得CustomerCommentDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.getEditRemarkCustomerDialog = function(options) {
	options = options || {}
	options.width = options.width || 380;
	options.height = options.height || 100;

	var dialog = W.registry['EditRemarkCustomerDialog'];
	if (!dialog) {
		//创建dialog
		xlog('create W.EditRemarkCustomerDialog');
		dialog = new W.EditRemarkCustomerDialog(options);
		W.registry['EditRemarkCustomerDialog'] = dialog;
	}
	return dialog;
};