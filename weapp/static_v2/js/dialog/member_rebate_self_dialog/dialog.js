ensureNS('W.dialog.mall');

W.dialog.mall.MemberReabteSelfDialog = W.dialog.Dialog.extend({
    events: _.extend({}, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#member-self-rebate-dialog-tmpl-src').template('member-self-rebate-dialog-tmpl');
        return 'member-self-rebate-dialog-tmpl';
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function(options) {
        this.memberId = options.memberId;
        this.rebateType = options.rebateType;
        this.table.reset();
    },
    
    onShow: function(options) {
        this.table.reload({'member_id': this.memberId, 'rebate_type': this.rebateType});
    }
});