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
		'click #submit-btn': 'onSubmit',
		'click a[data-type="text"]': 'onClickTextMessageTab',
		'click a[data-type="news"]': 'onClickNewsMessageTab',
		'click select[name="start_hour"]': 'onClickHourSelect',
		'click select[name="end_hour"]': 'onClickHourSelect',
		'click [name="active_type"]': 'onClickActiveTypeRadio',
		'click .xa-embededPhone-showBtn': 'onClickNewsMessageTab'
	},

	getTemplate: function() {
		$('#weixin-message-eidtor-tmpl-src').template('weixin-message-eidtor-tmpl');
		return 'weixin-message-eidtor-tmpl';
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.template = this.getTemplate();
		this.newses = options.newses || [];
		this.ruleId = options.ruleId || 0;
		this.materialId = options.materialId;
		this.answer = options.answer || '';

		this.enableEditPattern = options.enableEditPattern || false;
		this.patterns = options.patterns || ''

		this.enableRuleActivationController = options.enableRuleActivationController || false;
		this.activeType = options.activeType || false;
		this.startHour = options.startHour || 0;
		this.endHour = options.endHour || 0;

		this.render();
		this.$textMessageTab = $('a[href="#weixinMessageEditer-textMessageZone"]');
		this.$newsMessageTab = $('a[href="#weixinMessageEditer-newsMessageZone"]');

		//创建预览器
		this.phone = new W.view.weixin.EmbededPhoneView({
			el: this.$el.find('#embeded-phone-box').get()
		});
		this.phone.render();

		//创建文本消息
		this.textMessage = W.model.weixin.Message.createTextMessage();
		this.textMessage.set('text', answer);

		//创建富文本编辑器
		this.editor = new W.view.common.RichTextEditor({
			el: 'textarea',
			type: 'text',
			maxCount: 600
		});
		this.editor.bind('contentchange', function() {
			this.textMessage.set('text', this.editor.getHtmlContent());
		}, this);
		this.editor.setContent(this.answer);
		this.editor.render();

		/**
		 * 初始化pattern输入区域
		 */
		this.patternMessage = null;
		if (this.enableEditPattern) {
			this.patternsContainer = this.$('#weixinMessageEditor-patternsInput');

			this.patternMessage = W.model.weixin.Message.createTextMessage();
			var pattern = this.patterns.split('|')[0];
			this.patternMessage.set('text', pattern);
			this.patternsContainer.bind('input', _.bind(function() {
				var pattern = this.patternsContainer.val().split('|')[0];
				this.patternMessage.set('text', pattern);
			}, this));
		}

		/*
		 * 创建material的display view
		 */
		this.materialDisplayView = new W.view.weixin.MaterialDisplayView({
			el: '#weixinMessageEditer-newsMessageZone',
			enableEdit: true,
			enableChangeMaterial: true
		});
		this.materialDisplayView.bind('material-after-display', function(newses){
			this.newses = newses;
			this.showNewsesInPhone(this.newses);
		}, this);
		this.materialDisplayView.render();


		//确定在phone中显示的消息
		if(this.materialId > 0){
			//有material，显示图文消息
			this.materialDisplayView.showMaterial(this.materialId);
			this.$newsMessageTab.tab('show');
		}else{
			//无material，显示文本消息
			this.showTextMessage();
		}
    },

	render: function() {
		hours = []
		for (var i = 0; i < 25; ++i) {
			hours.push(i);
		}
		this.$el.html($.tmpl(this.template, {
			enableRuleActivationController: this.enableRuleActivationController,
			activeType: this.activeType,
			enableEditPattern: this.enableEditPattern,
			patterns: this.patterns,
			ruleId: this.ruleId,
			hours: hours,
			startHour: this.startHour,
			endHour: this.endHour
		}));
		return this;
	},

	/**
	 * 模拟器中显示多图文
	 * @param newses
	 */
	showNewsesInPhone: function (newses){
		this.phone.reset();
		//初始化微信消息
		var newsCount = newses ? newses.length : 0;
		for (var i = 0; i < newsCount; ++i) {
			var news = newses[i];
			news.summary = news.summary.replace(/<br\/>/g, '\n');
			var newsMessage = W.model.weixin.Message.createNewsMessage();
			newsMessage.set(news);
			if (i == 0) {
				this.phone.addNews(newsMessage);
			} else {
				this.phone.appendNews(newsMessage);
			}
		}
	},

	/**
	 * onClickTextMessageTab: 点击“文字”tab的响应函数 
	 */
	onClickTextMessageTab: function(){
		this.materialId = 0;
		this.showTextMessage();
	},

	/**
	 * onClickNewsMessageTab: 点击“图文”tab的响应函数 
	 */
	onClickNewsMessageTab: function(event){
		event.stopPropagation();
		event.preventDefault();

		var _this = this;
		W.dialog.showDialog('W.dialog.weixin.SelectMaterialDialog', {
			success: function(ids) {
				if (ids.length > 0) {
					_this.materialId = ids[0];
					_this.materialDisplayView.showMaterial(_this.materialId);
					_this.$newsMessageTab.tab('show');
				}
			}
		})
	},

	/**
	 * onClickHourSelect: 点击时间选择select 
	 */
	onClickHourSelect: function(event) {
		event.stopPropagation();
		event.preventDefault();
	},

	/**
	 * onClickActiveTypeRadio: 点击active type单选框 
	 */
	onClickActiveTypeRadio: function(event) {
		if ($('[name="active_type"]:checked').val() !== 2) {
			$('[name="start_hour"]').val(0);
			$('[name="end_hour"]').val(0);
		}
	},

	/**
	 * showTextMessage: 显示文本消息
	 */
	showTextMessage: function() {
		this.phone.reset();
		if (this.patternMessage) {
			this.phone.receiveTextMessage(this.patternMessage);
			this.patternsContainer.focus();
		}
		this.phone.addTextMessage(this.textMessage);
	},

	/**
	 * 提交按钮的响应函数
	 * @param event
	 */
	onSubmit: function(event) {
		if (!W.validate()) {
			return false;
		}
		
		var activeType = parseInt($('[name="active_type"]:checked').val());
		var startHour = parseInt($('[name="start_hour"]').val());
		var endHour = parseInt($('[name="end_hour"]').val());
		if (activeType === 2 && endHour < startHour) {
			W.getErrorHintView().show('开始时间不能晚于结束时间！');
			return false;
		}

		
		var patterns = "";
		var $patternsInput = $('#weixinMessageEditor-patternsInput');
		if ($patternsInput.length > 0) {
			patterns = $.trim($patternsInput.val());
		}

		var message = null;
		if(this.$newsMessageTab.parents('li').hasClass('active')){
			message = {
				type: 'news',
				materialId: this.materialId,
				answer: '',
				activeType: activeType,
				patterns: patterns,
				startHour: startHour,
				endHour: endHour
			}
		} else {
			message = {
				type: 'text',
				materialId: 0,
				answer: this.editor.getContent(),
				activeType: activeType,
				patterns: patterns,
				startHour: startHour,
				endHour: endHour
			}
		}
		this.trigger('finish-edit', message);
	}
});