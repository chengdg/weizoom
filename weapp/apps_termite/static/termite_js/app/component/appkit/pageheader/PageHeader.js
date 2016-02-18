/**
 * @class W.component.appkit.PageHeader
 * 
 */
W.component.appkit.PageHeader = W.component.Component.extend({
	type: 'appkit.pageheader',
    selectable: 'no',
	propertyViewTitle: '页头',

	properties: [
        {
            group: '属性1',
            fields: [{
                name: 'backgroud',
                type: 'dialog_select',
                displayName: '背景图片',
                isUserProperty: true,
                triggerButton: '选择图片...',
                dialog: 'W.workbench.SelectImageDialog',
                default: ''
            }, {
                name: 'logo',
                type: 'dialog_select',
                displayName: '头像',
                isUserProperty: true,
                triggerButton: '选择图片...',
                dialog: 'W.workbench.SelectImageDialog',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        backgroud: function($node, model, value, $propertyViewNode) {
            xlog('------'+$node.find('.wa-shop-backgroud').css('background'));
            $node.find('.wa-shop-backgroud').css('background', 'url("'+value+'")');
        },
        logo: function($node, model, value, $propertyViewNode) {
            $node.find('.wa-shop-logo').attr('src', value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '页头',
        imgClass: 'componentList_component_page_header'
    }
 });