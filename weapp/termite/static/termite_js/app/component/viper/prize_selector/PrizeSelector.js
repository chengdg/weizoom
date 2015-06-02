/**
 * @class W.component.viper.PrizeSelector
 * 
 */
W.component.viper.PrizeSelector = W.component.Component.extend({
	type: 'viper.prize_selector',
	propertyViewTitle: '奖励',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: 'Label'
            }]
        }
    ],

    propertyChangeHandlers: {
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
        name: '奖励选框',
        imgClass: 'componentList_component_select_menu'
    }
});
