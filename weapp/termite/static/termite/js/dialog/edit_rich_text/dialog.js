/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.workbench.EditRichTextDialog');
W.dialog.workbench.EditRichTextDialog = W.dialog.Dialog.extend({
    events: _.extend({
        //'keypress #editPythonDialog_codeEditor': 'onCodeEditorKeypress'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#edit-richtext-dialog-tmpl-src').template('edit-richtext-dialog-tmpl');
        return "edit-richtext-dialog-tmpl";
    },

    onInitialize: function(options) {
        var $textarea = this.$dialog.find('textarea');
        var width = this.$dialog.find('.modal-body').outerWidth() * 0.79;
        width = 850;
        this.editor = new W.workbench.RichTextEditor({
            el: $textarea.get(),
            type: 'full',
            imgSuffix: "uid="+W.uid,
            width: width,
            height: 300,
            autoHeight: false,
            wordCount: false
        });
        this.editor.render();
        this.editor.setContent(options.content || '');
    },

    beforeShow: function(options) {
        
    },

    onShow: function(options) {
        
    },

    onGetData: function() {
        return this.editor.getContent();
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