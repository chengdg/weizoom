/**
 * 
 */
W.component.jqm.NavIconGridButton = W.component.Component.extend({
    type: 'jqm.nav_icon_grid_button',
    selectable: 'no',
    propertyViewTitle: '图标Button',

    properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '文本',
                isUserProperty: true,
                default: 'Button'
            }, {
                name: 'icon',
                type: 'dialog_select',
                displayName: '图标',
                triggerButton: '选择图标...',
                dialog: 'W.dialog.workbench.SelectNavIconDialog',
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
            }, {
                name: 'color',
                type: 'dialog_select',
                displayName: '背景色',
                triggerButton: '选择颜色...',
                dialog: 'W.dialog.workbench.SelectColorDialog',
                isUserProperty: true,
                default: 'F46B41'
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value, $propertyViewNode) {
            $node.find('h3').text(value);
            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
            }
        },
        icon: function($node, model, value, $propertyViewNode) {
            var background = 'url(' + value + ')';
            $node.find('a').css('background-image', background);

            if ($propertyViewNode) {
                $propertyViewNode.find('.x-dynamicComponentIconField').css({
                    width: '60px',
                    height: '60px',
                    'background-color': '#AAAAAA',
                    'background-image': background,
                    'background-size': '50px 50px',
                    'background-repeat': 'no-repeat',
                    'background-position': '5px 5px'
                });
            }
        },
        target: function($node, model, value, $propertyViewNode) {
            if ($propertyViewNode) {
                $propertyViewNode.find('.x-targetText').text($.parseJSON(value)['data_path']);
            }
        },
        color: function($node, model, value, $propertyViewNode) {
            if (value !== 'none') {
                value = ('#' + value);
            } else {
                value = 'transparent';
            }
            xwarn('color: ' + value);
            $node.css('background-color', value);
            $node.find('a').css('background-color', value);

            if ($propertyViewNode) {
                $propertyViewNode.find('.x-dynamicComponentColorField').css({
                    width: '30px',
                    height: '30px',
                    'background-color': value
                });
            }
        }
    },

    initialize: function(obj) {
        this.super('initialize', obj);
    }
});

