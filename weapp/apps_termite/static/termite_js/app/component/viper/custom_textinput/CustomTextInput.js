/**
 * @class W.component.viper.CustomTextInput
 * 
 */
W.component.viper.CustomTextInput = W.component.Component.extend({
	type: 'viper.custom_textinput',
	propertyViewTitle: '定制输入框',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: 'Label'
            }, {
                name: 'text',
                type: 'text',
                displayName: '输入内容',
                placeholder: 'xx${name:validate}xx${..}xx',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        label: function($node, model, value) {
            $node.find('label').text(value+"：");

            W.Broadcaster.trigger('component:resize', this);
        },

        text: function($node, model, value) {
            if (this.refreshTimeId) {
                clearTimeout(this.refreshTimeId);
            }
            this.refreshTimeId = setTimeout(_.bind(this.__refresh, this), 1500);
        }
    },

    __refresh: function() {
        W.Broadcaster.trigger('designpage:refresh');
    }
}, {
    indicator: {
        name: '定制输入框',
        imgClass: 'componentList_component_text_input'
    }
});