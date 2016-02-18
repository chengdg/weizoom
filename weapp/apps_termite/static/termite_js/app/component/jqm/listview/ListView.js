/**
 * @class W.component.jqm.ListView
 * 
 */
W.component.jqm.ListView = W.component.Component.extend({
	type: 'jqm.listview',
	propertyViewTitle: 'List View',

    dynamicComponentTypes: [
        {type: 'jqm.listview_divider', model: {index: 1, text: 'Divider'}},
        {type: 'jqm.listview_button', model: {index: 2, text: 'Button', target: '', theme: 'c', bubble_text: '10'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'divider_theme',
                type: 'select',
                displayName: 'Divider',
                source: W.data.ThemeSwatchs,
                default: "b"
            }, {
                name: 'is_inset',
                type: 'boolean',
                displayName: 'Inset? ',
                default: "yes"
            }, {
                name: 'uploadWidth',
                type: 'text',
                displayName: '建议宽度',
                default: '200'
            }, {
                name: 'uploadHeight',
                type: 'text',
                displayName: '建议高度',
                default: "200"
            }]
        }, {
            group: '选项集',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
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
        divider_theme: function($node, model, value) {
            if (value === '') {
                value = 'c';
            }
            var oldTheme = model.previous('divider_theme');
            var oldClass= "ui-bar-" + oldTheme;
            var newClass = "ui-bar-" + value;
            xlog('oldClass: ' + oldClass);
            xlog('newClass: ' + newClass);
            $node.find('.ui-li-divider').removeClass(oldClass).addClass(newClass);
        },
        is_inset: function($node, model, value) {
            $ul = $node.find('ul').eq(0);
            if (value === 'yes') {
                $ul.addClass('ui-listview-inset ui-corner-all ui-shadow');
            } else {
                $ul.removeClass('ui-listview-inset').removeClass('ui-corner-all').removeClass('ui-shadow');
            }

            W.Broadcaster.trigger('component:resize', this);
        }
    },

    datasource: [
        {name: 'item.title'},
        {name: 'item.detail'},
        {name: 'item.link'},
        {name: 'item.image'}
    ],

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'List View',
        imgClass: 'componentList_component_listview'
    }
});