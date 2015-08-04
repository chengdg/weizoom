/**
 * @class W.component.jqm.PanelButton
 * 
 */
W.component.jqm.PanelButton = W.component.Component.extend({
	type: 'jqm.panel_button',
    selectable: 'no',
	propertyViewTitle: 'Panel Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: 'Text',
                default: 'Button'
            }, {
                name: 'target',
                type: 'select',
                displayName: '链接',
                source: W.data.getWorkbenchPages,
                default: ''
            }, {
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "a"
            }, {
                name: 'bubble_text',
                type: 'text',
                displayName: 'Bubble',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
