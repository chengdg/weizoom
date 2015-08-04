/**
 * @class W.component.jqm.ToggleSwitch
 * 
 */
W.component.jqm.ToggleSwitch = W.component.Component.extend({
	type: 'jqm.toggleswitch',
	propertyViewTitle: 'Toggle Switch',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'title',
                type: 'text',
                displayName: 'Title',
                default: 'Title'
            }, {
                name: 'is_mini',
                type: 'boolean',
                displayName: 'Mini? ',
                default: 'no'
            }, {
                name: 'off_text',
                type: 'text',
                displayName: '"off"text',
                default: '关闭'
            }, {
                name: 'on_text',
                type: 'text',
                displayName: '"on"text',
                default: '开启'
            }]
        }
    ],

    propertyChangeHandlers: {
        title: function($node, model, value) {
            $node.find('label').text(value);

            W.Broadcaster.trigger('component:resize', this);
        },

        is_mini: function($node, model, value) {
            if (value === 'yes') {
                $node.find('div.ui-slider').eq(0).addClass('ui-mini');
            } else {
                $node.find('div.ui-slider').eq(0).removeClass('ui-mini');
            }

            W.Broadcaster.trigger('component:resize', this);
        },

        off_text: function($node, model, value) {
            $node.find('span.ui-slider-label').eq(1).text(value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Toggle Switch',
        imgClass: 'componentList_component_toggle_switch'
    }
});
