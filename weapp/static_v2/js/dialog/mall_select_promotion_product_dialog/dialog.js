/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择促销商品对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.SelectPromotionProductDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectProduct': 'onSelectProduct',
        'click .xa-selectData': 'onSelectProduct',
        'click .xa-titleNav': 'onClickTitle',
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#mall-select-promotion-product-dialog-tmpl-src').template('mall-select-promotion-product-dialog-tmpl');
        return "mall-select-promotion-product-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        this.selectedProductIds = options.selectedProductIds || [];
        this.itemType = 'product';
        this.titles = options.title;
        this.setItemType(this.titles);
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
        this.setItemType(this.titles);
        this.onSearch();
    },

    defaultLoad: function () {
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
            if ($tr.find('.xa-selectData').is(':checked')) {
                data.push($tr.data('id'));
            }
        })

        return {
            type: this.itemType,
            data: data
        }
    },

/**
 * 积分增加选择分组 by liupeiyu 
 */
    setItemType: function(title, index){
        if (title) {
            if (index) {
                this.selectedItem = title[index];
                this.itemType = this.selectedItem.type;
            }else{
                this.selectedItem = title[0];
                this.itemType = this.selectedItem.type;
            }
        }
    },

    onClickTitle: function(event){
        var $el = $(event.currentTarget);
        this.itemType = $el.attr('data-nav');
        this.selectedItem = this.getItemByType(this.itemType);
        this.onSearch();
    },

    onSearch: function(event) {
        this.table.curPage = 1;
        if (this.selectedItem) {
            this.table.setApi(this.selectedItem.api);
            this.table.setTemplate(this.selectedItem.template);
        }

        if (this.itemType === 'product') {
            this.defaultLoad();
        } else {
            this.table.reload({});            
        }
    },

    getItemByType: function(type){
        return _.filter(this.titles, function(item) {
            return item.type == type;
        }, this)[0];
    },
});

W.dialog.mall.SelectForbiddenCouponProductDialog = W.dialog.mall.SelectPromotionProductDialog.extend({
    events: _.extend({
    }, W.dialog.mall.SelectPromotionProductDialog.prototype.events),
    getTemplate: function() {        
        $('#mall-select-forbiddenCoupon-product-dialog-tmpl-src').template('mall-select-forbiddenCoupon-product-dialog-tmpl');
        return "mall-select-forbiddenCoupon-product-dialog-tmpl";
    }
});
