ensureNS('W.view.termite');
W.view.termite.NavbarSecondNav = Backbone.View.extend({
	events: {
		'click .xa-navbar-secondnav-add': 'onClickAddSecondNav',
		'input input[type="text"]': 'onInputValue'
	},

	templates: {
		viewTmpl: '#termite-navbar-secondnav-tmpl',
		navTmpl: '#termite-navbar-secondnav-tmpl-nav'
	},

	initialize: function(options) {
		this.$el = $(this.el);
	},

	render: function() {
		var template = this.getTmpl('viewTmpl');
		var html = template({});
		this.$el.html(html);
	},

	onClickAddSecondNav: function(event) {
		var template = this.getTmpl('navTmpl');
		var html = template({});
		this.$('.xa-navbar-secondnav-navs').append($(html));
		var $conterolField = $(event.target).parents('.propertyGroup_property_dynamicControlField_content');
		W.Broadcaster.trigger("component:secondnav_add", $conterolField, false)
		console.log('trigger', 'update-show-box')
	},

	onInputValue: function(event) {
		var $navs = this.$('.xa-nav');
		var navs = [];
		for (var i = 0; i < $navs.length; ++i) {
			var $nav = $navs.eq(i);
			var title = $.trim($nav.find('[name="title"]').val());
			var target = $.trim($nav.find('[name="target"]').val());
			navs.push({
				title: title,
				target: target
			})
		}

		console.log(55555555, navs)
	}
});

W.registerUIRole('[data-ui-role="termite-navbar-secondnav"]', function() {
    var $el = $(this);
    var view = new W.view.termite.NavbarSecondNav({
        el: $el.get(0)
    });
    view.render();

    //缓存view
    $el.data('view', view);
});