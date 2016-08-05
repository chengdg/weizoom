ensureNS('W.view.mall');
W.view.mall.ProductsPoolFilterView = Backbone.View.extend({
    getTemplate: function() {
        $('#mall-products-pool-filter-view-tmpl-src').template('mall-products-pool-filter-view-tmpl');
        return 'mall-products-pool-filter-view-tmpl';
    },

    events: {
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButton'
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        // this.filter_value = '';
        // this.bind('clickStatusBox', this.clickStatusBox);
    },

    render: function() {
        var html = $.tmpl(this.getTemplate());
        this.$el.append(html);
    },

    onClickSearchButton: function(){
        var data = this.getFilterData();
    },

    onClickResetButton: function(){
        $('#name').val('');
        $('#supplier').val('');
        $('#status').val('-1');
        $('#supplier_type').val('-1');
    },

    // 获取条件数据
    getFilterData: function(){

        

        //商品名
        var name = $.trim(this.$('#name').val());

        //供货商
        var supplier = $.trim(this.$('#supplier').val());
        
        //状态
        var status = this.$('#status').val();

        //状态
        var supplier_type = this.$('#supplier_type').val();

        var data = {
            name: name,
            supplier: supplier,
            status: status,
            supplier_type:supplier_type
        }
        this.trigger('search', data);
    },

    // 初始化日历控件
    // addDatepicker: function() {
    //     var _this = this;
    //     $('input[data-ui-role="orderDatepicker"]').each(function() {
    //         var $datepicker = $(this);
    //         var format = $datepicker.attr('data-format');
    //         var min = $datepicker.attr('data-min');
    //         var max = $datepicker.attr('data-max');
    //         var $min_el = $($datepicker.attr('data-min-el'));
    //         var $max_el = $($datepicker.attr('data-max-el'));
    //         var options = {
    //             buttonText: '选择日期',
    //             currentText: '当前时间',
    //             numberOfMonths: 1,
    //             hourText: "小时",
    //             minuteText: "分钟",
    //             //dateFormat: format,
    //             dateFormat: 'yy-mm-dd',
    //             closeText: '确定',
    //             prevText: '&#x3c;上月',
    //             nextText: '下月&#x3e;',
    //             monthNames: ['一月','二月','三月','四月','五月','六月',
    //                 '七月','八月','九月','十月','十一月','十二月'],
    //             monthNamesShort: ['一','二','三','四','五','六',
    //                 '七','八','九','十','十一','十二'],
    //             dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
    //             dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
    //             dayNamesMin: ['日','一','二','三','四','五','六'],
    //             beforeShow: function(e) {
    //                 if(min === 'now') {
    //                     $(this).datepicker('option', 'minDate', new Date());
    //                 }else if(min){
    //                     $(this).datepicker('option', 'minDate', min);
    //                 }

    //                 if($min_el){
    //                     var startTime = $min_el.val();
    //                     if(startTime) {
    //                         $(this).datepicker('option', 'minDate', startTime);
    //                     }
    //                 }

    //                 if(max === 'now') {
    //                     $(this).datepicker('option', 'maxDate', new Date());
    //                 }else if(max){
    //                     $(this).datepicker('option', 'maxDate', max);
    //                 }

    //                 if($max_el){
    //                     var endTime = $max_el.val();
    //                     if(endTime) {
    //                         $(this).datepicker('option', 'maxDate', endTime);
    //                     }
    //                 }
    //             },
    //             onClose: function() {
    //             }
    //         };

    //         $datepicker.datetimepicker(options);
    //     });
    // }
});
