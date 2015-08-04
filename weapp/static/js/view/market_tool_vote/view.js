/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * 投票选项操作的View
 * @class vote_options 选项列表
 * @event deleteOption - 点击删除按钮，触发
 * @event addOption - 点击添加选项按钮，触发
 *
 * author: chuter
 */
ensureNS('W.view.market_tools.vote');
W.view.market_tools.vote.VoteOptionsListView = Backbone.View.extend({
    getOneVoteOptionTemplate: function () {
        $('#one-voteoption-tmpl-src').template('one-voteoption-tmpl');
        return 'one-voteoption-tmpl';
    },

    getVoteOptionsTableTemplate: function () {
        $('#voteoptions-list-tmpl-src').template('voteoptions-list-tmpl');
        return 'voteoptions-list-tmpl';
    },

    events: {
        'click .vote_delete_option': 'deleteOption',
        'click .vote_option_add': 'addOption',
    },

    saveOption: function (options, success_callback, failed_callback) {
        W.getApi().call({
            method: 'post',
            app: 'market_tools/vote',
            api: 'vote_option/create',
            async: false,
            args: options ? options : {},
            scope: this,
            success: function (data) {
                if (data.option_id) {
                    success_callback(data);
                } else {
                    W.getErrorHintView().show('保存投票选项失败，请稍后重试！');
                    failed_callback();
                }
            },
            error: function (resp) {
                //TODO 进行错误通知
                W.getErrorHintView().show('服务繁忙，请稍后重试！');
                failed_callback();
            }
        });
    },

    addOption: function (event) {
        this.renderNewOption();
    },

    renderNewOption: function () {
        var _this = this;

        var html = $.tmpl(this.oneOptionTemplate, {
            is_show_image: _this.is_show_image
        });

        this.$optionsList.append(html);

        if (this.is_show_image) {
            this.render_image();
        }
    },

    deleteOption: function (event) {
        var $el = $(event.currentTarget);
        var $tr = $el.parents('tr');
        $tr.remove();
    },

    show_image: function() {
        this.is_show_image = true;
    },

    hide_image: function() {
        this.is_show_image = false;
    },

    render: function () {
        var _this = this;

        this.$el.append($.tmpl(this.optionsTableTemplate, {
            is_show_image: _this.is_show_image
        }));

        this.$optionsList = $('#vote_options_list');

        if (this.voteOptions) {
            var optionsList = this.voteOptions;

            for (var index = 0; index < optionsList.length; index++) {
                this.$optionsList.append($.tmpl(this.oneOptionTemplate, {
                    vote_option: optionsList[index],
                    is_show_image: _this.is_show_image
                }));
            }
        }

        if (this.is_show_image) {
            this.render_image();
        }
    },

    initialize: function (options) {
        this.$el = options.el;

        this.oneOptionTemplate = this.getOneVoteOptionTemplate();
        this.optionsTableTemplate = this.getVoteOptionsTableTemplate();

        //展现方式支持：matrix(矩阵方式罗列选项)，line(进度条方式一行一个选项)
        this.showStyle = options.showStyle || 'matrix';
        this.is_show_image = this.showStyle == 'matrix' ? true : false;
        this.voteOptions = options.voteOptions;
    },

    //TODO 可支持只针对新增的节点进行处理
    render_image: function () {
        $('input[data-ui-role="image-selector"]').each(function () {
            var $imageInput = $(this);
            var width = parseInt($imageInput.attr('data-width'))
            var height = parseInt($imageInput.attr('data-height'));
            var $imageView = $imageInput.siblings('div[data-ui-role="image-selector-view"]').eq(0);
            var url = $imageInput.val();
            var view = new W.view.common.ImageView({
                el: $imageView.get(),
                picUrl: url,
                height: height,
                width: width,
                autoShowHelp: true
            });
            view.bind('upload-image-success', function (path) {
                $imageInput.val(path);
            });
            view.bind('delete-image', function () {
                $imageInput.val('');
            });
            view.render();
        });
    }
});