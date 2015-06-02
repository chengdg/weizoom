/**
 * @class W.component.jqm.Link
 * 
 */
W.component.Link = W.component.Component.extend({
	type: 'jqm.link',
	propertyViewTitle: 'Link',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文本',
                default: 'Link'
            }, {
                name: 'target',
                type: 'select',
                displayName: '链接',
                source: W.data.getWorkbenchPages,
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value) {
            $node.find('a').text(value);

            W.Broadcaster.trigger('component:resize', this);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Link',
        imgClass: 'componentList_component_link'
    }
});
