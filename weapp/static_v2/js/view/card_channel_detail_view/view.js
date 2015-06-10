ensureNS('W.view.card');
W.view.card.channelDetailFilter = Backbone.View.extend({
    events: {
        'click .seacrh-order-btn': 'seacrhBtn',
        'click .recently-week-day': 'setDateText',
        'click .xa-reset': 'onClickResetButton'
    },

    // 点击‘最近7天’或‘最近30天’
    setDateText: function(event){
        var $this = $(event.currentTarget);
        $this.parent().children().css("color","black");
        $this.css("color","#1262b7");
        var day = $this.attr('data-day') -1 ;//parseInt(.toSting()) - 1;
        var today = new Date(); // 获取今天时间

        today.setTime(today.getTime()-day*24*3600*1000);
        var begin = $.datepicker.formatDate('yy-mm-dd', today);
        var end = $.datepicker.formatDate('yy-mm-dd', new Date());

        $('#start_date').val(begin);
        $('#end_date').val(end);
        $('.seacrh-order-btn').trigger('click');
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
        console.log('dataView.options.args', dataView.options.args)
        dataView.reload();
        this.$el.trigger('end_click');
        this.setStatusActive();
    },

    // 获取条件数据
    getFilterValue: function(){
        var dataValue = [];
        var orderId = $('#order_id').val().trim();
        var cardId = $('#weizoom_card_id').val().trim();
        var cardName = $('#weizoom_card_name').val().trim();
        var startDate = $('#start_date').val().trim();
        var endDate = $('#end_date').val().trim();

        var moneyRex = /^\d*(\.\d{0,2})?$/;
        var lowMoney = $('#low_money').val().trim();
        var highMoney = $('#high_money').val().trim();
        if(!moneyRex.test(lowMoney) || !moneyRex.test(highMoney)){
            W.showHint('error', '请输入正确的价格');
            return false;
        }
        if (lowMoney.length === 0 && highMoney.length > 0) {
            W.showHint('error', '请输入起始价格！');
            return false;
        }
        if (highMoney.length === 0 && lowMoney.length > 0) {
            W.showHint('error', '请输入最高价格！');
            return false;
        }
        if (parseFloat(highMoney) < parseFloat(lowMoney)) {
            W.showHint('error', '最高价格不能低于起始价格');
            return false;
        }

        var cardStatus = $('#cardStatus').val();
        var memberName = $('#member_name').val().trim();

        var args = [];
        //card_id
        if (cardId.length > 0) {
            dataValue.push('card_id:'+cardId);
        }
        // card_name
        if (cardName.length > 0) {
            dataValue.push('name:'+cardName);
        }
        //order_id
        if (orderId.length > 0) {
            dataValue.push('order_id:'+orderId);
        }
        //status
        if (cardStatus != -1) {
            dataValue.push('status:'+cardStatus);
        }
        //use_name
        if (memberName != '') {
            dataValue.push('member:'+memberName);
        }
        // money
        if (lowMoney.length > 0 && highMoney.length > 0) {
            dataValue.push('money:'+lowMoney+'-'+highMoney)
        }
        //created_at
        if (startDate != "" && endDate != "") {
            dataValue.push('created_at:'+startDate+'--'+endDate)
        }

        var filter_value = dataValue.join('|');

        if (filter_value != ''){
            args.push('"filter_value":"'+filter_value+'"');
        }

        this.filter_value = filter_value;

        return args;
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

    getTemplate: function() {
        $('#card-channel-detail-filter-view-tmpl-src').template('card-channel-detail-filter-view-tmpl');
        return 'card-channel-detail-filter-view-tmpl';
    },

    render: function() {
        var _this = this;
        var status = this.options.status || '';
        var start_date = this.options.start_date || '';
        var end_date = this.options.end_date || '';
        W.getApi().call({
            method: 'post',
            app: 'card',
            api: 'card_channel_filter_params/get',
            args:{status:status},
            success: function(data) {
                var html = $.tmpl(this.getTemplate(), {
                    filters: _this.filterData,
                    cardStatus: data.cardStatus || [],
                    cardTypes: data.cardTypes || []
                });
                this.$el.append(html);
                _this.addDatepicker();
                $('.xa-showFilterBox').append($('.xa-timelineControl'));
                //时间
                $('#start_date').val(start_date);
                $('#end_date').val(end_date);
                var today = $.datepicker.formatDate('yy-mm-dd', new Date());//获取今天的日期
                if (end_date == today){
                    end_date = end_date.replace(/-/g,"/");
                    var a = new Date(end_date);
                    start_date = start_date.replace(/-/g,"/");
                    var b = new Date(start_date);
                    var dif = a.getTime() - b.getTime();
                    var day = Math.floor(dif / (1000 * 60 * 60 * 24));//计算天数
                    day+=1;
                    if (day==30 || day==60 || day==7){
                        $('.recently-week-day[data-day='+day+']').css("color","#1262b7");
                    }
                }
            },
            error: function(response) {
                alert('加载失败！请刷新页面重试！');
            },
            scope: this
        });
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
                numberOfMonths: 1,
                dateFormat: 'yy-mm-dd',
                timeFormat: '',
                closeText: '关闭',
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

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.render();
        this.filter_value = '';
    },

    onClickResetButton: function(){
        var $that = $('.recently-week-day[data-day=7]');
        $that.parent().children().css("color","black");
        $that.css("color","#1262b7");
        var day = $that.attr('data-day') -1 ;//parseInt(.toSting()) - 1;
        var today = new Date(); // 获取今天时间
        today.setTime(today.getTime()-day*24*3600*1000);
        var begin = $.datepicker.formatDate('yy-mm-dd', today);
        var end = $.datepicker.formatDate('yy-mm-dd', new Date());
        $('#start_date').val(begin);
        $('#end_date').val(end);
        $('#order_id').val('');
        $('#weizoom_card_id').val('');
        $('#weizoom_card_name').val('');
        $('#low_money').val('');
        $('#high_money').val('');
        $('#cardStatus').val(-1);
        $('#member_name').val('');
    }
});
