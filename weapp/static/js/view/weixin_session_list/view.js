/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 包含多个SessionView的message集合的view
 * @constructor
 */
ensureNS('W.view.weixin');
W.view.weixin.SessionListView = Backbone.View.extend({
	el: '',
	
	getTemplate: function() {
		$('#weixin-message-session-list-tmpl-src').template('weixin-message-session-list-tmpl');
		return 'weixin-message-session-list-tmpl';
	},

	events: {
		'click #unreadCountHint': 'onClickUnreadCountHint'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.$el.text('');
		this.is_fancyBox = options.is_fancyBox || false;
		//时间条件
		this.start_time = options.start_time || '';
		this.end_time = options.end_time || '';
		//创建view
		this.tmplName = this.getTemplate();
		this.$el.append($.tmpl(this.tmplName, {is_debug: options.is_debug}));

		this.sessionsContainer = this.$('#sessionList');
		this.is_collected = options.is_collected || '';
		this.search_content = options.search_content || '';
		//创建session集合
		if (this.is_collected != '' || this.search_content != ''){
			this.sessions = new W.model.weixin.WeixinMessages();
			this.sessions.is_collected = this.is_collected;
			this.sessions.search_content = this.search_content;
			this.fetchData();
			this.createPaginationView();
		}else{
			this.sessions = new W.model.weixin.Sessions();
			this.sessions.start_time = this.start_time;
			this.sessions.end_time = this.end_time;
			this.sessions.search_content = this.search_content;
			this.fetchData();
			this.createPaginationView();
		}
		
		
	},

	/**
	 * 执行检查未读数量的任务
	 */
	runCheckUnreadCountTask: function() {
		var task = new W.DelayedTask(function() {
			W.getApi().call({
				app: 'weixin/message/message',
				api: 'realtime_unread_count/get',
				success: function(data) {
					if (data.unread_count > 0) {
						this.$('#unreadCountHint').html(data.unread_count+'条未读消息，点击查看').show();
					}
					this.runCheckUnreadCountTask();
				},
				error: function() {
					this.runCheckUnreadCountTask();
				},
				scope: this
			})
		}, this);
		task.delay(10000);
	},

	/**
	 * 创建分页部分view
	 */
	createPaginationView: function() {
		_this = this;
		_this.paginationView = new W.view.common.PaginationView({
			el: $('.wx_paginationContent'),
			isHasDetailedPage: true,
			isHasJumpPage: true
		});
		_this.paginationView.bind('goto', _this.gotoPage, _this);
	},

    gotoPage: function(page){
    	_this = this;
        _this.sessions.setPage(page);
        _this.fetchData();
    },

	/**
	 * 从server端加载数据
	 */
	fetchData: function() {
		xlog('fetch sessions ...');
		W.getLoadingView().show();
		this.hide();
		this.$('#sessionList').empty();
		var _this = this;
		this.sessions.fetch({
			add: true,
			success: function(sessions, response) {
				sessions.each(function(session) {
					_this.addSessionView(session);
				})

				_this.show();
				_this.paginationView.setPageInfo(_this.sessions.getPageData(response));
				_this.paginationView.show();

				if (sessions.length === 0 && (parseInt(sessions.page, 10) === 1 || !sessions.page)) {
					_this.$('#no_messages').show();
				}
				else {
					_this.$('#no_messages').hide();
				}
				W.getLoadingView().hide();
				
				//开始检查后台新数据
				//_this.runCheckUnreadCountTask();
			},
			error: function(sessions, response) {
				//var msg = response.errMsg || '由于网络原因，加载失败，请重新刷新页面!';
				//alert(msg)
				if (response.errMsg) {
					alert(response.errMsg);
				}
			}
		});
	},

	/**
	 * 响应session的add事件，向页面添加一条信息元素
	 */
	addSessionView: function(session) {
        xlog('addSessionView');
		var options = {
			model: session
		};

		var sessionView = new W.view.weixin.SessionView(options);
		this.sessionsContainer.append(sessionView.render().el);
		if (this.is_fancyBox) {
					$('a.xui-sessionsImg').fancybox({
						data_type: 'image',
						centerOnScroll: 'false'
		});
		}
	}, 

	/**
	 * 未读区域点击事件的响应函数
	 */
	onClickUnreadCountHint: function(event) {
		W.getLoadingView().show();
		W.getApi().call({
			app: 'weixin/message/message',
			api: 'realtime_unread_count/reset',
			args: {},
			success: function() {
				window.location.reload();
			},
			error: function() {
				window.location.reload();
			}
		})
	},

	/**
	 * 显示view
	 */
	show: function() {
		this.$el.show();
	},
	
	/**
	 * 隐藏view
	 */ 
	hide: function() {
		this.$el.hide();
	},
	
});