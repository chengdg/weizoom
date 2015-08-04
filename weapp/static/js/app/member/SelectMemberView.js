/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 会员选择
 * @class
 */
W.SelectMemberView = Backbone.View.extend({
    el: '',

    events: {
        'click #right-move': 'onRightMoveButton',
        'click #left-move': 'onLeftMoveButton',
	    'click #all-right-move': 'onAllRightMoveButton',
	    'click #all-left-move': 'onAllLeftMoveButton'
    },

    getTemplate: function(){
        $('#select-member-list-tmpl-src').template('select-member-list-tmpl');
        return 'select-member-list-tmpl';
    },

    initialize: function(options) {
        this.$el = $(this.el);
		this.isShowOtherMember = options.isShowOtherMember;
        this.template = this.getTemplate();
	    this.render();

	    this.grade_id = options.grade_id || 0;
	    this.target_grade_id = options.target_grade_id || 0;
		if(this.isShowOtherMember == true){
			this.leftMemberListView = new W.MemberListView({
				el: '.left-member-list',
				grade_id: this.grade_id,
				memberListTitle: '普通会员'
			});
			this.rightMemberListView = new W.MemberListView({
				el: '.right-member-list',
				grade_id: this.target_grade_id,
				memberListTitle: '本组会员'
			});
		} else {
			this.leftMemberListView = new W.MemberListView({
				el: '.left-member-list',
				grade_id: this.grade_id,
				memberListTitle: '普通会员'
			});
			this.$('.center-button').hide();
			this.leftMemberListView.$el.find("input[name='member_check']").hide();
		}

    },

    render: function() {
        this.$el.html($.tmpl(this.template,{'isShowOtherMember': this.isShowOtherMember}));
        return this;
    },

    refresh: function(){
        xlog('refresh SwipePhotoList');
        this.swipePhoto.fetch();
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
		xlog('onAllLeftMoveButton')
		var models = this.rightMemberListView.getSelectCheck(true);
		this.rightMemberListView.removeModels(models);
		this.leftMemberListView.addModels(models);
	},

	getSaveMemberIds: function(){
		var memberIds = new Array();
		this.rightMemberListView.members.each(function(item){
			memberIds.push(item.get('id'));
		})
		return memberIds;
	}
});