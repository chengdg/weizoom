/**
 * @class W.component.viper.CheckboxButton
 * 
 */
W.component.viper.CheckboxButton = W.component.Component.extend({
	type: 'viper.checkbox_button',
    selectable: 'no',
	propertyViewTitle: 'Checkbox Button',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'text',
                displayName: 'Label',
                default: '选项'
            }, {
                name: 'name',
                type: 'text',
                displayName: 'Name',
                default: 'name'
            }, {
                name: 'value',
                type: 'text',
                displayName: 'Value',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        text: function($node, model, value, $propertyViewNode) {
            $node.find('span').text(value);

            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
            }

            W.Broadcaster.trigger('component:resize', this);
        },
        name: function($node, model, value, $propertyViewNode) {
            $node.find('.errorHint').text('name='+value);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);

        if (this.model.get('value') === '') {
            this.model.set('value', 'value ' + Date.now(), {silent: true});
        }
    }
});