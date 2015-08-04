/**
 * @class W.component.viper.TableColumn
 * 
 */
W.component.viper.TableColumn = W.component.Component.extend({
	type: 'viper.table_column',
    selectable: 'no',
	propertyViewTitle: 'Table Column',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: '列名',
                default: '列1'
            }, {
                name: 'width',
                type: 'text',
                displayName: '宽度',
                default: ''
            }, {
                name: 'field_target',
                type: 'select',
                displayName: '实体属性',
                source: W.data.getEntityProperty,
                default: ''
            }, {
                name: 'action',
                type: 'radio',
                displayName: '操作',
                source: [{name:'无', value:'no'}, {name:'可排序', value:'sortable'}, {name:'可过滤', value:'filterable'}, {name:'可搜索', value:'searchable'}],
                default: 'no'
            }, {
                name: 'is_link',
                type: 'boolean',
                displayName: '链接？',
                default: 'no'
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value, $propertyViewNode) {
            $node.text(value);
            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').eq(0).text(value);
            }
        },
        field_target: function($node, model, value, $propertyViewNode) {
            $node.text(model.get('text')+"("+value+")");
            var parentComponent = W.component.getComponent(this.pid);
            parentComponent.model.set('target_fields', 'update');
        },
        is_link: function($node, model, value, $propertyViewNode) {
            var parentComponent = W.component.getComponent(this.pid);
            parentComponent.model.set('target_fields', 'update');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});
