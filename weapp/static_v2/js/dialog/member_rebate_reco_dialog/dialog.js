ensureNS('W.dialog.mall');

W.dialog.mall.MemberReabteRecoDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-prev-month': 'onClickPrevMonth',
        'click .xa-next-month': 'onClickNextMonth',
        'blur .xa-month-input': 'onBlurPrevMonth',
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#member-reco-rebate-dialog-tmpl-src').template('member-reco-rebate-dialog-tmpl');
        return 'member-reco-rebate-dialog-tmpl';
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
    },

    onClickPrevMonth: function() {
        var curMonth = parseInt($('.xa-month-input').val()) - 1;
        curMonth = curMonth == 0 ? 12 : curMonth;
        $('.xa-month-input').val(curMonth);
        this.table.reload({'member_id': this.memberId, 'rebate_type': this.rebateType, 'month': curMonth});
    },

    onClickNextMonth: function() {
        var curMonth = parseInt($('.xa-month-input').val()) + 1;
        curMonth = curMonth == 13 ? 1 : curMonth;
        $('.xa-month-input').val(curMonth);
        this.table.reload({'member_id': this.memberId, 'rebate_type': this.rebateType, 'month': curMonth});
    },

    onBlurPrevMonth: function() {
        var curMonth = parseInt($('.xa-month-input').val());
        if (curMonth < 1 || curMonth > 12) {
            W.showHint('error', '请输入1~12');
            return;
        }
        this.table.reload({'member_id': this.memberId, 'rebate_type': this.rebateType, 'month': curMonth});
    }
});