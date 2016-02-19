/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 运费模板编辑器
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.ProductsPoolView = Backbone.View.extend({
    // getModelInfoTemplate: function() {
    //     $('#mall-product-list-view-model-info-tmpl-src').template('mall-product-list-view-model-info-tmpl');
    //     return 'mall-product-list-view-model-info-tmpl';
    // },

    initialize: function(options) {
        this.$el = $(this.el);
        this.options = options || {};
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        // this.modelInfoTemplate = this.getModelInfoTemplate();
        // this.type = options.type || 'onshelf';
    },

    events: {
        'click .xa-checkOffshelf': 'onClickAddOffShelf',
        'click .xa-batchOffshelf': 'onClickBatchAddOffShelf',
        'click .xa-update': 'onClickUpdateBtn',
        'click .xa-offshelf': 'onClickCreateProductOnShelf',


        // 'click .xa-batchOnshelf': 'onClickBatchUpdateProductShelveTypeLink',
        // 'click .xa-batchRecycle': 'onClickBatchUpdateProductShelveTypeLink',
        // 'click .xa-batchDelete': 'onClickBatchUpdateProductShelveTypeLink',

        // 'click .xa-modifyStandardModelStocks': 'onClickModifyStandardModelStocksLink',
        // 'click .xa-modifyCustomModelStocks': 'onClickModifyCustomModelStocksLink',
        // 'blur .xa-stockInput': 'onConfirmStockInput',
        // 'keypress .xa-stockInput': 'onPressKeyInStockInput',
        // 'blur .xa-rank': 'onBlurRank',
        // 'keypress .xa-rank': 'onPressKeyRank',
        // 'click .xa-showAllModels': 'onClickShowAllModelsButton',

        'click .xa-selectAll':'onClickSelectAll',
    },

    render: function() {
        this.filterView = new W.view.mall.ProductsPoolFilterView({
            el: '.xa-productFilterView'
        });
        this.filterView.on('search', _.bind(this.onSearch, this));
        this.filterView.render();
    },
    onClickAddOffShelf: function(){
        W.dialog.showDialog('W.dialog.mall.OffShelfProductsListDialog', {
            success: function(data) {}
            });
    },
    /**
     * onSearch: 响应filter view抛出的search事件
     */
    onSearch: function(data) {
        this.table.reload(data, {
            emptyDataHint: '没有符合条件的商品'
        });
    },
    /**
     * onClickSelectAll: 点击全选选择框时的响应函数
     */

    onClickCreateProductOnShelf: function(event) {
        var _this = this;
        var product_ids = [];
        var $el = $(event.currentTarget);
        var product_id = $el.parent().parent().data('id');
        product_ids.push(product_id);
        W.resource.mall2.ProductPool.put({
            data: {'product_ids': JSON.stringify(product_ids)},
            success: function(data){
                _this.table.reload();
            },
            error: function(data){}
        })
    },

    onClickSelectAll: function(event) {
        var $checkbox = $(event.currentTarget);
        var isChecked = $checkbox.is(':checked');
        this.$('tbody .xa-select').prop('checked', isChecked);
        this.$('.xa-selectAll').prop('checked', isChecked);
        // if (isChecked) {
            //this.$('.xa-selectAll').attr('checked', 'checked');
        // } else {
            //this.$('.xa-selectAll').removeAttr('checked');
        // }
    },
    onClickBatchAddOffShelf: function(){

    },
    onClickUpdateBtn: function(event){
        var $el = $(event.currentTarget);
        var productId = $el.parents('tr').data('id');
        var hasActivity = $el.parents('tr').data('product-has-promotion');
        var _this = this,
            width,
            templateAlign,
            msg;
        if(hasActivity && hasActivity == 1){
            width = 300;
            templateAlign = "vertical";
            msg = "该商品正在参加活动，更新后活动将结束，</br>是否确认更新该商品？";
        }else{
            width = 400;
            templateAlign = "";
            msg = "是否确认更新该商品？";
        }
        W.requireConfirm({
            $el: $el,
            width:width,
            position:'top',
            isTitle: false,
            templateAlign:templateAlign,
            privateContainerClass:'xui-updatePop',
            msg:msg
            ,
            confirm:function(){
                var args = {
                }
                W.getApi().call({
                    method: 'post',
                    app: 'mall2',
                    resource: 'order',
                    args: args,
                    success: function(data) {
                        _this.table.reload();
                    },
                    error: function() {
                        }
                })
            }
        })
    },
    // reset: function() {
    //     this.$('table').empty();
    //     this.frozenArgs = {};
    // },
});
