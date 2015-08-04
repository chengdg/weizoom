/**
 * @class W.component.TextAreaInput
 * 
 */
W.component.viper.TextAreaInput = W.component.Component.extend({
	type: 'viper.textarea',
	propertyViewTitle: 'Text Area',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: 'Label'
            }, {
                name: 'placeholder',
                type: 'text',
                displayName: 'PlaceHolder',
                default: ''
            }, {
                name: 'height',
                type: 'text',
                displayName: '高度',
                default: '100'
            }]
        }, {
            group: 'Validate',
            fields: [{
                name: 'validate',
                type: 'textarea',
                displayName: '校验规则',
                default: 'data-validate="required"\ndata-validate-max-length="1024"'
            }]
        }
    ],

    propertyChangeHandlers: {
        label: function($node, model, value) {
            $node.find('label').text(value+"：");

            W.Broadcaster.trigger('component:resize', this);
        },

        name: function($node, model, value) {
            $node.find('.errorHint').text('name="'+model.get('name')+'", validate="'+model.get('validate')+'"');
        },

        placeholder: function($node, model, value) {
            $node.find('textarea').attr('placeholder', value);
        },

        height: function($node, model, value) {
            $node.find('textarea').css('height', value+'px');

            W.Broadcaster.trigger('component:resize', this);
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