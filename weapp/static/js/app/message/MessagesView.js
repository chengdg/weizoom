/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 一个会话中多条message的view
 * @constructor
 */
W.MessagesView = Backbone.View.extend({
	el: '',
	
	getTemplate: function() {
		$('#session-history-tmpl-src').template('session-history-tmpl');
		return 'session-history-tmpl';
	},

	events: {
		'click .wx_submitReply': 'onSubmitReply'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.template = this.getTemplate();

		this.sessionId = options.sessionId || 0;
		this.receiverUserName = options.receiverUserName || '';
		this.receiverFakeId = options.receiverFakeId || '';
        this.$submitButton = this.$('input.wx_submitReply');
        this.is_subscribed = options.is_subscribed;


	}, 

	render: function() {
		if (this.is_subscribed == 0) {
			this.fetchData();
			return this;
		}
		this.submitButton = this.$('input.wx_submitReply');

		/*
		this.editer = new W.EditerView({
			el: this.$('textarea'),
			showAddLink: true,
			initClean: true
		});
		*/
		this.editor = new W.common.RichTextEditor({
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
		W.getApi().call({
			app: 'message',
			api: 'session_history/get',
			args: {
				session_id: sessionId
			},
			success: function(data) {
				var histories = data.items;
				var container = this.$el;
				_.each(histories, function(history){
					history.content = history.content.replace(/\n/g, '<br/>');
					var content = $.tmpl('session-history-tmpl', history);
					container.append(content);
				});
			},
			error: function(resp) {
				alert('获取数据失败');
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
        	app: 'weixin',
        	api: 'm/message/create',
        	method: 'post',
        	args: {
        		text: content,
        		type: 0,
        		uid: this.receiverFakeId,
        		access_token: W.mpUserAccessToken,
        		cookie: W.mpUserCookie
        	},
        	success: function(data) {
        		var _this = this;
        		this.editor.setContent('');
        		this.$('textarea').val('');
        		this.$submitButton.val('提交').removeAttr('disabled');
        		try {
	        		$.post('/message/api/session/reply/write_back/', {
	        			'session_id': this.sessionId, 
	        			'content': content, 
	        			'sender_fake_id': W.mpUserFakeId, 
	        			'recevier_fake_id': this.receiverFakeId, 
	        			'recevier_username': this.receiverUserName
        			}, function(response) {
        				window.location.reload();
					});
	        	} catch(e) {
	        		alert('exception');
	        	}
        	},
        	error: function(resp) {
        		this.$submitButton.val('提交').removeAttr('disabled');
        		alert("提交失败");
        		xlog(resp);
        	},
        	scope: this
        });
	}
});