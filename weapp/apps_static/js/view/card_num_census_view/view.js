ensureNS('W.view.card');
W.view.card.numFilter = Backbone.View.extend({
    events: {
        'click .seacrh-order-btn': 'seacrhBtn',
        'click .xui-dateFilter': 'setDateText',
        'click .xa-reset': 'onClickResetButton',
        'click .xa-reset-create-dateFilter,.xa-reset-activate-dateFilter,.xa-reset-use-dateFilter': 'onClickResetDateFilter'
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
        if ($this.hasClass('create_recently-week-day')){
            $('#create_start_date').val(begin);
            $('#create_end_date').val(end);
        }
        if ($this.hasClass('activate_recently-week-day')){
            $('#activate_start_date').val(begin);
            $('#activate_end_date').val(end);
        }
        if ($this.hasClass('use_recently-week-day')){
            $('#use_start_date').val(begin);
            $('#use_end_date').val(end);
        }
        // $('.seacrh-order-btn').trigger('click');
    },

    // 点击‘查询’按钮事件
    seacrhBtn: function(){
        var createStartDate = $('#create_start_date').val();
        var createEndDate = $('#create_end_date').val();
        var activateStartDate = $('#activate_start_date').val();
        var activateEndDate = $('#activate_end_date').val();
        var useStartDate = $('#use_start_date').val();
        var useEndDate = $('#use_end_date').val();
        if ((createStartDate.length > 0 && createEndDate.length == 0)||(activateStartDate.length > 0 && activateEndDate.length == 0)||(useStartDate.length > 0 && useEndDate.length == 0)) {
            W.getErrorHintView().show('请输入结束日期！');
            return false;
        }
        if ((createEndDate.length > 0 && createStartDate.length == 0)||(activateEndDate.length > 0 && activateStartDate.length == 0)||(useEndDate.length > 0 && useStartDate.length == 0)) {
            W.getErrorHintView().show('请输入开始日期！');
            return false;
        }
        var create_start = new Date(createStartDate.replace("-", "/").replace("-", "/"));
        var create_end = new Date(createEndDate.replace("-", "/").replace("-", "/"));
        var activate_start = new Date(activateStartDate.replace("-", "/").replace("-", "/"));
        var activate_end = new Date(activateEndDate.replace("-", "/").replace("-", "/"));
        var use_start = new Date(useStartDate.replace("-", "/").replace("-", "/"));
        var use_end = new Date(useEndDate.replace("-", "/").replace("-", "/"));
        if ((createStartDate.length > 0 || createEndDate.length > 0) && create_start > create_end){
            W.getErrorHintView().show('开始日期不能大于结束日期！');
            return false;
        }
        if ((activateStartDate.length > 0 || activateEndDate.length > 0) && activate_start > activate_end){
            W.getErrorHintView().show('开始日期不能大于结束日期！');
            return false;
        }
        if ((useStartDate.length > 0 || useEndDate.length > 0) && use_start > use_end){
            W.getErrorHintView().show('开始日期不能大于结束日期！');
            return false;
        }

        var dataView = this.options.dataView;
        var args = this.getFilterValue();
        dataView.options.args = this.getFilterValueByDict(args);
        dataView.setPage(1);
        dataView.reload();
        this.$el.trigger('end_click');
    },

    // 获取条件数据
    getFilterValue: function(){
        var dataValue = [];
        var cardId = $('#weizoom_card_id').val().trim();
        var cardName = $('#weizoom_card_name').val().trim();
        var cardType = $('#weizoom_card_type').val();

        var createStartDate = $('#create_start_date').val().trim();
        var createEndDate = $('#create_end_date').val().trim();
        var activateStartDate = $('#activate_start_date').val().trim();
        var activateEndDate = $('#activate_end_date').val().trim();
        var useStartDate = $('#use_start_date').val().trim();
        var useEndDate = $('#use_end_date').val().trim();

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

        var orderId = $('#order_id').val().trim();

        var args = [];

        // query
        if (cardId.length > 0) {
            dataValue.push('card_id:'+cardId)
        }
        if (cardStatus != -1) {
            dataValue.push('status:'+cardStatus);
        }
        if (cardType != -1) {
            dataValue.push('type:'+cardType);
        }
        if (memberName != '') {
            dataValue.push('member:'+memberName);
        }
        if (orderId != '') {
            dataValue.push('order_id:'+orderId);
        }
        // ship_name
        if (cardName.length > 0) {
            dataValue.push('name:'+cardName)
        }
        // ship_tel
        if (lowMoney.length > 0 && highMoney.length > 0) {
            dataValue.push('money:'+lowMoney+'-'+highMoney)
        }
        //日期
        if (createStartDate != "" && createEndDate != "") {
            dataValue.push('created_at:'+createStartDate+'--'+createEndDate)
        }
        if (activateStartDate != "" && activateEndDate != "") {
            dataValue.push('activated_at:'+activateStartDate+'--'+activateEndDate)
        }
        if (useStartDate != "" && useEndDate != "") {
            dataValue.push('used_at:'+useStartDate+'--'+useEndDate)
        }

        var filter_value = dataValue.join('|');

        if (filter_value != ''){
            args.push('"filter_value":"'+filter_value+'"')
        }

        this.filter_value = filter_value;

        return args
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

    getTemplate: function() {
        $('#card-num-filter-view-tmpl-src').template('card-num-filter-view-tmpl');
        return 'card-num-filter-view-tmpl';
    },

    render: function() {
        var _this = this;
        var status = this.options.status || '';
        W.getApi().call({
            method: 'post',
            app: 'card',
            api: 'card_num_filter_params/get',
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

                $('.xui-datePicker').val('');
                // $('#end_date').val('');
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

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.render();
        this.filter_value = '';
    },
    //重置
    onClickResetButton: function(){
        var $that_1 = $('.xa-reset-create-dateFilter');
        var $that_2 = $('.xa-reset-activate-dateFilter');
        var $that_3 = $('.xa-reset-use-dateFilter');
        $that_1.parent().children().css("color","black");
        $that_2.parent().children().css("color","black");
        $that_3.parent().children().css("color","black");
        $that_1.css("color","#1262b7");
        $that_2.css("color","#1262b7");
        $that_3.css("color","#1262b7");
        $('.xui-datePicker').val('');
        $('#weizoom_card_id').val('');
        $('#weizoom_card_name').val('');
        $('#weizoom_card_type').val(-1);
        $('#low_money').val('');
        $('#high_money').val('');
        $('#cardStatus').val(-1);
        $('#member_name').val('');
        $('#order_id').val('');
    },
    //不限
    onClickResetDateFilter: function(event){
        var $this = $(event.currentTarget);
        $this.parent().children().css("color","black");
        $this.css("color","#1262b7");
        if ($this.hasClass('xa-reset-create-dateFilter')){
            $('#create_start_date').val('');
            $('#create_end_date').val('');
        }
        if ($this.hasClass('xa-reset-activate-dateFilter')){
            $('#activate_start_date').val('');
            $('#activate_end_date').val('');
        }
        if ($this.hasClass('xa-reset-use-dateFilter')){
            $('#use_start_date').val('');
            $('#use_end_date').val('');
        }
        // $('.seacrh-order-btn').trigger('click');
    }
});
