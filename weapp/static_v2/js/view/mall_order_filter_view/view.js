ensureNS('W.view.mall.order');
W.view.mall.order.orderFilter = Backbone.View.extend({
    events: {
        'click .xa-create': 'createFilter',
        'click .xa-filter': 'filter',
        'click .seacrh-order-btn': 'seacrhBtn',
        'click .recently-week-day': 'setDateText',
        'click .export-btn': 'exportBtn'
    },

    // 点击‘最近7天’或‘最近30天’
    setDateText: function(event){
        var day = $(event.currentTarget).attr('data-day') -1 ;//parseInt(.toSting()) - 1;
        //获取要作用于哪个时间控件商
        var today = new Date(); // 获取今天时间
        today.setTime(today.getTime()-day*24*3600*1000);
        var begin = $.datepicker.formatDate('yy-mm-dd 00:00', today);
        var end = $.datepicker.formatDate('yy-mm-dd 23:59', new Date());
        $("input[name='start_date']").val(begin);
        $("input[name='end_date']").val(end);
    },
    // 点击‘筛选’按钮事件
    seacrhBtn: function(){
        // 时间类型，下单，付款，发货，
        var date_type = $("#date_type_select").val();
        var startDate = $("input[name='start_date']").val();
        var endDate = $("input[name='end_date']").val();
        //对三个时间选择框进行校验

        this.checkStartAndEndDate(startDate,endDate,date_type);

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
        var shipName = $('#ship_name').val().trim();
        var shipTel = $('#ship_tel').val().trim();
        var orderStatus = $('#orderStatus').val();
        var orderType = $('#orderType').val();
        var payType = $('#payType').val();
        var orderSource = $('#orderSource').val();
        var productName = $('#product_name').val().trim();

        var startDate = $("input[name='start_date']").val().trim();
        var endDate = $("input[name='end_date']").val().trim();
        var date_type = $("#date_type_select").val();
        var expressNumber = $('#express_number').val().trim();


        if ($('#isonlyweizoomcardpay').is(':checked')) {
            var isUseWeizoomCard = 1;
        }else {
            var isUseWeizoomCard = 0;
        }
        var args = [];

        // query
        if (orderId.length > 0) {
            args.push('"query":"'+orderId+'"')
        }

        // ship_name
        if (shipName.length > 0) {
            args.push('"ship_name":"'+shipName+'"')
        }
        // ship_tel
        if (shipTel.length > 0) {
            args.push('"ship_tel":"'+shipTel+'"')
        }
        //product_name
        if (productName.length > 0) {
            args.push('"product_name":"'+productName+'"');
        }
        // pay_type
        if (payType != '-1') {
            args.push('"pay_type":"'+payType+'"')
        }
        // express_number
        if (expressNumber.length > 0) {
            args.push('"express_number":"'+expressNumber+'"')
        }
        // order_source
        if (orderSource != '-1') {
            args.push('"order_source":"'+orderSource+'"')
        }
        // order_status
        // if (orderStatus != '-1') {
            args.push('"order_status":"'+orderStatus+'"')
        // }
        //date_interval
        if (startDate != "" && endDate != "") {
            args.push('"date_interval":"'+startDate+'|'+endDate+'"')
        }
        if (date_type != "") {
            args.push('"date_interval_type":"'+date_type+'"' )
        }

        //is_only_show_pay_by_weizoom_card
        if (isUseWeizoomCard) {
            args.push('"isUseWeizoomCard":"'+isUseWeizoomCard+'"')
        }
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

    // 组织导出的查询参数格式
    getArgsExportValueByDict: function(args){
        if (args.length == 0) {
            return ""
        }else{
            for (var i = args.length - 1; i >= 0; i--) {
                args[i] = args[i].replace(/"/g, '').replace(':', '=')
            };
            return args.join('&');
        }
    },

    getTemplate: function() {
        $('#mall-order-filter-view-tmpl-src').template('mall-order-filter-view-tmpl');
        return 'mall-order-filter-view-tmpl';
    },

    render: function() {
    	var _this = this;
        var status = this.options.status || '';
        W.getApi().call({
            method: 'get',
            app: 'mall2',
            resource: 'order_filter_params',
            args:{status:status},
            success: function(data) {
                var html = $.tmpl(this.getTemplate(), {
                	filters: _this.filterData,
	            	types: data.type || [],
		        	statuses: data.status || [],
		        	payTypes: data.pay_interface_type || [],
		        	orderSources: data.source || []
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

    initialize: function(options) {
    	this.options = options || {};
    	this.$el = $(options.el);
        this.render();
    	this.filter_value = '';
        this.bind('clickStatusBox', this.clickStatusBox);
    },

    // 导出按钮事件
    exportBtn: function(event){
        console.log('导出');
        var status = this.options.status || '';
        var url = '/mall2/order_export/';
        var args = this.getFilterValue();
        args = this.getArgsExportValueByDict(args);
        if (args.length > 0) {
            url = url + '?'+args+'&status='+status;
        } else {
            url = url + '?status='+status;
        }

        console.log(url, args);
       // W.getLoadingView().show();
        $('#spin-hint').html('玩命导出中...');
        var $frame=$('<iframe>').hide().attr('src',url);
        $('body').append($frame);
        setTimeout(function(){W.getLoadingView().hide()}, 5000);
    },

    // 设置状态选中事件
    setStatusActive: function(){
        var status = $('#orderStatus').val();
        $('.xa-count').removeClass('active');
        $('[data-total-status-value="'+status+'"]').addClass('active');
    },

    clickStatusBox: function(status_value){
        this.resetFrom();
        $('#orderStatus').val(status_value);
        // 调用搜索事件
        this.seacrhBtn();
    },
    //根据输入id的不同，分别对下单，付款，发货三者时间进行校验
    checkStartAndEndDate: function(startDate,endDate,tip_info){
        if (1==tip_info){
            tip_info= "下单"
        }else if (2==tip_info){
            tip_info = "付款"
        }else if (3 == tip_info){
            tip_info = "发货"
        }
        if (startDate.length > 0 && endDate.length == 0) {
            W.getErrorHintView().show('请输入'+tip_info+'结束日期！');
            return false;
        }
        if (endDate.length > 0 && startDate.length == 0) {
            W.getErrorHintView().show('请输入'+tip_info+'开始日期！');
            return false;
        }
        var start = new Date(startDate.replace("-", "/").replace("-", "/"));
        var end = new Date(endDate.replace("-", "/").replace("-", "/"));
        if ((startDate.length > 0 || endDate.length > 0) && start > end){
            W.getErrorHintView().show(tip_info+'开始日期不能大于结束日期！');
            return false;
        }
    },
    resetFrom: function(){
        $('#order_id').val('');
        $('#ship_name').val('');
        $('#ship_tel').val('');
        $('#start_date').val('');
        $('#end_date').val('');
        $('#orderStatus').val(-1);
        $('#payType').val(-1);
        $('#orderType').val(-1);
        $('#orderSource').val(-1);
        $('#express_number').val('');
        $('#product_name').val('');
    }
});
