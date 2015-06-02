/*
Copyright (c) 2011-2012 Weizoom Inc
*/

//TODO 和会员中心的关系dialog合并

ensureNS('W.webapp.markettools');
ensureNS('W.webapp.markettools.vote');
W.webapp.markettools.vote.VotedMember = Backbone.Model.extend({

});

W.webapp.markettools.vote.VotedMembers = W.ApiCollection.extend({
    model: W.webapp.markettools.vote.VotedMember,
    app: 'market_tools/vote',

    initialize: function(models, options) {
    },

    url: function() {
        var _this = this;
        return this.getApiUrl('voted_members/get', {
                vote_option_id: _this.voteOptionId
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
ensureNS('W.weapp.markettools.vote.dialog.VotedMembersDialog');
W.weapp.markettools.vote.dialog.VotedMembersDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#voted-members-dialog-tmpl-src').template('voted-members-dialog-tmpl');
        return "voted-members-dialog-tmpl";
    },

    getOneMemberTemplate: function() {
        $('#voted-members-dialog-one-member-tmpl-src').template('voted-members-dialog-one-member-tmpl');
        return 'voted-members-dialog-one-member-tmpl';
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
        this.voteOptionId = options.voteOptionId;
        this.votedMembers = new W.webapp.markettools.vote.VotedMembers();
        this.votedMembers.voteOptionId = this.voteOptionId;
        this.votedMembers.bind('add', this.onAdd, this);
        this.votedMembers.fetch();
        this.$dialog.find('.modal-body').html($.tmpl(this.tmplName, options));
    }
});