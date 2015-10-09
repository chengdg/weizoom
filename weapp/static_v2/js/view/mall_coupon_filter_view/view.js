ensureNS('W.view.mall');
W.view.mall.CouponFilterView = Backbone.View.extend({
    getTemplate: function() {
        $('#mall-coupon-code-filter-view-tmpl-src').template('mall-coupon-code-filter-view-tmpl');
        return 'mall-coupon-code-filter-view-tmpl';
    },

    events: {
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButton'
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
    },

    render: function() {
        var html = $.tmpl(this.getTemplate());
        this.$el.append(html);
        W.createWidgets(this.$el);
    },

    onClickSearchButton: function(){
        var data = this.getFilterData();
        this.trigger('search', data);
    },

    onClickResetButton: function(){
        xlog('reset');
        $('#coupon_code').val('');
        $('#member_name').val('');
        $('#use_status').val('all');
    },

    // 获取条件数据
    getFilterData: function(){
        //优惠码
        var couponCode = $.trim(this.$('#coupon_code').val());

        //使用状态
        var useStatus = this.$('#use_status').val();

        //领取人
        var memberName = $.trim(this.$('#member_name').val());

        return {
            couponCode: couponCode,
            useStatus: useStatus,
            memberName: memberName
        };
    }
});
