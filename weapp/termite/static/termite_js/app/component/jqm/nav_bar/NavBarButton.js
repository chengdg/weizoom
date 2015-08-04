/**
 * @class W.component.jqm.NavBarButton
 * 
 */
W.component.jqm.NavBarButton = W.component.Component.extend({
	type: 'jqm.nav_bar_button',
    selectable: 'no',
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
                name: 'icon',
                type: 'select',
                displayName: '图标',
                source: W.data.ButtonIcons,
                default: "home"
            }, {
                name: 'is_initial_active',
                type: 'boolean',
                displayName: '初始选中',
                default: 'no'
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
            $node.find('.ui-btn-text').text(value);
        },
        icon: function($node, model, value) {
            var oldClass = 'ui-icon-' + $node.attr('data-icon');
            var newClass = 'ui-icon-' + value;
            $node.find('.ui-icon').removeClass(oldClass).addClass(newClass);
        },
        is_initial_active: function($node, model, value) {
            if (value === 'yes') {
                $node.addClass('ui-btn-active');
            } else {
                $node.removeClass('ui-btn-active');
            }
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
