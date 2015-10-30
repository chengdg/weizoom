/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 微众卡规则追加时间对话框
 */
ensureNS('W.weapp.dialog.AppendWeizoomCardTimeDialog');
W.weapp.dialog.AppendWeizoomCardTimeDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .btn-cancel': 'onClickCancel'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#weizoom-card-append-card-time-dialog-tmpl-src').template('weizoom-card-append-card-time-dialog-tmpl');
        return "weizoom-card-append-card-time-dialog-tmpl";
    },

    onInitialize: function(options) {
        $('input[data-ui-role="date_time_picker_append"]').each(function() {
            var $datetimepicker = $(this);
            var format = $datetimepicker.attr('data-format');
            var min = $datetimepicker.attr('data-min');
            var max = $datetimepicker.attr('data-max');
            var $min_el = $($datetimepicker.attr('data-min-el'));
            var $max_el = $($datetimepicker.attr('data-max-el'));
            var options = {
                buttonText: '选择日期',
                numberOfMonths: 1,
                dateFormat: format,
                //timeFormat: 'HH:mm',
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
                        $(this).datetimepicker('option', 'minDate', new Date());
                    }else if(min){
                        $(this).datetimepicker('option', 'minDate', min);
                    }

                    if($min_el){
                        var startTime = $min_el.val();
                        if(startTime) {
                            $(this).datetimepicker('option', 'minDate', startTime);
                        }
                    }

                    if(max === 'now') {
                        $(this).datetimepicker('option', 'maxDate', new Date());
                    }else if(max){
                        $(this).datetimepicker('option', 'maxDate', max);
                    }

                    if($max_el){
                        var endTime = $max_el.val();
                        if(endTime) {
                            $(this).datetimepicker('option', 'maxDate', endTime);
                        }
                    }
                },
                onClose: function() {
                }
            };

            $datetimepicker.datetimepicker(options);
        });
    },

    onShow: function(options) {
        $('#valid_time_append').val('');
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var card_append_time = $.trim(this.$dialog.find('input[name="valid_time_append"]').val());
        if (card_append_time.length == 0) {
            W.showHint('error','请选择延期时间');
            return false;
        }
        data = {
            'rule_id': "",
            'card_append_time': card_append_time
        }
        return data;
    },
    
    /**
     * onClickCancel: 点击取消按钮的响应函数
     */
    onClickCancel: function(event) {
        this.$dialog.modal('hide');
    }
});