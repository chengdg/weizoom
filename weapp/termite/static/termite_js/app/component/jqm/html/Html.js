/**
 * @class W.component.jqm.Html
 * 
 */
W.component.jqm.Html = W.component.Component.extend({
	type: 'jqm.html',
	propertyViewTitle: 'HTML',

    capability: {
        editHtml: true
    },

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'is_content_from_data',
                type: 'boolean',
                displayName: '来自数据？',
                default: 'no'
            }, {
                name: 'html',
                type: 'html-editor',
                displayName: '',
                default: '<p>输入HTML内容...<p>'
            }]
        }
    ],

    propertyChangeHandlers: {
        html: function($node, model, value) {
            //$node.html(value);

            //W.Broadcaster.trigger('component:resize', this);
            W.Broadcaster.trigger('designpage:refresh');
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