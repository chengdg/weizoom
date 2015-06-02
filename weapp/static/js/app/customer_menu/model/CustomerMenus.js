/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * 一条菜单项消息
 * @class
 */
W.customerMenu.CustomerMenu = Backbone.Model.extend({
}, {
	idCounter: -99,
	index: 1,
	KEYWORD_TYPE: 1,
	LINK_TYPE: 2,

	createNewItem: function(type, metadata) {
		var id = this.idCounter;
		this.idCounter += 1;
		var index = this.index;
		this.index += 1;

		var scheduledDate = null;
		if (metadata) {
			if (metadata.scheduledDate) {
				scheduledDate = metadata.scheduledDate;
			}
		}
		if (!scheduledDate) {
			var date = new Date();
			scheduledDate = date.getMonth()+1+'月'+date.getDate()+'日';
		}
		var menuItem = new W.customerMenu.CustomerMenu({
			id: id,
			display_index: index,
			type: type,
			name: '',
			url: '',
			rule_id: -1,
			father_id: 0,
			is_active: 1,
			date: scheduledDate,
			metadata: {}
		});
		if (metadata) {
			menuItem.set('metadata', metadata);
		}

		return menuItem;
	},

	createKeyWordMessage: function(metadata) {
		return this.createNewItem(this.KEYWORD_TYPE, metadata);
	},

	createLinkMessage: function(metadata) {
		return this.createNewItem(this.LINK_TYPE, metadata);
	},
});


/**
 * 消息集合
 * @class
 */
W.customerMenu.CustomerMenus = Backbone.Collection.extend({
	model: W.customerMenu.CustomerMenu,

	initialize: function() {

	}
});