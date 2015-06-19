ensureNS('W.view.weixin');
W.view.weixin.RealtimeMessageFilterView = Backbone.View.extend({
    events: {
    	'click .xa-search-realtime-message': 'doSeacrh',
    },
    
    initialize: function(options) {
    	this.$el = $(options.el);
    	
    	this.options = options || {};
    	this.filter_value = '';
    	this.status = -1;
    	
    	this.render();
    	
        this.bind('doClickStatusTag', this.doClickStatusTag);
    },
    
    render: function() {
    	var html = $.tmpl(this.getTemplate(), {});
       	this.$el.append(html);
       	this.addDatepicker();
    },
    
    getTemplate: function() {
        $('#weixin-realtime-message-filter-view-tmpl-src').template('weixin-realtime-message-view-tmpl');
        return 'weixin-realtime-message-view-tmpl';
    },

    // 点击‘筛选’按钮事件
    doSeacrh: function(action){
    	if (action && action === 'search') {
	    	var startDate = $('#start_date').val();
	        var endDate = $('#end_date').val();
	        if (startDate.length > 0 && endDate.length == 0) {
	            W.getErrorHintView().show('请输入结束日期！');
	            return false;
	        }
	        if (endDate.length > 0 && startDate.length == 0) {
	            W.getErrorHintView().show('请输入开始日期！');
	            return false;
	        }
	        var start = new Date(startDate.replace("-", "/").replace("-", "/"));
	        var end = new Date(endDate.replace("-", "/").replace("-", "/"));
	        if ((startDate.length > 0 || endDate.length > 0) && start > end){
	            W.getErrorHintView().show('开始日期不能大于结束日期！');
	            return false;
	        }
        }
        
        var dataView = this.options.dataView;
        var args = this.getFilterValue();
        dataView.options.args = this.getFilterValueByDict(args);
        dataView.setPage(1);
        console.log('dataView.options.args', dataView.options.args)
        
        dataView.reload();
    },

    // 获取条件数据
    getFilterValue: function(){
        var dataValue = [];
        var content = $('#content').val();
        var startDate = $('#start_date').val().trim();
        var endDate = $('#end_date').val().trim();
        if (this.status !== -1) {
            dataValue.push('status:' + this.status);
        }
        if (content && content.length > 0) {
            dataValue.push('content:' + content);
        }
        
        var args = [];
        var filter_value = dataValue.join('|');
        if (filter_value != ''){
            args.push('"filter_value":"'+filter_value+'"')
        }
        //date_interval
        if (startDate != "" && endDate != "") {
            args.push('"date_interval":"' + startDate + '|' + endDate + '"')
        }
		
        return args
    },
    
    // 组织筛选的查询参数格式
    getFilterValueByDict: function(args){
        if (args.length == 0) {
            return ""
        }else{
            args.push('"page":1')
            return '{'+ args.join(',') +'}';
        }
    },
    
    // 初始化日历控件
    addDatepicker: function() {
        var _this = this;
        $('input[data-ui-role="orderDatepicker"]').each(function() {
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
                dateFormat: 'yy-mm-dd',
                //dateFormat: format,
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
                            $(this).datetimepicker('option', 'minDateTime', new Date(startTime));
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

            $datepicker.datetimepicker(options);
        });
    },

    doClickStatusTag: function(status_value){
    	// 清空搜索区域内容
    	this.$el.find('input').val('')
        this.status = status_value;
        // 调用搜索事件
        this.doSeacrh('filter');
    }
});
