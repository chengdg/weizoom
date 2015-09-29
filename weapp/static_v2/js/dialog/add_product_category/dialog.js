/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择轮播图的对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.AddProductCategoryDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-add-product-category-dialog-tmpl-src').template('mall-add-product-category-dialog-tmpl');
        return "mall-add-product-category-dialog-tmpl";
    },

    getProductsTemplate: function() {
        $('#mall-add-product-category-dialog-products-tmpl-src').template('mall-add-product-category-dialog-products-tmpl');
        return "mall-add-product-category-dialog-products-tmpl";
    },

    events: _.extend({
        'keyup .xa-query': 'onPressKeyInQueryInput',
        'click .xa-search': 'onClickSearch',
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.productsTemplate = this.getProductsTemplate();
        this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
    },

    onPressKeyInQueryInput: function(event) {
        var keyCode = event.keyCode;
        if (keyCode == 13) {
            xlog('search');
            this.search();
        }
    },

    onClickSearch: function(event) {
        this.search();
    },

    search: function() {
        var query = $.trim($('.xa-query').val());
        this.table.reload({
            id: this.categoryId,
            name: query
        });
    },

    onShow: function(options) {
	  var $titleInput = this.$el.find('.xa-titleInput');
	  $titleInput.attr('placeholder', '请在此输入商品分组名称');
	  $titleInput.attr('maxlength', 18);
      this.reset();
      this.$('.xa-query').val('');
      this.$('.xa-productTable').empty();

      this.categoryId = options.categoryId || -1;
    },

    createCollection: function(datas, extra) {
        if (extra) {
            _.each(datas, function(data) {
                _.extend(data, extra);
            });
        }

        return new Backbone.Collection(datas);
    },

    afterShow: function(options) {
        this.$dialog.find('input[type="text"]').eq(0).focus();
        this.table.reload({id: this.categoryId})
    },

    /**
     * onClickSubmitButton: 点击“完成”按钮后的响应函数
     */
    onGetData: function(event) {
        var name = $.trim(this.$dialog.find('.xa-titleInput').val());
        var productIds = this.table.getAllSelectedDataIds();
        return {
            "name": name,
            "product_ids": productIds
        };
    },

    /**
     * onClickSubmitButton: 重写点击“确定”按钮后的响应函数，支持successCallback返回值
     */
    onClickSubmitButton: function(event) {
        var data = this.onGetData(event);
        if (data) {
            if(!data.name){
                W.showHint('error', '请输入商品分组名称');
            }else{
                this.successCallback(data)
                this.$dialog.modal('hide');
                this.successCallback = null;
            }
        }
    },
});
