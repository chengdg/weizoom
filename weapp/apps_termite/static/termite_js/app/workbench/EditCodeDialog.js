/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 编辑javascript代码的对话框
 */
W.workbench.EditCodeDialog = Backbone.View.extend({
    events: {
        'click .editCodeDialog_submitBtn': 'onClickSubmitButton',
    },

    getTemplate: function() {
        $('#edit-code-dialog-tmpl-src').template('edit-code-dialog-tmpl');
        return "edit-code-dialog-tmpl";
    },

    initialize: function(options) {
        this.$el = $(this.el);

        this.template = this.getTemplate();
        $('body').append($.tmpl(this.template, {}));
        this.el = $('#editCodeDialog')[0];
        this.$el = $(this.el);

        this.$codeContainer = this.$('.editCodeDialog_body textarea');
        //this.$editor = codeEditor_codeEditor
        this.codeEditor = ace.edit("editCodeDialog_codeEditor");
        this.codeEditor.setTheme("ace/theme/monokai");
        this.codeEditor.getSession().setMode("ace/mode/javascript");
        this.successCallback = null;
    },

    render: function() {
    },

    show: function(options) {
        this.successCallback = options.success;
        var $field = options.$button.parents('.propertyGroup_property_input').find('input[type="hidden"]');
        var field = $field.attr('data-field');
        var code = options.component.model.get(field);
        this.codeEditor.setValue(code);
        //this.$codeContainer.val(options.component.model.get(field));
        this.$el.modal('show');

        var task = new W.DelayedTask(function() {
            this.$codeContainer.focus();
        }, this);
        task.delay(500);        
    },

    /**
     * onClickSubmitButton: 点击保存按钮后的响应函数
     */
    onClickSubmitButton: function(event) {
        var code = this.codeEditor.getValue().trim();
        this.$el.modal('hide');

        if (this.successCallback) {
            //调用success callback
            var _this = this;
            var task = new W.DelayedTask(function() {
                _this.successCallback(code);
                _this.successCallback = null;
            });
          
            task.delay(500);            
        }
    }
});