ensureNS('W.view.card.overview');

W.view.card.overview.OverviewFilterView = Backbone.View.extend({
    events: {
        'click .xa-create': 'createFilter',
        'click .xa-filter': 'filter',
        'click #search-order-btn': 'seacrhBtn',
        'click .recently-week-day': 'setDateText'
    },

        setDateText: function(event){
        var day = $(event.currentTarget).attr('data-day') -1 ;//parseInt(.toSting()) - 1;
        var today = new Date(); // 获取今天时间

        today.setTime(today.getTime()-day*24*3600*1000);
        var begin = $.datepicker.formatDate('yy-mm-dd', today);
        var end = $.datepicker.formatDate('yy-mm-dd', new Date());

        $('#start_date').val(begin);
        $('#end_date').val(end);
    },

    // 点击‘筛选’按钮事件
    seacrhBtn: function(){
        var startDate = $('#start_date').val();
        var endDate = $('#end_date').val();
        if (startDate.length > 0 && endDate.length == 0) {
            W.getErrorHintView().show('请输入结束日期！');
            return false;
        }
        if (endDate.length > 0 && startDate.length == 0) {
            W.getErrorHintView().show('请输入开始日期！');
            return false;
        }
        var start = new Date(startDate.replace("-", "/").replace("-", "/"));
        var end = new Date(endDate.replace("-", "/").replace("-", "/"));
        if ((startDate.length > 0 || endDate.length > 0) && start > end){
            W.getErrorHintView().show('开始日期不能大于结束日期！');
            return false;
        }
        var dataView = this.options.dataView;
        var args = this.getFilterValue();
        dataView.options.args = this.getFilterValueByDict(args);
        dataView.setPage(1);
        console.log('dataView.options.args', dataView.options.args);
        dataView.reload();

    },

    // 组织筛选的查询参数格式
    getFilterValueByDict: function(args){
        if (args.length == 0) {
            return ""
        }else{
            args.push('"page":1')
            return '{'+ args.join(',') +'}';
        }
    },


    // 获取条件数据
    getFilterValue: function(){
        var dataValue = [];
        var startDate = $('#start_date').val().trim();
        var endDate = $('#end_date').val().trim();

        var args = [];


        var filter_value = dataValue.join('|');

        if (filter_value != ''){
            args.push('"filter_value":"'+filter_value+'"')
        }
        //date_interval
        if (startDate != "" && endDate != "") {
            args.push('"date_interval":"'+startDate+'|'+endDate+'"');
        }
        return args
    },

    getTemplate: function() {
        $('#card-overview-filter-view-tmpl-src').template('card-overview-filter-view-tmpl');
        return 'card-overview-filter-view-tmpl';
    },

    render: function() {
        //var _this = this;
        var html = $.tmpl(this.getTemplate());
        this.$el.append(html);
        this.addDatepicker();
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.render();
        this.filter_value = '';
    },



    // 初始化日历控件
    addDatepicker: function(){
        var _this = this;
        $('input[data-ui-role="overviewDatepicker"]').each(function() {
            var $datepicker = $(this);
            var format = $datepicker.attr('data-format');
            var min = $datepicker.attr('data-min');
            var max = $datepicker.attr('data-max');
            var $min_el = $($datepicker.attr('data-min-el'));
            var $max_el = $($datepicker.attr('data-max-el'));
            var options = {
                buttonText: '选择日期',
                currentText: '当前时间',
                hourText: "小时",
                minuteText: "分钟",
                numberOfMonths: 1,
                dateFormat: 'yy-mm-dd',
                //dateFormat: format,
                closeText: '确定',
                prevText: '&#x3c;上月',
                nextText: '下月&#x3e;',
                monthNames: ['一月','二月','三月','四月','五月','六月',
                    '七月','八月','九月','十月','十一月','十二月'],
                monthNamesShort: ['一','二','三','四','五','六',
                    '七','八','九','十','十一','十二'],
                dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
                dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
                dayNamesMin: ['日','一','二','三','四','五','六'],
                beforeShow: function(e) {
                    if(min === 'now') {
                        $(this).datepicker('option', 'minDate', new Date());
                    }else if(min){
                        $(this).datepicker('option', 'minDate', min);
                    }

                    if($min_el){
                        var startTime = $min_el.val();
                        if(startTime) {
                            $(this).datepicker('option', 'minDate', startTime);
                            $(this).datepicker('option', 'minDateTime', new Date(startTime));
                        }



                    }

                    if(max === 'now') {
                        $(this).datepicker('option', 'maxDate', new Date());
                    }else if(max){
                        $(this).datepicker('option', 'maxDate', max);
                    }

                    if($max_el){
                        var endTime = $max_el.val();
                        if(endTime) {
                            $(this).datepicker('option', 'maxDate', endTime);
                        }
                    }
                },
                onClose: function() {
                }
            };

            $datepicker.datepicker(options);
        });
    }

});
