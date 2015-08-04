/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 通知提示框
 * 
 * author: herry
 */
ensureNS('W.weapp.dialog');
W.weapp.dialog.ManageNoticeDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#manager-notice-dialog-tmpl-src').template('manager-notice-dialog-tmpl');
        return "manager-notice-dialog-tmpl";
    },

    events: _.extend({
        'click .show-notice-detail': 'onClickShowNoticeDetailOne',
        'click .btn-danger': 'onClickDelete',
    }, W.dialog.Dialog.prototype.events),


    makeCheckboxes: function(options) {
        //显示所有的通知内容
        options = options.notices;
        
        var buf = [];
        var length = options.length;
        for (var i = 0; i < length; ++i) {
            if(!options[i]['has_read']){
                var strTemplate = '<tr class="'+options[i]['id']+'success" >'+'<td  width="25%" style="background-color:yellow">'+options[i]['create_time']+'</td>'+'<td style="background-color:yellow" class="show-notice-detail" '+'id='+'"'+options[i]['id']+'"'+'width="50%"><font color="green">'+options[i]['title']+'</font></td>'+'<td style="background-color:yellow" width="12%"><button id="'+options[i]['id']+'" class="btn btn-danger">删除</button></td>'+'</tr>'+'<tr class="hide new-notice-detail" id="'+options[i]['id']+'hide-notice-detail">'+'<td></td>'+'<td>'+options[i]['content']+'</td>'+'<td></td>'+'</tr>';
            }else{
                var strTemplate = '<tr class="'+options[i]['id']+'success" >'+'<td width="25%" >'+options[i]['create_time']+'</td>'+'<td class="show-notice-detail" '+'id='+'"'+options[i]['id']+'"'+'width="50%"><font color="green">'+options[i]['title']+'</font></td>'+'<td width="12%"><button id="'+options[i]['id']+'" class="btn btn-danger">删除</button></td>'+'</tr>'+'<tr class="hide new-notice-detail" id="'+options[i]['id']+'hide-notice-detail">'+'<td></td>'+'<td>'+options[i]['content']+'</td>'+'<td></td>'+'</tr>';
            }
                buf.push(strTemplate);
        }
        return $(buf.join(''));
    },


    onClickShowNoticeDetailOne: function(event) {
        //显示单条通知的详细信息
        var $link = $(event.currentTarget);

        if(!$link.parent().next().is(":visible")){

        var noticeId = $link.attr('id');
        $link.parent().parent().find('.new-notice-detail').hide(); 
        var thisOne = $link.parent().next().show();
        $link.parent().children().css('background-color','white');
        W.getApi().call({
             app: 'notice',
             api: 'notice/create_read',
             args: {'notice_id':noticeId},
             scope: this,
             success: function(data) {
                console.log("success");
                console.log('\n\n\n\n');
             },
             error: function(resp) {
                console.log('获得通知失败');
             }
         });  

        }else{
            $link.parent().parent().find('.new-notice-detail').hide(); 
        }

    },

    onInitialize: function(options) {
        console.log("onInitialize");
    },

    beforeShow: function() {
        console.log("beforeShow");
    },

    onShow: function(options){
        console.log(this);

        console.log("onShow start");
        this.$dialog.find('#showNoticeDetail-List').empty();

        W.getApi().call({
             app: 'notice',
             api: 'notice/get',
             args: {},
             scope: this,
             success: function(data) {
                var judge = false;
                try{
                    judge = data.notices[0]['id'];
                }catch(e){
                    console.log(e);
                }

                if(judge){
                    var $dialogBody = this.$dialog.find('#showNoticeDetail-List').append(this.makeCheckboxes(data));
                }else{
                    var $dialogBody = this.$dialog.find('#showNoticeDetail-List').append('<tr><td style="text-align:center;color:gray;">空</td></tr>');
                }

             },
             error: function(resp) {
                 alert('获得通知列表失败');
             }
         });
        console.log("onShow end");
    },

    afterShow: function(options) {
        console.log("afterShow");
    },

    onClickDelete:function(event){
        //删除通知
        currentThis  = this;

        var $link = $(event.currentTarget);
        var noticeId = $link.attr('id');

        var $el = $(event.currentTarget);
        var deleteCommentView = W.getItemDeleteView();
        deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){

            W.getApi().call({
                app: 'notice',
                api: 'notice/delete',
                args: {'notice_id':noticeId},
                scope: this,
                success: function(data) {
                   this.close();
                   currentThis.onShow();
                   console.log("删除通知成功。");
                },
                error: function(resp) {
                   console.log('删除通知失败!');
                }
            });  
        });
        deleteCommentView.show({
            $action: $el,
            info: '确定删除通知吗?'
        });
    },


});





