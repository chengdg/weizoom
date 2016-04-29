ensureNS('W.view.apps');

W.view.apps.TagsSelector = Backbone.View.extend({
	events: {
		'change select': 'onChangeSelect',
	},

	templates: {
		viewTmpl: "#apps-tags-selector-tmpl"
	},

	initialize: function(options) {
		this.$el = $(options.el);

		this.options = options || {};
		this.tags = options.tags || {type:'no_tags', data:null};
	},

	render: function() {
		var html = this.renderTmpl('viewTmpl', {tags:this.tags});
		this.$el.append(html);
	},

	onChangeSelect: function(event) {
		var $select = $(event.currentTarget);
		var tagsType = $select.val();
		// this.$('.xa-optionTarget').hide();
		// this.$('.xa-integral').val('');
		// if (tagsType === "coupon"){
		// 	this.$('.coupon_div').show().css('display', 'inline');
		// 	this.$('.coupon_div a').show();

		// }
		// else{
			// this.$('[data-target="'+tagsType+'"]').show();
		// }

		this.tags['type'] = tagsType;
		this.tags['data'] = null;
		this.$('.errorHint').text("");
		this.trigger('change-tags', _.deepClone(this.tags));
	}
});

W.registerUIRole('[data-ui-role="apps-tags-selector"]', function() {
    var $el = $(this);
    var tags = $el.data('tags');
    var view = new W.view.apps.TagsSelector({
        el: $el.get(0),
        tags: tags
    });
    view.render();

    //缓存view
    $el.data('view', view);
});