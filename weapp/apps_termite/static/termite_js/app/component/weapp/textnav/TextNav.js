/**
 * @class W.component.weapp.TextNav
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.TextNav = W.component.Component.extend({
	type: 'weapp.textnav',
	selectable: 'no',
	propertyViewTitle: '文本导航',

	properties: [
        {
            group: '属性1',
            fields: [{
            	name: 'title',
            	type: 'text',
            	displayName: '导航名称',
                isUserProperty: true,
            	default: '请输入'
            }, {
                name: 'target',
                type: 'dialog_select',
                displayName: '链接',
                isUserProperty: true,
                triggerButton: '选择页面...',
                dialog: 'W.dialog.workbench.SelectLinkTargetDialog'
            }]
        }
    ],

    propertyChangeHandlers: {
        title: function($node, model, value, $propertyViewNode) {
        	$node.find('.wa-inner-link').html(value);
        	$propertyViewNode.find('h3 span').html(value);
        },
        target: function($node, model, value, $propertyViewNode) {
            var data = $.parseJSON(value);
            if ($propertyViewNode) {
                $propertyViewNode.find('.x-targetText').text(data.data_path);
            }
        }
    }
});
