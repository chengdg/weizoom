/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.member.tag');
W.dialog.member.tag.TextareDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#textarea-dialog-tmpl-src').template('textarea-dialog-tmpl');
        return "textarea-dialog-tmpl";
    },

    /*getOneNewsTemplate: function() {
        $('#weixin-select-material-dialog-one-news-tmpl-src').template('weixin-select-material-dialog-one-news-tmpl');
        return 'weixin-select-material-dialog-one-news-tmpl-src';
    },*/

    onInitialize: function(options) {
        //创建文本消息
        this.textMessage = W.model.weixin.Message.createTextMessage();
        this.textMessage.set('text', answer);
       //创建富文本编辑器
        this.editor = new W.view.common.RichTextEditor({
            el: 'textarea',
            type: 'text',
            maxCount: 50000,
            wordCount: false,
            width: '630' 
        });
        this.editor.bind('contentchange', function() {
            this.textMessage.set('text', this.editor.getHtmlContent());
        }, this);
        this.editor.setContent(this.answer);
        this.editor.render();
    

    },
     render: function(){
        return this;
    },
    onShow: function(options) {
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var data = [];
        data = $('[name=answer]').val();
        
        return data;
    },
    /**
     * showTextMessage: 显示文本消息
     */
    showTextMessage: function() {
        if (this.patternMessage) {
            this.patternsContainer.focus();
        }
    },
});