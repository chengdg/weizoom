/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 运费模板编辑器
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.ProductReviewListView = Backbone.View.extend({

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(this.el);
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    events: {
        'click .xa-modify': 'onClickModify',
        'click .xa-batchPass': 'onClickBatchPass',
        'click .xa-batchShield': 'onClickBatchShield',
        'click .xa-selectAll': 'onClickSelectAll',
        'click .xa-select': 'onClickSelect'
    },

    render: function() {
        this.filterView = new W.view.mall.ProductReviewFilterView({
            el: '.xa-productReviewFilterView',
        });
        this.filterView.on('search', _.bind(this.onSearch, this));
        this.filterView.render();
    },


    onSearch: function(data) {
        this.table.reload(data, {
            emptyDataHint: '没有符合条件的商品评论'
        });
    },

    //置顶
    onClickModify: function(event){

        var $el = $(event.currentTarget);
        var product_review_id = $el.attr("data-product-review-id");
        var status = $el.attr("data-status");
        W.getApi().call({
            app: 'mall2',
            resource: 'product_review',
            method: 'post',
            args: {
                product_review_id: product_review_id,
                status: status
            },
            success: function(){
                W.showHint('success', '操作成功！');
                $('[data-ui-role="advanced-table"]').data('view').reload();
            },
            error: function(){
                W.showHint('error', '操作失败！');
            }
        })
    },

    //通过
    onClickBatchPass: function(event){
        var $link = $(event.currentTarget);
        var ids = this.table.getAllSelectedDataIds();
        this.batchUpdateReviews(ids, 'pass');

    },

    //屏蔽
    onClickBatchShield: function(event){
        var $link = $(event.currentTarget);
        var ids = this.table.getAllSelectedDataIds();
        this.batchUpdateReviews(ids, 'shield');
    },

    //批量操作
    batchUpdateReviews: function(reviewIds, action) {
        W.getApi().call({
            method: 'post',
            app: 'mall2',
            resource: 'product_review',
            args:{
                ids: reviewIds.join(','),
                action: action
            },
            scope: this,
            success: function(data) {
                W.showHint('success', '操作成功！');
                $('[data-ui-role="advanced-table"]').data('view').reload();
                $('#bottomSelectAll').prop('checked', false);
            },
            error: function() {
                W.showHint('error', '操作失败！');
            }
        })
    },

    /**
     * onClickSelectAll: 点击“全选”复选框的响应函数
     */
    onClickSelectAll: function(event) {
        var $checkbox = $(event.currentTarget);
        var isSelect = $checkbox.is(':checked');
        this.table.selectAll(isSelect);
    },

    onCheckedSelect: function(){
        var flag=0;
        $(".xa-select").each(function () {
            if ($(this).attr("checked")) {
                flag=1;
            }
        });
        return flag;
    }

});
