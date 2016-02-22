/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 运费模板编辑器
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.ProductListView = Backbone.View.extend({
    getModelInfoTemplate: function() {
        $('#mall-product-list-view-model-info-tmpl-src').template('mall-product-list-view-model-info-tmpl');
        return 'mall-product-list-view-model-info-tmpl';
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.options = options || {};
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        this.modelInfoTemplate = this.getModelInfoTemplate();
        this.type = options.type || 'onshelf';
    },

    events: {
        'click .xa-onshelf': 'onClickUpdateProductShelveTypeLink',
        'click .xa-offshelf': 'onClickUpdateProductShelveTypeLink',
        'click .xa-recycle': 'onClickUpdateProductShelveTypeLink',
        'click .xa-delete': 'onClickUpdateProductShelveTypeLink',

        'click .xa-batchOnshelf': 'onClickBatchUpdateProductShelveTypeLink',
        'click .xa-batchOffshelf': 'onClickBatchUpdateProductShelveTypeLink',
        'click .xa-batchRecycle': 'onClickBatchUpdateProductShelveTypeLink',
        'click .xa-batchDelete': 'onClickBatchUpdateProductShelveTypeLink',

        'click .xa-modifyStandardModelStocks': 'onClickModifyStandardModelStocksLink',
        'click .xa-modifyCustomModelStocks': 'onClickModifyCustomModelStocksLink',
        'blur .xa-stockInput': 'onConfirmStockInput',
        'keypress .xa-stockInput': 'onPressKeyInStockInput',
        'blur .xa-rank': 'onBlurRank',
        'keypress .xa-rank': 'onPressKeyRank',
        'click .xa-showAllModels': 'onClickShowAllModelsButton',

        'click .xa-selectAll':'onClickSelectAll',
    },

    render: function() {
        this.filterView = new W.view.mall.ProductFilterView({
            el: '.xa-productFilterView',
            low_stocks: this.options.low_stocks || '',  //支持从首页店铺提醒“库存不足商品”过来的请求 duhao 20150925
            high_stocks: this.options.high_stocks || ''  //支持从首页店铺提醒“库存不足商品”过来的请求 duhao 20150925
        });
        this.filterView.on('search', _.bind(this.onSearch, this));
        this.filterView.render();

        this.$('input[type="text"]').eq(0).focus();
    },

    onClickBatchUpdateProductShelveTypeLink: function(event) {
        var $link = $(event.currentTarget);
        var shelveType = null;
        if ($link.hasClass('xa-batchOnshelf')) {
            shelveType = 'onshelf';
        } else if ($link.hasClass('xa-batchOffshelf')) {
            shelveType = 'offshelf'
        } else if ($link.hasClass('xa-batchRecycle')) {
            shelveType = 'recycled'
        } else if ($link.hasClass('xa-batchDelete')) {
            shelveType = 'delete'
        }

        var ids = this.table.getAllSelectedDataIds();
        var _this = this;
        var updateAction = function() {
            W.getApi().call({
                method: 'post',
                app: 'mall2',
                resource: 'product_list',
                args: {
                    ids: ids,
                    shelve_type: shelveType
                },
                scope: this,
                success: function(data) {
                    for(var i = 0; i < ids.length; ++i) {
                        var id = ids[i];
                        this.$('[data-id="'+id+'"]').remove();
                    }

                    if (this.$('tbody tr').length == 0) {
                        _this.table.reload()
                    }
                }
            });
        }

        if (shelveType == 'recycled' || shelveType == 'delete') {
            var msg = shelveType == 'recycled' ? '确认将全部商品放入回收站？' : '确认将全部商品彻底删除？'
            W.requireConfirm({
                $el: $link,
                width:457,
                position:'top',
                isTitle: false,
                msg: msg,
                confirm: updateAction
            });
        } else {
            updateAction();
        }
    },

    onClickUpdateProductShelveTypeLink: function(event) {
        var $link = $(event.currentTarget);
        var shelveType = null;
        if ($link.hasClass('xa-onshelf')) {
            shelveType = 'onshelf';
        } else if ($link.hasClass('xa-offshelf')) {
            shelveType = 'offshelf'
        } else if ($link.hasClass('xa-recycle')) {
            shelveType = 'recycled'
        } else if ($link.hasClass('xa-delete')) {
            shelveType = 'delete'
        }

        var $tr = $link.parents('tr');
        var $trs = $link.parents('table').find('tr');
        var productId = $tr.data('id');
        var _this = this;
        var updateAction = function() {
            W.getApi().call({
                method: 'post',
                app: 'mall2',
                resource: 'product_list',
                args: {
                    id: productId,
                    shelve_type: shelveType
                },
                scope: this,
                success: function(data) {
                        _this.table.reload(this.extraArgs);

                }
            })
        };

        if (shelveType == 'recycled' || shelveType == 'delete') {

            var msg = shelveType == 'recycled' ? '是否放入回收站' : '确认将商品彻底删除'
            W.requireConfirm({
                $el: $link,
                width:420,
                height:55,
                position:'right-middle',
                isTitle: false,
                msg: msg,
                confirm: updateAction
            });
        } else {
            updateAction();
        }
    },

    /**
     * onClickModifyStandardModelStocksLink: 点击修改库存链接的响应函数
     */
    onClickModifyStandardModelStocksLink: function(event) {
        var $link = $(event.currentTarget);
        var $td = $link.parents('td');
        var $stockText = $td.find('.xa-stockText');
        var stockText = $.trim($stockText.text());
        var $stockInput = $td.find('.xa-stockInput');
        $stockText.hide();
        $stockInput.show().focus().val(stockText);
    },

    /**
     * onClickModifyCustomModelStocksLink: 点击修改库存链接的响应函数
     */
    onClickModifyCustomModelStocksLink: function(event) {
        var $target = $(event.currentTarget);
        var $td = $target.parents('td');
        var $tr = $target.parents('tr');
        var id = $tr.data('id');
        var product = this.table.getDataItem(id);
        var models = product.get('models');
        W.dialog.showDialog('W.dialog.mall.UpdateProductModelStocksDialog', {
            models: models,
            success: function(data) {
                var newModelInfos = data;
                W.getApi().call({
                method: 'post',
                app: 'mall2',
                resource: 'product_model',
                args: W.toFormData({'model_infos': newModelInfos}),
                scope: this,
                success: function(data) {
                    //遍历table中的model，如果该model在newModelInfos中出现，则:
                    //model.stock_type = newModelInfo.stock_type
                    //model.stocks = newModelInfo.stocks
                    var id2newModelInfo = {};
                    for (i = 0; i < newModelInfos.length; ++i) {
                        var newModelInfo = newModelInfos[i];
                        id2newModelInfo[newModelInfo.id] = newModelInfo;
                    }
                    var __sum = 0;  // 库存计数
                    for (i = 0; i < models.length; ++i) {
                        var model = models[i];
                        var newModelInfo = id2newModelInfo[model.id]
                        if (newModelInfo.stock_type == 'unlimit') {
                            model.stock_type = 0;
                            __sum += 1
                        } else {
                            model.stock_type = 1;
                            __sum += parseInt(newModelInfo.stocks);
                        }
                        model.stocks = newModelInfo.stocks;
                    }

                    //将页面上的库存信息替换为最小价格规格的库存信息
                    var sortedModels = _.sortBy(models, function(model) { return model.price; });
                    $td.find('.xa-stockText').text(sortedModels[0].stocks);


                    // 已售罄
                    //
                    $imgbox = $tr.find(".imgBox");
                    $imgbox.find('.xui-i-sellout').remove();

                    if(__sum!=0){
                        $imgbox.find('.xui-i-sellout').remove();
                    }else if(__sum===0){
                        $imgbox.append('<div class="xui-i-sellout">已售罄</div>');
                    }
                },
                error: function(resp) {
                    var msg = '更新库存失败!';
                    if(resp.errMsg.length > 0)
                        msg = resp.errMsg;
                    W.showHint('error', msg);
                }
            })
            }
        });
    },

    /**
     * onClickShowAllModelsButton: 鼠标点击“查看规格”区域的响应函数
     */
    onClickShowAllModelsButton: function(event) {
        var $target = $(event.currentTarget);
        var $tr = $target.parents('tr');
        var id = $tr.data('id');
        var product = this.table.getDataItem(id);
        var models = product.get('models');
        var properties = _.pluck(models[0].property_values, 'propertyName');
        var $node = $.tmpl(this.modelInfoTemplate, {properties: properties, models: models});
        W.popup({
            $el: $target,
            position:'top',
            isTitle: false,
            msg: $node
        });
    },

    /**
     * onConfirmStockInput: 焦点移出库存编辑框时的响应函数
     */
    onConfirmStockInput: function(event) {
        var $td = $(event.currentTarget).parent();
        var $tr = $td.parent();
        var productId = $tr.data('id');
        var $stockText = $td.find('.xa-stockText');
        var $stockInput = $td.find('.xa-stockInput');
        var stockText = $.trim($stockInput.val());
        var $imgbox = $tr.find('.imgBox');  // Image Box
        var productData = this.table.getDataItem(productId);
        if (stockText === '无限') {
            $stockInput.hide();
            $stockText.text(stockText).show();
            $imgbox.find('.xui-i-sellout').remove();
            /* Data Update */
            var data = {'model_infos': [{
                id: productData.get('standard_model').id,
                stock_type: 'unlimit',
                stocks: stockText
            }]};
            W.getApi().call({
                method: 'post',
                app: 'mall2',
                resource: 'product_model',
                args: W.toFormData(data),
                scope: this,
                success: function(data) {
                    $stockInput.hide();
                    $stockText.text(stockText).show();
                },
                error: function(resp) {
                    var msg = '更新库存失败!';
                    if(resp.errMsg.length > 0)
                        msg = resp.errMsg;
                    W.showHint('error', msg);
                }
            });
        } else if(stockText === "" || ((parseInt(stockText)).toString()==stockText)&&parseInt(stockText)>=0){
            if(stockText===""){stockText = 0;}
            else{stockText = parseInt(stockText);}

            /* Image display status update */
            $imgbox.find('.xui-i-sellout').remove();
            if(stockText){
                $imgbox.find('.xui-i-sellout').remove();
            }else{
                $imgbox.append('<div class="xui-i-sellout">已售罄</div>');
            }
            /* Data Update */
            var data = {'model_infos': [{
                id: productData.get('standard_model').id,
                stock_type: 'limit',
                stocks: stockText
            }]};
            W.getApi().call({
                method: 'post',
                app: 'mall2',
                resource: 'product_model',
                args: W.toFormData(data),
                scope: this,
                success: function(data) {
                    $stockInput.hide();
                    $stockText.text(stockText).show();
                },
                error: function(resp) {
                    var msg = '更新库存失败!';
                    if(resp.errMsg.length > 0)
                        msg = resp.errMsg;
                    W.showHint('error', msg);
                }
            })
        }else{
            W.showHint('error', '库存请输入非负整数');
        }
    },

    /**
     * onPressKeyInStockInput: 在库存编辑框中输入回车时的响应函数
     */
    onPressKeyInStockInput: function(event) {
        var keyCode = event.keyCode;
        if(keyCode === 13) {
            this.onConfirmStockInput(event);
        }
    },
    onPressKeyRank:function(event){
        var keyCode = event.keyCode;
        if(keyCode === 13) {
            this.onConfirmRankInput(event);
        }     
    },
    onBlurRank:function(event){
        var oldConfirmView = W.registry['common-popup-confirm-view'];
        var oldPos = $.trim($(event.currentTarget).data('display-index'));
        var rankText = $.trim($(event.currentTarget).val());
        if(rankText == oldPos){
            return;
        }
        if(!oldConfirmView || oldConfirmView.$el.css('display') == 'none'){
            this.onConfirmRankInput(event);
        }
    },
    /**
     * onConfirmRankInput: 在排序框失去焦点时的响应函数
     */
    onConfirmRankInput:function(event){
            _this = this;
            var $link = $(event.currentTarget);
            var rankText = $.trim($(event.currentTarget).val());/*文本框的值*/
            var id = $.trim($(event.currentTarget).data('id'));
            var oldPos = $.trim($(event.currentTarget).data('display-index'));
            var updateAction = function() {
                try{
                    has_index.val('0').data('display-index', 0);
                }
                catch(e){
                }
                finally{
                    W.getApi().call({
                        method: 'post',
                        app: 'mall2',
                        resource: 'product_pos',
                        args: {
                            update_type: 'update_pos',
                            id: id,
                            pos: rankText,
                        },
                        success: function(data){
                           $(event.currentTarget).data('display-index', rankText).val(rankText);
                            W.finishConfirm();
                        },
                        error: function(response){
                            W.showHint('error', '更新产品位置失效');
                        }

                    });
                }
            }

            if(rankText === '0') {  //如果改为0就直接更新
                updateAction();
            } else{
                var cancel = function(){
                    $(event.currentTarget).val(oldPos);
                }
                var has_index = false
                
                W.getApi().call({
                    method: 'get',
                    app: 'mall2',
                    resource: 'product_pos',
                    args: {
                        id: id,
                        pos: rankText,
                    },
                    success: function(data){
                       if (data.is_index_exists){
                            var rankTextList = $(event.currentTarget).parents('tr').siblings().find('.xa-rank').each(function(i){
                                var a_rank = $.trim($(this).data('display-index'));
                                if(rankText == a_rank){
                                    has_index = $(this);
                                }
                            });

                            var msg = "位置"+rankText+"已存在商品， 是否替换";
                            W.requireConfirm({
                                $el: $link,
                                width:480,
                                position:'top',
                                isTitle: false,
                                msg: msg,
                                confirm: updateAction,
                                cancel:cancel,
                                minClickTime:1
                            });
                       } else {
                            updateAction();
                       }
                    },
                    error: function(response){
                        W.showHint('error', '获取商品已有排序值失败');
                    }

                });
            }
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
    onClickSelectAll: function(event) {
        var $checkbox = $(event.currentTarget);
        var isChecked = $checkbox.is(':checked');
        this.$('tbody .xa-select').prop('checked', isChecked);
        this.$('.xa-selectAll').prop('checked', isChecked);
        if (isChecked) {
            //this.$('.xa-selectAll').attr('checked', 'checked');
        } else {
            //this.$('.xa-selectAll').removeAttr('checked');
        }
    },

    reset: function() {
        this.$('table').empty();
        this.frozenArgs = {};
    },
});
W.view.mall.offshelfProductsTable = W.view.common.AdvancedTable.extend({
    afterload:function(){
        $('.xa-selectTr').each(function(index, el) {
            if($(this).data('purchase-price').length !== 0 && $(this).data('purchase-price') == "0"){
                $(this).find('.xa-select').attr('disabled', 'disabled').removeClass('xa-select');
            }
        });
    }
});
W.registerUIRole('div[data-ui-role="offshelf-advanced-table"]', function() {
    var $div = $(this);
    var template = $div.data('template-id');
    var app = $div.data('app')
    var api = $div.attr('data-api');
    var args = $div.attr('data-args');
    var itemCountPerPage = $div.data('item-count-per-page');
    var enablePaginator = $div.data('enable-paginator');
    var enableSort = $div.data('enable-sort');
    var enableSelect = $div.data('selectable');
    var disableHeaderSelect = $div.data('disable-header-select');
    var outerSelecter = $div.data('outer-selecter');
    var advancedTable = new W.view.mall.offshelfProductsTable({
        el: $div[0],
        template: template,
        app: app,
        api: api,
        args: args,
        itemCountPerPage: itemCountPerPage,
        enablePaginator: enablePaginator,
        enableSort: enableSort,
        enableSelect: enableSelect,
        outerSelecter:outerSelecter,
        disableHeaderSelect: disableHeaderSelect,
        autoLoad: true
    });
    advancedTable.render();
    advancedTable.afterload();

    $div.data('view', advancedTable);
});
