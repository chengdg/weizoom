/**
 * @class W.component.wepage.PageHeader
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.personalityTheme = W.component.Component.extend({
	type: 'wepage.personalityTheme',
    selectable: 'no',
	propertyViewTitle: '个性模板',

	properties: [
        {
            group: '属性1',
            groupClass:'',
            fields: [{
                name: 'title',
                type: 'text',
                displayName: '导航名称',
                validate: 'data-validate="require-notempty::导航名称不能为空"',
                validateIgnoreDefaultValue: true,
                maxLength:7,
                isUserProperty: true,
                placeholder:'',
                default: ''
            }, {
                name: 'target',
                type: 'select_link',
                displayName: '链接到',
                isUserProperty: true,
                validate: 'data-validate="require-notempty::链接地址不能为空"',
                triggerButton: '从微站选择'
            }]
        }
    ],

    propertyChangeHandlers: {
      title: function($node, model, value, $propertyViewNode) {
            $node.find('a').text(value);
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

                $node.find('a').attr('href', linkData.data);
            }else{
                $propertyViewNode.find('.xa-selected-title-box').hide();
                $propertyViewNode.find('.xa-selectLink-url').val('').removeAttr('disabled');
                $propertyViewNode.find('.xa-selectLink-name').text('');
                $propertyViewNode.find('.xa-link-menu').html('从微站选择<span class="glyphicon glyphicon-menu-down"></span>');

                $node.find('a').attr('href', "#")
            }
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
 });