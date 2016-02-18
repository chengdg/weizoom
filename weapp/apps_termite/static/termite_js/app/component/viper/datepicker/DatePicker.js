/**
 * @class W.component.viper.DatePicker
 * 
 */
W.component.viper.DatePicker = W.component.Component.extend({
	type: 'viper.datepicker',
	propertyViewTitle: 'Date Picker',

    dynamicComponentTypes: [
        {type: 'viper.dateinput', model: {placeholder: '开始时间'}},
        {type: 'viper.dateinput', model: {placeholder: '结束时间'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: '选择日期'
            }, {
                name: 'enable_today_as_min_date',
                type: 'boolean',
                displayName: '最小当天?',
                default: 'yes'
            }, {
                name: 'enable_validate',
                type: 'boolean',
                displayName: '必填?',
                default: 'yes'
            }]
        }, {
            group: '输入控件',
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

            _.delay(_.bind(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this), 100);
        },
        label: function($node, model, value) {
            $node.find('label').text(value+"：");

            W.Broadcaster.trigger('component:resize', this);
        },
        input_count: function($node, model, value) {
            W.Broadcaster.trigger('designpage:refresh');
        },
        name: function($node, model, value) {
            $node.find('.errorHint').text('name="'+model.get('name')+'"');

            W.Broadcaster.trigger('component:resize', this);
        }
    }
}, {
    indicator: {
        name: 'Date Picker',
        imgClass: 'componentList_component_datepicker'
    }
});
