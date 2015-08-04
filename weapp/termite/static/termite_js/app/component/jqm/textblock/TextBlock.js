/**
 * @class W.component.jqm.TextBlock
 * 
 */
W.component.jqm.TextBlock = W.component.Component.extend({
	type: 'jqm.textblock',
	propertyViewTitle: 'TextBlock',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'textarea',
                displayName: '',
                placeholder: '输入文本内容...',
                default: '输入文本内容...'
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value) {
            $node.find('p').html(value.replace(/\n/g, '<br/>'));

            W.Broadcaster.trigger('component:resize', this);
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
        name: 'Text',
        imgClass: 'componentList_component_textblock'
    }
});

