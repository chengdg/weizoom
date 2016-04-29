ensureNS('W.view.apps');

W.view.apps.TagsSelector = Backbone.View.extend({
	events: {
		'change select': 'onChangeSelect'
	},

	templates: {
		viewTmpl: "#apps-tags-selector-tmpl"
	},

	initialize: function(options) {
		this.$el = $(options.el);

		this.options = options || {};
		this.tags = options.tags || {id:'2'};
	},

	render: function() {
		var html = this.renderTmpl('viewTmpl', {tags:this.tags});
		this.$el.append(html);
	},

	onChangeSelect: function(event) {
		var $select = $(event.currentTarget);
		var tagsId = $select.val();
		console.log('!!!!!!!!!!!!!!');
		console.log(tagsId);
		this.tags['id'] = tagsId;
		this.$('.errorHint').text("");
		this.trigger('change-tags', _.deepClone(this.tags));
	}
});

W.registerUIRole('[data-ui-role="apps-tags-selector"]', function() {
    var $el = $(this);
	W.getApi().call({
		method: 'get',
		app: 'apps/survey',
		resource: 'list_tags',
		args: {
		},
		success: function(data){
			var tags = data.tags;
			var view = new W.view.apps.TagsSelector({
				el: $el.get(0),
				tags: tags
			});
			view.render();

			//缓存view
			$el.data('view', view);
		},
		error: function(error){
			console.log('error');
		}
	});
});