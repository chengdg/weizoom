/**
 * @class W.component.viper.RadioButton
 * 
 */
W.component.viper.RadioButton = W.component.Component.extend({
	type: 'viper.radio_button',
    selectable: 'no',
	propertyViewTitle: 'Radio Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文本',
                help: '可使用:${name:validate}',
                default: 'Option'
            }, {
                name: 'value',
                type: 'text',
                displayName: 'Value',
                default: 'radio1'
            }, {
                name: 'is_checked',
                type: 'boolean',
                displayName: '默认选中? ',
                default: "no"
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value, $propertyViewNode) {
            $node.find('span').text(value);
            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
            }
        },
        is_checked: function($node, model, value) {
            $radio = $node.find('input').eq(0);
            //change button class
            if ('yes' === value) {
                $radio.attr('checked', 'checked');
            } else {
                $radio.removeAttr('checked');
            }
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
