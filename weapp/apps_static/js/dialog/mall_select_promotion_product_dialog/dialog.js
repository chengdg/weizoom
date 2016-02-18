/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择促销商品对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.SelectPromotionProductDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectProduct': 'onSelectProduct'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#mall-select-promotion-product-dialog-tmpl-src').template('mall-select-promotion-product-dialog-tmpl');
        return "mall-select-promotion-product-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function() {
        this.table.reset();
    },

    onShow: function(options) {
        this.name = options.name;
        this.barCode = options.barCode;
        this.enableMultiSelection = false;
        this.selectedProductIds = options.selectedProductIds || [];
        if (options.hasOwnProperty('enableMultiSelection')) {
            this.enableMultiSelection = options.enableMultiSelection;
        }
    },

    afterShow: function(options) {
        this.table.reload({
            "name": this.name,
            "barCode": this.barCode || "",
            "selectedProductIds": this.selectedProductIds.join('_')
        });
    },

    onSelectProduct: function(event) {
        var $checkbox = $(event.currentTarget);
        if (!this.enableMultiSelection) {
            var $label = this.$('label.checked');
            $label.find('input').prop('checked', false);
            $label.removeClass('checked');
            if($checkbox.parent().hasClass('checked')){
                $checkbox.parent('.checked').find('span').text('已选择');
            }else{
                $checkbox.parents('tr').siblings().find('label span').text('选取');
            }
        }
        if ($checkbox.is(':checked')) {
            $checkbox.parent().addClass('checked');
            $checkbox.parent('.checked').find('span').text('已选择');
        } else {
            $checkbox.parent().removeClass('checked');
            $checkbox.parent().find('span').text('选取');
        }
    },

    onGetData: function(options) {
        var data = [];
        var _this = this;

        this.$('tbody tr').each(function() {
            var $tr = $(this);
            if ($tr.find('.xa-selectProduct').is(':checked')) {
                var productId = $tr.data('id');
                data.push(_this.table.getDataItem(productId).toJSON());
            }
        })

        return data;
    }
});

W.dialog.mall.SelectForbiddenCouponProductDialog = W.dialog.mall.SelectPromotionProductDialog.extend({
    events: _.extend({
    }, W.dialog.mall.SelectPromotionProductDialog.prototype.events),
    getTemplate: function() {        
        $('#mall-select-forbiddenCoupon-product-dialog-tmpl-src').template('mall-select-forbiddenCoupon-product-dialog-tmpl');
        return "mall-select-forbiddenCoupon-product-dialog-tmpl";
    }
});
