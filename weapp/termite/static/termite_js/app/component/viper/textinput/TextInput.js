/**
 * @class W.component.viper.TextInput
 * 
 */
W.component.viper.TextInput = W.component.Component.extend({
	type: 'viper.textinput',
	propertyViewTitle: 'Text Input',

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
                name: 'prefix',
                type: 'text',
                displayName: '前导文本',
                default: ''
            }, {
                name: 'suffix',
                type: 'text',
                displayName: '后导文本',
                default: ''
            }]
        }, {
            group: 'Validate',
            fields: [{
                name: 'validate',
                type: 'textarea',
                help: '数值: int\n价格: price\n小数: float',
                displayName: '校验规则',
                default: 'data-validate="required"\ndata-validate-max-length="50"'
            }]
        }
    ],

    propertyChangeHandlers: {
        label: function($node, model, value) {
            $node.find('label').text(value+"：");

            W.Broadcaster.trigger('component:resize', this);
        },

        name: function($node, model, value) {
            $node.find('.errorHint').text('name="'+model.get('name')+'"');

            W.Broadcaster.trigger('component:resize', this);
        },

        placeholder: function($node, model, value) {
            $node.find('input').attr('placeholder', value);
        },

        prefix: function($node, model, value) {
            this.__processAddOn($node, model, value, 'prefix');
        },

        suffix: function($node, model, value) {
            this.__processAddOn($node, model, value, 'suffix');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    },

    __processAddOn: function($node, model, value, type) {
        var $addOnZone = $node.find('.xa-addOnZone');
        xlog($addOnZone);
        if ($addOnZone.length == 0) {
            W.Broadcaster.trigger('designpage:refresh');
            return;
        }

        if (!value) {
            W.Broadcaster.trigger('designpage:refresh');
            return;
        }

        var $input = $node.find('input');
        var $addOn = null;
        var action = null;
        if ('prefix' === type) {
            $addOn = $input.prev('span');   
            action = 'before';
        } else {
            $addOn = $input.next('span');
            action = 'after';
        }
        
        if ($addOn.length == 0) {
            $input[action]('<span class="add-on">'+value+'</span>')
        } else {
            $addOn.text(value);
        }
    }
}, {
    indicator: {
        name: 'Text Input',
        imgClass: 'componentList_component_text_input'
    }
});