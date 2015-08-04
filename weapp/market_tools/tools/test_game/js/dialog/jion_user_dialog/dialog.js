/*
Copyright (c) 2011-2012 Weizoom Inc
*/

//TODO 和会员中心的关系dialog合并

ensureNS('W.webapp.markettools');
ensureNS('W.webapp.markettools.test_game');
W.webapp.markettools.test_game.joinMember = Backbone.Model.extend({

});

W.webapp.markettools.test_game.joinMembers = W.ApiCollection.extend({
    model: W.webapp.markettools.test_game.joinMember,
    app: 'market_tools/test_game',

    initialize: function(models, options) {
    },

    url: function() {
        var _this = this;
        return this.getApiUrl('join_users/get', {
                game_id: _this.gameId
            });
    },

    parse: function(response){
        var data = response.data;
        if(!data) {
            return [];
        }
        return data.items;
    }
});

/**
 * 会员列表对话框
 */
ensureNS('W.weapp.markettools.test_game.dialog.JoinUsersDialog');
W.weapp.markettools.test_game.dialog.JoinUsersDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#join-users-dialog-tmpl-src').template('jion-users-dialog-tmpl');
        return "jion-users-dialog-tmpl";
    },

    getOneMemberTemplate: function() {
        $('#join-users-dialog-one-member-tmpl-src').template('join-users-dialog-one-member-tmpl');
        return 'join-users-dialog-one-member-tmpl';
    },

    onInitialize: function(options) {
        options = options || {};
        this.typeTextCount = 300;
        this.appName = options.appName;
    },

    onAdd: function(member) {
        this.$('.modal-body').prepend($.tmpl(this.getOneMemberTemplate(), member.toJSON()));
    },

    onShow: function(options) {
        this.gameId = options.gameId;
        this.joinMembers = new W.webapp.markettools.test_game.joinMembers();
        this.joinMembers.gameId = this.gameId;
        this.joinMembers.bind('add', this.onAdd, this);
        this.joinMembers.fetch();
        this.$dialog.find('.modal-body').html($.tmpl(this.tmplName, options));
    }
});