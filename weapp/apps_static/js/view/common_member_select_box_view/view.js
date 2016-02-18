/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 会员选择
 * @class
 */
ensureNS('W.view.common');
W.view.common.SelectDataForMemberView = Backbone.View.extend({
    el: '',

    events: {
        'click .xa-rightMove': 'onRightMoveButton',
        'click .xa-leftMove': 'onLeftMoveButton',
	    'click .xa-allRightMove': 'onAllRightMoveButton',
	    'click .xa-allLeftMove': 'onAllLeftMoveButton'
    },

    getTemplate: function(){
        $('#select-view-tmpl-src').template('select-box-view-tmpl');
        return 'select-box-view-tmpl';
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.template = this.getTemplate();
        this.options = options;
        this.app = options.app;
        this.api = options.api;
    },

    render: function() {
    	var _this = this;
        this.$el.html($.tmpl(this.template));
        this.leftMemberListView = new W.view.common.DataForMemberListView({
			el: this.$el.find('.left-data-list'),
			title: _this.options.leftTitle,
			app: this.app,
			api: this.api,
			oneTemplate: this.options.oneTemplate,
			args: $.parseJSON(this.options.args),
			search_data: this.options.search_data
		});
		this.leftMemberListView.bind('moveRightBox', function() {
	    	_this.trigger('moveRightView');
	    });
		this.rightMemberListView = new W.view.common.DataForMemberListView({
			el: this.$el.find('.right-data-list'),
			title: _this.options.rightTitle,
			oneTemplate: this.options.oneTemplate,
			search_data: this.options.search_data
		});
        return this;
    },
    
	onRightMoveButton: function(){
		var models = this.leftMemberListView.getSelectCheck(false);
		this.leftMemberListView.removeModels(models);
		this.rightMemberListView.addModels(models);
	},

	onLeftMoveButton: function(){
		var models = this.rightMemberListView.getSelectCheck(false);
		this.rightMemberListView.removeModels(models);
		this.leftMemberListView.addModels(models);
	},

	onAllRightMoveButton: function(){
		xlog('onAllRightMoveButton')
		var models = this.leftMemberListView.getSelectCheck(true);
		this.leftMemberListView.removeModels(models);
		this.rightMemberListView.addModels(models);
	},

	onAllLeftMoveButton: function(){
		xlog('onAllLeftMoveButton');
		var models = this.rightMemberListView.getSelectCheck(true);
		this.rightMemberListView.removeModels(models);
		this.leftMemberListView.addModels(models);
	}
});

/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 会员
 */

W.SelectDataForMemberModel = Backbone.Model.extend({
	isShow: true,
	
	initialize: function(){
	}
})


/**
 * 等级对应的会员
 */

W.SelectDataForMembers = W.ApiCollection.extend({
    model: W.SelectDataForMemberModel,

    initialize: function(options) {
    	this.app = options.app;
    	this.api = options.api || '';
    	this.args = options.args || {};
    },

    url: function() {
        var _this = this;
        return this.getApiUrl(_this.api, _this.args);
    },

    parse: function(response){
        var data = response.data;
        if(!data) {
            return [];
        }
        this.trigger('moveRight');
        return data.items;
    }
});



/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 会员列表
 * @class
 */
