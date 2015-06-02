/**
 * @class W.component.jqm.HtmlTag
 * 
 */
W.component.jqm.HtmlTag = W.component.Component.extend({
	type: 'jqm.html_tag',
	propertyViewTitle: 'HTML标签',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'tag',
                type: 'text',
                displayName: '标签',
                default: 'div'
            }]
        }
    ],

    propertyChangeHandlers: {
        
    },

    dragSortHandler: {
        handleComponentEnter: function($node, $itemNode, itemComponent) {
            $node.find('.xui-emptyFormIndicator').hide();
        },
        handleComponentLeave: function($node, $itemNode, itemComponent) {
            var $widgets = $node.find('[data-ui-behavior="xub-selectable"]');
            if ($widgets.length === 0) {
                $node.find('.xui-emptyFormIndicator').show();
            }
        },
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'HTML标签',
        imgClass: 'componentList_component_html'
    }
});