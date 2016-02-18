/**
 * @class W.component.jqm.SubmitButton
 * 
 */
W.component.jqm.SubmitButton = W.component.Component.extend({
	type: 'jqm.submitbutton',
	propertyViewTitle: 'Submit Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文本',
                default: '提交'
            }, {
                name: 'icon_position',
                type: 'radio-group',
                displayName: '图标位置',
                source: W.data.ImagePositions,
                default: 'left'
            }, {
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "e"
            }, {
                name: 'is_inline',
                type: 'boolean',
                displayName: 'Inline? ',
                default: "no"
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value) {
            $node.find('.ui-btn-text').text(value);

            W.Broadcaster.trigger('component:resize', this);
        },
        icon_position: function($node, model, value) {
            $node = $node.find('div.ui-submit').eq(0);
            var oldClass = 'ui-btn-icon-' + $node.attr('data-iconpos');
            var newClass = 'ui-btn-icon-' + value;
            $node.removeClass(oldClass).addClass(newClass);
            $node.attr('data-iconpos', value);

            W.Broadcaster.trigger('component:resize', this);
        },
        theme: function($node, model, value) {
            $node = $node.find('div.ui-submit').eq(0);
            if (value === '') {
                value = 'c';
            }
            var oldTheme = model.previous('theme');
            var oldClass= "ui-btn-up-" + oldTheme;
            var newClass = "ui-btn-up-" + value;
            $node.removeClass(oldClass).addClass(newClass).attr('data-theme', value);
        },
        is_inline: function($node, model, value) {
            $node = $node.find('div.ui-submit').eq(0);
            if (value === 'yes') {
                $node.addClass('ui-btn-inline');
            } else {
                $node.removeClass('ui-btn-inline');
            }

            W.Broadcaster.trigger('component:resize', this);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Submit Button',
        imgClass: 'componentList_component_submit'
    }
});