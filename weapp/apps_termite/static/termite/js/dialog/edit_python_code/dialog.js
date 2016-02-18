/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.workbench.EditPythonDialog');
W.dialog.workbench.EditPythonDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'keypress #editPythonDialog_codeEditor': 'onCodeEditorKeypress'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#edit-python-code-dialog-tmpl-src').template('edit-python-code-dialog-tmpl');
        return "edit-python-code-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.$codeContainer = this.$dialog.find('textarea');
        this.codeEditor = ace.edit("editPythonDialog_codeEditor");
        this.codeEditor.setTheme("ace/theme/monokai");
        this.codeEditor.getSession().setMode("ace/mode/python");
    },

    beforeShow: function(options) {
        this.codeEditor.setValue(options.code);
    },

    onShow: function(options) {
        var task = new W.DelayedTask(function() {
            this.codeEditor.focus();
        }, this);
        task.delay(500);
    },

    onGetData: function() {
        return this.codeEditor.getValue().trim();
    },

    /**
     * onCodeEditorKeypress: 在code editor中按下键盘的响应函数
     */
    onCodeEditorKeypress: function(event) {
        if (event.ctrlKey && event.which === 115) {
            event.preventDefault();
            event.stopPropagation();

            this.onClickSubmitButton();
        }    
    }
});