ensureNS('W.view.mall');
W.view.mall.ProductReviewFilterView = Backbone.View.extend({
    getTemplate: function() {
        $('#mall-product-review-filter-view-tmpl-src').template('mall-product-review-filter-view-tmpl');
        return 'mall-product-review-filter-view-tmpl';
    },

    events: {
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButton'
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.filterValue = "";
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
        $('#name').val('');
        $('#user_code').val('');
        $('#review_status').val('all');
        $('#start_date').val('');
        $('#end_date').val('');
        $('#product_score').val('all');
    },

    // 获取条件数据
    getFilterData: function(){
        //起止时间
        var args=[];
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
        if(startDate){
            args.push("startDate:"+startDate);
        }
        if(endDate){
            args.push("endDate:"+endDate);
        }
        //商品名
        var name = $.trim(this.$('#name').val());
        if(name){
            args.push("name:"+name);
        }
        //审核状态
        var reviewStatus = this.$('#review_status').val();
        if(reviewStatus!="all"){
            args.push("reviewStatus:"+reviewStatus);
        }
        //商品编码
        var userCode = $.trim(this.$('#user_code').val());
        if(userCode){
            args.push("userCode:"+userCode);
        }
        //商品评星
        var productScore = $.trim(this.$('#product_score').val());
        if(reviewStatus!='all'){
            args.push("productScore:"+productScore);
        }
        this.filterValue = args;
        return {
            name: name,
            reviewStatus: reviewStatus,
            userCode: userCode,
            startDate: startDate,
            endDate: endDate,
            productScore: productScore
        };
    }
});
