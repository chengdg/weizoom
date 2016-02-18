/**
 * @class W.component.viper.Table
 * 
 */
W.component.viper.Table = W.component.Component.extend({
	type: 'viper.table',
	propertyViewTitle: '表格',

    dynamicComponentTypes: [
        {type: 'viper.table_column', model: {index: 1, text: '列1', field_target: ''}},
        {type: 'viper.table_column', model: {index: 2, text: '列2', field_target: ''}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'title',
                type: 'text',
                displayName: '标题',
                default: '列表'
            }, {
                name: 'is_list_item_sortable',
                type: 'boolean',
                displayName: '可排序?',
                default: 'yes'
            }, {
                name: 'is_list_item_order_by_asc',
                type: 'boolean',
                displayName: '顺序显示?',
                default: 'no'
            }, {
                name: 'is_enable_paginate',
                type: 'boolean',
                displayName: '分页?',
                default: 'no'
            }, {
                name: 'count_per_page',
                type: 'text',
                displayName: '每页数量',
                default: '20'
            }, {
                name: 'is_enable_add_button',
                type: 'boolean',
                displayName: '添加?',
                default: 'yes'
            }, {
                name: 'target',
                type: 'select',
                displayName: '链接',
                source: W.data.getWorkbenchPages,
                default: ''
            }, {
                name: 'target_entity_name',
                type: 'hidden',
                displayName: '',
                default: '',
            }, {
                name: 'target_fields',
                type: 'hidden',
                displayName: '',
                default: '',
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
            this.propertyChangeHandlers['target_fields'].call(this, $node, model, 'update');

            var task = new W.DelayedTask(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this);
            task.delay(100);
        },
        title: function($node, model, value) {
            $node.find('.breadcrumb li.active').text(value);
        },
        is_enable_add_button: function($node, model, value) {
            if (value === 'yes') {
                $node.find('.breadcrumRightButton').show();
            } else {
                $node.find('.breadcrumRightButton').hide();
            }
        },
        is_list_item_sortable: function($node, model, value) {
            W.Broadcaster.trigger('designpage:refresh');
        },
        is_enable_paginate: function($node, model, value) {
            W.Broadcaster.trigger('designpage:refresh');
        },
        target: function($node, model, value) {
            var pageCid = value.split('-')[1];
            if (!pageCid || pageCid[0] === '$') {
                return;
            }

            var page = W.data.pageManager.getPageByCid(pageCid);
            var entityName = page.model.get('entityName');
            model.set('title', entityName+'列表');
            model.set('target_entity_name', entityName);

            $('#propertyView').find('[data-field="title"]').val(entityName+'列表');
        },
        target_entity_name: function($node, model, value) {
            $node.find('.breadcrumRightButton .btn-primary').text('添加'+value);
        },
        target_fields: function($node, model, value) {
            xlog('[table] enter target_fields...');
            var fields = [];
            for (var i = 0; i < this.components.length; ++i) {
                fields.push('');
            }
            _.each(this.components, function(sub_component) {
                var sub_component_model = sub_component.model;
                var field_target = sub_component_model.get('field_target');
                var field_type = 'text';
                if (sub_component_model.get('is_link') === 'yes') {
                    field_type = 'link'
                }
                fields[sub_component_model.get('index')-1] = (field_target + ':' + field_type);
            });
            
            model.set('target_fields', fields.join(','), {silent:true});
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
        //trigger component fill target_fields
        if (!this.model.get('target_fields')) {
            this.model.set('target_fields', 'init');
        }
    }
}, {
    indicator: {
        name: '表格',
        imgClass: 'componentList_component_grid'
    }
});