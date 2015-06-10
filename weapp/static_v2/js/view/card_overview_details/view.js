ensureNS('W.view.card.overview');
W.view.card.overview.DetailsView = Backbone.View.extend({

    getTemplate: function() {
    $('#card-overview-details-tmpl-src').template('card-overview-details-tmpl');
    return 'card-overview-details-tmpl';
    },

    render: function() {
        //var _this = this;
        var html = $.tmpl(this.getTemplate());
        this.$el.append(html);
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        this.render();
        this.filter_value = '';
    }

});