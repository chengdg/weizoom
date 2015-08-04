/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 一个会话中多条message的view
 * @constructor
 */
ensureNS('W.view.weixin');
W.view.weixin.SessionHistoryView = Backbone.View.extend({
	el: '',
	
	getTemplate: function() {
		$('#weixin-session-history-tmpl-src').template('weixin-session-history-tmpl');
		return 'weixin-session-history-tmpl';
	},

	getOneMessageTemplate: function() {
		$('#weixin-session-history-one-message-tmpl-src').template('weixin-session-history-one-message-tmpl');
		return 'weixin-session-history-one-message-tmpl';
	},

	events: {
		'click .wx_submitReply': 'onSubmitReply',
		'click .wx_collect_message': 'conClickCollectMessage',
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.is_fancyBox = options.is_fancyBox || false;
		this.top_message_id = options.top_message_id || '';
		this.template = this.getTemplate();
		this.oneMessageTemplate = this.getOneMessageTemplate();

		this.sessionId = options.sessionId || 0;
		this.receiverUserName = options.receiverUserName || '';
        this.$submitButton = this.$('input.wx_submitReply');
        this.is_subscribed = options.is_subscribed;
	}, 

	render: function() {
		this.$el.html($.tmpl(this.template, {}));

		this.$messageContainer = this.$('#histories_list');
		this.$editorContainer = this.$('#content_div');

		if (this.is_subscribed == 0) {
			this.fetchData();
			return this;
		}
		this.submitButton = this.$('input.wx_submitReply');

		this.editor = new W.view.common.RichTextEditor({
			el: 'textarea',
			type: 'text',
			width: 695,
			height: 80
		})
		this.editor.on('wordcount_overflow', function() {
			this.submitButton.attr('disabled', true);
		}, this);
		this.editor.on('wordcount_normal', function() {
			this.submitButton.attr('disabled', false);
		}, this);
		this.editor.render();
		this.editor.focus();
		this.fetchData();
		return this;
	},
	
	/**
	 * 从server端加载数据
	 */
	fetchData: function() {
		xlog('fetch session histories ...');
		W.getLoadingView().show();
		this.$messageContainer.hide();
		this.$editorContainer.hide();
		var _this = this;
		W.getApi().call({
			app: 'weixin/message/message',
			api: 'session_history/get',
			args: {
				session_id: sessionId
			},
			success: function(data) {
				var histories = data.items;
				this.is_active = data.is_active;
				_.each(histories, function(history){
					if (history.content != null ){
						history.content = history.content.replace(/\n/g, '<br/>');
					}
					var content = $.tmpl(this.oneMessageTemplate, history);
					this.$messageContainer.append(content);
					var content_edit = $.tmpl(this.template, history);
					
				}, this);
				W.getLoadingView().hide();
				if (this.is_active){
					this.$editorContainer.show();
				}
				if (_this.is_fancyBox) {
					$('a.xui-sessionsImg').fancybox({
						data_type: 'image',
						centerOnScroll: 'false'
					});
				}
				this.$messageContainer.show();
				if (this.top_message_id){
					$("html,body").animate({scrollTop:this.$("#"+this.top_message_id).position().top },1000);	
				}
				
			},
			error: function(resp) {
				alert('获取数据失败');
				W.getLoadingView().hide();
			},
			scope: this
		});
	},

	/**
	 * 提交按钮的响应函数
	 */
	onSubmitReply: function(event) {
		//检查内容是否为空
		var content = $.trim($('textarea').val());
		if (content.length == 0) {
			alert('请输入回复内容');
			return;
		}
		this.$submitButton.attr('disabled', 'disabled').val('提交中...');

		W.getApi().call({
        	app: 'weixin/message/message',
        	api: 'custome_message/create',
        	method: 'post',
        	args: {
        		text: content,
        		type: 0,
        		openid: this.receiverUserName,
        	},
        	success: function(data) {
        		var _this = this;
        		this.editor.setContent('');
        		this.$('textarea').val('');
        		this.$submitButton.val('提交').removeAttr('disabled');
        		try {
	        		$.post('/weixin/message/message/api/session/reply/write_back/', {
	        			'session_id': this.sessionId, 
	        			'content': content, 
	        			'receiver_username': this.receiverUserName
        			}, function(response) {
        				window.location.reload();
					});
	        	} catch(e) {
	        		alert('exception');
	        	}
        	},
        	error: function(resp) {
        		this.$submitButton.val('提交').removeAttr('disabled');
        		alert(resp.errMsg);
        		xlog(resp);
        	},
        	scope: this
        });
	},
	conClickCollectMessage: function(event) {
		var $el = $(event.currentTarget);
		var status = $el.attr('status');
		var message_id = $el.attr('value');

		W.getApi().call({
        	app: 'weixin/message/message',
        	api: 'collect/message',
        	method: 'post',
        	args: {
        		status: status,
        		message_id: message_id,
        	},
        	success: function(data) {
        			if (status == '1'){
        				$el.attr('status', '0');
        				$el.attr('class', 'wx_collect_message xui-session-btn xui-sessionsIcon-starActive');
						$el.attr('title', '取消收藏');
        			}else{
        				$el.attr('status', '1');
        				$el.attr('class', 'wx_collect_message xui-session-btn xui-sessionsIcon-star');
						$el.attr('title', '收藏消息');
        			}
        			/* 修改收藏按钮 */
        		
        	},
        	error: function(resp) {
             	alert("收藏失败");
        	},
        	scope: this
        });
	},
});