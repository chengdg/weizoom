/*
Copyright (c) 2011-2012 Weizoom Inc
*/
ensureNS('W.view.stats');

W.view.stats.MemberIncreasementEchart = Backbone.View.extend({
    getTemplate: function() {
        $('#stats-member-increasement-echart-tmpl-src').template('stats-member-increasement-echart-tmpl');
        return 'stats-member-increasement-echart-tmpl';
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

    reload: function(args) {
        this.load(args);
    },

    load: function(args) {
        this.loadChart(args);
    },

    loadChart: function(args) {
        var _this = this;
        xlog(args);
        W.getApi().call({
            app: this.options.app,
            resource: this.options.resource,
            method: 'get',
            args: args,
            scope: this,
            success: function(data) {
                var option = data;
                var myChart = echarts.init(_this.$chart.get(0));
                // 为echarts对象加载数据 
                myChart.setOption(option);
            },
            error: function(resp) {
                // alert('获取统计数据失败!');
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

W.registerUIRole('div[data-ui-role="statsMemberIncreasementEchart"]', function() {
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

    var echart = new W.view.stats.MemberIncreasementEchart({
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