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
            emptyDataHint: '没有符合条件的发放优惠券规则'
        });
    }



 })