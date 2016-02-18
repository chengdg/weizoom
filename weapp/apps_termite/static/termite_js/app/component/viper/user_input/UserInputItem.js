/**
 * @class W.component.viper.UserInputItem
 * 
 */
W.component.viper.UserInputItem = W.component.Component.extend({
	type: 'viper.user_input_item',
    selectable: 'no',
	propertyViewTitle: '用户输入项',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'is_mandatory',
                type: 'boolean',
                displayName: '必填?',
                default: 'yes'
            }, {
                name: 'text',
                type: 'text',
                displayName: '标题',
                default: '输入项'
            }, {
                name: 'type',
                type: 'select',
                displayName: '输入类型',
                source: [{name:"输入框", value:'text'}, {name:"单选框", value:'radio'}, {name:"复选框", value:'checkbox'}, {name:"上传图片", value:'image'}],
                default: 'text'
            }/*, {
                name: 'value',
                type: 'text',
                displayName: '初始数据',
                placeholder: '请输入文本框的输入提示',
                default: ''
            }*/]
        }
    ],

    propertyChangeHandlers: {
        type: function($node, model, value, $propertyViewNode) {
            $node.find('label').text(value+"：");

            W.Broadcaster.trigger('component:resize', this);
        }
    }
});
