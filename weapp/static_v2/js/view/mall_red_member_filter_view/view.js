ensureNS('W.view.mall');
W.view.mall.redMemberFilterView = Backbone.View.extend({
    events: {
        'click .xa-create': 'createFilter',
        'click .xa-search': 'seacrhBtn',
        'click .xa-reset': 'onClickReset'
    },

    // 点击‘查询’按钮事件
    seacrhBtn: function(){
        var dataView = this.options.dataView;
        var args = this.getFilterValue();
        dataView.options.args = this.getFilterValueByDict(args);
        dataView.setPage(1);
        console.log('dataView.options.args', dataView.options.args);
        dataView.reload();
        this.$el.trigger('end_click');
        this.setStatusActive();
    },

    // 获取条件数据
    getFilterValue: function(){
        var args = [];

        var name = $('#name').val().trim();
        if (name) {
            args.push('"name":"'+name+'"');
        }

        var coupon_status = $('#coupon_status').val().trim();
        if (coupon_status != -1) {
            args.push('"coupon_status":"'+coupon_status+'"');
        }
        var grade = $('#grade').val();
        if (grade != -1) {
            args.push('"grade_id":"'+grade+'"');
        }
        return args
    },

    // 组织筛选的查询参数格式
    getFilterValueByDict: function(args){
        if (args.length == 0) {
            return ""
        }else{
            args.push('"page":1');
            return '{'+ args.join(',') +'}';
        }
    },

    getTemplate: function() {
        $('#mall-red-member-filter-view-tmpl-src').template('mall-red-member-filter-view-tmpl');
        return 'mall-red-member-filter-view-tmpl';
    },

    render: function() {
        var _this = this;
        var status = this.options.status || '';
        W.getApi().call({
            app: 'apps/promotion',
            resource: 'red_members_filter_params',
            method: 'get',
            args: {
                status: status
            },
            success: function(data) {
                 var html = $.tmpl(this.getTemplate(), {
                    grades: data.grades,
                    coupon_status: data.coupon_status
                });
                this.$el.append(html);
                $('.xa-showFilterBox').append($('.xa-timelineControl'));
            },
            error: function(response) {
                alert('加载失败！请刷新页面重试！');
            },
            scope: this
        });
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
       /* var status = $('#orderStatus').val();
        $('.xa-count').removeClass('active');
        $('[data-total-status-value="'+status+'"]').addClass('active');*/
    },

    clickStatusBox: function(status_value){
        this.resetFrom();
        $('#orderStatus').val(status_value);
        // 调用搜索事件
        this.seacrhBtn();
    },

    resetFrom: function(){
        $('#name').val('');
        $('#grade').val(-1);
        $('#coupon_status').val(-1);
    },

    onClickReset:function(){
        this.resetFrom()
    }
});
