/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * News编辑器
 * @class
 */
ensureNS('W.view.weixin')
W.view.weixin.MessageEditorPopup = Backbone.View.extend({
	el: '',

	events: {
	},

	initialize: function(options) {
		this.editorMaxCount = options.editorMaxCount || 600;
		this.richTextEditorWidth = options.richTextEditorWidth;
		this.richTextEditorHeight = options.richTextEditorHeight;
		this.offset_Y = options.offset_Y || 0;
		this.offset_X = options.offset_X || 0;
		this.width = options.width || 400;
		if (options && options.el) {
			this.$editorBody = $(options.el);
			this.width = options.width;
			this.position = options.position;
			this.enableSubmitBtn = options.enableSubmitBtn || 'true';
			this.enableCancelBtn = options.enableCanelBtn || 'true';
			this.submitBtnText = options.submitBtnText;
			this.cancelBtnText = options.cancelBtnText;

		} else {
			this.$editorBody = $('body');
		}
	},
	
	render: function() {
		if ($('.wui-messageEditorPopup').length === 0 && this.$el.find('.wui-messageEditorPopup').length === 0) {
			this.$editorBody.append(
				'<div class="wui-messageEditorPopup xui-hide">' +
					'<div class="xa-messageEditorContainer mt10">' +
					'</div>' +
				'</div>'
			);
		}
		this.$el = $('.wui-messageEditorPopup');
		if (this.width) {
			this.$el.width(this.width);
			this.$el.find('.xa-messageEditorContainer').width(this.width);
		}
		if (this.position) {
			this.$el.css('position', this.position)
		}

		this.$el.css("width", this.width);
		
		this.editor = new W.view.weixin.MessageEditor({
			el: this.$el.find('.xa-messageEditorContainer'),
			enableSubmitBtn: this.enableSubmitBtn,
			enableCancelBtn: this.enableCanelBtn,
			submitBtnText: this.submitBtnText,
			cancelBtnText: this.cancelBtnText,
			editorMaxCount: this.editorMaxCount,
			richTextEditorWidth: this.richTextEditorWidth,
			richTextEditorHeight: this.richTextEditorHeight
		});

		this.editor.bind("finish-edit", function(message){
			this.hide();
			this.trigger('finish-edit', message);
		}, this);

		this.editor.bind("cancel-edit", function(){
			this.hide();
			this.trigger('cancel-edit');
		}, this);

		// var _this = this;
		// $('body').click(function(event) {
		// 	var $target = $(event.target);
		// 	if ($target.parents('.wui-messageEditorPopup').length === 0) {
		// 		_this.hide();
		// 	}
		// 	xlog(2);
		// });

	},

	setContent: function(content){
		this.editor.setContent(content);
	},

	displayNews: function(material) {
		this.editor.displayNews(material);
	},

	show: function($el) {
		this.showWithOffset($el, this.offset_X, this.offset_Y);
	},

	showWithOffset: function($el, x, y) {
		var elOffset = $el.offset();
		var elHeight = $el.outerHeight();
		this.editor.reset();
		this.$el.css({
			left: elOffset.left + x + 'px',
			top: elOffset.top + y + elHeight + 'px'
		})
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	}
});