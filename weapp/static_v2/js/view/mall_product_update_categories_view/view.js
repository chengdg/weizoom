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
        if(!this.isSingleModel && !categoryIds.length){
            W.showHint('error', "请选择至少一个分类");
            return;
        }

        this.submitSendApi(categoryIds)
    },

    submitSendApi: function(categoryIds){
        this.hide();
        var _this = this;
        var resource ;
        if(_this.productId !== undefined){
            resource = 'update_product_category';
        }

        var productIds = _this.productIds ? _this.productIds.join(',') : undefined;
        var productId = _this.productId;
        var args = {
                product_id:productId,
                product_ids: productIds,
                category_ids: categoryIds.join(','),
        };

        for(var k in args){
            if(args[k] === undefined){
               delete args[k];
            }
        }
        W.getApi().call({
            app: 'mall2',
            resource: resource,
            scope: this,
            method: 'post',
            args: args,
            success: function(data) {
                if (_this.dataView){
                    _this.dataView.reload();
                }
            },
            error: function(resp) {
                var msg = '编辑分组失败';
                if(resp && resp.data && resp.data.msg){
                    msg = resp.data.msg;
                }
                W.showHint('error', msg);
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
            var context =  {items:items,selectedIdMap:selectedIdMap};
             context.isSingleModel = _this.isSingleModel;
             _this.$content.html($.tmpl(_this.getTemplate(), context));
        });

    },
    getCategoriesData:function (callback) {
          var _this = this;
          var hiddenCategoryMap = this.hiddenCategoryMap;
          W.getApi().call({
            app: 'mall2',
            resource: 'categories',
            scope: this,
            method: 'get',
            args: {
                count_per_page: 1000000000,
            },
            success: function(data) {
                var items = data.items.filter(function (item) {
                    return !hiddenCategoryMap[item.id];
                });
                _this.items = items;
                callback(items);
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
        this.productId = options.productId;
        this.hiddenCategoryMap = options.hiddenCategoryMap || {}; // {id:true}
        this.isSingleModel = this.productId !== undefined;
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
