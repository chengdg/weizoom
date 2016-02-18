/**
 * 
 */
W.component.jqm.NavGridButton = W.component.Component.extend({
    type: 'jqm.nav_grid_button',
    selectable: 'no',
    propertyViewTitle: 'Button',

    properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文本',
                default: 'Button'
            }, {
                name: 'image',
                type: 'dialog_select',
                displayName: '图片',
                triggerButton: '选择图片...',
                dialog: 'W.workbench.SelectImageDialog',
                default: ''
            }, {
                name: 'target',
                type: 'dialog_select',
                displayName: '链接',
                triggerButton: '选择页面...',
                dialog: 'W.dialog.workbench.SelectLinkTargetDialog',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value, $propertyViewNode) {
            $node.find('.navGridButton_link_text').text(value);
            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
            }
        },
        image: function($node, model, value, $propertyViewNode) {
            $node.find('img').attr('src', value);
            if ($propertyViewNode) {
                $propertyViewNode.find('img').attr('src', value);
            }
        }
    },

    initialize: function(obj) {
        this.super('initialize', obj);
    }
});

