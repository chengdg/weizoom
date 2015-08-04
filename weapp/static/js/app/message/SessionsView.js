/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 包含多个SessionView的message集合的view
 * @constructor
 */
W.SessionsView = Backbone.View.extend({
	el: '#sessions',
	
	getTemplate: function() {
		$('#sessions-tmpl-src').template('sessions-view-tmpl');
		return 'sessions-view-tmpl';
	},

	events: {
		'click #unreadCountHint': 'onClickUnreadCountHint'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);

		//创建view
		this.tmplName = this.getTemplate();
		this.setIS_DEBUG(options.IS_DEBUG);

		this.$el.append($.tmpl(this.tmplName, {'IS_DEBUG': this.IS_DEBUG}));

		this.sessionsContainer = this.$('#sessionList');

		//创建session集合
		this.sessions = new W.Sessions();
		this.sessions.bind('add', this.addSessionView, this);
		this.fetchData();
		this.createPaginationView();
	},

	setIS_DEBUG: function(IS_DEBUG){
		if(IS_DEBUG == 'True'){
			this.IS_DEBUG = true;
		}else{
			this.IS_DEBUG = false;
		}
	},
	/**
	 * 执行检查未读数量的任务
	 */
	runCheckUnreadCountTask: function() {
		var task = new W.DelayedTask(function() {
			W.getApi().call({
				app: 'message',
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
		this.paginationView = new W.PaginationView({
			el: this.$('.wx_paginationContent'),
			isHasDetailedPage: true,
			isHasJumpPage: true
		});
		this.paginationView.bind('goto', this.gotoPage, this);
	},

    gotoPage: function(page){
        this.sessions.setPage(page);
        this.fetchData();
    },

	/**
	 * 从server端加载数据
	 */
	fetchData: function() {
		xlog('fetch sessions ...');
		var _this = this;
        $old_lis = this.$el.find('li');
		this.sessions.fetch({
			add: true,
			success: function(sessions, response) {
				_this.show();
				_this.paginationView.setPageInfo(_this.sessions.getPageData(response));
				_this.paginationView.show();

                if($old_lis.length <  _this.$el.find('li').length){
                    $old_lis.remove();
                }
				if (sessions.length === 0 && (parseInt(sessions.page, 10) === 1 || !sessions.page)) {
					_this.$('#no_messages').removeClass('hidden').show();
				}
				else {
					_this.$('#no_messages').hide();
				}

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

		var sessionView = new W.SessionView(options);
		this.sessionsContainer.append(sessionView.render().el);
	}, 

	/**
	 * 未读区域点击事件的响应函数
	 */
	onClickUnreadCountHint: function(event) {
		W.getLoadingView().show();
		W.getApi().call({
			app: 'message',
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
	}
});