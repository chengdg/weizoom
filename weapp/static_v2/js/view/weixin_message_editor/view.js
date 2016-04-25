/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 微信消息编辑器
 * @class
 */

ensureNS('W.view.weixin');
W.view.weixin.MessageEditor = Backbone.View.extend({
	el: '',

	events: {
		'click .xa-text': 'onClickTextMessageTab',
		'click .xa-news': 'onClickNewsMessageTab',
		'click .xa-submit': 'onSubmit',
		'click .xa-cancel': 'onCancel',
		'click .xa-changeNews': 'onClickChangeNewsLink'
	},

	getTemplate: function() {
		$('#weixin-message-eidtor-tmpl-src').template('weixin-message-eidtor-tmpl');
		return 'weixin-message-eidtor-tmpl';
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.template = this.getTemplate();

		//控制按钮显示
		this.enableSubmitBtn = options.enableSubmitBtn || 'true';
		this.enableCancelBtn = options.enableCanelBtn || 'true';
		this.submitBtnText = options.submitBtnText;
		this.cancelBtnText = options.cancelBtnText;
		this.editorMaxCount = options.editorMaxCount || 600;
		this.helptext = options.help || '';

		this.materialId = options.materialId || 0;
		this.material = options.material || null;
		this.answer = options.answer || '';
		this.newsesTitles = [];

		if (this.material && this.materialId) {
			this.material.id = this.materialId;
		}

		this.render();
		this.$textMessageTab = this.$('a[href="#weixinMessageEditer-textMessageZone"]');
		this.$newsMessageTab = this.$('a[href="#weixinMessageEditer-newsMessageZone"]');
		this.$newsMessageZone = this.$('.xa-newsMessageZone');

		//创建富文本编辑器
		var width = options.richTextEditorWidth || this.$el.outerWidth();
		var height = options.richTextEditorHeight;
		this.editor = new W.view.common.RichTextEditor({
			el: '#weixinMessageText',
			type: 'text',
			maxCount: this.editorMaxCount,
			width: width,
			height: height,
			autoHeight:false,
			pasteplain: !!options.pasteplain
		});
		// this.editor.bind('contentchange', function() {
		// 	this.textMessage.set('text', this.editor.getHtmlContent());
		// }, this);
		this.editor.setContent(this.answer);
		this.editor.render();
		this.$('.errorHint').hide();
		if (this.enableSubmitBtn === 'false') {
			this.$('.xa-submit').hide();
		} else{
			if (this.submitBtnText) {
				this.$('.xa-submit').html(this.submitBtnText);
			}
		}
		if (this.enableCancelBtn === 'false') {
			this.$('.xa-cancel').hide();
		} else{
			if (this.cancelBtnText) {
				this.$('.xa-cancel').html(this.cancelBtnText);
			}
		}

		this.type = 'text';
		if(this.materialId > 0){
			//有material，显示图文消息
			//this.materialDisplayView.showMaterial(this.materialId);
			this.type = 'news';
			this.displayNews(this.material);
		}else{
			//无material，显示文本消息
		}
    },

    reset: function(){
    	this.$el.find('.xa-text').click();
    },

	render: function() {
		this.$el.html($.tmpl(this.template, {helptext: this.helptext}));
		return this;
	},

	displayNews: function(material) {
		this.setNewsesTitles(material.newses);
		var newsView = new W.view.weixin.NewsView({
			material: material
		});
		var $el = newsView.render();
		this.$newsMessageZone.html($el);

		this.$newsMessageTab.tab('show');
	},

	setNewsesTitles: function(newses){
		for (var i = 0; i < newses.length; i++) {
			this.newsesTitles.push(newses[i].title);
		}
	},

	/**
	 * onClickTextMessageTab: 点击“文字”tab的响应函数
	 */
	onClickTextMessageTab: function(){
		this.materialId = 0;
		this.type = 'text';
	},

	/**
	 * onClickChangeNewsLink: 点击“更换”图文消息的链接
	 */
	onClickChangeNewsLink: function(event){
		this.onClickNewsMessageTab(event);
	},

	/**
	 * onClickNewsMessageTab: 点击“图文”tab的响应函数
	 */
	onClickNewsMessageTab: function(event){
		event.stopPropagation();
		event.preventDefault();
		this.type = 'news';

		var _this = this;
		W.dialog.showDialog('W.dialog.weixin.SelectMaterialDialog', {
			materialId: this.materialId,
			success: function(data) {
				_this.material = data;
				_this.materialId = _this.material.id;
				_this.displayNews(_this.material);
			}
		})
	},


	/**
	 * 提交按钮的响应函数
	 * @param event
	 */
	onSubmit: function(event) {
		var isUseTextMessage = ('text' === this.type);
		var textContent = '';
		if (isUseTextMessage) {
			var textContent = $.trim(this.$('[name="text_content"]').val());
			if (!textContent) {
				W.showHint('error', '内容不能为空');
				return;
			}
			if(textContent.length > this.editorMaxCount){
				W.showHint('error', '内容不能超过'+this.editorMaxCount+'字');
				return;
			}
		}

		var patterns = "";
		var $patternsInput = $('#weixinMessageEditor-patternsInput');
		if ($patternsInput.length > 0) {
			patterns = $.trim($patternsInput.val());
		}

		var message = null;
		if(isUseTextMessage) {
			message = {
				type: 'text',
				materialId: 0,
				answer: textContent
			}
		} else {
			message = {
				type: 'news',
				materialId: this.materialId,
				answer: '',
				//titles: this.newsesTitles
				material: this.material
			}
		}
		this.trigger('finish-edit', message);
	},

	setContent: function(content){
		this.editor.setContent(content);
		this.$('[name="text_content"]').val(content);
	},

	onCancel: function(event) {
		this.trigger('cancel-edit');
	}
});