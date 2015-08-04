/**
 * @class W.component.weapp.RelateLink
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.RelateLink = W.component.Component.extend({
	type: 'weapp.relatelink',
	selectable: 'no',
	propertyViewTitle: '关联链接',

	properties: [
        {
            group: '属性1',
            fields: [{
                name: 'title',
                type: 'text',
                default: '关联链接'

            },{
                name: 'target',
                type: 'dialog_select',
                displayName: '内容来源',
                isUserProperty: true,
                dialogParameter: '{"workspace_filter":"mall:cms", "data_category_filter":"category"}',
                triggerButton: '选择内容...',
                dialog: 'W.dialog.workbench.SelectLinkTargetDialog'
            },{
            	name: 'count',
            	type: 'select',
            	displayName: '显示条数',
                isUserProperty: true,
            	source: [{name:'1条', value:'1'},{name:'2条', value:'2'},{name:'3条', value:'3'},{name:'4条', value:'4'},{name:'5条', value:'5'}],
            	default: '3'
            }]
        }
    ],

    propertyChangeHandlers: {
        count: function($node, model, value) {
        	$node.find('.wa-inner-link').each(function(i,n){
                if(i<parseInt(value))
                    $(n).show();
                else $(n).hide();
                W.Broadcaster.trigger('component:resize', this)
            });
        },
        target: function($node, module, value) {
            var data = $.parseJSON(value);
            var productName = data['meta']['name'];
            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(productName);
                $propertyViewNode.find('.x-targetText').text(data.data_path);
            }
            var categoryId = data['meta']['id'];

            W.getLoadingView().show();
            api = '';
            data_type = data['meta']['type'];
            if (data_type == 'article_category') {
                api = 'articles_by_category_id/get';
            } else if (data_type == 'product_category') {
                api = 'products_by_category_id/get';
            }
            W.getApi().call({
                app: 'webapp',
                api: api,
                args: {
                    id: categoryId,
                    count: $node.find('.wa-inner-link span').length
                },
                success: function(apidata) {
                    W.getLoadingView().hide();
                    $node.find('.wa-inner-link span').each(function(i,n){
                        if(apidata.length > i)
                            $(n).html(apidata[i].name);
                        else
                            $(n).html(data.data_path)
                    });
                },
                error: function(resp) {
                    W.getLoadingView().hide();
                    W.getErrorHintView().show('加载分类数据失败!');
                }
            })
        }
    },

    initialize: function(obj){
        this.super('initialize', obj);
    }
});
