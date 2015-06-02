/**
 * @class W.component.viper.Simulator
 * 
 */

W.component.viper.Simulator = W.component.Component.extend({
	type: 'viper.simulator',
	propertyViewTitle: '模拟器',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'is_preview',
                type: 'boolean',
                displayName: '预览?',
                default: 'yes'
            }]
        }
    ],

    propertyChangeHandlers: {
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '模拟器',
        imgClass: 'componentList_component_map'
    }
});