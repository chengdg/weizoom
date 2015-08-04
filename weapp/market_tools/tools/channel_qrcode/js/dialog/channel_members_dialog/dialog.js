/*
Copyright (c) 2011-2012 Weizoom Inc
*/

ensureNS('W.webapp.markettools');
ensureNS('W.webapp.markettools.channel_qrcode');
W.webapp.markettools.channel_qrcode.ChannelMember = Backbone.Model.extend({

});

W.webapp.markettools.channel_qrcode.ChannelMembers = W.ApiCollection.extend({
    model: W.webapp.markettools.channel_qrcode.ChannelMember,
    app: 'market_tools/channel_qrcode',

    initialize: function(models, options) {
    },

    url: function() {
        var _this = this;
        return this.getApiUrl('channel_members/get', {
                setting_id: _this.settingId
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
ensureNS('W.weapp.markettools.channel_qrcode.dialog.ChannelMembersDialog');
W.weapp.markettools.channel_qrcode.dialog.ChannelMembersDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#channel-members-dialog-tmpl-src').template('channel-members-dialog-tmpl');
        return "channel-members-dialog-tmpl";
    },

    getOneMemberTemplate: function() {
        $('#channel-members-dialog-one-member-tmpl-src').template('channel-members-dialog-one-member-tmpl');
        return 'channel-members-dialog-one-member-tmpl';
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
        this.settingId = options.settingId;
        this.channelMembers = new W.webapp.markettools.channel_qrcode.ChannelMembers();
        this.channelMembers.settingId = this.settingId;
        this.channelMembers.bind('add', this.onAdd, this);
        this.channelMembers.fetch();
        this.$dialog.find('.modal-body').html($.tmpl(this.tmplName, options));
    }
});