/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * display_name编辑对话框
 */
W.EditDisplayNameDialog = W.DropBox.extend({
	SUCCESS_EVENT: 'submit_success',

	getTemplate: function() {
		$('#dialog-view-edit-statistic-display-name-tmpl-src').template('edit-statistic-display-name-dialog-tmpl');
		return 'edit-statistic-display-name-dialog-tmpl';
	},

	events: _.extend({}, W.Dialog.prototype.events, {
		'click .tx_submit': 'submit'
	}),

	initializePrivate: function(options) {
		this.tmplName = this.getTemplate();
		this.typeTextCount = 20;
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
			app: 'statistics',
			api: 'display_name/update',
			method: 'post',
			args: {
				id: _this.dataId,
				display_name: value,
				url: _this.url
			},
			success: _.bind(function() {
				this.trigger(this.SUCCESS_EVENT, {info: value});
				_this.$submit.bottonLoading({status:'hide'});
				this.close();
			}, this),
			error: function() {
				alert('修改失败！');
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
		this.dataId = options.dataId;
		this.url = options.url;
		this.$content.html($.tmpl(this.tmplName, options));
		this.$submit = this.$('.tx_submit');
		this.$textarea = this.$('.tx_textarea');
		var value = this.$textarea.val();
		this.$textarea.val('');
		this.$textarea.focus().val(value);
		this.setPosition('down-right');
	}
}, W.TextareaMethod);

/**
 * 获得EditDisplayNameDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.getEditDisplayNameDialog = function(options) {
	options = options || {}
	options.width = options.width || 320;
	options.height = options.height || 100;

	var dialog = W.registry['EditDisplayNameDialog'];
	if (!dialog) {
		//创建dialog
		xlog('create W.EditDisplayNameDialog');
		dialog = new W.EditDisplayNameDialog(options);
		W.registry['EditDisplayNameDialog'] = dialog;
	}
	return dialog;
};