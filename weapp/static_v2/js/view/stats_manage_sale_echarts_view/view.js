/*
Copyright (c) 2011-2012 Weizoom Inc
*/
ensureNS('W.view.common');

W.view.common.ManageSaleECharts = Backbone.View.extend({
    getTemplate:function() {
        $('#stats-manage-sale-echart-tmpl-src').template('stats-manage-sale-echart-tmpl');
        return 'stats-manage-sale-echart-tmpl';
    },

	events:  {
	},

    initialize: function(options) {
        this.$el = $(this.el);
        this.options = options;
        this.api = options.api;
        this.app = options.app;
        this.type = options.type;
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

        var onSelectDate = _.bind(this.onSelectDate, this);
        this.startDateView = this.$('[name="start_date"]').data('view');
        // this.startDateView.on('select-date', onSelectDate);
        this.endDateView = this.$('[name="end_date"]').data('view');
        // this.endDateView.on('select-date', onSelectDate);
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
    	W.getApi().call({
            app: this.options.app,
            api: this.options.api,
            args: args,
            scope: this,
            success: function(data) {
                var option = data; 
                var myChart = echarts.init(_this.$chart.get(0));
				// 为echarts对象加载数据 
                myChart.setOption(option);
            },
            error: function(resp) {
                //alert('获取统计数据失败!');
            }
        });
    },
    
    pic_data_render: function(char_data) {
    	var type = char_data.type || 'table';
    	if (data.type=='table') {
    		return;
    	}
    	var show_pic_data = data.data;
        var $div = this.$el.parent('div').find('.xa-interlockChart');
        var myChart = echarts.init($div[0]);
		// 为echarts对象加载数据 
        myChart.setOption(data);
    },

    //TODO 完成独立的表格组件
    loadTable: function(args) {
    	var advancedTable = new W.view.common.AdvancedTable({
	        el: this.$el,
	        template: '#table-view-box-tmpl-src',
	        app: this.options.app,
	        api: this.options.api,
	        args: JSON.stringify(args),
	        enablePaginator: true,
	        enableSort: false,
	        pic: this.show_pic
	    });
	    advancedTable.render();
	
	    $(this).data('view', advancedTable);
    },

    onClickShortcut: function(event) {
        this.$('[name="start_date"]').val('');
        this.$('[name="end_date"]').val('');
        this.$('.wui-i-activeLink').removeClass('wui-i-activeLink');
        $(event.target).addClass('wui-i-activeLink');
        this.load();
    },

    onSelectDate: function(date) {
        this.$('.wui-i-activeLink').removeClass('wui-i-activeLink');
        this.load()
    }
});

W.registerUIRole('div[data-ui-role="manage-sale-echart"]', function() {
        var $div = $(this);
        $div.removeData('view');
        var api = $div.attr('data-api');
        var app = $div.attr('data-app');
        var type = $div.attr('data-type') || "chart";
        var isActive = $div.attr('data-isactive');
        var args = $div.attr('data-args');
        if (args) {
            args = $.parseJSON(args);
        }

        var echart = new W.view.common.ManageSaleECharts({
            el: $div.get(0),
            app: app,
            api: api,
            type: type,
            args: args
        });
        echart.render();

        $div.data('view', echart);
    });