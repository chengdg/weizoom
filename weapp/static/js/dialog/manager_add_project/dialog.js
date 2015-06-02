/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.weapp.dialog.AddProjectDialog');
W.weapp.dialog.AddProjectDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'change select': 'onChangeProjectType',
        'click input[type="radio"]': 'onClickRawTypeProject'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#manager-add-project-dialog-tmpl-src').template('manager-add-project-dialog-tmpl');
        return "manager-add-project-dialog-tmpl";
    },

    makeRadios: function(options) {
        var buf = [];
        var length = options.length;
        for (var i = 0; i < length; ++i) {
            var option = options[i];
            buf.push('<label class="radio"><input name="category" type="radio" value="' + option.value + '"/>' + option.text + "</label>");
        }

        return $(buf.join(''));
    },

    onInitialize: function(options) {
    },

    onShow: function(options) {
        var task = new W.DelayedTask(function() {
            this.$dialog.find('input[type="text"]').eq(0).focus();    
        }, this);
        task.delay(300);        

        W.getApi().call({
            app: 'webapp',
            api: 'raw_mobile_projects/get',
            scope: this,
            args: {
                workspace_id: options.workspaceId
            },
            success: function(data) {
                var $node = this.makeRadios(data);
                this.$dialog.find('.x-rawProjects').empty().append($node);
            },
            error: function(resp) {
                alert('获取原生项目失败');
            }
        });
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var projectName = $.trim(this.$dialog.find('input[name="projectName"]').val());
        if (projectName.length == 0) {
            alert('请输入项目名称');
            return false;
        }

        var projectType = this.$dialog.find('select[name="projectType"]').val();
        if (projectType === 'unknown') {
            alert('请选择项目类型');
            return false;
        }

        var innerName = $.trim(this.$dialog.find('input[name="innerName"]').val());
        if (innerName.length == 0) {
            alert('请输入内部名');
            return false;
        }

        $('input[name="projectName"]').val('');
        $('input[name="innerName"]').val('');

        data = {
            'name': projectName,
            'innerName': innerName,
            'type': projectType
        }
        return data;
    },

    /**
     * onChangeProjectType: 切换项目类型的响应函数
     */
    onChangeProjectType: function(event) {
        var $select = $(event.currentTarget);
        var type = $select.val();
        if (type === 'raw') {
            this.$dialog.find('.x-rawProjects').show();
        } else {
            this.$dialog.find('.x-rawProjects').hide();
        }
    },

    /**
     * onClickRawTypeProject: 点击项目radio的响应函数
     */
    onClickRawTypeProject: function(event) {
        var $radio = $(event.currentTarget);
        var projectName = $radio.val();
        var items = projectName.split('_');
        var innerName = items[items.length-1];
        this.$dialog.find('input[name="innerName"]').val(innerName);
    }
});