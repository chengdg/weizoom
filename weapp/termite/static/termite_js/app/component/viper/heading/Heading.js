/**
 * @class W.component.viper.Heading
 * 
 */
W.component.viper.Heading = W.component.Component.extend({
	type: 'viper.heading',
	propertyViewTitle: 'Heading',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文字',
                default: 'Heading'
            }]
        }
    ],

    /* propertyChangeHandlers中的函数将在iframe中被调用 */
    propertyChangeHandlers: {
        text: function($node, model, value) {
            xlog('[heading]: change text property to :' + value);
            $node.text(value);
        }
    },

    datasource: [
        {name: 'text'}
    ],

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Heading',
        imgClass: 'componentList_component_heading'
    }
});
