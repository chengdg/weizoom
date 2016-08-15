ensureNS('W.view.weixin');
/**
 * 带参数二维码的View
 */
 W.view.weixin.QrcodeView = Backbone.View.extend({

    events: {
        "click .xa-searchBtn": "onClickSearchVal",
        'click .xa-search': 'onClickSearchButton',
        'click .xa-exportQrcode': 'onClickExportButton'
    },

    initialize: function(options) {
    	this.options = options || {};
        this.$el = $(options.el);
        this.table = $('[data-ui-role="advanced-table"]').data('view');
        this.on('search', _.bind(this.onSearch, this));
    },
    onClickSearchVal:function(){
    /*	alert('dgdgfgfg');
    	var inputVal = $(".xui-searchInput").val();
   console.log(inputVal+"ddddddddddddddddddddddddddddddddddd");*/

   },
   onClickSearchButton: function(){
        var data = this.getFilterData();
        this.trigger('search', data);
    },
    render: function() {
        var html = $.tmpl(this.getTemplate(), {
            promotionType: this.promotionType
        });
        this.$el.append(html);
        W.createWidgets(this.$el);
    },

    //导出二维码
    onClickExportButton: function(){
        console.log('导出');
        var url = '/new_weixin/qrcode_export/';
        var name = $.trim(this.$('.xa-search-title').val());

        if (name.length > 0) {
            url = url + '?query=' + name;
        }

        console.log(url, name)
       // W.getLoadingView().show();
        $('#spin-hint').html('玩命导出中...');
        var $frame=$('<iframe>').hide().attr('src',url);
        $('body').append($frame);
        //setTimeout(function(){W.getLoadingView().hide()}, 5000);
    },
    // 获取条件数据
    getFilterData: function(){


        //优惠券的名称
        var name = $.trim(this.$('.xa-search-title').val());
        return {
            query: name
        };
    },
    onSearch: function(data) {
        this.table.reload(data, {
            emptyDataHint: '没有符合条件的记录'
        });
    }



 })

 W.view.weixin.Distributions = Backbone.View.extend({

    events: {
        'click .xa-search': 'onClickSearchButton',
    },

    initialize: function(options) {
    	this.options = options || {};
        this.$el = $(options.el);
        this.table = $('[data-ui-role="advanced-table"]').data('view');
        this.on('search', _.bind(this.onSearch, this));
    },

   onClickSearchButton: function(){
        var data = this.getFilterData();
        this.trigger('search', data);
    },

    render: function() {
        var html = $.tmpl(this.getTemplate(), {
            promotionType: this.promotionType
        });
        this.$el.append(html);
        W.createWidgets(this.$el);
    },
    getFilterData: function(){
        var name = $.trim(this.$('.xa-search-title').val());
        return {
            query_name: name
        };
    },
    onSearch: function(data) {
        this.table.reload(data, {
            emptyDataHint: '没有符合条件的记录'
        });
    }
 });

W.view.weixin.DistributionsClear = Backbone.View.extend({

    events: {
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButtion',
        'change .xa-changeStatus': 'onChangeStatusButtion'
    },

    initialize: function(options) {
    	this.options = options || {};
        this.$el = $(options.el);
        this.selectOption = $(this);
        this.table = $('[data-ui-role="advanced-table"]').data('view');
        this.on('search', _.bind(this.onSearch, this));
    },

   onClickSearchButton: function(){
        var data = this.getFilterData();
        this.trigger('search', data);
    },

    onClickResetButtion: function () {
        $('input:text').each(function(){
            $(this).val('') ;
        });
    },

    onChangeStatusButtion: function(){
        var checkbox = $(event.currentTarget);
      // console.log(this.selectOption.data('id'));
      console.log(checkbox);

    },

    render: function() {
        var html = $.tmpl(this.getTemplate(), {
            promotionType: this.promotionType
        });
        this.$el.append(html);
        W.createWidgets(this.$el);
    },

    getFilterData: function(){
        var return_min = $.trim(this.$('[name="return_min"]').val());
        var return_max = $.trim(this.$('[name="return_max"]').val());
        var start_date = $.trim(this.$('[name="start_date"]').val());
        var end_date = $.trim(this.$('[name="end_date"]').val());
        return {
            return_min: return_min,
            return_max: return_max,
            start_date: start_date,
            end_date: end_date
        }
    },

    onSearch: function(data) {
        this.table.reload(data, {
            emptyDataHint: '没有符合条件的记录'
        });
    }
 });