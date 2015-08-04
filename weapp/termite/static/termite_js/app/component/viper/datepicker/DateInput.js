/**
 * @class W.component.viper.DateInput
 * 
 */
W.component.viper.DateInput = W.component.Component.extend({
	type: 'viper.dateinput',
    selectable: 'no',
	propertyViewTitle: 'Date Input',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'name',
                type: 'text',
                displayName: 'Name',
                default: ''
            }, {
                name: 'placeholder',
                type: 'text',
                displayName: 'PlaceHolder',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        placeholder: function($node, model, value) {
            $node.attr('placeholder', value);
        }
    }
});
