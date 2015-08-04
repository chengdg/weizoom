/**
 * @class W.component.jqm.Panel
 * 
 */
W.component.jqm.Panel = W.component.Component.extend({
	type: 'jqm.panel',
	propertyViewTitle: 'Panel',
    hasGlobalContent: 'yes',

    dynamicComponentTypes: [
        {type: 'jqm.panel_divider', model: {index: 1, text: 'Divider'}},
        {type: 'jqm.panel_button', model: {index: 2, text: 'Button', target: '', theme: 'a', bubble_text: '10'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文本',
                default: 'Panel'
            }, {
                name: 'icon',
                type: 'select',
                displayName: '图标',
                source: W.data.ButtonIcons,
                default: "home"
            }, {
                name: 'icon_position',
                type: 'radio-group',
                displayName: '图标位置',
                source: W.data.ImagePositions,
                default: 'left'
            }, {
                name: 'button_theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "c"
            }, {
                name: 'is_inline',
                type: 'boolean',
                displayName: 'Inline? ',
                default: "no"
            }, {
                name: 'position',
                type: 'select',
                displayName: 'Position',
                source: W.data.PanelPositions,
                default: "left"
            }, {
                name: 'display_mode',
                type: 'select',
                displayName: 'Display',
                source: W.data.PanelDisplayModes,
                default: "reveal"
            }, {
                name: 'divider_theme',
                type: 'select',
                displayName: 'Divider',
                source: W.data.ThemeSwatchs,
                default: "a"
            }, {
                name: 'panel_theme',
                type: 'select',
                displayName: 'Panel',
                source: W.data.ThemeSwatchs,
                default: "a"
            }]
        }, {
            group: '选项集',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
        items: function($node, model, value) {
            var index = 1;
            var orderedCids = value;
            _.each(orderedCids, function(cid) {
                W.component.CID2COMPONENT[cid].model.set('index', index++, {silent: true});
            });

            var task = new W.DelayedTask(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this);
            task.delay(100);
        },
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
        icon_position: function($node, model, value) {
            var oldClass = 'ui-btn-icon-' + $node.attr('data-iconpos');
            var newClass = 'ui-btn-icon-' + value;
            $node.removeClass(oldClass).addClass(newClass);
            $node.attr('data-iconpos', value);

            W.Broadcaster.trigger('component:resize', this);
        },
        button_theme: function($node, model, value) {
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
        name: 'Panel',
        imgClass: 'componentList_component_panel'
    }
});
