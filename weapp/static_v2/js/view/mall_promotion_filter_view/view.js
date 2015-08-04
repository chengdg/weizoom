ensureNS('W.view.mall');
W.view.mall.PromotionFilterView = Backbone.View.extend({
    getTemplate: function() {
        if(this.options.templateName){
            var tname = this.options.templateName.replace('-src','')
            $('#'+this.options.templateName).template(tname)
            return tname;
        }
        $('#mall-promotion-filter-view-tmpl-src').template('mall-promotion-filter-view-tmpl');
        return 'mall-promotion-filter-view-tmpl';
    },

    events: {
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButton'
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.promotionType = options.promotionType;
    },

    render: function() {
        var html = $.tmpl(this.getTemplate(), {
            promotionType: this.promotionType
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
        $('#bar_code').val('');
        $('#start_date').val('');
        $('#end_date').val('');
        $('#promotion_status').val('-1');
        $('#promotion_type').val('all');
        $('#coupon_id').val('');
        $('#coupon_promotion_type').val('-1');
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

        //促销状态
        var promotionStatus = this.$('#promotion_status').val();

        //促销类型
        var promotionType = this.$('#promotion_type').val() || 'all';

        //商品名
        var name = $.trim(this.$('#name').val());

        //商品编码
        var barCode = $.trim(this.$('#bar_code').val());

        //优惠码
        var couponId = $.trim(this.$('#coupon_id').val());

        //优惠券类型
        var couponPromotionType = this.$('#coupon_promotion_type').val() || 'all';

        return {
            name: name,
            promotionStatus: promotionStatus,
            promotionType: promotionType,
            barCode: barCode,
            startDate: startDate,
            endDate: endDate,
            couponId: couponId,
            couponPromotionType: couponPromotionType
        };
    }
});
