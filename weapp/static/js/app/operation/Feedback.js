/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

W.AddFeedbackDialog = W.Dialog.extend({
    SUBMIT_SUCCESS_EVENT: 'problem_submit',

    events: _.extend({
        'click .tx_cancel': 'close',
        'click .tx_submit': 'onSubmit'
    }, W.Dialog.prototype.events),

    getTemplate: function() {
        $('#edit-problem-dialog-src').template('edit-problem-dialog-tmpl');
        return 'edit-problem-dialog-tmpl';
    },

    initializeDialog: function() {
        this.render();
        this.$editEl = $('#editorView-editProblemDialog');
        this.editor_title = new W.common.RichTextEditor({
            el: '#title',
            type: 'text',
            height: 60,
            width:360,
            maxCount: 600
        });

        this.editor_title.render();
    },

    renderDialog: function() {
        var html = $.tmpl(this.getTemplate(), {state :this.state});
        this.$contentEl.html(html);
    },

    showDialog: function(options) {
        this.title = options.title;
        this.menu = options.menu;
        this.state = options.state;

        if(this.state =='create'){
            this.$('.tx_submit').html('添加');
        }else{
            this.$('.tx_submit').html('修改');
        }

        this.$('.errorHint').hide();
        /*$("#title").val(this.menus.get('title'));
        $('#right_feedback').val(this.menus.get('right_feedback'));
*//*
        this.editor_title.setContent(this.menus.get('title'));
        this.editor_right_feedback.setContent(this.menus.get('right_feedback'));*/

    },

    onSubmit: function() {
        if (!W.validate($('#editorView-editProblemDialog'))) {
            return;
        }

        //this.menu.set('title', $.trim(this.editor_title.getHtmlContent()));
        //this.menu.set('right_feedback', $.trim(this.editor_right_feedback.getHtmlContent()));
        

        this.trigger('submit', {
            title:$.trim(this.editor_title.getHtmlContent()),
        });
    },

    afterClose: function() {
        this.unbind();
        this.editor_title.setContent('');
        //this.editor_error_feedback.setContent('');
    }
});


/**
 * 获得getEditSiteDialog的单例实例
 * @param {Number} width - 宽度
 * @param {Number} height - 高度
 */
W.getFeedbackDialog = function(options) {
    var dialog = W.registry['AddFeedbackDialog'];
    if (!options) {
        options = {};
    }
    options.width = options.width || 500;
    options.height = options.height || 360;

    if (!dialog) {
        //创建dialog
        xlog('create W.AddFeedbackDialog');
        dialog = new W.AddFeedbackDialog(options);
        W.registry['AddFeedbackDialog'] = dialog;
    }
    return dialog;
};