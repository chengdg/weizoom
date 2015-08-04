/**
 * @class W.component.jqm.Form
 * 
 */
W.component.jqm.Form = W.component.Component.extend({
	type: 'jqm.form',
	propertyViewTitle: 'Form',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'action',
                type: 'text',
                displayName: 'URL',
                default: ''
            }, {
                name: 'method',
                type: 'select',
                displayName: 'Method',
                source: [{name: 'GET', value: 'get'}, {name: 'POST', value: 'post'}],
                default: 'post'
            }]
        }
    ],

    propertyChangeHandlers: {
        
    },

    dragSortHandler: {
        handleComponentEnter: function($node, $itemNode, itemComponent) {
            xlog('[form]: component enter form');
            $node.find('.xui-emptyFormIndicator').hide();
        },
        handleComponentLeave: function($node, $itemNode, itemComponent) {
            xlog('[form]: component leave form');
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
        name: 'Form',
        imgClass: 'componentList_component_form'
    }
});