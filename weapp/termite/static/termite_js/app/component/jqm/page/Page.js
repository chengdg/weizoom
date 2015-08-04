/**
 * @class W.component.jqm.Page
 * 页面
 */
W.component.jqm.Page = W.component.Component.extend({
	type: 'jqm.page',
	propertyViewTitle: '背景',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'content_padding',
                type: 'text',
                displayName: 'Padding',
                default: '15px'
            }, {
                name: 'theme',
                type: 'select',
                displayName: 'Theme',
                source: W.data.ThemeSwatchs,
                default: "a"
            }, {
                name: 'title',
                type: 'text',
                displayName: '页面名',
                default: '页面'
            }, {
                name: 'datasource_page_id',
                type: 'select',
                displayName: '数据页',
                source: W.data.getDatasourcePages,
                default: ''
            }, {
                name: 'background',
                type: 'dialog_select',
                isUserProperty: true,
                displayName: '图片',
                triggerButton: '选择图片...',
                dialog: 'W.workbench.SelectImageDialog',
                default: ''
            }, {
                name: 'uploadWidth',
                type: 'text',
                displayName: '建议宽度',
                default: '320'
            }, {
                name: 'uploadHeight',
                type: 'text',
                displayName: '建议高度',
                default: "568"
            }/*, {
                name: 'url',
                type: 'text',
                displayName: 'URL',
                default: '#'
            }, {
                name: 'is_index_page',
                type: 'boolean',
                displayName: '首页? ',
                default: 'no'
            }*/]
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
            $node.find('.ui-page').css('background-image', url);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
