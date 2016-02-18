ensureNS('W.view.weixin');
/**
 * 粉丝列表的View
 */
W.view.weixin.FansView = Backbone.View.extend({
    events: {
        "click .xa-showDialog": "onShowDialog",
        "click .xa-addFanCategory": "onAddFanCategory",
        "click .xa-addCancel": "onCancel",
        "hover .xa-hoverEditor": "onHoverEditor",
        "mouseleave .xa-hoverEditor": "onMouseLeaveHoverHide",
        "blur .xa-hoverEditor": "onBlurLeaveHoverHide",
        "click .xa-editorGroup": "onClickEditorGroup",
        "click .xa-delGroup": "onDeleteFanCategory",
        "click .xa-selectAll": "onClickSelectAll",
        "click .xa-hoverEditor": "onClickLiActive",
        "click .xa-weixin-materialsPage": "onClickOnPage",
        "mouseover .xa-weixin-materialsPage": "onMouseoverPage",
        "click .xa-sendMessageLink": "onClickSendMessageLink",
        "click .xa-sendMessageChosen": "onClickSendMessageChosen",
        "click .xa-sendMessageAll": "onClickSendMessageAll",
        "click .xa-sendMessageAll": "onClickSendMessageAll",
        "mouseover .xa-showUserData": "onMouseoverShowUserData",
        "mouseleave .xa-showUserData": "onMouseleaveShowUserData",
    },

    initialize: function(options) {
        $('.xui-i-addLi').find('.xa-hoverEditor').eq(0).addClass('xui-clickColor');
        flag = 0;
    },

    render: function() {},

    onShowDialog: function() {
        $('.xui-i-groupDialog').show();
        $('.xa-valueAdd').val("").focus();
        $('.data-error-hint').html('');
        // TODO: $roleList ?
        //$roleList.find('input[type="text"]').focus();
    },

    onAddFanCategory: function(event) {
        // 点击添加"确定"
        //xlog("in onAddCategory()");
        var inputVal = $('.xa-valueAdd').val();
        $('.data-error-hint').html("");
        if (!inputVal || inputVal.length < 1) {
            $('.data-error-hint').html("<span>分组名称不能为空</span>");
            //W.getErrorHintView().show("分组名称不能为空");
            return false;
        }
        if (inputVal.length > 6) {
            $('.data-error-hint').html("<span>分组名称为1-6个字</span>");
            return false;
        }
        //var args = $('.xui-i-dialogPOST').serializeObject();
        //args['category_id'] = 0;
        var _this = this;
        W.getApi().call({
            app: 'new_weixin',
            api: 'fans_category',
            method: 'put',
            args: {
                "category_name": inputVal
            },
            success: function(data) {
                var $bigbox = $('.xui-i-fans_List .xui-i-addLi');
                //$bigbox.append("<li class='xa-hoverEditor pl20' data-name='"+inputVal+"' data-id='"+data.category_id+"'><span class='xui-i-categoryName'>"+inputVal+"</span>（0）");
                $bigbox.append("<li class='xa-hoverEditor pl20' data-name='" + inputVal + " 'data-id='" + data.category_id + "'>" +
                    "<span class='xui-i-categoryName'>" + inputVal + "</span>（0）" +
                    '<div class="xui-i-hoverShow fr"><a class="xa-editorGroup"><img src="/static_v2/img/weixin/fansPencil.png" alt=""></a> <a class="xa-delGroup mr5 ml10"><img src="/static_v2/img/weixin/deleteEditor.png"></a>' +
                    '</div>' + "</li>");
                $('.xui-i-groupDialog').hide();
                _this.reloadGroupList(false); //重新加载搜索区的分组列表
            },
            error: function(resp) {
                var msg = resp.errMsg || '保存失败';
                W.getErrorHintView().show(msg);
                $('.xui-i-groupDialog').hide();
            }
        });
    },

    onCancel: function() {
        $('.xui-i-groupDialog').hide();
    },

    onHoverEditor: function(e) {
        var o = e ? e.target : event.srcElement;
        if (o.tagName == "LI") {
            if (o["index"] == undefined) {
                var ul = o.parentNode;
                var liList = ul.getElementsByTagName("li");
                for (var i = 0, li; li = liList[i]; ++i)
                    li["index"] = i;
            }
            var j = o["index"];
            $(".xui-i-hoverShow").eq(j).show();
        }

    },
    onMouseoverShowUserData: function(event) {
        this.$target = $(event.target);
        var userId = $(event.currentTarget).attr('data-id');
        xlog(userId + '===============================================================================');
        var category = '';
        var remark = '';
        var nickname = '';
        var location = '';
        var signature = '';
        var _this = this;
        W.getApi().call({
            app: 'new_weixin',
            api: 'fans_info',
            method: 'get',
            args: {
                'id': userId,
            },
            success: function(data) {
                xlog(data + 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww');
                console.log(_this.$target);
                _this.adduserdatabox(data, _this.$target);
                // $target.parent().append('<div  class="xui-userData pa"><h5 class="fb ml10">详细资料</h5><ul><li>昵称:<span>' + data.info.nickname + '</span></li><li>备注名:<span>' + data.info.remark + '</span></li><li>地区:<span>' + data.info.location + '</span></li><li>签名:<span>' + data.info.signature + '</span></li><li>分组:<span>' + data.info.category + '</span></li></ul></div>')
            },
            error: function(resp) {
                W.getErrorHintView().show('没有该粉丝的数据');
            }
        });
    },
    adduserdatabox: function(data, obj) {
        console.log('---------------');
        console.log(obj);
        console.log('---------------');
        obj.parent().append('<div  class="xui-userData pa"><h5 class="fb ml10">详细资料</h5><ul><li><div class="xui-bigwrapper"><div class="xui-wrapperleft">昵称:</div><div class="xui-wrapperright">' + data.info.nickname + '</div></div></li><li style="clear:both;"><div class="xui-bigwrapper"><div class="xui-wrapperleft">备注:</div><div class="xui-wrapperright">' + data.info.remark + '</div></div></li><li style="clear:both;"><div class="xui-bigwrapper"><div class="xui-wrapperleft">地区:</div><div class="xui-wrapperright">' + data.info.location + '</div></li><li style="clear:both;"><div class="xui-wrapperleft">分组:</div><div class="xui-wrapperright">' + data.info.category + '</div></li></ul></div>')
        xlog(data.info.location+'================================================----------wwwwwwggggggg')
    },
    onMouseleaveShowUserData: function() {
        $('.xui-userData').css({
            'display': 'none'
        });
    },
    onMouseoverPage:function(){
        $('.xui-userData').css({
            'display': 'none'
        });
    },

    onMouseLeaveHoverHide: function() {
        $(".xui-i-hoverShow").hide();
    },
    onClickEditorGroup: function(event) {
        // 编辑分组名称
        var $link = $(event.target);
        var $target = $link;
        var $li = $link.parents('.xa-hoverEditor');
        var categoryName = $li.attr('data-name');
        var categoryId = $li.attr('data-id');
        //xlog("categoryName:" + categoryName + ", id:" + categoryId);

        var $edit = $li.children('.xa-editorInput');
        $edit.show().val(categoryName).focus();

        var _this = this;
        //$(".xa-editorInput").keydown(function(event) {
        $edit.blur(function(event) {
            event.preventDefault();
            var $target = $(event.target);
            var newName = $target.val();
            if (newName) {
                W.getApi().call({
                    app: 'new_weixin',
                    api: 'fans_category',
                    method: 'post',
                    args: {
                        'category_id': categoryId,
                        'category_name': newName
                    },
                    success: function(data) {
                        W.getSuccessHintView().show('修改成功');
                        $li.children('.xui-i-categoryName').html(newName);
                        $li.attr('data-name', newName);
                        _this.reloadGroupList(false); //重新加载搜索区的分组列表
                    },
                    error: function(resp) {
                        W.getErrorHintView().show('分组名称为1-6个字');
                    }
                });
                //$(".xa-groupNameInput").hide();
                $edit.hide();
            }
        });
        $edit.keydown(function(event) {
            // 处理按键的事件
            var ENTER_KEY = 13;
            //xlog("in .xa-hoverEditor.keydown(), event.which=" + event.which + ", char=" + String.fromCharCode(event.which));
            if (event.which !== ENTER_KEY) {
                return;
            }
            // 当按下ENTER处理更新粉丝分类的操作
            event.preventDefault();
            //xlog("pressed ENTER");

            //var val = this.refs.newField.getDOMNode().value.trim();
            var $target = $(event.target);
            var newName = $target.val();
            //xlog("new categoryName=" + newName);
            if (newName) {
                W.getApi().call({
                    app: 'new_weixin',
                    api: 'fans_category',
                    method: 'post',
                    args: {
                        'category_id': categoryId,
                        'category_name': newName
                    },
                    success: function(data) {
                        W.getSuccessHintView().show('修改成功');
                        $li.children('.xui-i-categoryName').html(newName);
                        $li.attr('data-name', newName);
                        _this.reloadGroupList(false); //重新加载搜索区的分组列表
                    },
                    error: function(resp) {
                        W.getErrorHintView().show('修改失败');
                    }
                });
                //$(".xa-groupNameInput").hide();
                $edit.hide();
            }
        });

    },

    /**
     * 删除粉丝分组的响应函数
     */
    onDeleteFanCategory: function(event) {
        var $target = $(event.target);
        var $li = $target.parents('.xa-hoverEditor');
        //var categoryName = $li.attr('data-name');
        var categoryId = $li.attr('data-id');
        //xlog("id:" + categoryId);

        var _this = this;
        W.requireConfirm({
            //$el: $li,
            $el: $target,
            width: 420,
            height: 55,
            position: 'right-middle',
            isTitle: false,
            msg: '确定删除？',
            confirm: function() {
                W.getApi().call({
                    app: 'new_weixin',
                    api: 'fans_category',
                    method: 'delete',
                    args: {
                        'category_id': categoryId
                    },
                    success: function(data) {
                        W.getSuccessHintView().show('成功删除分类');
                        //_this.reloadGroupList(true); //重新加载搜索区的分组列表
                        setTimeout(function() {
                            location.reload()
                        }, 500); // 刷新页面
                    },
                    error: function(resp) {
                        W.getErrorHintView().show('删除分类失败');
                    }
                });
            }
        });
    },

    onClickSelectAll: function(event) {
        var $checkbox = $(event.currentTarget);
        var isChecked = $checkbox.is(':checked');
        this.$('tbody .xa-select').prop('checked', isChecked);
    },

    onClickLiActive: function(e) {
        var o = e ? e.target : event.srcElement;
        if (o.tagName == "SPAN") {
            o = o.parentNode;
            if (o["index"] == undefined) {
                var ul = o.parentNode;
                var liList = ul.getElementsByTagName("li");
                for (var i = 0, li; li = liList[i]; ++i)
                    li["index"] = i;
            }
            var k = o["index"];
            $('.xui-i-addLi').find('.xa-hoverEditor').eq(k).addClass('xui-clickColor').siblings().removeClass('xui-clickColor');

            var categoryId = $('.xui-i-addLi').find('.xa-hoverEditor').eq(k).attr('data-id');
            xlog(categoryId + 'dddddddddddddddddddddddddddddddddddddd')
            var filterValue = 'category_id:' + categoryId;
            var table = $('[data-ui-role="advanced-table"]').data('view');
            var data = {
                'filter_value': filterValue
            }
            table.reload(data, {
                emptyDataHint: '该分组下没有会员'
            });

            $('#category').val(categoryId); //同步下拉框的选项
        }
    },


    onClickSendMessageLink: function() {
        var number = $('#__item_count').attr('data-member-count');
        if (flag == 0) {
            $('.xa-sendMessageLink').append('<div style=\"color:#333\" class="xui-sendMessage pa"><li class="xa-sendMessageChosen">选中的人</li><li class="xa-sendMessageAll">筛选出来的' + number + '人(已跑路除外)</li></div>')
            flag = 1;
            $('.xui-sendMessage').show();
        }
    },

    //在页面其他部分点击鼠标时，已弹出的下拉框能消失
    onClickOnPage: function(event) {
        className = event.target.className;
        if (className.indexOf("xa-sendMessageLink") < 0) {
            if (flag == 1) {
                $('.xui-sendMessage').hide();
                flag = 0;
            }
        }
    },

    onClickSendMessageAll: function() {
        var members = W.loadJSON('members');
        //传递搜索条件，在获取用户open id的时候重新搜索
        //避免直接获取全部用户信息造成粉丝列表页加载过慢
        var category = $('#category option:selected').text();
        var status = $('#status option:selected').text();
        var sex = $('#sex option:selected').text();
        var filterValue = this.getFilterValue();
        var params = 'category=' + category + '&status=' + status + '&sex=' + sex + '&filter_value=' + filterValue;

        if (members && members.length > 0) {
            $('form.xa-postSendMessageAll input').val(params);
            $('form.xa-postSendMessageAll').submit();
        } else {
            W.showHint('error', "没有可以发送的用户");
        }
    },

    onClickSendMessageChosen: function() {
        //获取各个member的id，去库中查询open id然后群发
        //而不是在粉丝列表页加载会员列表的时候就取open id
        //那样代价太大，有过多的sql查询，会使列表页加载变慢
        var memberIdArray = $('[data-ui-role="advanced-table"]').data('view').getAllSelectedDataIds();
        if (memberIdArray.length > 0) {
            var memberIds = 'member_ids=' + memberIdArray.join('|');
            $('form.xa-postSendMessageAll input').val(memberIds);
            $('form.xa-postSendMessageAll').submit();
        } else {
            W.showHint('error', "没有选中的用户");
        }
    },

    onClickaddGrouping: function() {
        if (flag == 0) {
            $('.xui-inlineblock').append('<div class="xui-addGrouping pa"><li>全部分组</li><li>未分组</li><li>活跃</li><li>星标</li></div>')
            flag = 1;
        } else {
            $('.xui-addGrouping').hide();
            flag = 0;
        }
    },

    // 获取条件数据
    getFilterValue: function() {
        var dataValue = [];
        var name = $('#name').val().trim();
        if (name) {
            dataValue.push('name:' + name);
        }
        var categoryId = $('#category').val().trim();
        if (categoryId != -1) {
            dataValue.push('category_id:' + categoryId);
        }
        var status = $('#status').val();
        if (status != -1) {
            dataValue.push('status:' + status);
        }
        var sex = $('#sex').val();
        if (sex != -1) {
            dataValue.push('sex:' + sex);
        }

        var filter_value = dataValue.join('|');

        return filter_value
    },

    clearDialog: function() {

    },


    onChangeCategory: function(event) {
        xlog("in onChangeCategory()");
    },

    reloadGroupList: function(isDelete) {
        xlog("in reloadGroupList()");
        W.getApi().call({
            method: 'get',
            app: 'new_weixin',
            resource: 'fans_category',

            args: {},
            success: function(data) {
                //先获取当前选中的值
                var categoryId = $("#category ").val();
                //解析数组
                $("#category").empty();
                $("#category").append("<option value='-1'>全部</option>");
                $.each(data.categories, function(i, item) {
                    $("#category").append("<option value=" + item.id + ">" + item.name + "</option>");
                });

                //把下拉框选中的值设置为之前选中的
                if (!isDelete) {
                    $('#category').val(categoryId);
                }
            },
            error: function(resp) {
                alert('获取分组列表失败!');
            }
        });
    }
});