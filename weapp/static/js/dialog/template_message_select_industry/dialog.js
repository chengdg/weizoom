/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 模板消息选择行业对话框
 */
ensureNS('W.weapp.dialog.SelectIndustryDialog');
W.weapp.dialog.SelectIndustryDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click li a': 'onChangeMenuItem',
        'click .btn-cancel': 'onClickCancel'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#template-message-select-industry-dialog-tmpl-src').template('template-message-select-industry-dialog-tmpl');
        return "template-message-select-industry-dialog-tmpl";
    },

    onInitialize: function(options) {
    },
    
    makeOptions: function(options) {
        var buf = [];
        buf.push('<option value=""></option>');
        var length = options.length;
        for (var i = 0; i < length; ++i) {
            var option = options[i];
            buf.push('<option text="' + option.name + '" value="' + option.type + '">' + option.name + '</option>');
        }

        return $(buf.join(''));
    },

    onShow: function(options) {
        var task = new W.DelayedTask(function() {
            this.$dialog.find('input[type="text"]').eq(0).focus();    
        }, this);
        task.delay(300);
        
        W.getApi().call({
            app: 'market_tools/template_message',
            api: 'industry/get',
            scope: this,
            success: function(data) {
                var $node = this.makeOptions(data.items);
                this.$dialog.find('select').empty().append($node);
                //设置下拉列表初始状态
                this.$dialog.find('.xa-major').find('option[text="' + $('.major').html() + '"]').attr("selected",true);
                this.$dialog.find('.xa-deputy').find("option[text='" + $('.deputy').html() + "']").attr("selected",true);
            },
            error: function(resp) {
                alert('获取账号失败');
            }
        });
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
    	var $major = this.$dialog.find('.xa-major');
        var major = $.trim($major.find("option:selected").text());
        if (major.length == 0) {
            alert('请选择主营行业');
            return false;
        }
    	var $deputy = this.$dialog.find('.xa-deputy');
    	var deputy = $.trim($deputy.find("option:selected").text());
    	if (major === deputy) {
    		alert('主营行业与副营行业不能相同');
    		return false;
    	}
        data = {
            'major_type': $major.val(),
            'deputy_type': $deputy.val()
        }
        return data;
    },
    
	/**
     * onClickCancel: 点击“取消”按钮后的响应函数
     */
    onClickCancel: function(event) {
    	this.$dialog.modal('hide');
    },
});