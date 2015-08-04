/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/*
*册除下拉框
*/
W.ItemDeleteView = W.DropBox.extend({
	SUBMIT_EVENT: 'submit',
	
	CLOSE_EVENT: 'close',
	
	isArrow: true,
	
	isTitle: false,
	
	events:{
		'click .tx_submit': 'submit',
		'click .tx_cancel': 'close'
	},
	
	getTemplate: function() {
		return '<dl class="itemDeleteView"><dt class="tx_info"></dt>'
				+'<dd><button type="button" class="tx_submit btn btn-success">确定</button> '
				+'<button type="button" class="tx_cancel btn">取消</button>'
				+'</dd></dl>';
	},

	initializePrivate: function(options) {
		this.$el = $(this.el);
		this.render();
	},
	
	render: function() {
		html = this.getTemplate();
		this.$content.html(html);
	},
	
	showPrivate: function(options) {
		this.$('.tx_info').html(options.info);
		this.$('.tx_submit').focus();
		this.setPosition();
	},
	
	submit: function() {
		this.$('.tx_submit').bottonLoading({status:'show'});
		this.trigger(this.SUBMIT_EVENT);
	},
	
	closePrivate: function() {
		this.$('.tx_submit').bottonLoading({status:'hide'});
		this.trigger(this.CLOSE_EVENT);
	}
});

/**
 * 获得ItemDeleteView的单例实例
 */
W.getItemDeleteView = function(options) {
	var dialog = W.registry['ItemDeleteView'];
	if (!dialog) {
		//创建dialog
		xlog('create ItemDeleteView');
		dialog = new W.ItemDeleteView(options);
		W.registry['ItemDeleteView'] = dialog;
	}
	//dialog.unbind(dialog.SUBMIT_EVENT);
	return dialog;
};