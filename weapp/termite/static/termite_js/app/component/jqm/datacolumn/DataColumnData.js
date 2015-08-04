/**
 * @class W.component.jqm.DataColumnData
 * 
 */
W.component.jqm.DataColumnData = W.component.Component.extend({
	type: 'jqm.datacolumn_data',
    selectable: 'no',
	propertyViewTitle: '数据',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'image',
                type: 'dialog_select',
                displayName: '图片',
                triggerButton: '选择图片...',
                dialog: 'W.workbench.SelectImageDialog',
                isUserProperty: true,
                default: ''
            }, {
                name: 'text',
                type: 'text',
                displayName: '标题',
                isUserProperty: true,
                default: ''
            }, {
                name: 'price',
                type: 'text',
                displayName: '现价',
                isUserProperty: true,
                default: ''
            }, {
                name: 'original_price',
                type: 'text',
                displayName: '原价',
                isUserProperty: true,
                default: ''
            }, {
                name: 'target',
                type: 'dialog_select',
                displayName: '链接',
                triggerButton: '选择页面...',
                dialog: 'W.dialog.workbench.SelectLinkTargetDialog',
                isUserProperty: true,
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value, $propertyViewNode) {
            $node.find('.xui-inner-productName').text(value);
            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
            }
        },
        image: function($node, model, value, $propertyViewNode) {
            $node.find('img').attr('src', value);
            W.Broadcaster.trigger('component:resize', this);
            if ($propertyViewNode) {
                $propertyViewNode.find('img').attr('src', value);
            }
        },
        target: function($node, model, value, $propertyViewNode) {
            if ($propertyViewNode) {
                $propertyViewNode.find('.x-targetText').text($.parseJSON(value)['data_path']);
            }
        },
        price: function($node, model, value, $propertyViewNode) {
            $node.find('.xui-inner-price').text('￥'+value);
        },
        original_price: function($node, model, value, $propertyViewNode) {
            $node.find('.xui-inner-originalPrice').text('￥'+value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
