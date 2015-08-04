/**
 * @class W.component.viper.Button
 * 
 */

W.component.viper.Button = W.component.Component.extend({
	type: 'viper.button',
	propertyViewTitle: 'Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文本',
                default: 'Button'
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
    }
}, {
    indicator: {
        name: 'Button',
        imgClass: 'componentList_component_button'
    }
});
