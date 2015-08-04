/**
 * @class W.component.viper.RichTextEditor
 * 
 */

 W.data.viper.RichTextEditorTypes = [
    {name: 'Full', value: 'full'},
    {name: 'Text', value: 'text'},
    {name: 'RichText', value: 'richtext'}
];

W.component.viper.RichTextEditor = W.component.Component.extend({
	type: 'viper.richtext_editor',
	propertyViewTitle: '富文本编辑器',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'label',
                type: 'text',
                displayName: 'Label',
                default: 'Label'
            }, {
                name: 'type',
                type: 'select',
                displayName: '类型',
                source: W.data.viper.RichTextEditorTypes,
                default: 'full'
            }, {
                name: 'height',
                type: 'text',
                displayName: '高度',
                default: '200'
            }]
        }, {
            group: 'Validate',
            fields: [{
                name: 'validate',
                type: 'textarea',
                displayName: '校验规则',
                default: 'data-validate="required"\ndata-validate-max-length="10240"'
            }]
        }
    ],

    propertyChangeHandlers: {
        label: function($node, model, value) {
            $node.find('label').text(value+"：");
        },
        name: function($node, model, value) {
            $node.find('.errorHint').text('name="'+model.get('name')+'"');
        },
        type: function($node, model, value) {
            $node.find('.x-richtexteditor_image').hide();
            $node.find('.x-richtexteditor_'+value).show();

            W.Broadcaster.trigger('component:resize', this);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '富文本编辑器',
        imgClass: 'componentList_component_html'
    }
});