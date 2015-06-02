/**
 * @class W.component.jqm.PageFooter
 * 页面的header
 */
W.component.jqm.PageFooter = W.component.Component.extend({
	type: 'jqm.page_footer',
	propertyViewTitle: 'Page Footer',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "a"
            }, {
                name: 'is_fixed',
                type: 'boolean',
                displayName: 'Fixed? ',
                default: "yes"
            }]
        }
    ],

    subComponentTypes: [
        {type: 'jqm.heading', model: {text: 'Footer'}}
    ],

    propertyChangeHandlers: {
        theme: function($node, model, value) {
            if (value === '') {
                value = 'c';
            }
            //for footer itself
            var oldTheme = model.previous('theme');
            var oldClass = "ui-bar-" + oldTheme;
            var newClass = "ui-bar-" + value;
            $node.find('.'+oldClass).removeClass(oldClass).addClass(newClass).attr('data-theme', value);

            //for button
            var oldClass = "ui-btn-up-" + oldTheme;
            var newClass = "ui-btn-up-" + value;
            $node.find('.'+oldClass).removeClass(oldClass).addClass(newClass);            
        },
        is_fixed: function($node, model, value) {
            if (value === 'yes') {
                $node.addClass('ui-footer-fixed').addClass('slideup').attr('data-position', 'fixed');
            } else {
                $node.removeClass('ui-footer-fixed').removeClass('slideup').removeAttr('data-position');
            }
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Page Footer',
        imgClass: 'componentList_component_footer'
    }
});
