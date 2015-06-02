ensureNS('W.view.weixin');
W.view.weixin.FansFilterView = Backbone.View.extend({
    events: {
        'click .xa-search': 'doSeacrh'
    },

    initialize: function(options) {
        this.$el = $(options.el);
        this.options = options || {};
        console.log(this.options)
        this.filter_value = '';

        W.getApi().call({
            method: 'get',
            app: 'new_weixin',
            resource: 'fans_category',

            args: {},
            success: function(data) {
                //解析数组
                $("#category").empty();
                $("#category").append("<option value='-1'>全部</option>");
                $.each(data.categories, function(i, item) {
                    $("#category").append("<option value=" + item.id + ">" + item.name + "</option>");
                });
            },
            error: function(resp) {
                alert('获取分组列表失败!');
            }
        });


        this.render();
    },

    render: function() {

        var html = $.tmpl(this.getTemplate(), {});
        this.$el.append(html);
    },

    getTemplate: function() {
        $('#weixin-fans-filter-view-tmpl-src').template('weixin-fans-filter-view-tmpl');
        return 'weixin-fans-filter-view-tmpl';

    },

    // 点击‘筛选’按钮事件
    doSeacrh: function(action) {
        var dataView = this.options.dataView;
        console.log(dataView)
        var args = this.getFilterValue();
        dataView.options.args = this.getFilterValueByDict(args);
        dataView.setPage(1);
        console.log('dataView.options.args:', dataView.options.args)
        dataView.reload();

    },

    // 获取条件数据
    getFilterValue: function() {
        var dataValue = [];
        var name = $('#name').val().trim();
        if (name) {
            dataValue.push('name:' + name);
        }
        var categoryId = $('#category').val().trim();
        if (categoryId != -1) {
            dataValue.push('category_id:' + categoryId);
        }
        var status = $('#status').val();
        if (status != -1) {
            dataValue.push('status:' + status);
        }
        var sex = $('#sex').val();
        if (sex != -1) {
            dataValue.push('sex:' + sex);
        }

        var args = [];
        var filter_value = dataValue.join('|');
        if (filter_value != '') {
            args.push('"filter_value":"' + filter_value + '"')
        }

        return args
    },

    // 组织筛选的查询参数格式
    getFilterValueByDict: function(args) {
        if (args.length == 0) {
            return ""
        } else {
            args.push('"page":1')
            return '{' + args.join(',') + '}';
        }
    }
});
