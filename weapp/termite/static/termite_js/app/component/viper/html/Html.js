/**
 * @class W.component.viper.Html
 * 
 */
W.component.viper.Html = W.component.Component.extend({
	type: 'viper.html',
	propertyViewTitle: 'HTML',

    capability: {
        editHtml: true
    },

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'html',
                type: 'html-editor',
                displayName: '',
                default: '<p>输入HTML内容...<p>'
            }]
        }
    ],

    propertyChangeHandlers: {
        html: function($node, model, value) {
            $node.html(value);

            W.Broadcaster.trigger('component:resize', this);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'HTML',
        imgClass: 'componentList_component_html'
    }
});