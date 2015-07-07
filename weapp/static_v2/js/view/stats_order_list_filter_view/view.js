ensureNS('W.view.stats');
W.view.stats.StatsOrderListFilterView = Backbone.View.extend({
    events: {
        'click .xa-search-stats-order': 'doSearch',
        'click .xa-reset-section-time': 'doReset',
        'click .xa-export-order-list': 'doExport',
        'click .xa-quick-look': 'doQuicklook',
        'change .xa-status-checkbox': 'doStatusCheckbox'
    },

    initialize: function(options) {
        this.$el = $(options.el);
        this.options = options || {};
        this.filter_value = '';
        this.render();

    },

    render: function() {
        var html = $.tmpl(this.getTemplate(), {});
        this.$el.append(html);
        this.addDatepicker();
        $('.xa-showFilterBox').append($('.xa-timelineControl'));
    },

    getTemplate: function() {
        $('#stats-order-filter-view-tmpl-src').template('stats-order-filter-view-tmpl');
        return 'stats-order-filter-view-tmpl';

    },

    doStatusCheckbox: function(event){
        var t = event.target;
        if(!t.checked) {
            var tmpnum = 0;

            this.$('.xa-status-checkbox').each(function(){
                if(!this.checked) tmpnum ++;
            });

            if(tmpnum >= 3) {
                t.checked = true;
                W.getErrorHintView().show('至少要选中一项！');
            }
        }

    },


    // 点击‘筛选’按钮事件
    doSearch: function() {
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
        this.updateTimeTags();
        
        var dataView = this.options.dataView;
        var args = this.getFilterValue();
        console.log(args);
        dataView.options.args = this.getFilterValueByDict(args);
        dataView.setPage(1);
        // console.log('dataView.options.args', dataView.options.args)
        dataView.reload();
        this.$el.trigger('end_click');
        this.setStatusActive();
    },

    updateTimeTags: function() {
        var now = new Date();
        var days, tmp_start_date, tmp_end_date;
        var view_obj = this;
        var start_date = $('#start_date').val();
        var end_date = $('#end_date').val();
        
        this.$('.wui-i-activeLink').removeClass('wui-i-activeLink');
        this.$('.wui-i-shortcutLink').each(function() {
            days = $(this).data('day');
            tmp_start_date = view_obj.getPastDateStr(now, days);
            if(days == 1) {
                tmp_end_date = tmp_start_date;
            } else {
                tmp_end_date = view_obj.getDateStr(now);
            }
            
            if((start_date.indexOf(tmp_start_date) >= 0) && (end_date.indexOf(tmp_end_date) >= 0)) {
                $(this).addClass('wui-i-activeLink');
                return false;
            }
        });
    },

    // 获取条件数据
    getFilterValue: function(){
        var dataValue = [];
        var orderId = $('#order_id').val().trim();
        var product_name = $('#product_name').val().trim();
        var payType = $('#payType').val();
        var repeat_buy = $('#repeat_buy').val();
        var buyer_source = $('#buyer_source').val();
        var startDate = $('#start_date').val();
        var endDate = $('#end_date').val();

        //订单状态
        if ($('#iswait_send').is(':checked')) {
            var iswait_send = 1;
        }else {
            var iswait_send = 0;
        }
        if ($('#isalready_send').is(':checked')) {
            var isalready_send = 1;
        }else {
            var isalready_send = 0;
        }
        if ($('#isalready_complete').is(':checked')) {
            var isalready_complete = 1;
        }else {
            var isalready_complete = 0;
        }

        //优惠抵扣
        if ($('#iswzcard_pay').is(':checked')) {
            var iswzcard_pay = 1;
        }else {
            var iswzcard_pay = 0;
        }
        if ($('#isintegral_deduction').is(':checked')) {
            var isintegral_deduction = 1;
        }else {
            var isintegral_deduction = 0;
        }
        if ($('#isfavorable_coupon').is(':checked')) {
            var isfavorable_coupon = 1;
        }else {
            var isfavorable_coupon = 0;
        }
        if ($('#iswzcard_integral').is(':checked')) {
            var iswzcard_integral = 1;
        }else {
            var iswzcard_integral = 0;
        }
        if ($('#iswzcard_discountcoupon').is(':checked')) {
            var iswzcard_discountcoupon = 1;
        }else {
            var iswzcard_discountcoupon = 0;
        }


        var args = [];


        // query
        if (orderId.length > 0) {
            args.push('"query":"'+orderId+'"')
        }
        // product_name
        if (product_name.length > 0) {
            args.push('"product_name":"'+product_name+'"')
        }
        // payType
        if (payType != '-1') {
            args.push('"pay_type":"'+payType+'"')
        }
        // repeat_buy
        if (repeat_buy != '-1') {
            args.push('"repeat_buy":"'+repeat_buy+'"')
        }
        // buyer_source
        if (buyer_source != '-1') {
            args.push('"buyer_source":"'+buyer_source+'"')
        }
        //date_interval
        if (startDate != "" && endDate != "") {
            args.push('"date_interval":"'+startDate+'|'+endDate+'"')
        }

        //订单状态
        //show_wait_send
        if (iswait_send) {
            args.push('"iswait_send":"'+iswait_send+'"')
        }
        //show_already_receive
        if (isalready_send) {
            args.push('"isalready_send":"'+isalready_send+'"')
        }
        //show_already_complete
        if (isalready_complete) {
            args.push('"isalready_complete":"'+isalready_complete+'"')
        }

        //优惠抵扣
        //show_wait_send
        if (iswzcard_pay) {
            args.push('"iswzcard_pay":"'+iswzcard_pay+'"')
        }
        //show_already_receive
        if (isintegral_deduction) {
            args.push('"isintegral_deduction":"'+isintegral_deduction+'"')
        }
        //show_already_complete
        if (isfavorable_coupon) {
            args.push('"isfavorable_coupon":"'+isfavorable_coupon+'"')
        }        
        //show_already_receive
        if (iswzcard_integral) {
            args.push('"iswzcard_integral":"'+iswzcard_integral+'"')
        }
        //show_already_complete
        if (iswzcard_discountcoupon) {
            args.push('"iswzcard_discountcoupon":"'+iswzcard_discountcoupon+'"')
        } 

        return args
    },

    doQuicklook: function(event) {
        var start_el = this.$('[name="start_date"]').val('');
        var end_el = this.$('[name="end_date"]').val('');
        
        this.$('.wui-i-activeLink').removeClass('wui-i-activeLink');
        $(event.target).addClass('wui-i-activeLink');
        var days = $(event.target).data('day');
        
        var now = new Date();
        var target_date_str = this.getPastDateStr(now, days);
        start_el.val(target_date_str);
        if (days == 1) {
            end_el.val(target_date_str);
            return;
        }
        end_el.val(this.getDateStr(now));
    },
    
    getDateStr: function(date) {
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var date = date.getDate();
        
        var result = year + "-";
        if(month < 10) result += "0";
        result += month + "-";
        if(date < 10) result += "0";
        result += date;
        
        return result;
    },
    
    getPastDateStr: function(now, days) {
        if(days < 0) {
            return "2013-01-01";
        }
        
        var now_time = now.getTime();
        var target_time = now_time - (days * 24 * 60 * 60 * 1000);
        return this.getDateStr(new Date(target_time));
    },

    // 设置状态选中事件
    setStatusActive: function(){
        var status = $('#orderStatus').val();
        $('.xa-count').removeClass('active');
        $('[data-total-status-value="'+status+'"]').addClass('active');
    },

    //重置按钮事件
    doReset:function(){
        var now_date_str = this.getDateStr(new Date());
        $('#start_date').val(now_date_str);
        $('#end_date').val(now_date_str);
        this.updateTimeTags();
        
        $('#product_name').val('');
        $('#order_id').val('');
        $('#payType').val(-1);
        $('#repeat_buy').val(-1);
        $('#buyer_source').val(-1);
        $('.xa-status-checkbox').attr('checked',true);
        $('.xa-discount-checkbox').attr('checked',false);
    },

    // 导出按钮事件
    doExport: function(event){
        console.log('导出');
        var status = this.options.status || '';
        var url = '/stats/order_export/';
        var args = this.getFilterValue();
        console.log(args,">>>>>>>>>>>>>>>");
        args = this.getArgsExportValueByDict(args);
        if (args.length > 0) {
            url = url + '?'+args;
        }
        console.log(url, args);
       // W.getLoadingView().show();
        $('#spin-hint').html('玩命导出中...');
        var $frame=$('<iframe>').hide().attr('src',url);
        $('body').append($frame);
        setTimeout(function(){W.getLoadingView().hide()}, 5000);
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

    // 初始化日历控件
    addDatepicker : function() {
        var _this = this;
        $('input[data-ui-role="date-picker-order"]').each(function() {
            var $datepicker = $(this);
            var format = $datepicker.attr('data-format');
            var min = $datepicker.attr('data-min');
            var max = $datepicker.attr('data-max');
            var $min_el = $($datepicker.attr('data-min-el'));
            var $max_el = $($datepicker.attr('data-max-el'));
            var options = {
                buttonText : '选择日期',
                currentText : '当前时间',
                // hourText : "小时",
                // minuteText : "分钟",
                showTimepicker: false,
                numberOfMonths : 1,
                dateFormat : 'yy-mm-dd',
                //dateFormat: format,
                closeText : '关闭',
                prevText : '&#x3c;上月',
                nextText : '下月&#x3e;',
                monthNames : [ '一月', '二月', '三月', '四月', '五月',
                        '六月', '七月', '八月', '九月', '十月', '十一月',
                        '十二月' ],
                monthNamesShort : [ '一', '二', '三', '四', '五',
                        '六', '七', '八', '九', '十', '十一', '十二' ],
                dayNames : [ '星期日', '星期一', '星期二', '星期三', '星期四',
                        '星期五', '星期六' ],
                dayNamesShort : [ '周日', '周一', '周二', '周三', '周四',
                        '周五', '周六' ],
                dayNamesMin : [ '日', '一', '二', '三', '四', '五',
                        '六' ],
                beforeShow : function(e) {
                    if (min === 'now') {
                        $(this).datetimepicker('option',
                                'minDate', new Date());
                    } else if (min) {
                        $(this).datetimepicker('option',
                                'minDate', min);
                    }

                    if ($min_el) {
                        var startTime = $min_el.val();
                        if (startTime) {
                            $(this).datetimepicker('option',
                                    'minDate', startTime);
                            $(this).datetimepicker('option',
                                    'minDateTime',
                                    new Date(startTime));
                        }
                    }

                    if (max === 'now') {
                        $(this).datetimepicker('option',
                                'maxDate', new Date());
                    } else if (max) {
                        $(this).datetimepicker('option',
                                'maxDate', max);
                    }

                    if ($max_el) {
                        var endTime = $max_el.val();
                        if (endTime) {
                            $(this).datetimepicker('option',
                                    'maxDate', endTime);
                        }
                    }
                },
                onClose : function() {
                }
            };

            $datepicker.datetimepicker(options);
        });
    },

    // 组织筛选的查询参数格式
    getFilterValueByDict: function(args) {
        if (args.length == 0) {
            return ""
        } else {
            args.push('"page":1')
            return '{' + args.join(',') + '}';
        }
    }
});
