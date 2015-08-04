/**
 * @class W.component.jqm.PageHeader
 * 页面的header
 */
W.component.jqm.PageHeader = W.component.Component.extend({
	type: 'jqm.page_header',
	propertyViewTitle: 'Page Header',

    dynamicComponentTypes: [
        {type: 'jqm.header_button', model: null}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "a"
            }, {
                name: 'is_fixed',
                type: 'boolean',
                displayName: 'Fixed? ',
                default: "no"
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

    subComponentTypes: [
        {type: 'jqm.heading', model: {text: 'Header'}}
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
        theme: function($node, model, value) {
            if (value === '') {
                value = 'c';
            }
            //for footer itself
            var oldTheme = model.previous('theme');
            var oldClass = "ui-bar-" + oldTheme;
            var newClass = "ui-bar-" + value;
            $node.removeClass(oldClass).addClass(newClass).attr('data-theme', value);

            //for button
            var oldClass = "ui-btn-up-" + oldTheme;
            var newClass = "ui-btn-up-" + value;
            $node.removeClass(oldClass).addClass(newClass);            
        },
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Page Header',
        imgClass: 'componentList_component_header'
    }
});
