/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * text message编辑面板
 * @class
 */

W.EditContentPanel = Backbone.View.extend({
	el: '#edit-message-panel',

	events: {
		'click #submit-btn': 'onSubmit',
		'click a[data-type="text"]': 'onClickTabText',
		'click a[data-type="news"]': 'onClickTabNews'
	},

	getTemplate: function() {
		$('#edit-content-view-tmpl-src').template('edit-content-tmpl');
		return 'edit-content-tmpl';
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.template = this.getTemplate();
		this.newses = options.newses;
		this.ruleId = options.ruleId || 0;
		this.materialId = options.materialId;
		this.answer = options.answer || '';
		this.patterns = options.patterns || ''

		this.isUnmatchRule = options.isUnmatchRule || false;
		this.isPatterns = options.isPatterns || false;

		this.isActive = options.isActive || "false";
		this.render();

		this.phone = new W.common.EmbededPhoneView({
			el: $('#embeded-phone-box')
		});
		this.phone.render();



		this.patternsContainer = this.$('#patterns');
		if(this.patternsContainer.length > 0 ){
			this.patternMessage = W.common.Message.createTextMessage();
			var pattern = this.patternsContainer.val().split('|')[0];
			if (pattern) {
				this.patternMessage.set('text', pattern);
			}
			this.phone.receiveTextMessage(this.patternMessage);
			this.patternsContainer.bind('input', _.bind(function() {
				var pattern = this.patternsContainer.val().split('|')[0];
				this.patternMessage.set('text', pattern);
			}, this));
		}



		this.answerContainer = this.$('#answer');
		this.message = W.common.Message.createTextMessage();
		var answer = this.answerContainer.val();
		if (answer) {
			this.answerMessage.set('text', answer);
		}
		this.phone.addTextMessage(this.message);


		this.old_messages = this.phone.messages;
		this.phoneShowNewses(this.newses);

		if (this.ruleId != -1 && this.materialId <= 0) {
			this.message.set('text', this.answer);
			this.phone.addTextMessage(this.message);
		}

		this.editor = new W.common.RichTextEditor({
			el: 'textarea',
			type: 'text',
			maxCount: 600
		});
		this.editor.bind('contentchange', function() {
			this.message.set('text', this.editor.getHtmlContent());
		}, this);
		this.editor.setContent(this.answer);
		this.editor.render();

		this.optionsDialog = {
			title: '选择图文素材',
			selectedCount: 0,
			count: 3
		}
		this.selectNewsDialog = W.material.getSelectNewsDialog(this.optionsDialog);
		this.$textMessageTab = $('a[href="#timedWeixinEditer-textMessageZone"]');
		this.$newsMessageTab = $('a[href="#timedWeixinEditer-newsMessageZone"]');

		/*
		 * 右侧显示的选择后的图文消息
		 */
		this.selectNewsTypeView = new W.SelectNewsTypeView({
			el: '#timedWeixinEditer-newsMessageZone'
		});
		this.selectNewsTypeView.bind('showMaterialed', function(newses){
			// phone
			this.phoneShowNewses(newses);
		}, this);
		this.selectNewsTypeView.render();

		if(this.materialId > 0){
			this.selectNewsTypeView.showMaterial(this.materialId);
			this.$newsMessageTab.tab('show');
		}else{
			console.log('ddddddddddddddddddddddddd');
			this.$(".shop-service[data-id='-99']").show();
			this.$(".shop-service[data-id='-98']").show();
		}
    },

	render: function() {
		this.$el.html($.tmpl(this.template, {
			isUnmatchRule: this.isUnmatchRule,
			isActive: this.isActive,
			isPatterns: this.isPatterns,
			patterns: this.patterns,
			ruleId: this.ruleId
		}));
		return this;
	},

	/**
	 * 模拟器中显示多图文
	 * @param newses
	 */
	phoneShowNewses: function (newses){
		this.deleteNewses();
		//初始化微信消息
		var newsCount = newses ? newses.length : 0;
		for (var i = 0; i < newsCount; ++i) {
			var news = newses[i];
			news.summary = news.summary.replace(/<br\/>/g, '\n');
			var newsMessage = W.common.Message.createNewsMessage();
			newsMessage.set(news);
			if (i == 0) {
				this.phone.addNews(newsMessage);
			} else {
				this.phone.appendNews(newsMessage);
			}
		}
		//
		this.hideTextDiv();
	},
	/*
	 * 删除图文
	 */
	deleteNewses: function(){
		var listMessage = [];
		this.phone.messages.filter(function(message) {
			if(message.get("type") == "news"){
				listMessage.push(message);
			}
		}, this);

		_.each(listMessage, function(message){
			this.phone.messages.remove(message);
		}, this);
	},

	/*
	 * 隐藏文本
	 */
	hideTextDiv: function(){
		this.$(".shop-service[data-id='-99']").hide();
		this.$(".shop-service[data-id='-98']").hide();
	},

	onClickTabText: function(){
		this.phone.reset(this.old_messages);
		this.deleteNewses();
		this.message.set('text', this.editor.getHtmlContent());
		this.phone.addTextMessage(this.message);
		this.materialId = 0;
	},

	onClickTabNews: function(event){
		event.stopPropagation();
		event.preventDefault();
		this.optionsDialog.selectedCount = 0;
		this.optionsDialog.count = 1;
		this.optionsDialog.materialId = this.materialId;
		this.selectNewsDialog.show(this.optionsDialog);
		this.selectNewsDialog.bind('finish-submit-news',function(ids){
			if(ids.length > 0) {
				// tab区域
				this.materialId = ids[0];
				this.newses = this.selectNewsTypeView.showMaterial(this.materialId);
				this.$newsMessageTab.tab('show');
			}
		}, this);
	},

	/**
	 * 提交按钮的响应函数
	 * @param event
	 */
	onSubmit: function(event) {
		xlog('ddd')
		if (!W.validate()) {
			return false;
		}
		var materialId = 0;
		if(this.$newsMessageTab.parents('li').hasClass('active')){
			materialId = this.materialId;
		}
		this.trigger('submit-end', materialId);
	}
});