/*
Copyright (c) 2011-2012 Weizoom Inc
*/
ensureNS('W.view.common');

W.view.common.ECharts = Backbone.View.extend({
    getTemplate:function() {
        $('#common-echart-tmpl-src').template('common-echart-tmpl');
        return 'common-echart-tmpl';
    },

	events:  {
        'click .xa-shortcut': 'onClickShortcut'
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
        this.startDateView.on('select-date', onSelectDate);
        this.endDateView = this.$('[name="end_date"]').data('view');
        this.endDateView.on('select-date', onSelectDate);
        this.updateDateField(6);  //设置筛选日期框的值  duhao 20150917
        this.load();
	},

    reload: function(options) {
        this.load();
    },

    load: function(options) {
        var args = {};

        var startDate = this.$('[name="start_date"]').val();
        var endDate = this.$('[name="end_date"]').val();
        if (startDate && endDate) {
            args['days'] = startDate + '~' + endDate;
        }

        if (!args.days) {
            days = this.$('.wui-i-activeLink').data('value');
            args['days'] = days;
        }

        if (args.days) {
            if (this.options.args) {
                _.extend(args, this.options.args);
            }

            if (this.type === 'table') {
                this.loadTable(args);
            } else {
                this.loadChart(args);
            }
        }
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
        // this.$('[name="start_date"]').val('');
        // this.$('[name="end_date"]').val('');
        this.$('.wui-i-activeLink').removeClass('wui-i-activeLink');
        $(event.target).addClass('wui-i-activeLink');
        this.updateDateField($(event.target).data('value'));  //设置筛选日期框的值  duhao 20150917
        this.load();
    },

    updateDateField: function(days) {
        var now = new Date();
        var target_date_str = this.getPastDateStr(now, days);
        this.$('[name="start_date"]').val(target_date_str);
        if (days == 1) {
            this.$('[name="end_date"]').val(target_date_str);
        } else {
            this.$('[name="end_date"]').val(this.getDateStr(now));
        }
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

    onSelectDate: function(date) {
        this.$('.wui-i-activeLink').removeClass('wui-i-activeLink');
        this.load()
    }
});

// W.registerUIRole('div[data-ui-role="echart-section"]', function() {
//     var $div = $(this);
//     var api = $div.attr('data-api');
//     var app = $div.attr('data-app');
//     var type = $div.attr('data-type');
//     var isactive = $div.attr('data-isactive');
//     var interlock_chart = $div.attr('data-show-pic') || '';
//     if (interlock_chart==='true' || interlock_chart==='True') {
//     	interlock_chart = true;
//     } else {
//     	interlock_chart = false;
//     }

//     var echart = new W.view.common.Echarts({
//         app: 'app/' + app,
//         el: $div[0],
//         api: api,
//         type: type,
//         interlock_chart: interlock_chart
//     });
//     if (isactive === 'true') {
//         echart.render();
//     }

//     $div.data('view', echart);
// });

W.registerUIRole('div[data-ui-role="echart"]', function() {
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

        var echart = new W.view.common.ECharts({
            el: $div.get(0),
            app: app,
            api: api,
            type: type,
            args: args
        });
        echart.render();

        $div.data('view', echart);
    });