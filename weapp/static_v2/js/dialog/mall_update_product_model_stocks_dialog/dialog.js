/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 定制商品规格的对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.UpdateProductModelStocksDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click input[type="text"]': 'onClickStocksInput',
        'click input[type="radio"]': 'onClickStockTypeRadio'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#mall-update-product-model-stocks-dialog-tmpl-src').template('mall-update-product-model-stocks-dialog-tmpl');
        return "mall-update-product-model-stocks-dialog-tmpl";
    },

    getTableTemplate: function() {
        $('#mall-update-product-model-stocks-dialog-table-tmpl-src').template('mall-update-product-model-stocks-dialog-table-tmpl');
        return "mall-update-product-model-stocks-dialog-table-tmpl";
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

    onClickStocksInput: function(event) {
        event.stopPropagation();
        event.preventDefault();
        var $radio = $(event.currentTarget).siblings('input[type="radio"]');
        $radio.prop('checked', true);
    },

    onClickStockTypeRadio: function(event) {
        var $radio = $(event.currentTarget);
        // var re = /^\d+$/;
        if ($radio.val() === 'unlimit') {
            tmp = $radio.parents(".radio").next().find('.xa-stocksInput').val();
            $radio.parents(".radio").next().find('.xa-stocksInput').css('visibility', 'hidden');
            $radio.parents(".radio").next().find('.errorHint').text("");
            $radio.parents('td').find('.xa-stocksInput').val(0);
        } else {
            $radio.parents('td').find('.xa-stocksInput').css('visibility', 'visible')
            // if (re.test(tmp)) {
            //    $radio.parents('td').find('.xa-stocksInput').val('').focus().val(tmp);
            //} else {
                $radio.parents('td').find('.xa-stocksInput').val('').focus().val(0);
            // }
        }
    },

    onGetData: function(options) {
        if(!W.validate($("#mallUpdateProductModelStocksDialog"))) {
            return false;
        }
        var data = [];

        this.$('tbody tr').each(function() {
            xlog('in tr');
            var $tr = $(this);
            var propertyValueId = $tr.data('propertyValueId');
            var type = $tr.find('input[type="radio"]:checked').val();
            var value = $tr.find('input[type="text"]').val();
            data.push({
                id: propertyValueId,
                stock_type: type,
                stocks: value
            })
        })

        return data;
    }
});
