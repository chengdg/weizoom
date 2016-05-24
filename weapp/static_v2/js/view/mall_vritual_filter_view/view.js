ensureNS('W.view.mall');
W.view.mall.PromotionFilterView = Backbone.View.extend({
    getTemplate: function() {
        if(this.options.templateName){
            var tname = this.options.templateName.replace('-src','')
            $('#'+this.options.templateName).template(tname)
            return tname;
        }
        $('#mall-welfarePage-filter-view-tmpl-src').template('mall-welfarePage-filter-view-tmpl');
        return 'mall-welfarePage-filter-view-tmpl';
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
            startDate: this.options.startDate || '',  //支持从首页店铺提醒“即将到期的活动”过来的请求 duhao 20150925
            endDate: this.options.endDate || ''  //支持从首页店铺提醒“即将到期的活动”过来的请求 duhao 20150925
        });
        this.$el.append(html);
        W.createWidgets(this.$el);
    },

    onClickSearchButton: function(){
        xlog("in onClickSearchButton()");
        var data = this.getFilterData();
        console.log(data,'+++++++++')
        this.trigger('search', data);
    },

    onClickResetButton: function(){
        xlog('reset');
        $('#name').val('');
        $('#product_name').val('');
        $('#start_date').val('');
        $('#end_date').val('');
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



        //活动名
        var name = $.trim(this.$('#name').val());

        //商品名
        var productName = $.trim(this.$('#product_name').val());

        return {
            name: name,
            product_name: productName,
            start_time: startDate,
            end_time: endDate,
        };
    }
});
