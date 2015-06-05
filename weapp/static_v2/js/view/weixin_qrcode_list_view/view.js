ensureNS('W.view.weixin');
/**
 * 带参数二维码的View
 */
 W.view.weixin.QrcodeView = Backbone.View.extend({

    events: {
        "click .xa-searchBtn": "onClickSearchVal",
        'click .xa-search': 'onClickSearchButton',
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