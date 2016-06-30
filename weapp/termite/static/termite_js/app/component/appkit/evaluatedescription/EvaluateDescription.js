/**
 * @class W.component.appkit.PowerMeDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.EvaluateDescription = W.component.Component.extend({
	type: 'appkit.evaluatedescription',
	selectable: 'no',
	propertyViewTitle: '商品评价',

    dynamicComponentTypes: [],

	properties: [],
	propertyChangeHandlers: {},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
