/**
 * @class W.component.jqm.NavBar
 * 
 */
W.component.jqm.NavBar = W.component.Component.extend({
	type: 'jqm.nav_bar',
	propertyViewTitle: 'Nav Bar',

    dynamicComponentTypes: [
        {type: 'jqm.nav_bar_button', model: {text: 'Button 1'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'icon_position',
                type: 'radio-group',
                displayName: '图标位置',
                source: W.data.ImagePositions,
                default: 'left'
            }]
        }, {
            group: '按钮集',
            fields: [{
                name: 'buttons',
                type: 'dynamic-generated-control',
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
        buttons: function($node, model, value) {
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
        icon_position: function($node, model, value) {
            var $buttons = $node.find('.ui-btn');
            var oldClass = 'ui-btn-icon-' + model.previous('icon_position');
            var newClass = 'ui-btn-icon-' + value;
            $buttons.removeClass(oldClass).addClass(newClass);
            $buttons.attr('data-iconpos', value);

            W.Broadcaster.trigger('component:resize', this);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Nav Bar',
        imgClass: 'componentList_component_nav_bar'
    }
});
