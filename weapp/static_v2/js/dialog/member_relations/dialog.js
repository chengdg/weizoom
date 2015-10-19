/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 会员关系对话框
 */
ensureNS('W.member.dialog.UserCenterRelationsDialog');
W.member.dialog.UserCenterRelationsDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'change select': 'onChangeProjectType',
        'click .show_fans': 'onClickShowFansCheckbox'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#member-relations-dialog-tmpl-src').template('member-relations-dialog-tmpl');
        return "member-relations-dialog-tmpl";
    },

    getOneRelationTemplate: function() {
        $('#member-relations-dialog-one-relation-tmpl-src').template('member-relations-dialog-one-relation-tmpl');
        return 'member-relations-dialog-one-relation-tmpl';
    },

    onInitialize: function(options) {

        this.$dialog.find('.modal-body').html('');
        $('.friend_count').text('');
        $('.fans_count').text('');
        options = options || {};
        this.typeTextCount = 300;
        this.appName = options.appName;
        this.onlyFans = false;
        this.memberId = options.memberId;
        this.friendCount = options.friendCount;
        this.fansCount = options.fansCount;
        
    },

    onAdd: function(relation){
        this.$('.modal-body').prepend($.tmpl(this.getOneRelationTemplate(), relation.toJSON()));
    },

    onShow: function(options) {
        this.friendCount = options.friendCount;
        this.fansCount = options.fansCount;
         $('.friend_count').text(this.friendCount);
        $('.fans_count').text(this.fansCount);

        this.memberId = options.memberId;
        this.relations = new W.member.Relations();
        this.relations.onlyFans =  this.onlyFans;
        this.relations.memberId = this.memberId;
        this.relations.bind('add', this.onAdd, this);
        this.relations.fetch();
        this.$dialog.find('.modal-body').html($.tmpl(this.tmplName, options));


    },

    //bert add
    onClickShowFansCheckbox: function(event){
        var $currentTarget = $(event.currentTarget);   
        var is_checked = $currentTarget.is(':checked');

        if (is_checked){
            this.onlyFans = true;
        }else{
            this.onlyFans = false;
        }
        this.onShow(this);

    }
});

/*
ensureNS('W.member.dialog.MemberDetailRelationsDialog');
W.member.dialog.MemberDetailRelationsDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'change select': 'onChangeProjectType',
        'click .show_fans': 'onClickShowFansCheckbox'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#member-detail-relations-dialog-tmpl-src').template('member-detail-relations-dialog-tmpl');
        return "member-detail-relations-dialog-tmpl";
    },

    getOneRelationTemplate: function() {
        $('#member-relations-dialog-one-relation-tmpl-src').template('member-relations-dialog-one-relation-tmpl');
        return 'member-relations-dialog-one-relation-tmpl';
    },

    onInitialize: function(options) {
        this.$dialog.find('.modal-body').html('');

        options = options || {};
        this.typeTextCount = 300;
        this.appName = options.appName;
        this.memberId = options.memberId;
        this.dataValue = options.dataValue;
        console.log(this.dataValue)
    },

    onAdd: function(relation){
        this.$('.modal-body').prepend($.tmpl(this.getOneRelationTemplate(), relation.toJSON()));
    },

    onShow: function(options) {
        this.friendCount = options.friendCount;
        this.fansCount = options.fansCount;
        this.dataValue = options.dataValue;
        this.memberId = options.memberId;
        this.relations = new W.member.Relations();
        this.relations.memberId = this.memberId;
        this.relations.dataValue = this.dataValue;
        this.relations.bind('add', this.onAdd, this);
        this.relations.fetch();
        this.$dialog.find('.modal-body').html($.tmpl(this.tmplName, options));

    },

    //bert add
    onClickShowFansCheckbox: function(event){
        var $currentTarget = $(event.currentTarget);   
        var is_checked = $currentTarget.is(':checked');

        if (is_checked){
            this.onlyFans = true;
        }else{
            this.onlyFans = false;
        }
        this.onShow(this);

    }
});
*/


ensureNS('W.member.dialog.MemberDetailRelationsDialog');
W.member.dialog.MemberDetailRelationsDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'change select': 'onChangeProjectType',
        'click .show_fans': 'onClickShowFansCheckbox'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#member-detail-relations-dialog-tmpl-src').template('member-detail-relations-dialog-tmpl');
        return "member-detail-relations-dialog-tmpl";
    },
/*
    getOneRelationTemplate: function() {
        $('#member-relations-dialog-one-relation-tmpl-src').template('member-relations-dialog-one-relation-tmpl');
        return 'member-relations-dialog-one-relation-tmpl';
    },
*/
    onInitialize: function(options) {
        this.getTemplate();
        this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
        options = options || {};
        this.typeTextCount = 300;
        this.appName = options.appName;
        this.memberId = options.memberId;
        this.dataValue = options.dataValue;
        console.log(this.dataValue)
    },
/*
    onAdd: function(relation){
        this.$('.modal-body').prepend($.tmpl(this.getOneRelationTemplate(), relation.toJSON()));
    },
*/
    onShow: function(options) {
        this.friendCount = options.friendCount;
        this.fansCount = options.fansCount;
        this.dataValue = options.dataValue;
        this.memberId = options.memberId;
        /*
        this.relations = new W.member.Relations();
        */
        // this.relations.memberId = this.memberId;
        // this.relations.dataValue = this.dataValue;
        // this.relations.bind('add', this.onAdd, this);
        // this.relations.fetch();
        // this.$dialog.find('.modal-body').html($.tmpl(this.tmplName, options));
        var _this = this;
        if (!_this.table) {
            _this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
        }
        if (options.isReload == true && _this.table) {
            _this.table.curPage = 1;
        }
        $('#member-detail-relations-dialog-tmpl-src').html('');
        _this.table.reload({data_value:_this.dataValue,member_id:this.memberId});
    },

    //bert add
    onClickShowFansCheckbox: function(event){
        var $currentTarget = $(event.currentTarget);   
        var is_checked = $currentTarget.is(':checked');

        if (is_checked){
            this.onlyFans = true;
        }else{
            this.onlyFans = false;
        }
        this.onShow(this);

    }
});



/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 详情影响力
 */

ensureNS('W.member');
W.member.Relation = Backbone.Model.extend({

})


/**
 * 详情影响力s
 */

W.member.Relations = W.ApiCollection.extend({
    model: W.member.Relation,
    app: 'member',
    method:'post',

    initialize: function(models, options) {

    },

    url: function() {
        var _this = this;
        var onlyFans = 0;
        if (_this.onlyFans){
            onlyFans = 1;
        }

        if (_this.dataValue) {
            return this.getApiUrl('follow_relations',{data_value:_this.dataValue,member_id:this.memberId});
        } else { 
        //return this.getApiUrl('follow_relations/'+_this.memberId+'/'+onlyFans);
            return this.getApiUrl('follow_relations',{member_id:this.memberId,only_fans:onlyFans});
        }
    },

    parse: function(response){
        var data = response.data;
        if(!data) {
            return [];
        }
        return data.items;
    }
});

