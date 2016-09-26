/**
 * @class W.component.appkit.EventRichtext
 *
 */
ensureNS('W.component.appkit');
W.component.appkit.EventRichtext = W.component.Component.extend({
	type: 'appkit.eventrichtext',
	selectable: 'yes',
	propertyViewTitle: '',

	properties: [{
		group: '快捷模块',
		groupClass: 'xui-propertyView-app-TextEvent',
		fields: [{
			name: 'description2',
			type: 'rich_text2',
			displayName: '内容二',
			isUserProperty: true,
			default: ''
		}]
	}],

	propertyChangeHandlers: {
		description2: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
}, {
	indicator: {
		name: '快捷模块',
		imgClass: 'componentList_component_memberinfo' // 控件icon
	}
});
