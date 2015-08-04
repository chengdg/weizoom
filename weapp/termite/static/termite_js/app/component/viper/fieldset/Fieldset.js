/**
 * @class W.component.viper.Fieldset
 * 
 */
W.component.viper.Fieldset = W.component.Component.extend({
	type: 'viper.fieldset',
	propertyViewTitle: 'Fieldset',

    capability: {
        editHtml: true
    },

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'legend',
                type: 'text',
                displayName: 'Legend',
                default: '控件组'
            }, {
                name: 'is_horizontal',
                type: 'boolean',
                displayName: '水平控件?',
                default: 'yes'
            }]
        }
    ],

    propertyChangeHandlers: {
        legend: function($node, model, value) {
            $node.find('legend').text(value);
            W.Broadcaster.trigger('component:resize', this);
        },
        is_horizontal: function($node, model, value) {
            if ('yes' === value) {
                $node.addClass('form-horizontal');
            } else {
                $node.removeClass('form-horizontal');
            }

            W.Broadcaster.trigger('component:resize', this);
        },
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Fieldset',
        imgClass: 'componentList_component_html'
    }
});