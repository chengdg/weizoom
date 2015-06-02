/*
Copyright (c) 2011-2012 Weizoom Inc
*/
ensureNS('W.view.common');

W.view.common.fansECharts = Backbone.View.extend({
    getTemplate: function() {
        $('#common-fans-echart-tmpl-src').template('common-fans-echart-tmpl');
        return 'common-fans-echart-tmpl';
    },

    events: {
        'mouseover .xa-tips': 'onMouseoverTips',
        'mouseout .xa-tips': 'onMouseoutTips',
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.options = options;
        this.api = options.api;
        this.app = options.app;
        this.resource = options.resource;
        this.type = options.type;
        this.wrapEl = options.wrapEl;
        this.template = this.getTemplate();
    },

    render: function() {
        this.$el.addClass("wui-echart");
        var data = {
            id: this.$el.attr('id')
        }
        var $node = $.tmpl(this.template, data);

        this.$el.append($node);
        W.createWidgets(this.$el);
        this.$chart = this.$('.wui-i-content').eq(0);

        this.load();
    },

    reload: function(options) {
        this.load();
    },

    load: function(options) {
        var args = {};
        var _this = this;
        W.getApi().call({
            app: this.options.app,
            resource: this.options.resource,
            method: 'get',
            args: args,
            scope: this,
            success: function(data) {
                var option = data;
                xlog(_this.$chart.get(0));
                var myChart = echarts.init(_this.$chart.get(0));
                xlog(_this.$chart.get(0));
                // 为echarts对象加载数据 
                option.legend = null;  //强制去除图例信息
                myChart.setOption(option);
            },
            error: function(resp) {
                alert('获取统计数据失败!');
            }
        });
    },

    onMouseoverTips: function(event){
        console.log('onMouseoverTips', this.wrapEl)
        if (this.wrapEl) {
            $(this.wrapEl).css("display","block");
        };
    },

    onMouseoutTips: function(event){
        if (this.wrapEl) {
            $(this.wrapEl).css("display","none");     
        }   
    },
});

W.registerUIRole('div[data-ui-role="fansEchart"]', function() {
    var $div = $(this);
    $div.removeData('view');
    var api = $div.attr('data-api');
    var app = $div.attr('data-app');
    var resource = $div.attr('data-resource');
    var type = $div.attr('data-type') || "chart";
    var isActive = $div.attr('data-isactive');
    var args = $div.attr('data-args');
    var wrapEl = $div.attr('data-wrap-el') || null;
    if (args) {
        args = $.parseJSON(args);
    }

    var echart = new W.view.common.fansECharts({
        el: $div.get(0),
        app: app,
        api: api,
        resource: resource,
        type: type,
        args: args,
        wrapEl: wrapEl
    });
    echart.render();

    $div.data('view', echart);
});