ensureNS('W.view.card.overview');
W.view.card.overview.OverviewBoardView = Backbone.View.extend({
    
    getTemplate: function() {
        $('#card-overview-board-view-tmpl-src').template('card-overview-board-view-tmpl');//编译src模板，命名为tmpl
        return 'card-overview-board-view-tmpl';//返回模板名
    },

    render: function() {
        //var _this = this;
        var html = $.tmpl(this.getTemplate());// tmpl(模板，context)
        this.$el.append(html);//加入到html
    },

    initialize: function(options) {
        this.$el = $(options.el);
        this.render();
    }


});
