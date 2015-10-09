/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 修改会员标签
 *
 * author: bert
 */
ensureNS('W.view.member');
W.view.member.MemberTagsUpdateView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#member-update-tag-dialog-tmpl-src').template('member-update-tag-dialog-tmpl');
        return "member-update-tag-dialog-tmpl";
    },

    getTagsTemplate: function() {
        $('#tags-tmpl-src').template('tags-tmpl');
        return "tags-tmpl";
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
        this.getTagsTemplate = this.getTagsTemplate();
        this.getGradeTemplate = this.getGradeTemplate();
    },

    onClickSubmit: function(event) {
        var $el = $(event.currentTarget);
        this.submitSendApi(this.isUpdateGrade,this.memberId)
    },

    submitSendApi: function(isUpdateGrade, memberId){
        var type = 'grade';
        if (!isUpdateGrade) {
            type = 'tag';
        }
        var check_value = [];
        var tag_values = [];
        $("input[name='tag_id']:checked").each(function () {
            check_value.push(this.value)
            dict = {}
            dict["id"] = this.value;
            dict["value"] = $(this).attr("data-value");
            tag_values.push(dict);

        })
        args  = {checked_ids : check_value.join("_"), type : type, member_id : memberId}
        var _this = this;
        if (this.isPostData){
            W.resource.member.UpdateMemberTagOrGrade.post({
                data: args,
                success: function(data) {
                    //window.location.reload();
                    _this.dataView.reload();
                },
                error: function() {
                }
            });
        } else {
            $(".tag-group").text('');
            tag_values = tag_values.reverse();
            $.each(tag_values, function(index, value) {
                $(".tag-group").prepend('<span class="mr30">'+value["value"]+'</span>' );
                $(".tag-group").prepend('<input name = "tag_id" class="tag_id" id = "tag_id" hidden = "hidden" value="'+value["id"]+'">  ');
            });
        }
    },

    validate: function() {

    },

    getTag: function(options) {
         console.log( options);
        this.isUpdateGrade = options.isUpdateGrade;
        this.memberId = options.memberId;
        this.tagIds = options.tagIds;
        this.isPostData = options.isPostData;
        this.dataView = options.dataView;

        W.resource.member.UpdateMemberTagOrGrade.get({
            scope: this,
            success: function(data) {
                var tags = '';
                if (this.isUpdateGrade){
                    tags = data['grades'];
                    currentTemplate = this.getGradeTemplate;
                } else {
                    tags = data['tags'];
                    for(var i = 0; i < tags.length; i++){
                        if($.inArray(tags[i].id, this.tagIds) > -1){
                            tags[i].in_this_tag = true;
                        }
                    }
                    currentTemplate = this.getTagsTemplate;
                }
                var $tags = $.tmpl(currentTemplate, {
                    'tags': tags,
                });
                $('.xa-drop-box-content .xa-i-content').empty().append($tags);
            },
            error: function(resp) {
            }
        })
    },

    render: function() {
        this.$content.html($.tmpl(this.getTemplate()));
    },

    onShow: function(options) {
    },

    showPrivate: function(options) {
        this.getTag(options);
    },
});


W.getMemberTagsUpdateView = function(options) {
    var dialog = W.registry['W.view.member.MemberTagsUpdateView'];
    if (!dialog) {
        //创建dialog
        xlog('create W.view.member.MemberTagsUpdateView');
        dialog = new W.view.member.MemberTagsUpdateView(options);
        W.registry['W.view.member.MemberTagsUpdateView'] = dialog;
    }
    return dialog;
};