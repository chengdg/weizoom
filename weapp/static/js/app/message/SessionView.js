/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 一个微信会话的view
 * @constructor
 */
W.SessionView = Backbone.View.extend({
	getTemplate: function() {
		$('#one-session-tmpl-src').template('one-session-tmpl');
		return 'one-session-tmpl';
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.tmplName = this.getTemplate();		
		this.sessionId = this.model.get('id');
		this.username = this.model.get('sender_username');
		this.fakeId = this.model.get('sender_fake_id');
        this.is_subscribed = this.model.get('is_subscribed');
        this.$submitButton = this.$('input.wx_submitReply');
		this.maxCount = 300;
	},
	
	events: {
		'click .wx_replyLink': 'onClickReplyLink',
		'click .wx_submitReply': 'onSubmitReply',
		'click .wx_deletLink': 'deleteMessage',
		'click .oneSession_replyForm': 'stopPropagation',
		'click .oneSession': 'viewHistory',
		// 选择分组
		'click .tx_selectGroup': 'selectGroup',
		// 修改备注
		'click .tx_addRemarkOneCustomer': 'addRemarkOneCustomer'
	},

	render: function() {
		var context = this.model.toJSON();
		this.$el.append($.tmpl(this.tmplName, context));
		this.submitButton = this.$('input.wx_submitReply');

		this.editer = new W.EditerView({
			el: this.$('textarea'),
			showAddLink: true,
			initClean: true
		})
		this.editer.on('exceed_count_limit', function() {
			this.submitButton.attr('disabled', true);
		}, this);
		this.editer.on('under_count_limit', function() {
			this.submitButton.attr('disabled', false);
		}, this);
		this.editer.render();

		var _this = this;
		this.$('dl').hover(function(event){
			_this.$el.find('.tx_editRemark').show();
		}, function(event){
			if(!_this.isDoing){
				_this.$el.find('.tx_editRemark').hide();
			}
		});
		return this;
	},
	
	/**
	 * "回复"链接的点击的响应函数
	 */
	onClickReplyLink: function(event) {
		this.replyForm = this.$el.find('.oneSession_replyForm');

        if (this.replyForm.is(":visible")) {
			this.replyForm.hide().find('textarea').val('');
		} else {
			this.replyForm.show().find('textarea').focus();
		}
		event.stopPropagation();
		event.preventDefault();
	},
	
	/**
	 * 提交按钮的响应函数
	 */
	onSubmitReply: function(event) {
		//检查内容是否为空
		var length = 300 - this.editer.getLength().length;
		if (length == 0) {
			alert('请输入回复内容');
			return;
		}
		this.replyForm = this.$el.find('.oneSession_replyForm');
		this.replyForm.find('input.wx_submitReply').attr('disabled', 'disabled').val('提交中...');
		
		var content = this.editer.val();
		W.getApi().call({
        	app: 'weixin',
        	api: 'm/message/create',
        	method: 'post',
        	args: {
        		text: content,
        		type: 0,
        		uid: this.fakeId,
        		access_token: W.mpUserAccessToken,
        		cookie: W.mpUserCookie
        	},
        	success: function(data) {
        		var _this = this;

				_this.replyForm = _this.$el.find('.oneSession_replyForm');
				_this.replyForm.find('input.wx_submitReply').val('提交').removeAttr('disabled');
     
        		$.post('/message/api/session/reply/write_back/', {'session_id': _this.sessionId, 'content': content, 'sender_fake_id': W.mpUserFakeId, 'recevier_fake_id': _this.fakeId, 'recevier_username': _this.username}, function (response) {
					_this.$el.find('.oneSession_content').text(content);
					_this.$el.find('.oneSession_createdAt').text('刚刚');
					_this.$el.find('.unreadMessageCount').hide();
					_this.replyForm.hide().find('textarea').val('');
				})
        	},
        	error: function(resp) {
        		this.replyForm.hide().find('textarea').val('');
        		this.replyForm = this.$el.find('.oneSession_replyForm');
				this.replyForm.find('input.wx_submitReply').val('提交').removeAttr('disabled');
             	alert("提交失败");
        		xlog(resp);
        	},
        	scope: this
        });
	},
	
	deleteMessage: function(event) {
		var _this = this;
		var $el = $(event.currentTarget);
		var deleteCommentView = W.getItemDeleteView();
		deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
			W.getApi().call({
				app: 'message',
				api: 'session/delete',
				args: {
					session_id: _this.sessionId
				},
				success: function(resp) {
					_this.$el.remove();
					deleteCommentView.close();
				},
				error: function(resp) {
					alert('删除失败');
					deleteCommentView.close();
				}
			});
		});
		deleteCommentView.show({
			$action: $el,
			info: '确定删除此信息吗?'
		});

		event.stopPropagation();
		event.preventDefault();
	},
	
	viewHistory: function(event) {
		var url = this.$el.find('.viewHistory').attr('href');
		this.$el.find('.unreadMessageCount').remove();
		location.href = url;
		event.stopPropagation();
		event.preventDefault();
	},
	
	stopPropagation: function(event) {
		event.stopPropagation();
		event.preventDefault();
	},

	selectGroup: function(event) {
		xlog('selectGroup');
		W.ISELECTED_GROUPS_LOADING = false;
		var moveDropBox = W.getMoveTimelineDropBox();
		moveDropBox.show({
			locationElement:$(event.currentTarget),
			isShowAddGroupButton : true
		});
		moveDropBox.bind(moveDropBox.CLICK_ACTIONS_EVENT, function(resp) {
			W.getApi().call({
				app: 'customer',
				api: 'customer_group/update',
				method: 'post',
				args: {
					ids: this.model.get('customer_id'),
					groupId: resp.id
				},
				success: function(data) {
					this.setGroupHtml(resp.name);
					this.model.set({'group_id': resp.id});
				},
				error: function(resp) {
				},
				scope: this
			});
		}, this);

		event.stopPropagation();
		event.preventDefault();
	},

	/*
	 * 设置页面中显示分组
	 */
	setGroupHtml: function(name){
		this.$('.tx_selectGroup').html(name+'&nbsp;<span class="caret"></span>');
	},

	setTimelineDoing: function(dropBox) {
		dropBox.bind('show', function() {this.isDoing = true;}, this);
		dropBox.bind('close', function() {
			this.isDoing = false;
			this.$el.find('.tx_editRemark').hide();
			this.$el.find('.tx_editRemark').removeClass('open');
		}, this);
	},

	addRemarkOneCustomer: function(event) {
		event.preventDefault();
		event.stopPropagation();

		var _this = this;
		var $el = $(event.currentTarget);
		$el.parent('span').addClass('open');
		var html;
		var commentDialog = W.getEditRemarkCustomerDialog();
		var remark = $el.attr('data-remark');
		this.setTimelineDoing(commentDialog);
		commentDialog.bind(commentDialog.SUCCESS_EVENT, function(resp) {
			remark = resp.info;
			html = remark
			$el.attr('data-remark', remark);
			this.$el.find('.member_remarks_name').html(html);
			if(html.trim() == ''){
				this.$el.find('.tx_remarkLayout').hide();
			}else{
				this.$el.find('.tx_remarkLayout').show();
			}
		}, this)
		var customerId = $el.attr('data-id');
		commentDialog.show({
			$action: $el,
			title: '编辑备注',
			customerId: customerId,
			remark: remark
		});
	}
});