/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 会员关系对话框
 */
ensureNS('W.weapp.dialog.UserCenterRelationsDialog');
W.weapp.dialog.UserCenterRelationsDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'change select': 'onChangeProjectType',
        'click .show_fans': 'onClickShowFansCheckbox'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#usercenter-relations-dialog-tmpl-src').template('usercenter-relations-dialog-tmpl');
        return "usercenter-relations-dialog-tmpl";
    },

    getOneRelationTemplate: function() {
        $('#usercenter-relations-dialog-one-relation-tmpl-src').template('usercenter-relations-dialog-one-relation-tmpl');
        return 'usercenter-relations-dialog-one-relation-tmpl';
    },

    onInitialize: function(options) {
        options = options || {};
        this.typeTextCount = 300;
        this.appName = options.appName;
        this.onlyFans = false;
        this.memberId = options.memberId;
        this.friendCount = options.friendCount;
        this.fansCount = options.fansCount;
         $('.friend_count').text(this.friendCount);
        $('.fans_count').text(this.fansCount);
        console.log('0000000000000000',$('.friend_count'));
        console.log($('.fans_count'));
    },

    onAdd: function(relation){
        this.$('.modal-body').prepend($.tmpl(this.getOneRelationTemplate(), relation.toJSON()));
    },

    onShow: function(options) {
        this.memberId = options.memberId;
        this.relations = new W.webapp.usercenter.Relations();
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