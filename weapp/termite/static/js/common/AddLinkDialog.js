/*
Copyright (c) 2011-2012 Weizoom Inc
*/

W.AddLinkDialog = W.Dialog.extend({
	SUBMIT_SUCCESS_EVENT: 'submit',
	
	events: _.extend({
		'click .tx_cancel': 'close',
		'click .tx_submit': 'onSubmit'
	}, W.Dialog.prototype.events),

	getTemplate: function() {
		$('#add-link-dialog-src').template('add-link-dialog-tmpl');
		return 'add-link-dialog-tmpl';
	},
	
	initializeDialog: function() {
		this.render();
		this.$('#contentInput').focus();
	},
	
	renderDialog: function() {
		var html = $.tmpl(this.getTemplate(), {});
		this.$contentEl.html(html);
	},
	
	showDialog: function(options) {
	},
	
	onSubmit: function() {
		if (!W.validate($('#editorView-addLinkDialog'), true)) {
			return;
		}
		var content = $.trim(this.$('#contentInput').val());
		var url = $.trim(this.$('#urlInput').val());
		this.link = '<a href="'+ url +'">' + content + '</a>';
		this.trigger(this.SUBMIT_SUCCESS_EVENT, {url: url, title: content});
	},
	
	afterClose: function() {
		this.unbind();
		this.$('#contentInput, #urlInput').val('');
	}
});

/**
 * 获得AddLinkDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.getAddLinkDialog = function(options) {
	var dialog = W.registry['AddLinkDialog'];
	if (!options) {
		options = {};
	}
	options.width = options.width || 450;
	options.height = options.height || 160;
	if (!dialog) {
		//创建dialog
		xlog('create W.AddLinkDialog');
		dialog = new W.AddLinkDialog(options);
		W.registry['AddLinkDialog'] = dialog;
	}
	return dialog;
};