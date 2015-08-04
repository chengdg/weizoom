/**
 * @class W.component.jqm.CheckboxButton
 * 
 */
W.component.jqm.CheckboxButton = W.component.Component.extend({
	type: 'jqm.checkbox_button',
    selectable: 'no',
	propertyViewTitle: 'Checkbox Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: 'Text',
                default: 'Checkbox'
            }, {
                name: 'value',
                type: 'text',
                displayName: 'Value',
                default: ''
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
            $checkbox = $node.parents('.ui-checkbox').eq(0);
            //change button class
            if ('yes' === value) {
                oldClass = 'ui-checkbox-off';
                newClass = 'ui-checkbox-on';
            } else {
                oldClass = 'ui-checkbox-on';
                newClass = 'ui-checkbox-off';
            }
            $checkbox.find('.ui-btn').removeClass(oldClass).addClass(newClass);

            //change icon class
            if ('yes' === value) {
                oldClass = 'ui-icon-checkbox-off';
                newClass = 'ui-icon-checkbox-on';
            } else {
                oldClass = 'ui-icon-checkbox-on';
                newClass = 'ui-icon-checkbox-off';
            }
            $checkbox.find('.ui-icon').removeClass(oldClass).addClass(newClass);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);

        if (this.model.get('value') === '') {
            this.model.set('value', 'value ' + Date.now(), {silent: true});
        }
    }
});