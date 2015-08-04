/**
 * @class W.component.jqm.TextAreaInput
 * 
 */
W.component.jqm.TextAreaInput = W.component.Component.extend({
	type: 'jqm.textarea',
	propertyViewTitle: 'Text Area',

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
                name: 'placeholder',
                type: 'text',
                displayName: 'PlaceHolder',
                default: ''
            }, {
                name: 'initial_text',
                type: 'text',
                displayName: 'Initial Text',
                default: ''
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
                $node.find('textarea').eq(0).addClass('ui-mini');
            } else {
                $node.find('textarea').eq(0).removeClass('ui-mini');
            }

            W.Broadcaster.trigger('component:resize', this);
        },

        placeholder: function($node, model, value) {
            $node.find('textarea').attr('placeholder', value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Text Area',
        imgClass: 'componentList_component_text_area'
    }
});
