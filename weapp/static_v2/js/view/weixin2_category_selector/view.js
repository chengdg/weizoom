/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择分类
 * 
 * @see 'member_update_tag'
 *
 * Author: Victor, Bert
 * 
 */
ensureNS('W.view.weixin');
W.view.weixin.CategorySelector = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#category-selector-dialog-tmpl-src').template('category-selector-dialog-tmpl');
        return "category-selector-dialog-tmpl";
    },

    getGradeTemplate: function() {
        $('#selector-tmpl-src').template('selector-tmpl');
        return "selector-tmpl";
    },

    events: {
        //'click .xa-submit': 'onClickSubmit',
        'click .xa-selectCategory': 'onSelectCategory',
    },

    initializePrivate: function(options) {
        xlog("in CategorySelector.initializePrivate()");
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
        this.selectorTemplate = this.getGradeTemplate();
        xlog("selectorTemplate: " + this.selectorTemplate);
    },

    //onClickSubmit: function(event) {
    /* 点击分类选项的事件处理函数 */
    onSelectCategory: function(event) {
        xlog("in CategorySelector.onSelectCategory()");
        //xlog(this.memberId);
        // TODO: 传入回调函数，由调用端控制
        //this.submitSendApi(this.isUpdateGrade,this.memberId)
        var $target = $(event.currentTarget);
        var fanId = $target.attr('data-id');
        xlog('fanId:'+fanId);
        this.updateCategory(this.memberId, fanId);

        /*var _this = this;
        $("input[name='tag_id']:checked").each(function() {
            var fanId = this.value;
            _this.updateCategory(_this.memberId, fanId);
        })*/
        //xlog(tag_values);
    },

    updateCategory: function(fanId, categoryId) {
        xlog("in updateCategory(), fanId: " + fanId);
        W.getApi().call({
            app: 'new_weixin',
            api: 'fans_category_relation',
            method: 'post',
            args: {
                'fan_ids': fanId,
                'category_id': categoryId,
            },
            success: function(data) {
                //xlog("updated successfully");
                W.getSuccessHintView().show('修改分组成功');
                setTimeout(function(){location.reload()},500);
            },
            error: function(data) {
                var errMsg = data.errMsg || "修改分组失败";
                //xlog("failed to update");
                W.getErrorHintView().show(errMsg);
            }
        });
    },

    validate: function() {

    },

    getOptions: function(options) {
        xlog("in getOptions()");
        // 获得选项
        //xlog("options: " + options);
        //this.isUpdateGrade = options.isUpdateGrade;
        this.memberId = options.memberId;
        this.isPostData = options.isPostData;

        xlog("this.isPostData: " + this.isPostData);
        var _this = this;
        W.getApi().call({
            app: 'new_weixin',
            api: 'fans_category',
            method: 'get',
            args: {
                fan_id: this.memberId
            },
            success: function(data) {
                var tags = data.categories;
                var fanHasCategoryId = data.fan_has_category_id;

                currentTemplate = _this.selectorTemplate;
                var $tags = $.tmpl(currentTemplate, {
                    'tags': tags,
                    'fanHasCategoryId': fanHasCategoryId
                });
                $('.xa-drop-box-content .xa-i-content').empty().append($tags);
            },
            error: function(resp) {
                xlog("Error: " + resp.errMsg || "Failed to get the category list");
            }
        });
    },

    render: function() {
        //xlog("in CategorySelector.render()");
        this.$content.html($.tmpl(this.getTemplate()));
    },

    onShow: function(options) {},

    showPrivate: function(options) {
        xlog("in showPrivate()");
        this.getOptions(options);
    },
});


W.getCategorySelector = function(options) {
    xlog('create W.view.weixin.CategorySelector');
    var dialog = W.registry['W.view.weixin.CategorySelector'];
    if (!dialog) {
        //创建dialog并缓存？
        xlog('create W.view.weixin.CategorySelector');
        dialog = new W.view.weixin.CategorySelector(options);
        W.registry['W.view.weixin.CategorySelector'] = dialog;
    }
    return dialog;
    //return new W.view.weixin.CategorySelector(options);
};
