/**
 * @class W.component.viper.SwipeImage
 * 
 */

W.component.viper.SwipeImage = W.component.Component.extend({
	type: 'viper.swipe_image',
	propertyViewTitle: '轮播图',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: 'Label'
            }, {
                name: 'count',
                type: 'select',
                displayName: '图片数',
                source: W.data.getIntegerRanges(3, 8),
                default: '3'
            }, {
                name: 'image_width',
                type: 'text',
                displayName: '图片宽度',
                default: '800'
            }, {
                name: 'image_height',
                type: 'text',
                displayName: '图片高度',
                default: '600'
            }]
        }
    ],

    propertyChangeHandlers: {
        label: function($node, model, value) {
            $node.find('label').text(value+"：");
        },
        name: function($node, model, value) {
            $node.find('.errorHint').text('name="'+model.get('name')+'"');
        },
        image_width: function($node, model, value) {
            $node.find('.x-imageSelector-width').text(value);
        },
        image_height: function($node, model, value) {
            $node.find('.x-imageSelector-height').text(value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '轮播图',
        imgClass: 'componentList_component_swipe_image'
    }
});
