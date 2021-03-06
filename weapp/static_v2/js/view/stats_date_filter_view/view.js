ensureNS('W.view.stats');
W.view.stats.DateFilterView = Backbone.View.extend({
    events: {
        'click .xa-shortcut': 'onClickShortcut'
    },

    templates: {
        "viewTmpl": "#stats-date-filter-view-tmpl-src"
    },

    initialize: function(options) {
        this.$el = $(this.el);
    },

    render: function() {
        var html = this.getTmpl('viewTmpl')({});
        this.$el.append(html);
        this.addDatepicker();
    },

    onClickShortcut: function(event) {
        var start_el = this.$('[name="start_date"]').val('');
        var end_el = this.$('[name="end_date"]').val('');

        this.$('.xui-i-activeLink').removeClass('xui-i-activeLink');
        $(event.target).addClass('xui-i-activeLink');
        var days = $(event.target).data('value');

        var now = new Date();
        var target_date_str = this.getPastDateStr(now, days);
        start_el.val(target_date_str);
        if (days == 1) {
            end_el.val(target_date_str);
        } else {
            end_el.val(this.getDateStr(now));
        }
        $('.xa-date-search').trigger("click");
    },

    getDateStr: function(date) {
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var date = date.getDate();

        var result = year + "-";
        if (month < 10) result += "0";
        result += month + "-";
        if (date < 10) result += "0";
        result += date;

        return result;
    },

    getPastDateStr: function(now, days) {
        if (days < 0) {
            return "2014-01-01";
        }

        var now_time = now.getTime();
        var target_time = now_time - (days * 24 * 60 * 60 * 1000);
        return this.getDateStr(new Date(target_time));
    },

    updateTimeTags: function() {
        var now = new Date();
        var days, tmp_start_date, tmp_end_date;
        var view_obj = this;
        var start_date = this.$('[name="start_date"]').val();
        var end_date = this.$('[name="end_date"]').val();

        this.$('.xui-i-activeLink').removeClass('xui-i-activeLink');
        this.$('.xui-i-shortcutLink').each(function() {
            days = $(this).data('value');
            tmp_start_date = view_obj.getPastDateStr(now, days);
            if (days == 1) {
                tmp_end_date = tmp_start_date;
            } else {
                tmp_end_date = view_obj.getDateStr(now);
            }

            if ((start_date.indexOf(tmp_start_date) >= 0) && (end_date.indexOf(tmp_end_date) >= 0)) {
                $(this).addClass('xui-i-activeLink');
                return false;
            }
        });
    },

    // 初始化日历控件
    addDatepicker: function() {
        var _this = this;
        $('input[data-ui-role="orderDatepicker"]')
            .each(
                function() {
                    var $datepicker = $(this);
                    var format = $datepicker.attr('data-format');
                    var min = $datepicker.attr('data-min');
                    var max = $datepicker.attr('data-max');
                    var $min_el = $($datepicker.attr('data-min-el'));
                    var $max_el = $($datepicker.attr('data-max-el'));
                    var options = {
                        buttonText: '选择日期',
                        currentText: '当前时间',
                        // hourText : "小时",
                        // minuteText : "分钟",
                        showTimepicker: false,
                        numberOfMonths: 1,
                        dateFormat: 'yy-mm-dd',
                        //dateFormat: format,
                        closeText: '关闭',
                        prevText: '&#x3c;上月',
                        nextText: '下月&#x3e;',
                        monthNames: ['一月', '二月', '三月', '四月', '五月',
                            '六月', '七月', '八月', '九月', '十月', '十一月',
                            '十二月'
                        ],
                        monthNamesShort: ['一', '二', '三', '四', '五',
                            '六', '七', '八', '九', '十', '十一', '十二'
                        ],
                        dayNames: ['星期日', '星期一', '星期二', '星期三', '星期四',
                            '星期五', '星期六'
                        ],
                        dayNamesShort: ['周日', '周一', '周二', '周三', '周四',
                            '周五', '周六'
                        ],
                        dayNamesMin: ['日', '一', '二', '三', '四', '五',
                            '六'
                        ],
                        beforeShow: function(e) {
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
                        onClose: function() {}
                    };

                    $datepicker.datetimepicker(options);
                });
    }
});
