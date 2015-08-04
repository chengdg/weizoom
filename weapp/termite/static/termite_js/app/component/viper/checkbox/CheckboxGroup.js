/**
 * @class W.component.viper.CheckboxGroup
 * 
 */

W.component.viper.CheckboxGroup = W.component.Component.extend({
	type: 'viper.checkbox_group',
	propertyViewTitle: 'Checkbox Group',

    dynamicComponentTypes: [
        {type: 'viper.checkbox_button', model: {name: '', text: '选项', value: ''}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: 'Label'
            }, {
                name: 'datasource_page',
                type: 'select',
                displayName: '数据Page',
                source: W.data.getWorkbenchPages,
                default: '#'
            }, {
                name: 'datasource_field',
                type: 'select',
                displayName: '数据Field',
                source: function(component) {
                    var pageCid = component.model.get('datasource_page').split('-')[1];
                    if (pageCid) {
                        var fields = W.data.getWorkbenchPageFields(pageCid);
                        return fields;
                    } else {
                        return []
                    }
                },
                default: '#'
            }, {
                name: 'is_filter_in_list_page',
                type: 'boolean',
                displayName: 'List过滤?',
                default: 'yes'
            }]
        }, {
            group: '选项集',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
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
        label: function($node, model, value) {
            $node.find('label.control-label').text(value+"：");
        },
        datasource_page: function($node, model, value) {
            var pageCid = value.split('-')[1];
            if (pageCid) {
                var fields = W.data.getWorkbenchPageFields(pageCid);
                var $datasourceField = $('select[name="datasource_field"]').eq(0);
                var items = [];
                _.each(fields, function(field) {
                    items.push('<option value="' + field.value + '">' + field.name + '</option>');
                });
                $datasourceField.html(items.join('')).val('#');
            }
            $node.find('.errorHint').text('datasource_page="'+value+'", datasource_field="' + model.get('datasource_field') +'"');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Checkbox',
        imgClass: 'componentList_component_checkbox'
    }
});