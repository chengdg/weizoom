/**
 * @class W.component.weapp.Button
 * 
 */
W.data.getComponentModelField = function(field) {
    var func = function(component) {
        xwarn(arguments);
        return component.model.get('field');
    }
    return func;
}

ensureNS('W.component.weapp');
W.component.weapp.Button = W.component.Component.extend({
	type: 'weapp.button',
	propertyViewTitle: 'Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                isUserProperty: true,
                displayName: '文本',
                default: 'Button'
            }, {
                name: 'icon',
                type: 'select',
                displayName: '图标',
                isUserProperty: true,
                source: W.data.ButtonIcons,
                default: "home"
            }, {
                name: 'icon_position',
                type: 'radio-group',
                displayName: '图标位置',
                isUserProperty: true,
                source: W.data.ImagePositions,
                default: 'left'
            }, {
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                isUserProperty: true,
                source: W.data.ThemeSwatchs,
                default: "a"
            }, {
                name: 'target',
                type: 'select',
                displayName: '链接',
                isUserProperty: true,
                source: W.data.getWorkbenchPages,
                default: ''
            }, {
                name: 'is_inline',
                type: 'boolean',
                displayName: 'Inline? ',
                isUserProperty: true,
                default: "no"
            }]
        }, 
        {
            group: '事件',
            fields: [{
                name: 'event:onclick',
                type: 'dialog_select',
                displayName: 'Click',
                isUserProperty: true,
                triggerButton: '编辑代码...',
                dialog: 'W.workbench.EditCodeDialog',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value) {
            $node.find('.ui-btn-text').text(value);

            W.Broadcaster.trigger('component:resize', this);
        },
        icon: function($node, model, value) {
            var oldClass = 'ui-icon-' + $node.attr('data-icon');
            var newClass = 'ui-icon-' + value;
            $node.find('.ui-icon').removeClass(oldClass).addClass(newClass);
        },
        icon_position: function($node, model, value) {
            var oldClass = 'ui-btn-icon-' + $node.attr('data-iconpos');
            var newClass = 'ui-btn-icon-' + value;
            $node.removeClass(oldClass).addClass(newClass);
            $node.attr('data-iconpos', value);

            W.Broadcaster.trigger('component:resize', this);
        },
        theme: function($node, model, value) {
            if (value === '') {
                value = 'c';
            }
            var oldTheme = model.previous('theme');
            var oldClass= "ui-btn-up-" + oldTheme;
            var newClass = "ui-btn-up-" + value;
            $node.removeClass(oldClass).addClass(newClass).attr('data-theme', value);
        },
        is_inline: function($node, model, value) {
            if (value === 'yes') {
                $node.addClass('ui-btn-inline');
            } else {
                $node.removeClass('ui-btn-inline');
            }

            W.Broadcaster.trigger('component:resize', this);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Button',
        imgClass: 'componentList_component_button'
    }
});
