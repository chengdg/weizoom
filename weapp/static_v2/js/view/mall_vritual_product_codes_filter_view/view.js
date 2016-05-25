ensureNS('W.view.mall');
W.view.mall.VirtualProductCodeFilterView = Backbone.View.extend({
    getTemplate: function() {
        if(this.options.templateName){
            var tname = this.options.templateName.replace('-src','')
            $('#'+this.options.templateName).template(tname)
            return tname;
        }
        $('mall-virtualProductCodes-filter-view-tmpl-src').template('mall-virtualProductCodes-filter-view-tmpl');
        return 'mall-virtualProductCodes-filter-view-tmpl';
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
        xlog("in onClickSearchButton(),VirtualProductCodeFilterView");
        var data = this.getFilterData();
        console.log("data~~~",data)
        this.trigger('search', data);
    },

    onClickResetButton: function(){
        xlog('reset');
        $('#code').val('');
        $('#member_name').val('');
        $('#order_id').val('');
        $('#status').val('-1');
        $('#get_time_start').val('');
        $('#get_time_end').val('');
        $('#validity_time_start').val('');
        $('#validity_time_end').val('');
    },

    // 获取条件数据
    getFilterData: function(){
        //领取时间
        var getTimeStart = $.trim(this.$('#get_time_start').val());
        var getTimeEnd = $.trim(this.$('#get_time_end').val());
        //有效期
        var validityTimeStart = $.trim(this.$('#validity_time_start').val());
        var validityTimeEnd = $.trim(this.$('#validity_time_end').val());

        if ( (getTimeStart.length === 0 && getTimeEnd.length > 0) || 
            (validityTimeStart.length === 0 && validityTimeEnd.length > 0)) {
            W.showHint('error', '请输入开始日期！');
            return false;
        }
        if ((getTimeEnd.length === 0 && getTimeStart.length > 0) || 
            (validityTimeEnd.length === 0 && validityTimeStart.length > 0)) {
            W.showHint('error', '请输入结束日期！');
            return false;
        }
        if ((getTimeStart > getTimeEnd) || (validityTimeStart > validityTimeEnd)) {
            W.showHint('error', '开始日期不能大于结束日期！');
            return false;
        }



        //卡券码
        var code = $.trim(this.$('#code').val());
        //领取人
        var memberName = $.trim(this.$('#member_name').val());
        // 订单编号
        var orderId = $.trim(this.$('#order_id').val());
         // 领用状态
        var status = $.trim(this.$('#status').val());


        return {
            code: code,
            member_name: memberName,
            order_id: orderId,
            status: status,
            get_time_start:getTimeStart,
            get_time_end:getTimeEnd,
            valid_time_start:validityTimeStart,
            valid_time_end:validityTimeEnd,
        };
    }
});
