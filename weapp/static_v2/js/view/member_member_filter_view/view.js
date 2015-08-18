ensureNS('W.view.member');
W.view.member.memberFilterView = Backbone.View.extend({
    events: {
        'click .xa-create': 'createFilter',
        'click .xa-search': 'seacrhBtn',
        //'click .seacrh-order-btn': 'seacrhBtn',
        'click .recently-week-day': 'setDateText',
        'click .export-btn': 'exportBtn',
        'click .xa-more-filter': 'onClickMoreFilterButton',
        'click .xa-reset': 'onClickReset'
    },

    // 点击‘最近7天’或‘最近30天’
    setDateText: function(event){
        var day = $(event.currentTarget).attr('data-day') -1 ;//parseInt(.toSting()) - 1;
        var today = new Date(); // 获取今天时间

        today.setTime(today.getTime()-day*24*3600*1000);
        var begin = $.datepicker.formatDate('yy-mm-dd', today);;
        var end = $.datepicker.formatDate('yy-mm-dd', new Date());

        $('#start_date').val(begin)
        $('#end_date').val(end);
    },

    // 点击‘筛选’按钮事件
    seacrhBtn: function(){
        var firstPayStartDate = $('#first_pay_start_date').val();
        var firstPayEndDate = $('#first_pay_end_date').val();
        if (firstPayStartDate.length > 0 && firstPayEndDate.length == 0) {
            W.getErrorHintView().show('请输入最后购买结束日期！');
            return false;
        }
        if (firstPayEndDate.length > 0 && firstPayStartDate.length == 0) {
            W.getErrorHintView().show('请输入最后购买开始日期！');
            return false;
        }
        var start = new Date(firstPayStartDate.replace("-", "/").replace("-", "/"));
        var end = new Date(firstPayEndDate.replace("-", "/").replace("-", "/"));
        if ((firstPayStartDate.length > 0 || firstPayEndDate.length > 0) && start > end){
            W.getErrorHintView().show('最后购买开始日期不能大于最后购买结束日期！');
            return false;
        }

        var firstMessageStartDate = $('#last_message_start_time').val();
        var firstMessgeEndDate = $('#last_message_end_time').val();
        if (firstMessageStartDate.length > 0 && firstMessgeEndDate.length == 0) {
            W.getErrorHintView().show('请输入最后对话时间！');
            return false;
        }
        if (firstMessgeEndDate.length > 0 && firstMessageStartDate.length == 0) {
            W.getErrorHintView().show('请输入最后对话时间！');
            return false;
        }
        var start = new Date(firstMessageStartDate.replace("-", "/").replace("-", "/"));
        var end = new Date(firstMessgeEndDate.replace("-", "/").replace("-", "/"));
        if ((firstMessageStartDate.length > 0 || firstMessgeEndDate.length > 0) && start > end){
            W.getErrorHintView().show('最后最后对话时间开始时间不能大于最后对话时间结束时间！');
            return false;
        }

        var subStartDate = $('#sub_start_date').val();
        var subEndDate = $('#sub_end_date').val();
        if (subStartDate.length > 0 && subEndDate.length == 0) {
            W.getErrorHintView().show('请输入关注结束日期！');
            return false;
        }
        if (subEndDate.length > 0 && subStartDate.length == 0) {
            W.getErrorHintView().show('请输入关注开始日期！');
            return false;
        }
        var start = new Date(subStartDate.replace("-", "/").replace("-", "/"));
        var end = new Date(subEndDate.replace("-", "/").replace("-", "/"));
        if ((subStartDate.length > 0 || subEndDate.length > 0) && start > end){
            W.getErrorHintView().show('关注开始日期不能大于关注结束日期！');
            return false;
        }

        $('.m_unit_price').each(function(i, val){
            if (val.value.trim() && isNaN(val.value.trim())) {
                W.getErrorHintView().show('请输入正确客单价！');
                return false;
            }
        });

        $('.pay_money').each(function(i, val){
            if (val.value.trim() && isNaN(val.value.trim())) {
                W.getErrorHintView().show('请输入正确消费总额！');
                return false;
            }
        });

        $('.integral').each(function(i, val){
            if (val.value.trim() && isNaN(val.value.trim())) {
                W.getErrorHintView().show('请输入正确积分！');
                return false;
            }
        });

        //$('.friend_count').each(function(i, val){
         //   if (val.value.trim() && isNaN(val.value.trim())) {
         //       W.getErrorHintView().show('请输入正确好友数！');
         //       return false;
         //   }
        //});

        $('.pay_times').each(function(i, val){
            if (val.value.trim() && isNaN(val.value.trim())) {
                W.getErrorHintView().show('请输入正确购买次数！');
                return false;
            }
        });


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

        var m_unit_price = [];
        $('.m_unit_price').each(function(i, val){
            if (val.value.trim()) {
                m_unit_price.push(val.value.trim());
            }
        });
        if (m_unit_price.length > 0) {
            dataValue.push("unit_price:" + m_unit_price.join('-'));
        }
        var pay_money = [];
        $('.pay_money').each(function(i, val){
            if (val.value.trim()) {
                pay_money.push(val.value.trim());
            }
        });

        if (pay_money.length > 0) {
            dataValue.push("pay_money:"+pay_money.join('-'))
        }
        var integral = [];
        $('.integral').each(function(i, val){
           if (val.value.trim()) {
                integral.push(val.value.trim());
            }
        });
        if (integral.length > 0) {
            dataValue.push("integral:" + integral.join('--'))
        }
       // var friend_count = [];
        //$('.friend_count').each(function(i, val){
        //   if (val.value.trim()) {
        //        friend_count.push(val.value.trim());
         //   }
        //});
        //if (friend_count.length > 0) {
        //    dataValue.push("friend_count:" + friend_count.join('-'))
        //}
        var pay_times = [];
        $('.pay_times').each(function(i, val){
          if (val.value.trim()) {
                pay_times.push(val.value.trim());
            }
        });
        if (pay_times.length > 0) {
            dataValue.push("pay_times:" + pay_times.join('-'))
        }

        var firstPayStartDate = $('#first_pay_start_date').val();
        var firstPayEndDate = $('#first_pay_end_date').val();

        if (firstPayStartDate && firstPayEndDate) {
            dataValue.push("first_pay:"+firstPayStartDate+"--"+firstPayEndDate)
        }

        var subStartDate = $('#sub_start_date').val();
        var subEndDate = $('#sub_end_date').val();
        if (subStartDate && subEndDate) {
            dataValue.push("sub_date:"+ subStartDate+"--"+subEndDate)
        }

        var messageStartDate = $('#last_message_start_time').val();
        var messageEndDate = $('#last_message_end_time').val();
        if (messageStartDate && messageEndDate) {
            dataValue.push("last_message_time:"+ messageStartDate+"--"+messageEndDate)
        }


        var args = [];
        var name = $('#name').val().trim();
        // filter_value=type:object|status:0|pay_interface_type:0|source:0
        if (name) {
            dataValue.push('name:'+name);
        }

        var tagId = $('#member_tag').val().trim();
        if (tagId != -1) {
            dataValue.push('tag_id:'+tagId);
        }
        var grade = $('#grade').val();
        if (grade != -1) {
            dataValue.push('grade_id:'+grade);
        }
        var status = $('#status').val();
        // if (status != -1) {
            //#无论如何这地方都要带有status参数，不然从“数据罗盘-会员分析-关注会员链接”过来的查询结果会有问题
            dataValue.push('status:'+status);
        // }
        var source = $('#source').val();
        if (source != '-1') {
            dataValue.push('source:'+source);
        }

        var filter_value = dataValue.join('|');
        console.log("filter_value", filter_value);

        if (filter_value != ''){
            args.push('"filter_value":"'+filter_value+'"')
        }

        console.log("filters----", filter_value, args);
        this.filter_value = filter_value;
        return args
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

    onClickMoreFilterButton: function(){
        if ($('.more-filter').is(":hidden")){
            $('.more-filter').removeClass('hidden');
             $('.more-filter').show();
             $('.xa-more-filter').html('<span class="mr20">>>收起</span>');
        } else {
            $('.more-filter').addClass('hidden');
            $('.more-filter').hide();
            $('.xa-more-filter').html('<span  class="mr20">>>展开</span>');
        }
    },
    getTemplate: function() {
        $('#member-filter-view-tmpl-src').template('member-filter-view-tmpl');
        return 'member-filter-view-tmpl';
    },

    render: function() {
        var _this = this;
        var status = this.options.status || '';
        W.getApi().call({
            method: 'post',
            app: 'member',
            api: 'members_filter_params/get',
            args:{status:status},
            success: function(data) {
                 var html = $.tmpl(this.getTemplate(), {
                    grades: data.grades,
                    tags: data.tags
                });
                /*var html = $.tmpl(this.getTemplate(), {
                    filters: _this.filterData,
                    types: data.type || [],
                    statuses: data.status || [],
                    payTypes: data.pay_interface_type || [],
                    orderSources: data.source || []
                });*/
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
                numberOfMonths: 1,
                hourText: "小时",
                minuteText: "分钟",
                //dateFormat: format,
                dateFormat: 'yy-mm-dd',
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

        console.log(url, args)
       // W.getLoadingView().show();
        $('#spin-hint').html('玩命导出中...');
        var $frame=$('<iframe>').hide().attr('src',url);
        $('body').append($frame);
        setTimeout(function(){W.getLoadingView().hide()}, 5000);
    },

    // 设置状态选中事件
    setStatusActive: function(){
       /* var status = $('#orderStatus').val();
        $('.xa-count').removeClass('active');
        $('[data-total-status-value="'+status+'"]').addClass('active');*/
    },

    clickStatusBox: function(status_value){
        this.resetFrom();
        $('#orderStatus').val(status_value);
        // 调用搜索事件
        this.seacrhBtn();
    },

    resetFrom: function(){
        $('#name').val('');
        $('#first_pay_start_date').val('');
        $('#first_pay_end_date').val('');
        $('#member_tag').val('-1');
        $('.m_unit_price').val('');
        $('#grade').val(-1);
        $('#sub_start_date').val('');
        $('#sub_end_date').val('');
        $('.pay_money').val('');
        $('.integral').val('');
        $('.friend_count').val('');
        $('.pay_times').val('');
        $('#status').val('-1');
        $('#source').val('-1');
        $('#last_message_start_time').val('');
        $('#last_message_end_time').val('');
    },

    onClickReset:function(){
        this.resetFrom()
    }
});
