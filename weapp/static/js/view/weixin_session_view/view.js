/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 一个微信会话的view
 * @constructor
 */
ensureNS('W.view.weixin');
W.view.weixin.SessionView = Backbone.View.extend({
	getTemplate: function() {
		$('#weixin-message-one-session-tmpl-src').template('weixin-message-one-session-tmpl');
		return 'weixin-message-one-session-tmpl';
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.is_fancyBox = options.is_fancyBox || false;
		this.tmplName = this.getTemplate();		
		this.sessionId = this.model.get('session_id');
		this.username = this.model.get('sender_username');
		this.fakeId = this.model.get('sender_fake_id');
        this.is_subscribed = this.model.get('is_subscribed');
        this.$submitButton = this.$('input.wx_submitReply');
		this.maxCount = 300;
	},
	
	events: {
		'click .wx_replyLink': 'onClickReplyLink',
		'click .wx_submitReply': 'onSubmitReply',
		//'click .wx_deletLink': 'deleteMessage',
		'click .oneSession': 'viewHistory',
		// 选择分组
		'click .tx_selectGroup': 'selectGroup',
		// 修改备注
		'click .tx_addRemarkOneCustomer': 'addRemarkOneCustomer',
		'click .dropdown-menu': 'onClickDropdownMenuZone',
		'click .x-editRemarkLink': 'onClickEditRemarkLink',
		'click .x-editRemark .btn-success': 'onClickSubmitRemarkButton',
		'click .wx_collect_message': 'conClickCollectMessage',
	},

	onClickDropdownMenuZone: function(event) {
		event.stopPropagation();
	},

	onClickEditRemarkLink: function(event) {
		var $link = $(event.currentTarget);
		var $session = $link.parents('.oneSession').eq(0);
		var $input = $session.find('input[type="text"]');
		$input.val('');
		var remark = $session.find('.member_remarks_name').text();
		var task = new W.DelayedTask(function() {
			$input.val(remark).focus();
		});
		task.delay(100);
	},

	/**
	 * onClickSubmitRemarkButton: 点击修改备注“确定”按钮后的响应函数
	 */
	onClickSubmitRemarkButton: function(event) {
		var $button = $(event.currentTarget);
		var $session = $button.parents('.oneSession');
		var $input = $button.parent().find('input[type="text"]');
		var newRemark = $input.val();
		var customerId = $session.attr('data-member-id');
		
		$button.bottonLoading({status:'show'});
		
		W.getApi().call({
			app: 'modules/member',
			api: 'member_remarks_name/update',
			method: 'post',
			args: {
				id: customerId,
				remarks_name: newRemark
			},
			success: _.bind(function() {
				$button.bottonLoading({status:'hide'});
				$session.find('.member_remarks_name').text(newRemark);
				// $session.find('.dropdown-toggle').dropdown('toggle');
				$session.find('.x-editRemarkLink').click();
				
			}, this),
			error: function() {
				alert('备注修改失败！');
				$button.bottonLoading({status:'hide'});
			}
		});
	},

	render: function() {
		var context = this.model.toJSON();
		this.$el.append($.tmpl(this.tmplName, context));
		this.submitButton = this.$('input.wx_submitReply');


		this.editor = new W.view.weixin.SessionReplyEditor({
			el: this.$('textarea'),
			showAddLink: false,
			initClean: true
		})
		this.editor.on('exceed_count_limit', function() {
			this.submitButton.attr('disabled', true);
		}, this);
		this.editor.on('under_count_limit', function() {
			this.submitButton.attr('disabled', false);
		}, this);
		this.editor.render();
		xlog(this)
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
		var length = 300 - this.editor.getLength().length;
		if (length == 0) {
			alert('请输入回复内容');
			return;
		}
		this.replyForm = this.$el.find('.oneSession_replyForm');
		this.replyForm.find('input.wx_submitReply').attr('disabled', 'disabled').val('提交中...');
		
		var content = this.editor.val();
		W.getApi().call({
        	app: 'weixin/message/message',
        	api: 'custome_message/create',
        	method: 'post',
        	args: {
        		text: content,
        		type: 0,
        		openid: this.username,
        	},
        	success: function(data) {
        		var _this = this;

				_this.replyForm = _this.$el.find('.oneSession_replyForm');
				_this.replyForm.find('input.wx_submitReply').val('提交').removeAttr('disabled');
     
        		$.post('/weixin/message/message/api/session/reply/write_back/', {'session_id': _this.sessionId, 'content': content, 'receiver_username': _this.username}, function (response) {
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
	
	/*
	deleteMessage: function(event) {
		var _this = this;
		var $el = $(event.currentTarget);
		var deleteCommentView = W.getItemDeleteView();
		deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
			W.getApi().call({
				app: 'weixin/message/message',
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
	*/
	
	viewHistory: function(event) {
		var $el = $(event.target);
		
		if ($el.hasClass('oneSession') || $el.hasClass('oneSession_info') || $el.hasClass('oneSession_content')) {
			var url = this.$el.find('.viewHistory').attr('href');
			this.$el.find('.unreadMessageCount').remove();
			location.href = url;
			event.stopPropagation();
			event.preventDefault();	
		}
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
	/*
	 *
	 *
	 */
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
	}
});