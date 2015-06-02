/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 会员列表
 * @class
 */
W.MemberListView = Backbone.View.extend({
    el: '',

    events: {
	    'keydown [name="search_member"]': 'onEnterEvent',
        'click .search_member_button': 'onSearchBtn'
    },

    getTemplate: function(){
        $('#member-list-tmpl-src').template('member-list-tmpl');
        return 'member-list-tmpl';
    },

	getOneMemberTemplate: function(){
		$('#one-member-info-tmpl-src').template('one-member-info-tmpl');
		return 'one-member-info-tmpl';
	},

    initialize: function(options) {
        this.$el = $(this.el);
	    this.memberListTitle = options.memberListTitle
		this.isShowOtherMember = options.isShowOtherMember | true;
        this.template = this.getTemplate();
	    this.oneMemberTemplate = this.getOneMemberTemplate();
		this.render();

        //创建collection对象，绑定其add事件
        this.members = new W.GradeHasMembers();
	    this.members.grade_id = options.grade_id;
        this.members.bind('add', this.onAdd, this);
	    this.members.bind('remove', this.removeOne, this);
	    this.refresh();

    },

    render: function() {
        this.$el.html($.tmpl(this.template,{'isShowOtherMember': this.isShowOtherMember, 'memberListTitle': this.memberListTitle}));
	    this.$container = this.$('.member_list_div').find('ul');
        return this;
    },

    refresh: function(){
        xlog('refresh MemberList');
	    if(parseInt(this.members.grade_id) >= 0){
		    this.members.fetch();
	    }
    },


    /**
     * 接收到一条item时的响应函数
     */
    onAdd: function(item) {
	    if(item.is_show == true){
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
			var model = _this.members.get(this.value);
			if(model.is_show == true){
				models.push(model);
			}
		});
		return models
	},

	removeModels: function(models){
		var _this = this;
		for(var i=0; i<models.length; i++){
			var item = models[i];
			_this.members.remove(item);
		}
	},

	addModels: function(models){
		var _this = this;
		for(var i=0; i<models.length; i++){
			var item = models[i];
			_this.members.add(item);
		}
	},

	onSearchBtn: function(){
		var search_value = this.$('input[name="search_member"]').val().trim();
		this.members.each(function(item){
			if(search_value == ''){
				item.is_show = true;
			}else if(item.get('username').toLowerCase().indexOf(search_value.toLowerCase()) >= 0)	{
				item.is_show = true;
			}else{
				item.is_show = false;
			}
		});
		this.refresh_list();
	},

	refresh_list: function(){
		var _this = this;
		this.$container.html('');
		this.members.each(function(item){
			_this.onAdd(item);
		});
	},

	onEnterEvent: function(event){
		if (event.keyCode == "13") {//keyCode=13是回车键
			event.stopPropagation();
			event.preventDefault();
			xlog('eeee');
			this.onSearchBtn();
		}
	}
});