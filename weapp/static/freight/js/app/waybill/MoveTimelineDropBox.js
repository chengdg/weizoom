/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
W.ExpressModels = W.ApiCollection.extend({
	dataCache: null,

	url: function() {
		var appName = 'express/companies/get';
		var url = W.getApi().getUrl('tools', appName);
		return url;
	},

	editJson: function(data) {
		var i, k, name;
		for(i = 0, k = data.length; i<k; i++) {
			name = data[i].name;
			data[i].name = name;
		}
		return data;
	},

	parse: function(resp) {
		var data = resp.data;
		this.dataCache = data;
		return this.dataCache;
	}
});

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
		this.collection = new W.ExpressModels();
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

		this.$el.css({
			margin: '10px 0px 0 50px'
		})
	},

	addShowGroup: function(event) {
		if (!W.validate()) {
			return false;
		}
		var group_name = this.$el.find('#group_name').val();
		W.getApi().call({
			app: 'ft/waybill',
			api: 'express/add',
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
W.getMoveTimeLineDropBox = function(options) {
	var view = W.registry['MoveTimelineDropBox'];
	if (!view) {
		xlog('create W.MoveTimelineDropBox');
		view = new W.MoveTimelineDropBox(options);
		W.registry['MoveTimelineDropBox'] = view;
	}

	return view;
};