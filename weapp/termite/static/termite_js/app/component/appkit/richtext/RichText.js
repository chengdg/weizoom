/**
 * @class W.component.appkit.RichText
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.RichText = W.component.Component.extend({
    type: 'appkit.richtext',
    propertyViewTitle: '富文本',
    properties: [{
        group: '属性1',
        fields: [{
            name: 'content',
            type: 'rich_text',
            displayName: '内容',
            isUserProperty: true,
            dialogParameter: 'W.component.appkit.RichText.getComponentContent',
            triggerButton: '编辑内容...',
            dialog: 'W.dialog.workbench.EditRichTextDialog',
            default: ''
        }]
    }],
    propertyChangeHandlers: {
        content: function($node, model, value) {
            $node.html(value);
            W.Broadcaster.trigger('component:resize', this);
        }
    }
}, {
    indicator: {
        name: '富文本',
        imgClass: 'componentList_component_richtext'
    }
});

W.component.appkit.RichText.getComponentContent = function(component) {
    return {
        'content': component.model.get('content')
    };
}
