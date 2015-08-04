/**
 * @class W.component.jqm.SelectMenu
 * 
 */
W.component.jqm.SelectMenu = W.component.Component.extend({
	type: 'jqm.select_menu',
	propertyViewTitle: 'Select Menu',

    dynamicComponentTypes: [
        {type: 'jqm.select_menu_item', model: {index:1, text: 'Option', value: 'value', theme: 'c'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'title',
                type: 'text',
                displayName: 'Title',
                default: '选择'
            }, {
                name: 'is_mini',
                type: 'boolean',
                displayName: 'Mini? ',
                default: "no"
            }, {
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "c"
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
        title: function($node, model, value) {
            $node.find('label.ui-select').text(value+':');
        },
        is_mini: function($node, model, value) {
            if (value === 'yes') {
                $node.find('a.ui-btn').addClass('ui-mini');
            } else {
                $node.find('a.ui-btn').removeClass('ui-mini');
            }

            W.Broadcaster.trigger('component:resize', this);
        },
        theme: function($node, model, value) {
            var $button = $node.find('a.ui-btn');
            if (value === '') {
                value = 'c';
            }
            var oldTheme = model.previous('theme');
            var oldClass= "ui-btn-up-" + oldTheme;
            var newClass = "ui-btn-up-" + value;
            $button.removeClass(oldClass).addClass(newClass).attr('data-theme', value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Select Menu',
        imgClass: 'componentList_component_select_menu'
    }
});