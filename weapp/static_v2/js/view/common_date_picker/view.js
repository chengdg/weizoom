/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * W.view.common.DatePicker: 日期选择器
 # @constructor
 */
ensureNS('W.view.common');
W.view.common.DatePicker = Backbone.View.extend({
    el: '',

    events: {
        
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.onSelectDateHandler = null;
        this.min = this.$el.attr('data-min');
        this.$minEl = $(this.$el.attr('data-min-el'));
        this.max = this.$el.attr('data-max');
        this.$maxEl = $(this.$el.attr('data-max-el'));

        this.isEnableTimePicker = !!this.$el.data('enableSelectTime');
    },

    render: function() {
        var _this = this;
        var options = {
            buttonText: '选择日期',
            currentText: '当前时间',
            hourText: "小时",
            minuteText: "分钟",
            showTimepicker: this.isEnableTimePicker,
            showButtonPanel: this.isEnableTimePicker,
            defaultDate: new Date(),
            numberOfMonths: 1,
            dateFormat: 'yy-mm-dd',
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
            beforeShow: function(inputElement, ui) {
                if(_this.min === 'now') {
                    $(this).datepicker('option', 'minDate', new Date());
                }else if(_this.min){
                    $(this).datepicker('option', 'minDate', _this.min);
                }

                if(_this.$minEl.length > 0){
                    var startTime = _this.$minEl.val();
                    startTime = startTime.split(' ');
                    $(this).datepicker('option', 'minDate', startTime[0]);
                    if(startTime.length == 2){
                        $(this).datepicker('option', 'minDateTime', new Date(startTime[0].replace('-','/').replace('-','/')+' '+startTime[1]+':00'));
                    }
                }

                if(_this.max === 'now') {
                    $(this).datepicker('option', 'maxDate', new Date());
                }else if(_this.max){
                    $(this).datepicker('option', 'maxDate', _this.max);
                }

                if(_this.$maxEl.length > 0){
                    var endTime = _this.$maxEl.val();
                    endTime = endTime.split(' ')
                    $(this).datepicker('option', 'maxDate', endTime[0]);
                    if(endTime.length == 2){
                        $(this).datepicker('option', 'maxDateTime', new Date(endTime[0].replace('-','/').replace('-','/')+' '+endTime[1]+':00'));
                    }
                }

                setTimeout(function() {
                    ui.dpDiv.css({'z-index': 9999});
                });
            },
            onSelect: function(date, ui) {
                _this.trigger('select-date', date);
            }
        }

        this.$el.datetimepicker(options);
    }
});

W.registerUIRole('[data-ui-role="date-picker"]', function() {
    var $input = $(this);
    var view = new W.view.common.DatePicker({
        el: $input.get(0)
    });
    view.render();

    //缓存view
    $input.data('view', view);
});