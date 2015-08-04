/**
 * @class W.component.jqm.Slider
 * 
 */
W.component.jqm.Slider = W.component.Component.extend({
	type: 'jqm.slider',
	propertyViewTitle: 'Slider',

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
                name: 'value',
                type: 'text',
                displayName: 'Value',
                default: '50'
            }, {
                name: 'min_value',
                type: 'text',
                displayName: 'Min Value',
                default: '0'
            }, {
                name: 'max_value',
                type: 'text',
                displayName: 'Max Value',
                default: '100'
            }, {
                name: 'is_show_highlight',
                type: 'boolean',
                displayName: 'Highlight? ',
                default: 'no'
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
                $node.find('div.ui-slider-track').eq(0).addClass('ui-mini');
            } else {
                $node.find('div.ui-slider-track').eq(0).removeClass('ui-mini');
            }

            W.Broadcaster.trigger('component:resize', this);
        },

        is_show_highlight: function($node, model, value) {
            if (value === 'yes') {
                $node.find('div.ui-slider-track').eq(0).prepend('<div class="ui-slider-bg ui-btn-active ui-btn-corner-all" style="width: ' + model.get('value') + '%;"></div>');
            } else {
                
                $node.find('div.ui-slider-track div').eq(0).remove();
            }
            
        },

        value: function($node, model, value) {
            $node.find('input').val(value);

            var percentage = (parseInt(model.get('value')) + 0.0) / parseInt(model.get('max_value')) * 100;
            $node.find('div.ui-slider-bg').css('width', percentage+'%');
            $node.find('div.ui-slider-track > a').css('left', percentage+'%');
        },

        max_value: function($node, model, value) {
            var percentage = (parseInt(model.get('value')) + 0.0) / parseInt(model.get('max_value')) * 100;
            $node.find('div.ui-slider-bg').css('width', percentage+'%');
            $node.find('div.ui-slider-track > a').css('left', percentage+'%');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Slider',
        imgClass: 'componentList_component_slider'
    }
});
