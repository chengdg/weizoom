ensureNS('W.view.card.cards');

W.view.card.cards.cardListFilter = Backbone.View.extend({
    events: {
        'click .xa-filter': 'filter',
        'click .seacrh-card-btn': 'seacrhBtn',
        'click .recently-week-day': 'setDateText',
        'click .xa-reset': 'resetFrom'
    },

        setDateText: function(event){
        var day = $(event.currentTarget).attr('data-day') -1 ;//parseInt(.toSting()) - 1;
        var today = new Date(); // 获取今天时间

        today.setTime(today.getTime()-day*24*3600*1000);
        var begin = $.datepicker.formatDate('yy-mm-dd', today);;
        var end = $.datepicker.formatDate('yy-mm-dd', new Date());

        $('#start_date').val(begin)
        $('#end_date').val(end);
    },

    // 点击‘筛选’按钮事件
    seacrhBtn: function(){

        var dataView = this.options.dataView;
        var args = this.getFilterValue();
        dataView.options.args = this.getFilterValueByDict(args);
        dataView.setPage(1);
        dataView.reload();
        this.$el.trigger('end_click');
        this.setStatusActive();
    },

    // 获取条件数据
    getFilterValue: function(){
        var dataValue = [];
        var card_number = $('#card_number').val();
        var cardStatus = $('#cardStatus').val().trim();
        var args = [];


        if (card_number.length > 0) {
            dataValue.push('card_number:'+card_number);
        }
        if (cardStatus != -1) {
            dataValue.push('cardStatus:'+cardStatus);
        }

        var filter_value = dataValue.join('|');

        if (filter_value != ''){
            args.push('"filter_value":"'+filter_value+'"')
        }
        this.filter_value = filter_value
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

    getTemplate: function() {
        $('#card-list-filter-view-tmpl-src').template('card-list-filter-view-tmpl');
        return 'card-list-filter-view-tmpl';
    },

    render: function() {
        var _this = this;
        var status = this.options.status || '';

        var html = $.tmpl(this.getTemplate(), {
            filters: _this.filterData,
        });
        this.$el.append(html);
        $('.xa-showFilterBox').append($('.xa-timelineControl'));
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.render();
        this.filter_value = '';
        this.bind('clickStatusBox', this.clickStatusBox);
    },

    // 设置状态选中事件
    setStatusActive: function(){
        var status = $('#orderStatus').val();
        $('.xa-count').removeClass('active');
        $('[data-total-status-value="'+status+'"]').addClass('active');
    },

    clickStatusBox: function(status_value){
        this.resetFrom();
        $('#orderStatus').val(status_value);
        // 调用搜索事件
        this.seacrhBtn();
    },

    resetFrom: function(){
        $('#card_number').val('');
        $('#cardStatus').val(-1);
    }
});
