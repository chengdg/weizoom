/**
 * @class W.component.jqm.GridContainer
 * 
 */
W.component.jqm.GridContainer = W.component.Component.extend({
	type: 'jqm.grid_container',
    selectable: 'no',
	propertyViewTitle: 'GridContainer',

	properties: [
        {
            group: 'Model属性',
            fields: []
        }
    ],

    dragSortHandler: {
        handleComponentEnter: function($node, $itemNode, itemComponent) {
            xlog('[grid_container]: component enter form');
            $node.find('.xui-emptyFormIndicator').hide();
        },
        handleComponentLeave: function($node, $itemNode, itemComponent) {
            xlog('[grid_container]: component leave form');
            var $widgets = $node.find('[data-ui-behavior="xub-selectable"]');
            if ($widgets.length === 0) {
                $node.find('.xui-emptyFormIndicator').show();
            }
        },
    },

    propertyChangeHandlers: {
        
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});

