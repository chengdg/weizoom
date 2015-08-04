/*
 *Copyright (c) 2011-2012 Weizoom Inc
 *collection集合类--通过全局变量传入
*/
W.MoveTimelineDropBox = W.ListDropBox.extend({
	events:_.extend({
		'click .tx_addGroupButton': 'addShowGroup',
		'click .tx_addGroup': 'showGroupBox'
	}, W.ListDropBox.prototype.events),

	CLICK_ACTIONS_EVENT: 'filter_clickEvent',

	initializePrivate: function(options) {
		this.$el = $(this.el);
		this.collection = new W.MessageTimelineMoves();
		this.errorMsg = '无其它分类,不能修改！';
		this.fetchData();
		this.bind('render', this.isShowHtml, this);
	},

	bindClickEvent: function(options) {
		this.trigger(this.CLICK_ACTIONS_EVENT, options);
	},

	showGroupBox: function(){
		this.$el.find('.tx_addGroup').hide();
		this.$el.find('.tx_groupBox').removeClass('hidden');
		this.$el.find('.errorHint').html('');
		this.$el.find('#group_name').val('');
	},

	showPrivate: function(options) {
		this.isShowAddGroupButton = options.isShowAddGroupButton || false;
		this.isShowAll = options.isShowAll || false;
		this.isShowAddBox = options.isShowAddBox || false;
		this.isShowHtml();
		this.bind(this.ACTIONS_EVENT, this.bindClickEvent, this);
	},

	isShowHtml: function(){
		this.$content.find('li>a').show();

		if(this.isShowAddGroupButton){
			this.$content.find('li.divider').show();
			this.$content.find('li .tx_addGroup').show();
		}else{
			this.$content.find('li.divider').hide();
			this.$content.find('li .tx_addGroup').hide();
		}

		if(this.isShowAll){
			this.$content.find('li.tx_all').show();
		}else{
			this.$content.find('li.tx_all').hide();
		}

		this.$el.find('.tx_groupBox').addClass('hidden');
		if(this.isShowAddBox){
			this.$content.find('li.divider').show();
			this.$el.find('.tx_groupBox').removeClass('hidden');
		}
	},

	addShowGroup: function(event) {
		if (!W.validate()) {
			return false;
		}
		var group_name = this.$el.find('#group_name').val();
		W.getApi().call({
			app: 'customer',
			api: 'group/add',
			method: 'post',
			args: {
				name: group_name
			},
			success: function(data) {
				this.fetchData();
				this.bind('render', this.isShowHtml, this);
			},
			error: function(resp) {
			},
			scope: this
		});

		event.preventDefault();
		event.stopPropagation();
	}
});

/**
 * 获得ReplyMessagesView的单例实例
 * @param {int} width - 宽度
 */
W.getMoveTimelineDropBox = function(options) {
	var view = W.registry['MoveTimelineDropBox'];
	if (!view) {
		xlog('create W.MoveTimelineDropBox');
		view = new W.MoveTimelineDropBox(options);
		W.registry['MoveTimelineDropBox'] = view;
	}

	return view;
};