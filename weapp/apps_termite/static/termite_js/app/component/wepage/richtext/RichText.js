/**
 * @class W.component.wepage.RichText
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.RichText = W.component.Component.extend({
    type: 'wepage.richtext',
    propertyViewTitle: '富文本',
    properties: [{
        group: '属性1',
        fields: [{
            name: 'content',
            type: 'rich_text',
            isUserProperty: true,
            dialogParameter: 'W.component.wepage.RichText.getComponentContent',
            triggerButton: '编辑内容...',
            dialog: 'W.dialog.workbench.EditRichTextDialog',
            default: ''
        }]
    }],
    propertyChangeHandlers: {
        content: function($node, model, value) {
            value = this.getDisplayValue(value, 'content');
            xwarn(value);
            if (!value) {
                value = '<div><h2 class="wui-h2">点击编辑[富文本]内容</h2>'
                        + '<div class="">1.您可以在这里进行文字编辑（<b>加粗</b>、<em>斜体</em>、<sapn calss="wui-underline" style="text-decoration: underline;">下划线</sapn>、<span class="wui-line-through">删除线</span>、<span class="wui-color">文字颜色</span>、<span class="wui-bgColor">背景色</span>、以及<span class="wui-size">字号大小</span>等）操作。</div>'
                        + '<div class="mt20">2. 您可以在这里加入表格并对此编辑。'
                        + '    <table class="wui-table">'
                        + '        <tr>'
                        + '            <td>标题</td><td>标题</td><td>标题</td>'
                        + '        </tr>'
                        + '        <tr>'
                        + '            <td>内容</td><td>内容</td><td>内容</td>'
                        + '        </tr>'
                        + '    </table>'
                        + '</div>'
                        + '<div class=""><p>您可以在这里添加图片，建议图片最大宽度480px - 600px之间，最大高度960px</p></div></div>';
            };
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

W.component.wepage.RichText.getComponentContent = function(component) {
    return {
        'content': component.model.get('content')
    };
}
