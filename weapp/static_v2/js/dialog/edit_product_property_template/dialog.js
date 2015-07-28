/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择轮播图的对话框
 *
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.EditProductPropertyDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-edit-product-property-template-dialog-tmpl-src').template('mall-edit-product-property-template-dialog-tmpl');
        return "mall-edit-product-property-template-dialog-tmpl";
    },

    getTableTemplate: function() {
        $('#mall-edit-product-property-template-dialog-table-tmpl-src').template('mall-edit-product-property-template-dialog-table-tmpl');
        return "mall-edit-product-property-template-dialog-table-tmpl";
    },

    getRowTemplate: function() {
        $('#mall-edit-product-property-template-dialog-table-row-tmpl-src').template('mall-edit-product-property-template-dialog-table-row-tmpl');
        return "mall-edit-product-property-template-dialog-table-row-tmpl";
    },

    events: _.extend({
        'click .xa-add': 'onClickAddButton',
        'click .xa-delete': 'onClickDeleteButton',
        'blur .xa-contenteditable': 'onLeaveEditableCell',
        'focus .xa-contenteditable': 'onClickEditableCell',
        'click .xa-btn-save': 'onClickButtonSave',
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.tableTemplate = this.getTableTemplate();
        this.rowTemplate = this.getRowTemplate();
        this.deletedIds = [];
        var $input = this.$dialog.find('.wui-titleInput'); // Input at top
        $input.attr("placeholder", "请在此处输入属性模板名称");
        $input.attr("maxlength", '18');
        $input.attr("data-validate", "require-string");
        $input.after("<label class='errorHint' data-error-hint='请输入18位以内的字符， 且不为空'></label>");
    },

    onPressKeyInQueryInput: function(event) {
        var keyCode = event.keyCode;
        if (keyCode == 13) {
            xlog('search');
            this.search();
        }
    },

    onClickAddButton: function(event) {
        var id = 0-this.$('tr').length;
        var $node = $.tmpl(this.rowTemplate, {id:id});
        $node.insertBefore(this.$('.xa-addActionRow'));
    },

    onClickDeleteButton: function(event) {
        var $tr = $(event.target).parents('tr');
        $tr.remove();
        this.deletedIds.push($tr.data('propertyId'));
    },

    onLeaveEditableCell: function(event) {
        var $td = $(event.target);
        var content = $.trim($td.text());
        $td.val(content);
        var oldContent = $td.data('oldContent');
        if (content !== oldContent) {
            $td.addClass('xui-dirtyContent');
            $td.attr("value", content);
        }
    },

    onClickEditableCell: function(event) {
        var $td = $(event.target);
        var content = $.trim($td.text());
        if (content === '点击添加') {
            $td.text('');
        }
    },

    onClickButtonSave: function(event){
        $div = $(event.currentTarget).parents('.modal-content');
        $td_set = $div.find('.xa-contenteditable');
        $td_set.each(function(index){
            $(this).val($(this).attr('value'));
        });
    },

    onShow: function(options) {

        this.reset();
        W.validate.toggleErrorHint($('.modal-content'), true);
        $('.xa-titleInput').parent().removeClass('has-error');
        this.$('.xa-propertyTable').empty();
        this.templateId = options.templateId || -1;
    },

    afterShow: function(options) {
        this.$dialog.find('input[type="text"]').eq(0).focus();

        W.getApi().call({
            app: 'mall2',
            resource: 'property_list',
            args: {
                id: this.templateId
            },
            scope: this,
            success: function(data) {
                var $node = $.tmpl(this.tableTemplate, {'properties': data});
                this.$('.xa-propertyTable').empty().append($node);
            },
            error: function(resp) {

            }
        });
    },

    onGetData: function(event) {
        var hasError=false;
        hasError = (!W.validate($('#mallEditProductPropertyTemplateDialog input')));
        $('#mallEditProductPropertyTemplateDialog [contenteditable]').each(function(i,n){
            if(!W.validate($(n))){
                hasError=true
                $(n).css('border-color', '#cc0000');
                W.getErrorHintView().show($(n).attr('errorhint-value'));
            }
        })
        if(hasError){
            return;
        }
        var title = this.getDialogTitle();
        var newProperties = [];
        var updateProperties = [];
        this.$('tbody tr').each(function() {
            var $tr = $(this);
            var $name = $tr.find('.xa-name');
            var $value = $tr.find('.xa-value');
            var propertyId = $tr.data('propertyId');
            if (!propertyId) {
                return;
            }

            propertyId = parseInt(propertyId);
            var target = null;
            if (propertyId < 0) {
                //新数据
                target = newProperties;
            } else {
                if ($tr.find('.xui-dirtyContent').length > 0) {
                    //被编辑过的数据
                    target = updateProperties;
                }
            }
            if (target) {
                target.push({
                    id: propertyId,
                    name: $.trim($name.text()),
                    value: $.trim($value.text())
                })
            }
        })
        return {
            "title": title,
            "newProperties": newProperties,
            "updateProperties": updateProperties,
            "deletedIds": this.deletedIds
        };
    },
});
