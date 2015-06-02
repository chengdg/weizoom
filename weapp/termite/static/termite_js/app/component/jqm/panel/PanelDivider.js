/**
 * @class W.component.jqm.PanelDivider
 * 
 */
W.component.jqm.PanelDivider = W.component.Component.extend({
	type: 'jqm.panel_divider',
    selectable: 'no',
	propertyViewTitle: 'Panel Divider',

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
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
