/**
 * @class W.component.jqm.RadioButton
 * 
 */
W.component.jqm.RadioButton = W.component.Component.extend({
	type: 'jqm.radio_button',
    selectable: 'no',
	propertyViewTitle: 'Radio Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文本',
                default: 'Option'
            }, {
                name: 'value',
                type: 'text',
                displayName: 'Value',
                default: 'radio1'
            }, {
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "c"
            }, {
                name: 'is_checked',
                type: 'boolean',
                displayName: '选中? ',
                default: "no"
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value) {
            $node.parent().find('.ui-btn-text').text(value);
        },
        theme: function($node, model, value) {
            if (value === '') {
                value = 'c';
            }
            var oldTheme = model.previous('theme');
            var oldClass= "ui-btn-up-" + oldTheme;
            var newClass = "ui-btn-up-" + value;
            $node.parent().find('label').removeClass(oldClass).addClass(newClass).attr('data-theme', value);
        },
        is_checked: function($node, model, value) {
            $radio = $node.parents('.ui-radio').eq(0);
            //change button class
            if ('yes' === value) {
                oldClass = 'ui-radio-off';
                newClass = 'ui-radio-on';
            } else {
                oldClass = 'ui-radio-on';
                newClass = 'ui-radio-off';
            }
            $radio.find('.ui-btn').removeClass(oldClass).addClass(newClass);

            //change icon class
            if ('yes' === value) {
                oldClass = 'ui-icon-radio-off';
                newClass = 'ui-icon-radio-on';
            } else {
                oldClass = 'ui-icon-radio-on';
                newClass = 'ui-icon-radio-off';
            }
            $radio.find('.ui-icon').removeClass(oldClass).addClass(newClass);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
