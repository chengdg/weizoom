/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * W.view.common.RichTextEditor: 富文本编辑器
 # @constructor
 */
ensureNS('W.view.common');
W.view.common.DatePicker = Backbone.View.extend({
    el: '',

    events: {
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.onSelectDateHandler = options.selectDateHandler || null;
        this.enableTodayAsMinDate = false;
        if (options.hasOwnProperty('enableTodayAsMinDate')) {
            this.enableTodayAsMinDate = options.enableTodayAsMinDate;
        }
    },

    render: function() {
        var _this = this;
        var options = {
            buttonText: '选择日期',
            defaultDate: new Date(),
            numberOfMonths: 1,
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
            beforeShow: function(inputElement, ui) {                
                setTimeout(function() {
                    ui.dpDiv.css({'z-index': 9999});
                });
            },
            onSelect: function(date, ui) {
                if (_this.onSelectDateHandler) {
                    _this.onSelectDateHandler(date);
                }                
                // if(ui.input.attr('name') === 'start_at') {
                //     $endTime.datepicker('option', 'minDate', date);
                // }
                return false;
            }
        }

        if (this.enableTodayAsMinDate) {
            options['minDate'] = new Date();
        }
        this.$el.datepicker(options);
    }
});

W.registerUIRole('[data-ui-role="date-picker-group"]', function() {
    var $datePickerGroup = $(this);
    var $inputs = $datePickerGroup.find('[data-ui-role="date-picker"]');

    var count = $inputs.length;
    var onSelectDateHandler = function(date) {
        if (count == 2) {
            $inputs.eq(1).datepicker('option', 'minDate', date);
        }
    }
    for (var i = 0; i < count; ++i) {
        var $input = $inputs.eq(i);
        var enableTodayAsMinDate = ($input.attr('data-today-as-min-date') === 'true');
        var options = {
            el: $input.get(),
            enableTodayAsMinDate: enableTodayAsMinDate
        };
        if (count == 2 && i == 0) {
            //对2个date picker中的第一个设置select date的handler
            options['selectDateHandler'] = onSelectDateHandler;
        }
        var view = new W.view.common.DatePicker(options);
        view.render();

        //缓存view
        $input.data('view', view);
    };
});