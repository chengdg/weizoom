/*
Copyright (c) 2011-2013 Weizoom Inc
*/

/**
 * 全局事件响应
 */
$(document).ready(function(event) {
    //为需要校验的标签增加 星号提示
    $(document).ready(function() {
        $('[data-validate^="requir"]').each(function() {
            var $input = $(this);
            $controlGroup = $input.parents('.form-group');
            if ($controlGroup.length > 0 && !$input.parents('.form-group').hasClass('nostar')) {
                $controlGroup.find('label').eq(0).addClass('star_show');
            }
        });
    });

    //为wx_delete元素安装删除确认机制
    xlog('install hander for wx_delete link')
    // $(document).delegate('.wx_delete', 'click', function(event) {
    //     event.stopPropagation();
    //     event.preventDefault();
    //     var $el = $(event.currentTarget);
    //     var deleteCommentView = W.getItemDeleteView();
    //     deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
    //         window.location.href = $el.attr('href');
    //     });
    //     deleteCommentView.show({
    //         $action: $el,
    //         info: '确定删除吗?'
    //     });
    // });


    //创建datepicker
    // data-min和data-max可以有两种值：
    //      一种为‘now’获取当天日期；
    //      一种为‘2013年09月05日'日期，可以随意设置日期，但格式要和data-format一致。
    $('input[data-ui-role="datepicker"]').each(function() {
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
                dateFormat: format,
                timeFormat: 'HH:mm',
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

});