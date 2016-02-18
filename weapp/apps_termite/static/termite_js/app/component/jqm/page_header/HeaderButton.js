/**
 * @class W.component.jqm.HeaderButton
 * 
 */
W.component.jqm.HeaderButton = W.component.Component.extend({
	type: 'jqm.header_button',
    selectable: 'no',
	propertyViewTitle: 'Header Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: 'Text',
                default: 'Button'
            }, {
                name: 'icon',
                type: 'select',
                displayName: '图标',
                source: W.data.ButtonIcons,
                default: "home"
            }, {
                name: 'target',
                type: 'select',
                displayName: '链接',
                source: W.data.getWorkbenchPages,
                default: ''
            }, {
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "c"
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value) {
            if (value) {
                $node.find('.ui-btn-text').text(value);
                if ($node.hasClass('ui-btn-icon-notext')) {
                    $node.removeClass('ui-btn-icon-notext').addClass('ui-btn-icon-left')
                }
            } else {
                $node.removeClass('ui-btn-icon-left').addClass('ui-btn-icon-notext');
            }

            W.Broadcaster.trigger('component:resize', this);
        },
        icon: function($node, model, value) {
            var oldClass = 'ui-icon-' + $node.attr('data-icon');
            var newClass = 'ui-icon-' + value;
            $node.find('.ui-icon').removeClass(oldClass).addClass(newClass);
        },
        theme: function($node, model, value) {
            if (value === '') {
                value = 'c';
            }
            var oldTheme = model.previous('theme');
            var oldClass= "ui-btn-up-" + oldTheme;
            var newClass = "ui-btn-up-" + value;
            $node.removeClass(oldClass).addClass(newClass).attr('data-theme', value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
