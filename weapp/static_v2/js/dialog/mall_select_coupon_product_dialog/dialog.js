/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择促销商品对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.SelectCouponProductDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectProduct': 'onSelectProduct',
        'click .xa-search': 'onSearch',
        'keypress .xa-query': 'onPressKey',
        'click .xa-titleNav': 'onClickTitle'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#mall-select-coupon-product-dialog-tmpl-src').template('mall-select-coupon-product-dialog-tmpl');
        return "mall-select-coupon-product-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        this.titles = options.title;
        this.setItemType(this.titles);
    },

    setItemType: function(title, index){
        if (index) {
            this.selectedItem = title[index];
            this.itemType = this.selectedItem.type;
            this.titleName = this.selectedItem.name;
        }else{
            this.selectedItem = title[0];
            this.itemType = this.selectedItem.type;
            this.titleName = this.selectedItem.name;
        }
    },

    beforeShow: function() {
        this.table.reset();
    },

    onShow: function(options) {
        this.enableMultiSelection = false;
        this.selectedProductIds = options.selectedProductIds || [];
        if (options.hasOwnProperty('enableMultiSelection')) {
            this.enableMultiSelection = options.enableMultiSelection;
        };
        this.$el.find('.xa-query').val("");
    },

    afterShow: function(options) {
        this.table.reload({});
    },

    onPressKey: function(event) {
        var keyCode = event.keyCode;
        if (keyCode == 13) {
            this.onSearch(event);
        }
    },

    onSearch: function(event) {
        var query = $.trim(this.$el.find('.xa-query').val());
        this.table.reload({
            filter_name: query
        })
    },

    onClickTitle: function(event){
        var $el = $(event.currentTarget);
        this.itemType = $el.attr('data-nav');
        this.$el.find('.xa-query').val();

        console.log(this.itemType);

        this.selectedItem = this.getItemByType(this.itemType);

        this.onSearch();
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


