/**
 * @class W.component.jqm.ListViewDivider
 * 
 */
W.component.jqm.ListViewDivider = W.component.Component.extend({
	type: 'jqm.listview_divider',
    selectable: 'no',
	propertyViewTitle: 'Listview Divider',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: 'Text',
                default: 'Divider'
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value) {
            $node.text(value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
