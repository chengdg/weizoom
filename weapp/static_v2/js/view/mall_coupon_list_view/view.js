/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 运费模板编辑器
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.CouponListView = Backbone.View.extend({

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(this.el);
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    events: {
        'click .xa-batchDelete': 'onClickBatchDeleteLink',

        'click .xa-selectAll': 'onClickSelectAll',
        'click .xa-select': 'onClickSelect'
    },

    render: function() {
        this.filterView = new W.view.mall.CouponFilterView({
            el: '.xa-couponFilterView',
        });
        this.filterView.on('search', _.bind(this.onSearch, this));
        this.filterView.render();
        $('.xa-batchDelete').attr("disabled",true);
    },

    onSearch: function(data) {
        this.table.reload(data, {
            emptyDataHint: '没有符合条件的优惠券'
        });
    },

    onClickBatchDeleteLink: function(event) {
        var $link = $(event.currentTarget);
        var ids = this.table.getAllSelectedDataIds();
        var _this = this;
        W.requireConfirm({
            $el: $link,
            width: 398,
            position:'top',
            isTitle: false,
            msg: '确认删除优惠券吗？',
            confirm: function() {
                _this.deleteCoupons(ids);
            }
        });
    },

    deleteCoupons: function(couponsId) {
        W.getApi().call({
            method: 'post',
            app: 'mall_promotion',
            api: 'coupons/delete',
            args: {
                ids: couponsId,
            },
            success: function(data) {
                W.showHint('success', '删除成功!');
                window.location.reload();
            },
            error: function(resp) {
                W.showHint('error', '删除失败!');
            }
        });
    },

    /**
     * onClickSelectAll: 点击“全选”复选框的响应函数
     */
    onClickSelectAll: function(event) {
        var $checkbox = $(event.currentTarget);
        var isSelect = $checkbox.is(':checked');
        this.table.selectAll(isSelect);
        this.onClickSelect();
    },

    onCheckedSelect: function(){
        var flag=0;
        $(".xa-select").each(function () {
            if ($(this).attr("checked")) {
                flag=1;
            }
        });
        return flag;
    },

    onClickSelect: function(event) {
        var is_checked = this.onCheckedSelect();
        if(is_checked){
            $('.xa-batchDelete').attr("disabled", false);
        }
        else{
            $('.xa-batchDelete').attr("disabled", true);
        }
    },
});
