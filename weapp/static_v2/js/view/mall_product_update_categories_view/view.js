/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 修改会员标签
 * 
 * author: bert
 */
ensureNS('W.view.member');
W.view.mall.MallProductUpdateCategoriesView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#mall_product_update_categories-dialog-tmpl-src').template('mall_product_update_categories-dialog-tmpl');
        return "mall_product_update_categories-dialog-tmpl";
    },
    
    events:{
        'click .xa-submit': 'onClickSubmit'
    },

    initializePrivate: function(options) {
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
    },
    
    onClickSubmit: function(event) {
        var categoryIds = this.$content.find('.xa-categories-list input:checked').map(function (i,el) {
            return $(el).data('id');
        }).toArray();
        if(!categoryIds.length){
            W.showHint('error', "请选择至少一个分类");
            return;
        }
        this.submitSendApi(this.productIds, categoryIds)
    },

    submitSendApi: function(productIds, categoryIds){
        this.hide();
        var _this = this;
        W.getApi().call({
            app: 'mall2',
            resource: 'batch_update_product_category',
            scope: this,
            method: 'post',
            args: {
                product_ids: productIds.join(','),
                category_ids: categoryIds.join(','),
            },
            success: function(data) {
                if (_this.dataView){
                    _this.dataView.reload();
                }
            },
            error: function(resp) {
                W.showHint('error', resp.data.msg || '编辑分组失败');
            }
        });
    },
    


    render: function() {
        var _this = this;
        var selectedIds = this.selectedIds || [];
        var selectedIdMap = {};
        selectedIds.forEach(function (id) {
            selectedIdMap[id] = true;
        });
        this.getCategoriesData(function (items) {
             _this.$content.html($.tmpl(_this.getTemplate(), {items:items,selectedIdMap:selectedIdMap}));
        });

    },
    getCategoriesData:function (callback) {
          var _this = this;

          // if(_this.items){
          //     callback(_this.items);
          //     return;
          // }

          W.getApi().call({
            app: 'mall2',
            resource: 'categories',
            scope: this,
            method: 'get',
            args: {
                count_per_page: 1000000000,
            },
            success: function(data) {
                _this.items = data.items;
                callback(data.items);
            },
            error: function(resp) {
                W.showHint('error', '获取分组信息失败');
            }
        });
    },

    onShow: function(options) {

    },
    
    showPrivate: function(options) {
        this.dataView = options.dataView;
        this.selectedIds = options.selectedIds;
        this.productIds = options.productIds;
    },
});

W.getMallProductUpdateCategoriesView  = function(options) {
    var dialog = W.registry['W.view.mall.MallProductUpdateCategoriesView'];
    if (!dialog) {
        //创建dialog
        xlog('create W.view.mall.MallProductUpdateCategoriesView');
        dialog = new W.view.mall.MallProductUpdateCategoriesView(options);
        W.registry['W.view.mall.MallProductUpdateCategoriesView'] = dialog;
    }
    return dialog;
};
