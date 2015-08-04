/**
 * @class W.component.jqm.Image
 * 
 */
W.component.jqm.Image = W.component.Component.extend({
	type: 'jqm.image',
	propertyViewTitle: 'Image',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'image',
                type: 'dialog_select',
                isUserProperty: true,
                displayName: '图片',
                triggerButton: '选择图片...',
                dialog: 'W.workbench.SelectImageDialog',
                default: ''
            }, {
                name: 'width',
                type: 'text',
                displayName: 'Width',
                default: '100%'
            }, {
                name: 'height',
                type: 'text',
                displayName: 'Height',
                default: "200px"
            }, {
                name: 'uploadWidth',
                type: 'text',
                displayName: '建议宽度',
                default: '100%'
            }, {
                name: 'uploadHeight',
                type: 'text',
                displayName: '建议高度',
                default: "200px"
            }, {
                name: 'target',
                type: 'select',
                displayName: '链接',
                source: W.data.getWorkbenchPages,
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        image: function($node, model, value) {
            var $img = $node.find('img').eq(0);
            var src = $img.attr('src');
            if (src === '/static/termite_img/image.png') {
                $node.empty().html('<img width="98%" height="98%" src="' + value + '" />');
            } else {
                $img.attr('src', value);
            }
            $node.find('img').attr('src', value);
        },
        width: function($node, model, value) {
            $node.css('width', value);

            W.Broadcaster.trigger('component:resize', this);
        },
        height: function($node, model, value) {
            $node.css('height', value);

            W.Broadcaster.trigger('component:resize', this);
        }
    },

    datasource: [
        {name: 'image'}
    ],

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Image',
        imgClass: 'componentList_component_image'
    }
});
