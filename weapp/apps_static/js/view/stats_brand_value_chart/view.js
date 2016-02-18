ensureNS("W.view.stats");

W.view.stats.BrandValueChart = Backbone.View.extend({
    events: {
        'click .xa-selectBrandValueFreq': 'onChangeDateFreq'
    },

    getTemplate: function() {
        $('#stats-brand-value-echart-tmpl-src').template('stats-brand-value-echart-tmpl');
        return 'stats-brand-value-echart-tmpl';
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.options = options;
        this.template = this.getTemplate();
    },

    render: function() {
        //xlog("in render()");
        $node = $.tmpl(this.template, {});
        this.$chart = $node.find('#stats-brand-value-chart');
        this.$el.append($node);
    },

    reload: function(options) {
        var _this = this;
        args = {
            //"start_date": options.startDate,
            // 如果没有指定endDate，就默认用构造时指定的endDate
            "end_date": options.endDate || _this.options.endDate,
            "freq_type": options.freqType || 'week',
        };
        if (options.periods) {
            args.periods = options.periods;
        }
        W.getApi().call({
            app: 'stats',
            resource: 'brand_value',
            args: args,
            success: function(data) {
                var option = data;
                option.legend = null;
                var echartBrandValue = echarts.init(_this.$chart.get(0));
                echartBrandValue.setOption(data, true);
            },
            error: function(data) {
                xlog("Failed!");
            }
        });
    },


    // 处理选择"周"、"月"的事件
    onChangeDateFreq: function(event) {
        //xlog("in onChangeDateFreq()");
        var $el = $(event.currentTarget);
        this.$el.find('.xa-selectBrandValueFreq').removeClass('xui-bv-period-selected');
        $el.addClass('xui-bv-period-selected')
        //xlog($el.attr('data-value'));
        var freq = $el.attr('data-value');
        var periods = 20;
        if (freq == 'year') {
            periods = 12;
        }
        this.reload({
            freqType: freq,
            periods: periods
        });
    },
});


/*W.registerUIRole('div[data-ui-role="statsBrandValueEChart', function() {

});*/
