/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 修改会员标签
 * 
 * author: bert
 */
ensureNS('W.view.member');
W.view.member.MemberUpdateIntegralView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#member-update-integral-dialog-tmpl-src').template('member-update-integral-dialog-tmpl');
        return "member-update-integral-dialog-tmpl";
    },
    
    getIntegralTemplate: function() {
        $('#integral-tmpl-src').template('integral-tmpl');
        return "integral-tmpl";
    },

    getGradeTemplate: function() {
        $('#grade-tmpl-src').template('grade-tmpl');
        return "grade-tmpl";
    },
    
    events:{
        'click .xa-submit': 'onClickSubmit'
    },

    initializePrivate: function(options) {
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
        this.getIntegralTemplate = this.getIntegralTemplate();
    },
    
    onClickSubmit: function(event) {
        if (!W.validate($("#member-update-integral-dialog-tmpl-src"))) {
                return false;
            }
        var integral = $("#integral").val();
        var reason = $("#reason").val();
        var $el = $(event.currentTarget);
        this.submitSendApi(this.memberId, integral, reason)
    },

    submitSendApi: function(memberId, integral, reason){
        this.hide()
        var _this = this;
        W.getApi().call({
            app: 'member',
            api: 'integral/update',
            scope: this,
            method: 'post',
            args: {
                member_id: memberId,
                integral: integral,
                reason: reason
                },
            success: function(data) {
                //window.location.reload();
                if (_this.dataView){
                    _this.dataView.reload();
                }else{
                    window.location.reload();
                }
                
            },
            error: function(resp) {
            }
        });
    },
    


    render: function() {
        this.$content.html($.tmpl(this.getTemplate()));
    },

    onShow: function(options) {
    },
    
    showPrivate: function(options) {
        this.memberId = options.memberId;
        this.dataView = options.dataView;
    },
});

W.getMemberIntegralUpdateView = function(options) {
    var dialog = W.registry['W.view.member.MemberUpdateIntegralView'];
    if (!dialog) {
        //创建dialog
        xlog('create W.view.member.MemberUpdateIntegralView');
        dialog = new W.view.member.MemberUpdateIntegralView(options);
        W.registry['W.view.member.MemberUpdateIntegralView'] = dialog;
    }
    return dialog;
};