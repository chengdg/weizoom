ensureNS('W.dialog.mall');

W.dialog.mall.RedEnvelopeDetailDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectCoupon': 'onSelectCoupon',
        'click .xa-up': 'upCounter',
        'click .xa-down': 'downCounter'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#red-envelope-detail-dialog-tmpl-src').template('red-envelope-detail-dialog-tmpl');
        return "red-envelope-detail-dialog-tmpl";
    }
});