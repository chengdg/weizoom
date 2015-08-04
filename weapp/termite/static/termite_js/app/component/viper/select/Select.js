/**
 * @class W.component.viper.SelectMenu
 * 
 */
W.component.viper.SelectMenu = W.component.Component.extend({
	type: 'viper.select_menu',
	propertyViewTitle: '下拉选框',

    dynamicComponentTypes: [
        {type: 'viper.select_menu_item', model: {index:1, text: '选项', value: 'value'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: 'Label'
            }]
        }, {
            group: 'Validate',
            fields: [{
                name: 'validate',
                type: 'textarea',
                displayName: '校验规则',
                default: 'data-validate="require-select-valid-option"'
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
            $node.find('label').text(value+"：");

            W.Broadcaster.trigger('component:resize', this);
        },

        name: function($node, model, value) {
            $node.find('.errorHint').text('name="'+model.get('name')+'"');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '下拉选框',
        imgClass: 'componentList_component_select_menu'
    }
});
