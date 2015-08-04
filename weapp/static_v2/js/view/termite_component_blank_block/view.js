ensureNS('W.termite');
//W.termite = W.termite || {};


W.termite.BlankBlockComponent = Backbone.View.extend({
	events: {

	},

	templates: {
		'viewTmpl': '#component-blank-block-tmpl-src',
	},

	initialize: function(options) {
		xlog("in W.termite.basic.BlankBlockComponent()");
		this.$el = $(this.el);
	},

	render: function() {
		xlog("in render()");
		var html = this.getTmpl('viewTmpl')({});
		this.$el.append(html);
	}
});
