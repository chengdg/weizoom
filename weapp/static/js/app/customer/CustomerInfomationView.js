/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * 包含多个CustomerInfomationsView的timeline集合的view
 * @class
 */
W.CustomerInfomationView = Backbone.View.extend({
	tagName: 'li',
	className: 'li1',

	events: {
		//改备注
		'click .tx_addRemarkOneCustomer': 'addRemarkOneCustomer',
		//点击单选框
		'click .customer_checkeBox': 'selectCustomer',
		//与他对话
		'click .tx_session': 'showSession',

		'click .tx_selectGroup': 'selectGroup'
	},

	getOneCustomerTemplate: function() {
		var name = 'one-customer-tmpl';
		$('#one-customer-tmpl-src').template(name);
		return name;
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.model = options.model;
		this.selectGroupId = options.selectGroupId || -1;

		this.oneCustomerTemplate = this.getOneCustomerTemplate();
		this.model.bind('change:isSelected', this.selectHandler, this);
		this.model.bind('change:group_id', this.changeGroup, this);
	},

	changeGroup: function(model){
		// 全部下model不移除，页面不移除
		if(this.selectGroupId > 0 && this.selectGroupId != model.get('group_id')){
			this.$el.remove();
		}
	},

	addRemarkOneCustomer: function(event) {
		event.preventDefault();
		event.stopPropagation();

		var _this = this;
		var $el = $(event.currentTarget);
		var html;
		var commentDialog = W.getEditRemarkCustomerDialog();
		var remark = $el.attr('data-remark');
		this.setTimelineDoing(commentDialog);
		commentDialog.bind(commentDialog.SUCCESS_EVENT, function(resp) {
			remark = resp.info;
			html = remark
			$el.attr('data-remark', remark);
			this.$el.find('.tx_remarkLayout').html(html);
		}, this)
		var customerId = $el.attr('data-id');
		commentDialog.show({
			$action: $el,
			title: '编辑备注',
			customerId: customerId,
			remark: remark
		});
	},

	/*
	 * 设置页面中显示分组
	 */
	setGroupHtml: function(name){
		this.$('.tx_selectGroup').html(name+'&nbsp;<span class="caret"></span>');
	},

	setTimelineDoing: function(dropBox) {
		dropBox.bind('show', function() {this.isDoing = true;}, this);
		dropBox.bind('close', function() {this.isDoing = false;}, this);
	},

	showSession: function(event){
		var session_history = this.model.get('session_history');

		W.getApi().call({
			app: 'customer',
			api: 'customer_weixin_user/get',
			args: {
				weixin_id: this.model.get('weixin_id')
			},
			success: function(data) {
				if(session_history === -1){
					W.getErrorHintView().show('与此用户的会话已被删除，暂时无法对话');
				}else if(data.is_subscribed === 0){
					W.getErrorHintView().show('用户已经取消对你的关注，无法与他对话');
				}else{
					window.location.href="/message/session_history/show/?"+session_history+"&return_path=customer&nav_name=customer-management";
				}
			},
			error: function(resp) {
			},
			scope: this
		});
	},

	render: function() {
		var context = this.model.toJSON();

		var customerDom = $.tmpl(this.oneCustomerTemplate, context);
		$(this.el).append(customerDom);

		this.trigger('render');
		return this;
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
					ids: this.model.get('id'),
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
	},

	remove: function() {
		var _this = this;
		this.$el.slideUp('fast', function() {
			_this.$el.remove();
		});
		this.$el.unbind();
	},

	/**
	 * 响应model的isSelected属性的change事件, 更新头像右下角的选中状态
	 * @param model
	 */
	selectHandler: function(model) {
		var isSelected = model.get('isSelected');
		this.$('.customer_checkeBox').attr('checked', isSelected);
	},

	/**
	 * 响应左侧头像右下角的选中事件，更新model的isSelected属性
	 * @param event
	 */
	selectCustomer: function(event) {
		var oldValue = this.model.get('isSelected');
		this.model.set({'isSelected': !oldValue});
	},

	clear: function(){
		this.customerInfomactions.reset([])
		this.$el.find('li').remove();
	}

});
