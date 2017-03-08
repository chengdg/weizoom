ensureNS('W.dialog.mall');

W.dialog.mall.MemberSpreadVipDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-valid-vip': 'onClickValidVip',
        'click .xa-invalid-vip': 'onClickInvalidVip'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#member-spread-vip-dialog-tmpl-src').template('member-spread-vip-dialog-tmpl');
        return 'member-spread-vip-dialog-tmpl';
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function(options) {
        this.memberId = options.memberId;
        this.table.reset();
    },
    
    onShow: function(options) {
        this.table.reload({'member_id': this.memberId, 'member_type': 'valid'});
    },
    
    afterShow: function(options) {
    },

    onClickValidVip: function(options) {
        $('.xa-invalid-vip').removeClass('active');
        $('.xa-valid-vip').addClass('active');
        this.table.reload({'member_id': this.memberId, 'member_type': 'valid'});
    },

    onClickInvalidVip: function(options) {
        $('.xa-valid-vip').removeClass('active');
        $('.xa-invalid-vip').addClass('active');
        this.table.reload({'member_id': this.memberId, 'member_type': 'invalid'});
    }
});