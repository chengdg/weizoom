/**
 * @class W.component.wepage.TextNav
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.TextNav = W.component.Component.extend({
	type: 'wepage.textnav',
	selectable: 'no',
	propertyViewTitle: '文本导航',

	properties: [
        {
            group: '属性1',
            fields: [{
            	name: 'title',
            	type: 'text',
            	displayName: '导航名称',
                maxLength:30,
                validate: 'data-validate="require-notempty::导航名称不能为空"',
                validateIgnoreDefaultValue: true,
                isUserProperty: true,
                placeholder:'编辑[文本导航]',
            	default: '编辑[文本导航]'
            }, {
                name: 'target',
                type: 'select_link',
                displayName: '链接到',
                isUserProperty: true,
                validate: 'data-validate="require-notempty::链接地址不能为空"',
                triggerButton: '从微站选择',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        title: function($node, model, value, $propertyViewNode) {
            value = this.getDisplayValue(value, 'title');
            $node.find('.wa-inner-link').html(value);
        },
        target: function($node, model, value, $propertyViewNode) {
            xwarn(value);
            if (value.length > 0) {
                var linkData = $.parseJSON(value);
                if (linkData.type === 'manualInput') {

                } else {
                    $propertyViewNode.find('.xa-selected-title-box').show();
                    $propertyViewNode.find('.xa-selectLink-url').val(linkData.data).attr('disabled','disabled');
                    $propertyViewNode.find('.xa-selectLink-name').text(linkData.data_path);
                    $propertyViewNode.find('.xa-link-menu').html('修改<span class="glyphicon glyphicon-menu-down"></span>');
                }
            }else{
                $propertyViewNode.find('.xa-selected-title-box').hide();
                $propertyViewNode.find('.xa-selectLink-url').val('').removeAttr('disabled');
                $propertyViewNode.find('.xa-selectLink-name').text('');
                $propertyViewNode.find('.xa-link-menu').html('从微站选择<span class="glyphicon glyphicon-menu-down"></span>');
            }
        }
    }
});
