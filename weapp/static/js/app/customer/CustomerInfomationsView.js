/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * 包含多个CustomerInfomationsView的timeline集合的view
 * @class
 */
W.CustomerInfomationsView = Backbone.View.extend({
	el: '#CustomersContent',


	events: {
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.$container = this.$('.centent_customer');
		this.loadingView = W.getLoadingView();

		//加载数据
//		this.getLoading();

		//创建collection对象，绑定其add事件
		this.customerInfomactions = new W.CustomerInfomations();
		this.customerInfomactions.bind('add', this.addNewView, this);
		this.customerInfomactions.bind('change:isSelected', this.selectHandler, this);
		this.fetchData();

		//列表头部VIEW
		this.importTitleActionView();

		//导入创建分页模块
		this.importPaginationView();

	},

	/*导入创建分页模块*/
	importPaginationView: function() {
		this.paginationView = new W.PaginationView({
			el: this.$('.tx_paginationContent'),
			isHasDetailedPage: true,
			isHasJumpPage: true,
		});
		this.paginationView.bind('goto', this.gotoPage, this);
	},

	/*导入列表头部模板*/
	importTitleActionView: function() {

		var actionView = new W.TimelinesView({
			el: this.$('.tx_timelinesActionView'),
			collection: this.customerInfomactions
		});
		actionView.render();
		actionView.bind('selectGroup', this.reload, this);
		actionView.bind('moveGroup', this.moveGroup, this);
	},

	getLoading: function() {
		this.loadingView.show(this.fetchData(), 30);
	},

	gotoPage: function(page) {
		//清理老数据
		this.customerInfomactions.setPage(page);
		this.paginationView.hide();
		$(window).scrollTop(0);

		//加载数据
		this.getLoading();
	},

	reload: function(options) {
		this.setGroupId(options.groupId)
		this.gotoPage(1);
	},

	setTimelineDoing: function(dropBox) {
		dropBox.bind('show', function() {this.isDoing = true;}, this);
		dropBox.bind('close', function() {this.isDoing = false;}, this);
	},

	setGroupId: function(groupId){
		this.customerInfomactions.setGroupId(groupId);
	},

	/*
	 * 响应timelines的add事件，向页面添加一条客户元素
	 */
	addNewView: function(model) {
		var options = _.extend({
			model: model,
			selectGroupId: this.customerInfomactions.getGroupId()
		});
		var customerView = new W.CustomerInfomationView(options);
		customerView.model.bind('change:group_id', this.moveGroup, this);
		this.$container.append(customerView.render().el);
	},

	moveGroup:function(model){
		// 全部下model不移除，页面不移除
		if(this.customerInfomactions.getGroupId() > 0){
			this.customerInfomactions.remove(model);
			if(this.customerInfomactions.length === 0) {
				this.fetchData();
			}
		}
		if(W.ISELECTED_GROUPS_LOADING){
			this.fetchData();
		}
	},
	/**
	 * 从server端加载数据
	 */
	fetchData: function() {
		xlog('fetchData')
		var _this = this;
		this.clear();

		this.customerInfomactions.fetch({
			reset: false,
			success: function(sessions, response) {
				_this.paginationView.setPageInfo(_this.customerInfomactions.getPageData());
				_this.loadingView.hide();
				if (_this.customerInfomactions.length === 0) {
					_this.$('#no_timelines').removeClass('hidden').show();
					_this.paginationView.hide();
				}
				else {
					_this.paginationView.show();
					_this.$('#no_timelines').hide();
				}
			},
			error: function(sessions, response) {
				if (response.errMsg) {
					alert(response.errMsg);
				}
				//var msg = response.errMsg || '由于网络原因，加载失败，请重新刷新页面!';
				//alert(msg)
			}
		});
	},

	clear: function(){
		this.customerInfomactions.reset([])
		this.$el.find('li').remove();
	}

});
