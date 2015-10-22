/**
 * 微信公众号重新授权对话框
 */
ensureNS('W.dialog.weixin');
W.dialog.weixin.MpuserRehitDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .btn-success': 'onClickSubmitButton'
    }, W.dialog.Dialog.prototype.events),

    templates: {
        dialogTmpl: '#weixin-mpuser-rehit-dialog-tmpl-src'
    },

    onInitialize: function(options) {
    },

    beforeShow: function() {
    },

    onShow: function(options) {
    },

    afterShow: function(options) {
    },

    onGetData: function(event) {
        return null;
    },
    onClickSubmitButton: function(event) {
        var data = this.onGetData(event);

        if (!data) {
            this.$dialog.modal('hide');
            console.log(this.successCallback);
            if (this.successCallback) {
                //调用success callback
                var _this = this;
                var task = new W.DelayedTask(function() {
                    _this.successCallback(data);
                    _this.successCallback = null;
                });
              
                task.delay(100);
            }
        }
    }
});