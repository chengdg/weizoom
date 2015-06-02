/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * AdvancedTable: 拥有searchable, column sortable, item sortable功能的高级table
 */
ensureNS('W.view.common');
W.view.common.CodeEditor = Backbone.View.extend({
    el: '',

    events: {
        'keypress #codeEditor_editor': 'onCodeEditorKeypress'
    },

    getTemplate: function() {
    },
    
    initialize: function(options) {
        this.$el = $(this.el);

        this.isCodeLoaded = false;
        this.editorWidth = 0;
        this.codeEditor = null;
        this.functionName = null;
    },

    render: function() {
        this.$el.append('<div id="codeEditor_editor" style="width: 100%; height: 100%;"></div>')
        this.codeEditor = ace.edit("codeEditor_editor");
        this.codeEditor.setTheme("ace/theme/monokai");
        this.codeEditor.getSession().setMode("ace/mode/python");
        this.codeEditor.setValue("#come on baby");

        return;
    },

    setCode: function(functionName, code) {
        this.functionName = functionName;
        this.codeEditor.setValue(code)
    },

    runCode: function() {
        W.getApi().call({
            app: 'example', 
            api: 'code/run',
            method: 'post',
            scope: this,
            args: {
                code: this.codeEditor.getValue().trim()
            },
            success: function(data) {
                this.trigger('code-execute-success', data.result, data.sqls);
            },
            error: function(resp) {
                this.trigger('code-execute-failed', resp.innerErrMsg);
            }
        });
    },

    /**
     * onCodeEditorKeypress: 在code editor中按下键盘的响应函数
     */
    onCodeEditorKeypress: function(event) {
        xlog(event.which);
        if (event.ctrlKey && event.which === 114) {
            event.preventDefault();
            event.stopPropagation();

            this.runCode();
        }    
    }
});