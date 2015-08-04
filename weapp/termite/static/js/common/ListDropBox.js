/*
Copyright (c) 2011-2012 Weizoom Inc  
*/

W.ListDropBox = W.DropBox.extend({
	isArrow: false,
	
	isTitle: false,
	
	ACTIONS_EVENT: 'select_action',
	
	collectionClass: null,
	
	getTemplate: function() {
		$('#list-drop-box').template('list-drop-box-tmpl');
		return 'list-drop-box-tmpl';
	},
	
	events: {
		'click li a:not(.tx_addGroup)': 'changeStatus'
	},
	
	initializePrivate: function(options) {
		this.collection = new this.collectionClass();
		this.fetchData();
	},
	
	changeStatus: function(event) {
		var $el = $(event.currentTarget);
		this.trigger(this.ACTIONS_EVENT, {id:$el.attr('value'), name:$el.attr('valueName')});
		this.close();
	},
	
	render: function() {
		data = this.collection.toJSON();
		if(this.collection.editJson) {
			data = this.collection.editJson(data);
		}
		if(data.length) {
			data = {
				statuss: data
			}
		}
		else {
			data = {
				statuss: data,
				error_msg: this.errorMsg
			}
		}
		xlog(data)
		this.$content.html($.tmpl(this.getTemplate(), data));
		this.trigger('render', this);
		this.setPosition();
	},
	
	fetchData: function() {
		var _this = this;
		this.collection.fetch({
			success: function() {
				_this.render();
			}
		})
	},
    
    closePrivate: function() {
        this.unbind(this.ACTIONS_EVENT);
    }
});