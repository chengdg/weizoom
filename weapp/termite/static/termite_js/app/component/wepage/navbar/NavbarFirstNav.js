/**
 * @class W.component.wepage.TextNav
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.NavbarFirstNav = W.component.Component.extend({
	type: 'wepage.navbar_firstnav',
	selectable: 'no',
	propertyViewTitle: '一级菜单',

	properties: [
        {
            group: '属性1',
            groupClass:'xui-propertyView-navbar-firstnav-property',
            fields: [{
            	name: 'title',
            	type: 'text',
            	displayName: '导航名称',
                maxLength:30,
                validateIgnoreDefaultValue: true,
                isUserProperty: true,
                placeholder:'编辑[文本导航]',
            	default: '编辑[文本导航]'
            }, {
                name: 'target',
                type: 'select_link',
                displayName: '链接到',
                isUserProperty: true,
                triggerButton: '从微站选择',
                default: ''
            }, {
                name: 'second_navs',
                type: 'second_navs',
                displayName: '',
                isUserProperty: true,
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
        },
        items: function($node, model, value) {
            this.refresh($node, {resize:true, refreshPropertyView:true});
        }
    }
});
