ensureNS('W.view.mall');
W.view.mall.RedEnvelopeFilterView = Backbone.View.extend({
    getTemplate: function() {
        $('#mall-red-envelope-filter-view-tmpl-src').template('mall-red-envelope-filter-view-tmpl');
        return 'mall-red-envelope-filter-view-tmpl';
    },

    events: {
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButton'
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.coupon_rule = $(options.coupon_rule);
        this.table = $('[data-ui-role="advanced-table"]').data('view');
        this.on('search', _.bind(this.onSearch, this));
    },

    render: function() {
        var html = $.tmpl(this.getTemplate(), {
            coupon_rule: this.coupon_rule,
            startDate: this.options.startDate || '',  //支持从首页店铺提醒“即将到期的活动”过来的请求 duhao 20150925
            endDate: this.options.endDate || ''  //支持从首页店铺提醒“即将到期的活动”过来的请求 duhao 20150925
        });
        this.$el.append(html);
        W.createWidgets(this.$el);
    },

    onClickSearchButton: function(){
        var data = this.getFilterData();
        this.trigger('search', data);
    },

    onClickResetButton: function(){
        xlog('reset');
        $('#name').val('');
        $('#start_date').val('');
        $('#end_date').val('');
        $('#coupon_rule').val('0');
    },

    // 获取条件数据
    getFilterData: function(){
        //起止时间
        var startDate = $.trim(this.$('#start_date').val());
        var endDate = $.trim(this.$('#end_date').val());
        if (startDate.length === 0 && endDate.length > 0) {
            W.showHint('error', '请输入开始日期！');
            return false;
        }
        if (endDate.length === 0 && startDate.length > 0) {
            W.showHint('error', '请输入结束日期！');
            return false;
        }
        if (startDate > endDate) {
            W.showHint('error', '开始日期不能大于结束日期！');
            return false;
        }

        //优惠券的名称
        var name = $.trim(this.$('#name').val());

        //优惠券类型
        var couponRule = this.$('#coupon_rule').val() || '0';
        return {
            name: name,
            couponRule: couponRule,
            startDate: startDate,
            endDate: endDate
        };
    },

    onSearch: function(data) {
        this.table.reload(data, {
            emptyDataHint: '没有符合条件的分享红包规则'
        });
    }
});

