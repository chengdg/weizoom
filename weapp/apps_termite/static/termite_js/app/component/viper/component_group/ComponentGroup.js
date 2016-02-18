/**
 * @class W.component.ComponentGroup
 * 
 */
W.component.viper.ComponentGroup = W.component.Component.extend({
	type: 'viper.component_group',
	propertyViewTitle: 'Component Group',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: 'Label'
            }, {
                name: 'is_enbale_add',
                type: 'boolean',
                displayName: '开启增加？',
                default: 'yes'
            }, {
                name: 'count_limit',
                type: 'text',
                displayName: '个数限制',
                help: '0为无限制',
                default: '0'
            }, {
                name: 'entity_name',
                type: 'text',
                displayName: '实体名',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        label: function($node, model, value) {
            $node.find('label').eq(0).text(value+"：");

            W.Broadcaster.trigger('component:resize', this);
        },
        is_enbale_add: function($node, model, value) {
            if (value === 'yes') {
                $node.find('.xui-inner-actionArea').removeClass('xui-hide');
            } else {
                $node.find('.xui-inner-actionArea').addClass('xui-hide');
            }
        },
        count_limit: function($node, model, value) {
            var $countLimit = $node.find('.xui-inner-actionArea .xa-countLimit');
            if ($countLimit.length > 0) {
                if (value === '0') {
                    $countLimit.text('');
                } else {
                    $countLimit.text('(最多'+value+'个)');
                }
            }
        },
        name: function($node, model, value) {
            $node.find('.errorHint').text('name="'+model.get('name')+'"');

            W.Broadcaster.trigger('component:resize', this);
        }
    }
}, {
    indicator: {
        name: '组件集合',
        imgClass: 'componentList_component_textblock'
    }
});