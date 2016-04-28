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
	},

	render: function(tags) {
        this.tags = tags || this.tags;
		var selectId = this.tags.selectId || 0;
		var html = this.renderTmpl('viewTmpl', {taglist:this.tags.taglist,selectId:selectId});
		this.$el.append(html);
	},

	onChangeSelect: function(event) {
		var $select = $(event.currentTarget);
		var tagsId = $select.val();
        this.tags['selectId'] = tagsId;
        this.$('.errorHint').text("");
        this.trigger('change-tags', _.deepClone(this.tags));
	}
});

W.registerUIRole('[data-ui-role="apps-tags-selector"]', function() {
    var $el = $(this);
    var tags = $el.data('tags');
    var view = new W.view.apps.TagsSelector({
        el: $el.get(0)
    });
    $el.data('view', view);
	W.getApi().call({
		method: 'get',
		app: 'apps/survey',
		resource: 'list_tags',
		args: {
		},
		success: function(data){
            tags.taglist = data.tags;
			view.render(tags);
		},
		error: function(error){
			console.log(error);
		}
	});
});