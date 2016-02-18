/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择批量发货的对话框
 *
 * author: robert
 */
ensureNS('W.dialog.common');

W.dialog.common.OrderResultBatchDeliverDialog = W.dialog.Dialog.extend({

    getTemplate: function() {
        $('#common-order-result-batch-deliver-dialog-tmpl-src').template('common-order-result-batch-deliver-dialog-tmpl');
        return "common-order-result-batch-deliver-dialog-tmpl";
    },

    getOrderInfoTemplate: function() {
        $('#mall-order-info-dialog-products-tmpl-src').template('mall-order-info-dialog-products-tmpl');
        return "mall-order-info-dialog-products-tmpl";
    },

    getOrderCountTemplate: function() {
        $('#mall-order-count-dialog-products-tmpl-src').template('mall-order-count-dialog-products-tmpl');
        return "mall-order-count-dialog-products-tmpl";
    },

    onInitialize: function(options) {
        this.orderInfoTemplate = this.getOrderInfoTemplate();
        this.orderCountTemplate = this.getOrderCountTemplate();
    },

    onShow: function(options) {
        this.reloadErrorOrders(options.data);
        //this.reloadCountOrders(options.data);
    },

    afterShow: function(options) {
    },

    onGetData: function(event) {

    },

    reloadCountOrders: function(data) {
        var $ordersCount = $.tmpl(this.orderCountTemplate, {
            'allCount': data.success_count + data.error_count,
            'successCount': data.success_count,
            'errorCount': data.error_count
        });
        this.$('.xa-orderCount').empty().append($ordersCount);
    },

    reloadErrorOrders: function(data) {
        var $ordersCount = $.tmpl(this.orderCountTemplate, {
            'allCount': data.success_count + data.error_count,
            'successCount': data.success_count,
            'errorCount': data.error_count
        });
        this.$('.xa-orderCount').empty().append($ordersCount);
        var $ordersInfo = $.tmpl(this.orderInfoTemplate, {
            'ordersinfo': data.error_items
        });
        this.$('.xa-orderInfoTable').empty().append($ordersInfo);
    }
});