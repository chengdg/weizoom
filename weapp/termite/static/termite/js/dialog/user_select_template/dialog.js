/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.workbench');
W.dialog.workbench.SelectTemplateeDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#user-select-template-dialog-tmpl-src').template('user-select-template-dialog-tmpl');
        return "user-select-template-dialog-tmpl";
    },

    makeRadios: function(templates, targetTemplateProjectId) {
        var buf = [];
        var length = templates.length;
        for (var i = 0; i < length; ++i) {
            var template = templates[i];
            if (template.id === targetTemplateProjectId) {
                buf.push('<label class="radio">' + 
                            '<input type="radio" checked="checked" name="template" data-id="' + template.id + '" value="' + template.innerName + '" />' + template.name +
                        '</label>');
            } else {
                buf.push('<label class="radio">' + 
                            '<input type="radio" name="template" data-id="' + template.id + '" value="' + template.innerName + '" />' + template.name +
                        '</label>');
            }
        }

        return $(buf.join(''));
    },

    onInitialize: function(options) {
    },

    onShow: function(options) {
        W.getApi().call({
            app: 'webapp',
            api: 'project_templates/get',
            args: {
                project_id: W.projectId
            },
            scope: this,
            success: function(data) {
                var templates = data.templates;
                var currentTemplateProjectId = data.currentTemplateProjectId;
                this.$dialog.find('.modal-body').append(this.makeRadios(templates, currentTemplateProjectId));
            },
            error: function(resp) {
                alert('获得模板集合失败！');
            }
        })
    },

    /**
     * onGetData: 获取数据
     */
    onGetData: function(event) {
        var $radio = this.$dialog.find('input[type="radio"]:checked');
        var innerName = $radio.val();
        var id = $radio.attr('data-id');
        this.$dialog.find('.modal-body').empty();

        var data = {
            innerName: innerName,
            id: id
        };
        return data;
    }
});