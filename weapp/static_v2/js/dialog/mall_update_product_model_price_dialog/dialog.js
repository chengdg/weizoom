/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 定制商品规格的对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.UpdateProductModelPriceDialog = W.dialog.Dialog.extend({
    events: _.extend({
        // 'click input[type="text"]': 'onClickStocksInput',
        // 'click input[type="radio"]': 'onClickStockTypeRadio'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#mall-update-product-model-price-dialog-tmpl-src').template('mall-update-product-model-price-dialog-tmpl');
        return "mall-update-product-model-price-dialog-tmpl";
    },

    getTableTemplate: function() {
        $('#mall-update-product-model-price-dialog-table-tmpl-src').template('mall-update-product-model-price-dialog-table-tmpl');
        return "mall-update-product-model-price-dialog-table-tmpl";
    },

    onInitialize: function(options) {
        this.tableTemplate = this.getTableTemplate();
    },

    beforeShow: function(options) {
        this.$('.modal-body').empty();
    },

    onShow: function(options) {
        var models = options.models;
        var properties = _.pluck(models[0].property_values, 'propertyName');
        var $node = $.tmpl(this.tableTemplate, {properties: properties, models: models});
        this.$('.modal-body').append($node);
    },

    // onClickStocksInput: function(event) {
    //     event.stopPropagation();
    //     event.preventDefault();
    //     var $radio = $(event.currentTarget).siblings('input[type="radio"]');
    //     $radio.prop('checked', true);
    // },

    onGetData: function(options) {
        if(!W.validate($("#mallUpdateProductModelPriceDialog"))) {
            return false;
        }
        var data = [];

        this.$('tbody tr').each(function() {
            xlog('in tr');
            var $tr = $(this);
            var propertyValueId = $tr.data('propertyValueId');
            var value = $tr.find('input[type="text"]').val();
            data.push({
                id: propertyValueId,
                price: value
            })
        })

        return data;
    }
});
