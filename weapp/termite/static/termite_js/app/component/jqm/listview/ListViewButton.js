/**
 * @class W.component.jqm.ListViewButton
 * 
 */
W.component.jqm.ListViewButton = W.component.Component.extend({
	type: 'jqm.listview_button',
    selectable: 'no',
	propertyViewTitle: 'Listview Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: 'Text',
                isUserProperty: true,
                default: 'Button'
            }, {
                name: 'image',
                type: 'dialog_select',
                displayName: '图片',
                triggerButton: '选择图片...',
                dialog: 'W.workbench.SelectImageDialog',
                isUserProperty: true,
                default: ''
            }, {
                name: 'detail',
                type: 'text',
                displayName: 'Detail',
                default: ''
            }, {
                name: 'icon',
                type: 'select',
                displayName: '图标',
                source: W.data.ButtonIcons,
                default: "arrow-r"
            }, {
                name: 'target',
                type: 'dialog_select',
                displayName: '链接',
                triggerButton: '选择页面...',
                dialog: 'W.dialog.workbench.SelectLinkTargetDialog',
                isUserProperty: true,
                default: ''
            }/*, {
                name: 'target',
                type: 'select',
                displayName: '链接',
                source: W.data.getWorkbenchPages,
                default: ''
            }*/, {
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "c"
            }, {
                name: 'bubble_text',
                type: 'text',
                displayName: 'Bubble',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value, $propertyViewNode) {
            $node.find('.xui-listview-button-text').text(value);
            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
            }
        },
        detail: function($node, model, value) {
            if ($node.find('h2').length === 0) {
                W.Broadcaster.trigger('mobilepage:refresh');
            } else {
                $node.find('.xui-listview-button-detail').text(value);
                W.Broadcaster.trigger('component:resize', this);
            }
        },
        image: function($node, model, value, $propertyViewNode) {
            if ($node.find('h2').length === 0) {
                W.Broadcaster.trigger('mobilepage:refresh');
            } else {
                $node.find('img').attr('src', value);
                W.Broadcaster.trigger('component:resize', this);
                if ($propertyViewNode) {
                    $propertyViewNode.find('img').attr('src', value);
                }
            }
        },
        target: function($node, model, value, $propertyViewNode) {
            if ($propertyViewNode) {
                $propertyViewNode.find('.x-targetText').text($.parseJSON(value)['data_path']);
            }
        },
        icon: function($node, model, value) {
            var $icon = $node.find('.ui-icon');
            if (value) {
                //从无到有，或者切换
                var $icon = $node.find('.ui-icon');
                if ($icon.length === 0) {
                    //从无到有
                    var html = '<span class="ui-icon ui-icon-' + value + ' ui-icon-shadow"> </span>';
                    $node.find('.ui-li').append(html);
                } else {
                    //切换
                    var oldClass = 'ui-icon-' + $node.attr('data-icon');
                    var newClass = 'ui-icon-' + value;
                    $icon.removeClass(oldClass).addClass(newClass);
                }
            } else {
                //从有到无
                $icon.remove();
            }
        },
        theme: function($node, model, value) {
            if (value === '') {
                value = 'c';
            }
            var oldTheme = model.previous('theme');
            var oldClass= "ui-btn-up-" + oldTheme;
            var newClass = "ui-btn-up-" + value;
            $node.removeClass(oldClass).addClass(newClass).attr('data-theme', value);
        },
        bubble_text: function($node, model, value) {
            if (value.length == 0) {
                $node.find('span.ui-li-count').remove();
            } else {
                var $count = $node.find('span.ui-li-count');
                if ($count.length == 0) {
                    $node.find('a').append($('<span class="ui-li-count ui-btn-up-c ui-btn-corner-all">'+value+'</span>'));
                } else {
                    $count.text(value);
                }
                
            }
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
