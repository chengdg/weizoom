/**
 * @class W.component.viper.ImageSelector
 * 
 */

W.component.viper.ImageSelector = W.component.Component.extend({
	type: 'viper.image_selector',
	propertyViewTitle: '图片上传器',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: 'Label'
            }, {
                name: 'width',
                type: 'text',
                displayName: '宽度',
                default: '300'
            }, {
                name: 'height',
                type: 'text',
                displayName: '高度',
                default: '200'
            }]
        }, {
            group: 'Validate',
            fields: [{
                name: 'validate',
                type: 'textarea',
                displayName: '校验规则',
                default: 'data-validate="require-image"'
            }]
        }
    ],

    propertyChangeHandlers: {
        label: function($node, model, value) {
            xlog($node);
            xlog(value);
            $node.find('label').text(value+"：");
        },
        name: function($node, model, value) {
            $node.find('.errorHint').text('name="'+model.get('name')+'"');
        },
        width: function($node, model, value) {
            $node.find('.x-imageSelector-width').text(value);
        },
        height: function($node, model, value) {
            $node.find('.x-imageSelector-height').text(value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '图片上传器',
        imgClass: 'componentList_component_image'
    }
});