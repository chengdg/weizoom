/**
 * @class W.component.jqm.DataColumn
 * 
 */
W.component.jqm.DataColumnGroup = W.component.Component.extend({
	type: 'jqm.datacolumn_group',
	propertyViewTitle: '数据集',
    forceDisplayInPropertyView: 'yes',

    dynamicComponentTypes: [
        {type: 'jqm.datacolumn', model: {index: 1, text: '数据列1'}},
        {type: 'jqm.datacolumn', model: {index: 2, text: '数据列2'}},
        {type: 'jqm.datacolumn', model: {index: 3, text: '数据列3'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '标题',
                isUserProperty: true,
                default: '数据分类'
            }, {
                name: 'columns',
                type: 'select',
                displayName: '列数',
                isUserProperty: true,
                source: W.data.getIntegerRanges(1, 3),
                default: '3'
            }, {
                name: 'target',
                type: 'dialog_select',
                displayName: '链接',
                triggerButton: '选择页面...',
                dialog: 'W.dialog.workbench.SelectLinkTargetDialog',
                isUserProperty: true,
                default: ''
            }, {
                name: 'is_only_show_product_name',
                type: 'boolean',
                displayName: '名字模式?',
                isUserProperty: true,
                default: 'no'
            }]
        }, {
            group: '选项集',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
        items: function($node, model, value) {
            var index = 1;
            var orderedCids = value;
            _.each(orderedCids, function(cid) {
                W.component.CID2COMPONENT[cid].model.set('index', index++, {silent: true});
            });

            var task = new W.DelayedTask(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this);
            task.delay(100);
        },
        text: function($node, model, value) {
            $node.find('.xui-inner-categoryTitle-text').text(value);
        },
        columns: function($node, model, value) {
            var columnCount = parseInt(value);
            var originalColumnCount = this.components.length;
            if (originalColumnCount == columnCount) {
                return;
            } else if (originalColumnCount > columnCount) {
                //缩减
                this.components = this.components.slice(0, columnCount);
            } else {
                //增加
                var addedCount = columnCount - originalColumnCount;
                for (var i = 0; i < addedCount; ++i) {
                    var container = new W.component.jqm.DataColumn();
                    this.addComponent(container);
                }
            }

            W.Broadcaster.trigger('designpage:refresh');
        },
        is_only_show_product_name: function($node, model, value) {
            W.Broadcaster.trigger('designpage:refresh');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});