/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 微信消息编辑器
 * @class
 */

ensureNS('W.view.weixin');
W.view.weixin.addQrcodeView = Backbone.View.extend({
	el: '',

	events: {
		'click .xa-text': 'onClickTextMessageTab',
		'click .xa-news': 'onClickNewsMessageTab',
		'click .xa-submit': 'getPrizeInfo',
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

		this.materialId = options.materialId || 0;
		this.material = options.material || null;
		this.answer = options.answer || '';
		this.newsesTitles = [];

		if (this.material && this.materialId) {
			this.material.id = this.materialId;
		};

		this.render();
		this.$textMessageTab = this.$('a[href="#weixinMessageEditer-textMessageZone"]');
		this.$newsMessageTab = this.$('a[href="#weixinMessageEditer-newsMessageZone"]');
		this.$newsMessageZone = this.$('.xa-newsMessageZone');
 
		//创建富文本编辑器
		var width = options.richTextEditorWidth || this.$el.outerWidth();
		var height = options.richTextEditorHeight;
		this.editor = new W.view.common.RichTextEditor({
			el: 'textarea',
			type: 'text',
			maxCount: this.editorMaxCount,
			width: width,
			height: height
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
		this.$el.html($.tmpl(this.template, {}));
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
	getPrizeInfo: function() {
		alert('xxxxxxxxxxxxxmmmmmm')
        if (this.isNonPrizeType) {
            return {'id':-1, 'name':'non-prize', 'type':'无奖励'};
        } else if (this.isScorePrizeType) {
            var score = parseInt(this.$('#prize_score_input').val());
            return {'id':score, 'name':'_score-prize_', 'type':'积分'};
        } else if (this.isRealPrizeType) {
            var prize_name = this.$('#prize_real_prize_input').val();
            return {'id':0, 'name':prize_name, 'type':'实物奖励'};
        } else {
            var $slectPrizeType = this.$("#prizeTypesSelector option:selected");
            var prizeType = $slectPrizeType.val();

            var $selectedPrize = this.$("#prize_list option:selected");
            var id = parseInt($selectedPrize.val());
            var prizeName = $selectedPrize.html();
            return {'id':id, 'name':prizeName, 'type':prizeType};
        }
    },

	setContent: function(content){		
		this.editor.setContent(content);
		this.$('[name="text_content"]').val(content);
	},

	onCancel: function(event) {
		this.trigger('cancel-edit');
	}
});