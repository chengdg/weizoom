/**
 * @class W.component.jqm.CollpsibleGroup
 * 
 */
W.component.jqm.CollapsibleGroup = W.component.Component.extend({
	type: 'jqm.collapsible_group',
	propertyViewTitle: 'Collapsible Group',

    dynamicComponentTypes: [
        {type: 'jqm.collapsible', model: {text: 'Section Header', id: '', is_collapsed: 'yes'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'header_theme',
                type: 'select',
                displayName: 'Header',
                source: W.data.ThemeSwatchs,
                default: "b"
            }, {
                name: 'content_theme',
                type: 'select',
                displayName: 'Content',
                source: W.data.ThemeSwatchs,
                default: "b"
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
        header_theme: function($node, model, value) {
            if (value === '') {
                value = 'c';
            }
            var oldTheme = model.previous('header_theme');
            var oldClass= "ui-btn-up-" + oldTheme;
            var newClass = "ui-btn-up-" + value;
            $node.find('a.ui-collapsible-heading-toggle').removeClass(oldClass).addClass(newClass);
        },
        content_theme: function($node, model, value) {
            if (value === '') {
                value = 'c';
            }
            var oldTheme = model.previous('content_theme');
            var oldClass= "ui-body-" + oldTheme;
            var newClass = "ui-body-" + value;
            $node.find('div.ui-collapsible-content').removeClass(oldClass).addClass(newClass);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Collapsible',
        imgClass: 'componentList_component_collapsible'
    }
});
