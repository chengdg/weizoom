ensureNS('W.view.card.cards');

W.view.card.cards.cardChargeFilter = Backbone.View.extend({
    events: {
        'click .seacrh-recharge-card-btn': 'seacrhBtn',
        'click .xa-reset': 'resetFrom',
        'click .exportBtn': 'exportBtn'
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
        console.log(args);
        console.log(this.getFilterValueByDict(args));
        dataView.options.args = this.getFilterValueByDict(args);
        dataView.setPage(1);
        dataView.reload();
        this.$el.trigger('end_click');
    },

    // 获取条件数据
    getFilterValue: function(){
        var cardType = $('#cardType').val();
        var cardAttr = $('#cardAttr').val();
        var startDate = $('#start_date').val().trim();
        var endDate = $('#end_date').val().trim();
        var card_num = $('#card_num').val().trim();
        var args = [];
        var dataValue = [];
        var filter_value = '';
        if (cardType != -1) {
            filter_value += '&cardType='+cardType;
            args.push('"cardType":"'+cardType+'"');
        }
        if (cardAttr != -1) {
            filter_value += '&cardAttr='+cardAttr;
            args.push('"cardAttr":"'+cardAttr+'"');
        }
         if (card_num != ''){
            //卡号长度为7检查
            // if (card_num.length != 7){
            //     W.getErrorHintView().show('卡号长度错误！');
            //     return false;
            // }
            filter_value += '&card_number='+card_num;
            args.push('"card_number":"'+card_num+'"');
            // dataValue.push('card_number:'+card_num);
        }
        if (startDate != "" && endDate != "") {
            args.push('"date_interval":"'+startDate+'|'+endDate+'"')
            filter_value += '&date_interval='+startDate+'|'+endDate;
        }
        this.filter_value = filter_value;
        return args;
    },

    // 组织筛选的查询参数格式
    getFilterValueByDict: function(args){
        if (args.length == 0) {
            return ""
        }else{
            args.push('"page":1');
            return '{'+ args.join(',') +'}';
        }
    },
    exportBtn: function(){
        var url = '/card/recharge_card_export/get/?is_export='+1;
        if (this.filter_value) {           
            url = url + this.filter_value;
        }
        window.open(url);
    },
    getTemplate: function() {
        $('#card-recharge-filter-view-tmpl-src').template('card-filter-view-tmpl');
        return 'card-filter-view-tmpl';
    },

    render: function() {
        var _this = this;
        var status = this.options.status || '';
        W.getApi().call({
            method: 'post',
            app: 'card',
            api: 'card_filter_params/get',
            args:{status:status},
            success: function(data) {
                var html = $.tmpl(this.getTemplate(), {
                    filters: _this.filterData,
                    types: data.card_types || [],
                    card_attrs: data.card_attrs || []
                });
                this.$el.append(html);
                _this.addDatepicker();
                $('.xa-showFilterBox').append($('.xa-timelineControl'));
            },
            error: function(response) {
                alert('加载失败！请刷新页面重试！');
            },
            scope: this
        });
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.render();
        this.filter_value = '';
        this.bind('clickStatusBox', this.clickStatusBox);
    },


    // 初始化日历控件
    addDatepicker: function() {
        var _this = this;
        $('input[data-ui-role="orderDatepicker"]').each(function() {
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

            $datepicker.datetimepicker(options);
        });
    },

    clickStatusBox: function(status_value){
        this.resetFrom();
        // 调用搜索事件
        this.seacrhBtn();
    },

    resetFrom: function(){
        $('#card_name').val('');
        $('#start_date').val('');
        $('#end_date').val('');
        $('#cardType').val(-1);
        $('#cardAttr').val(-1);
        $('#card_num').val('');
    }
});
