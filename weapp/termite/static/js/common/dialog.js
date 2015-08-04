/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */

W.Dialog = Backbone.View.extend({
	tagName: 'div',

	events: {
		'click .close': 'close'
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.isDialogCreated = false; //created标识dialog是否已经创建，该属性由派生类修改
		this.$el.addClass('dialog-bg').prepend(W.Dialog.HEAD).append(W.Dialog.TAIL);
		$('body').append(this.$el);
		this.$contentEl = this.$('.dialog-content');
		this.initializeDialog(options);
	},

	reset: function(options) {
		_.extend(this.options, options);
	},

	initializeDialog: function(options){},

	render: function(options) { this.renderDialog(options); },

	renderDialog: function(options) {},

	show: function(options) {
		var width = $('body').width()-2;
		var height = $('body').innerHeight()-2;
		var windowHeight = $(window).height()-2;
		if(height < windowHeight) {
			height = windowHeight;
		}

		var scrollTop = $(document).scrollTop();
		var dialogTop = scrollTop + 150;

		var overlay = $('#overlay');
		overlay.css('width', width+'px').css('height', height+'px').css('display', 'block');

		var dialog = $('#'+this.id);

		var dialogOptions = this.options;
		var title = (options && options.title) ? options.title : null
					|| (dialogOptions && dialogOptions.title) ? dialogOptions.title : null
					|| '';
		this.setTitle(title);
		
		var dialogLeft = (width-dialogOptions.width)/2;

		this.$el.css('left', dialogLeft)
				.css('top', dialogTop+'px')
				.css('width', dialogOptions.width)
				.css('_height', dialogOptions.height)
				.css('display', 'block');
				
		this.$('.boxBorder').css('min-height', dialogOptions.height)

		this.showDialog(options);
		W.ACTIVE_DIALOG = this;
	},

	showDialog: function(options) {},

	setTitle: function(title) {
		this.$('.dialog-title .title').html(title);
	},

	close: function(options) {
		this.$el.hide();
		$('#overlay').hide();
		W.ACTIVE_DIALOG = null;
		
		this.afterClose = this.afterClose || this.options.afterClose;
		if (this.afterClose) {
			this.afterClose(options);
		}
	}
});

W.Dialog.HEAD =
'<div class="boxBorder">\
<div class="dialog-title">\
	<div class="title"></div>\
</div>\
<div class="dialog-content"><div class="tc">加载数据...</div></div>\
</div>';

W.Dialog.TAIL =
'<div class="close-zone">\
	<button type="button" class="close">×</button>\
</div>';


/**
 * 使用iframe显示内容的Dialog
 */
W.ExternalDialog = W.Dialog.extend({
	initialize: function() {
		W.Dialog.prototype.initialize.call(this);
		this.$contentEl.html('<iframe src="/account/loading/" scrolling="no" frameborder="0" marginheight="0" marginwidth="0" hspace="0" vspace="0" width="0" height="0"></iframe>');
	},

	show: function(options) {
		this.isDialogCreated = true;
		W.Dialog.prototype.show.call(this);
		var options = _.extend({}, this.options, options);
		var url = this.getUrl(options);
		if (url) {
			options.src = url;
		}
		this.$('iframe').attr('src', options.src)
						.attr('width', options.width-2)
						.attr('height', options.height)
						.attr('scrolling', options.scroll ? 'auto' : 'no');


		this.setTitle(this.options.title);
	},

	/**
	 * 获得iframe中的src的值，由子类覆盖
	 */
	getUrl: function() {
		return null;
	},

	close: function(options) {
		W.Dialog.prototype.close.call(this, options);
		this.$('iframe').attr('src', '/account/loading/');
	}
});

//支持external dialog的关闭
W.ACTIVE_DIALOG = null;
/**
 * 关闭对话框，从external dialog的iframe中的页面中调用，options用来在iframe中的页面和主页面中传递信息
 * @param options
 */
W.Dialog.close = function(options) {
	xlog('close dialog');
	if (W.ACTIVE_DIALOG) {
		W.ACTIVE_DIALOG.close(options);
	}
}