W.view.common.DataForMemberListView = Backbone.View.extend({
    el: '',

    events: {
	    'keydown [name="search_member"]': 'onEnterEvent',
        'click .xa-searchMemberButton': 'onSearchBtn'
    },

    getTemplate: function(){
        $('#select-data-for-member-list-view-tmpl-src').template('select-data-for-member-list-view-tmpl');
        return 'select-data-for-member-list-view-tmpl';
    },

	getOneMemberTemplate: function(){
		// $('#one-select-data-for-member-view-tmpl-src').template('one-select-data-for-member-view-tmpl');
		$(this.oneTemplate).template('one-select-data-for-member-view-tmpl');
		return 'one-select-data-for-member-view-tmpl';
	},

    initialize: function(options) {
        this.$el = $(this.el);
        this.options = options || {};
        this.template = this.getTemplate();
        this.oneTemplate = options.oneTemplate;
	    this.oneMemberTemplate = this.getOneMemberTemplate();
		this.render();
        //创建collection对象，绑定其add事件
        this.dataForMembers = new W.SelectDataForMembers({
        	app: options.app,
        	api: options.api,
        	args: options.args || {}
        });
	    this.dataForMembers.bind('add', this.onAdd, this);
	    this.dataForMembers.bind('remove', this.removeOne, this);
	    this.refresh();
	    var _this = this;
	    this.dataForMembers.bind('moveRight', function() {
	    	_this.trigger('moveRightBox');
	    })
    },

    render: function() {
        this.$el.html($.tmpl(this.template, {title: this.options.title || '列表'}));
	    this.$container = this.$('.data_list_div').find('ul');
        // return this;
    },

    refresh: function(){
    	var _this = this;
    	if (this.options.app) {
			 this.dataForMembers.fetch({
			 	add: true,
			 	success: function() {
			 		if (_this.dataForMembers.length===0){
			 			var $li = $('<li>暂无数据</li>');
			 			_this.$container.append($li);
			 		}
			 	}
			 });
		 } else {
		 	this.dataForMembers.remove(this.dataForMembers.models[0]);
		 }
    },


    /**
     * 接收到一条item时的响应函数
     */
    onAdd: function(item) {
    	var isShow = item['isShow'] || false;
    	if (isShow) {
			this.$container.prepend($.tmpl(this.oneMemberTemplate, item.toJSON()));
		}
    },

    /**
     * 将一条消息从页面上移除
     */
    removeOne: function(item) {
	    this.$container.find('li[data-id="'+item.get('id')+'"]').remove();
    },

	getSelectCheck: function(isAll){
		var models = new Array();
		var _this = this;
		var findStr = "input[name='member_check']:checked";
		if(isAll){
			findStr = "input[name='member_check']";
		}
		this.$(findStr).each(function () {
			var model = _this.dataForMembers.get(this.value);
			models.push(model);
		});
		return models
	},

	removeModels: function(models){
		var _this = this;
		for(var i=0; i<models.length; i++){
			var item = models[i];
			_this.dataForMembers.remove(item);
		}
	},

	addModels: function(models){
		var _this = this;
		for(var i=0; i<models.length; i++){
			var item = models[i];
			_this.dataForMembers.add(item);
		}
	},

	onSearchBtn: function(){
		var search_value = this.$('input[name="search_member"]').val().trim();
		var _this = this;
		this.dataForMembers.each(function(item){
			var name = _this.options.search_data || 'name';
			var username = item.get(name) || item[name] || '';
			if(search_value == ''){
				item.isShow = true;
			}else if(username.toLowerCase().indexOf(search_value.toLowerCase()) >= 0)	{
				item.isShow = true;
			}else{
				item.isShow = false;
			}
		});
		this.refresh_list();
	},

	refresh_list: function(){
		var _this = this;
		this.$container.html('');
		this.dataForMembers.each(function(item){
			_this.onAdd(item);
		});
	},

	onEnterEvent: function(event){
		if (event.keyCode == "13") {//keyCode=13是回车键
			event.stopPropagation();
			event.preventDefault();
			this.onSearchBtn();
		}
	}
	
});

W.registerUIRole('div[data-ui-role="select-box-for-member-view"]', function() {
    var $div = $(this);
	var url = $div.attr('data-url');
	var app = $div.attr('data-app');
	var api = $div.attr('data-api');
	var title = $div.attr('data-title');
	var args = $div.attr('data-args');
	var search_data = $div.attr('data-search-data');
	var titles = title.split(';');
	var oneTemplate = $div.attr('data-one-template') || '#one-select-data-for-member-view-tmpl-src';
    var selectView = new W.view.common.SelectDataForMemberView({
        el: $div[0],
        app: app,
        api: api,
        url: url,
        search_data: search_data,
        leftTitle: titles[0],
        rightTitle: titles[1] || '己选',
        oneTemplate: oneTemplate,
        args: args
    });
    selectView.render();
    $div.data('view', selectView);
});