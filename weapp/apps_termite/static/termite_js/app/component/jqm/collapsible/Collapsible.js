/**
 * @class W.component.jqm.Collapsible
 * 
 */
W.component.jqm.Collapsible = W.component.Component.extend({
	type: 'jqm.collapsible',
    selectable: 'no',
	propertyViewTitle: 'Collapsible',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: 'Text',
                default: 'Section Header'
            }, {
                name: 'id',
                type: 'text',
                displayName: 'Id',
                default: ''
            }, {
                name: 'is_collapsed',
                type: 'boolean',
                displayName: 'Collapsed? ',
                default: "yes"
            }]
        }
    ],

    dragSortHandler: {
        handleComponentEnter: function($node, $itemNode, itemComponent) {
            xlog('[collapsible]: component enter form');
            $node.find('.xui-emptyFormIndicator').hide();
        },
        handleComponentLeave: function($node, $itemNode, itemComponent) {
            xlog('[collapsible]: component leave form');
            var $widgets = $node.find('[data-ui-behavior="xub-selectable"]');
            if ($widgets.length === 0) {
                $node.find('.xui-emptyFormIndicator').show();
            }
        },
    },

    propertyChangeHandlers: {
        text: function($node, model, value) {
            $node.find('span.ui-btn-text').text(value);
        },
        is_collapsed: function($node, model, value) {
            $content = $node.find('div.ui-collapsible-content');
            $icon = $node.find('span.ui-icon');
            if ('yes' === value) {
                $content.addClass('ui-collapsible-content-collapsed');
                $icon.removeClass('ui-icon-minus').addClass('ui-icon-plus');
            } else {
                $content.removeClass('ui-collapsible-content-collapsed');
                $icon.removeClass('ui-icon-plus').addClass('ui-icon-minus');
            }

            W.Broadcaster.trigger('component:resize', this);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});