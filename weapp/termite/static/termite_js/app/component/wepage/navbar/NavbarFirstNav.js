/**
 * @class W.component.wepage.TextNav
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.NavbarFirstNav = W.component.Component.extend({
	type: 'wepage.navbar_firstnav',
	selectable: 'no',
	propertyViewTitle: '一级菜单',
    shouldShowPropertyViewTitle: true,

	properties: [
        {
            group: '属性1',
            groupClass:'xui-propertyView-navbar-firstnav-property',
            groupName: '一级菜单',
            fields: [{
            	name: 'title',
            	type: 'text',
            	displayName: '标题',
                maxLength:5,
                validate: 'data-validate="require-notempty::标题名不能为空"',
                validateIgnoreDefaultValue: true,
                validateIgnoreDefaultValue: true,
                isUserProperty: true,
                placeholder:'标题名',
            	default: ''
            }, {
                name: 'target',
                type: 'select_link',
                displayName: '链接',
                isUserProperty: true,
                triggerButton: '从微站选择',
                otherUpdateDisplayName:'菜单',
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
            var $linkSelectFieldNode = $($propertyViewNode.find('.propertyGroup_property_linkSelectField'));
            if (value.length > 0) {
                var linkData = $.parseJSON(value);
                if (linkData.type === 'manualInput') {

                } else {
                    $linkSelectFieldNode.find('.xa-selected-title-box').show();
                    $linkSelectFieldNode.find('.xa-selectLink-url').val(linkData.data).attr('disabled','disabled');
                    $linkSelectFieldNode.find('.xa-selectLink-name').text(linkData.data_path);
                    $linkSelectFieldNode.find('.xa-link-menu').html('修改<span class="glyphicon glyphicon-menu-down"></span>');
                }
            }else{
                $linkSelectFieldNode.find('.xa-selected-title-box').hide();
                $linkSelectFieldNode.find('.xa-selectLink-url').val('').removeAttr('disabled');
                $linkSelectFieldNode.find('.xa-selectLink-name').text('');
                $linkSelectFieldNode.find('.xa-link-menu').html('从微站选择<span class="glyphicon glyphicon-menu-down"></span>');
            }
        },
        second_navs: function($node, model, value, $propertyViewNode) {
            model.set('second_navs', $.parseJSON(value), {silent:true});
            var parentComponent = W.component.getComponent(this.pid);
            parentComponent.refresh($node, {resize:true});
        }
    },

    setLimitation: function(args) {
        xwarn('----- set limitation -----');
        xwarn(args);

        this.name2field['title'].maxLength = args.titleMaxLength;
        W.component.getFieldsByType('wepage.navbar_firstnav')[0].maxLength = args.titleMaxLength;
    },

    updateViewTitle: function(args) {
        this.propertyViewTitle = args.propertyViewTitle;
        this.properties[0].fields[1].otherUpdateDisplayName = args.otherUpdateDisplayName;
        this.updateComponent();
    },

    updateComponent: function(){
        // 修改 propertyViewTitle
        W.component.TYPE2COMPONENT[this.type].prototype.propertyViewTitle = this.propertyViewTitle;

        // 修改 
        W.component.TYPE2COMPONENT[this.type].prototype.properties[0].fields[1].otherUpdateDisplayName = this.properties[0].fields[1].otherUpdateDisplayName;
    },

    initialize: function(obj) {
        this.super('initialize', obj);
        if (W.WEAPAGE_NAVBARTYPE == 'slide') {
            this.setLimitation({
                titleMaxLength: 10
            });
            this.propertyViewTitle = '一级分类';
            this.properties[0].fields[1].otherUpdateDisplayName = '分类';
        }else{
            this.propertyViewTitle = '一级菜单';
            this.properties[0].fields[1].otherUpdateDisplayName = '菜单';
        }

        this.updateComponent();
    }
});
