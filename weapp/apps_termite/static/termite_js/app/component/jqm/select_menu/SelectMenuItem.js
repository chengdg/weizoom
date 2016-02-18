/**
 * @class W.component.jqm.SelectMenuItem
 * 
 */
W.component.jqm.SelectMenuItem = W.component.Component.extend({
	type: 'jqm.select_menu_item',
    selectable: 'no',
	propertyViewTitle: 'Select Menu Item',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: 'Text',
                default: 'Option'
            }, {
                name: 'value',
                type: 'text',
                displayName: 'Value',
                default: ''
            }, {
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "c"
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value) {
            if (model.get('index') === 1) {
                var $select = $node.parents('div.ui-select').eq(0);
                $select.find('.ui-btn-text span').text(value);
            }
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
