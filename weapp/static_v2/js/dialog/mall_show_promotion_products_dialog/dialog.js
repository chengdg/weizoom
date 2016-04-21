/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择促销商品对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.ShowCouponProductsDialog = W.dialog.Dialog.extend({
    events: _.extend({
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#mall-show-coupon-products-dialog-tmpl-src').template('mall-show-coupon-products-dialog-tmpl');
        return "mall-show-coupon-products-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        this.promotionId = options.promotionId;
    },

    beforeShow: function() {
        this.table.reset({
            id: this.promotionId
        });
    },

    onShow: function(options) {
        this.promotionId = options.promotionId;
    },

    afterShow: function(options) {
        this.table.reload({
            id: this.promotionId
        });
    },

    onGetData: function(options) {
    }
});


