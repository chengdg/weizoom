/**
 * @class W.component.viper.UserInput
 * 
 */
W.component.viper.UserInput = W.component.Component.extend({
	type: 'viper.user_input',
	propertyViewTitle: '用户输入项目',

    dynamicComponentTypes: [
        {type: 'viper.user_input_item', model: {is_mandatory:'yes', text:'姓名', type:'input', value:''}},
        {type: 'viper.user_input_item', model: {is_mandatory:'yes', text:'手机号', type:'input', value:''}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: '用户输入项'
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
    }
}, {
    indicator: {
        name: '用户输入项',
        imgClass: 'componentList_component_text_input'
    }
});
