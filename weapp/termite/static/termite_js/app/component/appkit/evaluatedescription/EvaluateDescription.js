/**
 * @class W.component.appkit.PowerMeDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.EvaluateDescription = W.component.Component.extend({
	type: 'appkit.evaluatedescription',
	selectable: 'yes',
	propertyViewTitle: '商品评价',

    dynamicComponentTypes: [],

	properties: [{
		group: '活动名称',
		groupClass: 'xui-propertyView-app-PowerMeGroup',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '标题',
			isUserProperty: true,
			maxLength: 35,
			validate: 'data-validate="require-notempty::页面标题不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: '',
			placeholder: '活动标题'
		}]
	}],
	propertyChangeHandlers: {

	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
