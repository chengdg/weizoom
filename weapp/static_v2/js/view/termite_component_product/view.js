/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 右侧的property视图
 * @class
 */
ensureNS('W.termite');
W.termite.ProductComponent = Backbone.View.extend({
	el: '',

	events: {
	},

    getTemplate: function() {
        $('#product-property-view-tmpl-src').template('product-property-view-tmpl');
        return "product-property-view-tmpl";
    },
	
	initialize: function(options) {
		this.$el = $(this.el);
        this.template = this.getTemplate();
	},

    render: function() {
        this.$el.append($.tmpl(this.template, {}));
    }
});