/**
 * @class W.component.viper.SelectMenuItem
 * 
 */
W.component.viper.SelectMenuItem = W.component.Component.extend({
	type: 'viper.select_menu_item',
    selectable: 'no',
	propertyViewTitle: 'Select Menu Item',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: 'Text',
                default: '选项'
            }, {
                name: 'value',
                type: 'text',
                displayName: 'Value',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value, $propertyViewNode) {
            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
            }
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
