/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * text message编辑面板
 * @class
 */

W.EditMessagePanel = Backbone.View.extend({
	el: '#edit-message-panel',

	events: {
		'click #submit-btn': 'onSubmitAnswer'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);

		/**
		 * 初始化模拟器
		 */
		this.phone = new W.common.EmbededPhoneView({
			el: $('#embeded-phone-box'),
			type: 'text',
			maxCount: 600
		});
		this.phone.render();

		this.ruleId = options.ruleId;
        this.categoryId = options.categoryId;
        this.patternsContainer = options.patternsContainer;
        this.answerContainer = options.answerContainer;

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

        this.answerMessage = W.common.Message.createTextMessage();
        var answer = this.answerContainer.val();
        if (answer) {
        	this.answerMessage.set('text', answer);
        }
        this.phone.addTextMessage(this.answerMessage);

        //创建EditerView
        this.editor = new W.common.RichTextEditor({
			el: this.answerContainer,
			type: 'text'
		});
		this.editor.bind('contentchange', function() {
			this.answerMessage.set('text', this.editor.getHtmlContent());
		}, this);
		this.editor.render();
    },

	/**
	 * 提交按钮的响应函数
	 * @param event
	 */
	onSubmitAnswer: function(event) {
		if (!W.validate()) {
			return false;
		}
		var patternsInput = $('#patterns');
		var patterns = $.trim(patternsInput.val());
        var answer = $.trim($('#answer').val());

        var api = 'rule/update'
        if (this.ruleId == -1) {
            api = 'rule/add';
        }

        W.getLoadingView().show();
		var task = new W.DelayedTask(function() {
			W.getApi().call({
				app: 'qa',
				api: api,
				method: 'post',
				args: {
					rule_id: this.ruleId,
	                category_id: this.categoryId,
					answer: answer,
					patterns: patterns
				},
				success: function(rule) {
                    window.location.href = '/qa/rules/'+this.categoryId+'/';
				},
				error: function(response) {
					alert('添加规则失败');
		            W.getLoadingView().hide();
				},
				scope: this
			});
		}, this);
		task.delay(300);
	}
});