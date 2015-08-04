/**
 * @class W.component.wepage.Page
 * 页面
 */
ensureNS('W.component.wepage');
W.component.wepage.Page = W.component.Component.extend({
	type: 'wepage.page',
	propertyViewTitle: '背景',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'title',
                type: 'hidden',
                displayName: '页面名',
                default: '页面'
            }, {
                name: 'site_title',
                type: 'text',
                displayName: '页面名称',
                isUserProperty: true,
                maxLength: 20,
                validate: 'data-validate="require-notempty::页面标题不能为空"',
                validateIgnoreDefaultValue: true,
                default: '微页面标题',
                placeholder: '微页面标题'
            }, {
                name: 'site_description',
                type: 'text',
                displayName: '页面描述',
                isUserProperty: true,
                default: '',
                placeholder: '通过微信分享时，会显示该描述'
            }]
        }, 
        {
            group: '事件',
            fields: [{
                name: 'event:onload',
                type: 'dialog_select',
                displayName: 'Click',
                triggerButton: '编辑代码...',
                dialog: 'W.workbench.EditCodeDialog',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        is_index_page: function($node, model, value) {
            _.each(W.data.pageManager.getPages(), function(page) {
                page.model.set('is_index_page', 'no', {silent: true});
            });

            model.set('is_index_page', 'yes', {silent: true})
        },
        background: function($node, model, value) {
            var url = 'url(' + value + ')';
            $node.find('.wa-page').css('background-image', url);
        },
        site_title: function($node, model, value) {
            value = this.getDisplayValue(value, 'site_title');
            W.Broadcaster.trigger('designpage:update_site_title', value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
