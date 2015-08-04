/*
Copyright (c) 2011-2013 Weizoom Inc
*/
ensureNS('W.dialog');

//<name, dialog>缓存
W.dialog.NAME2DIALOG = {};


W.dialog.Dialog = Backbone.View.extend({
    events: {
        'click .btn-success': 'onClickSubmitButton',
		'click .xa-submit-dialog': 'onClickSubmitButton',
    },

    getTemplate: function() {
        throw "Please implement dialog's \"getTemplate\" function in your own dialog";
    },

    onInitialize: function(options) {
    },

    beforeShow: function(options) {
    },

    onShow: function(options) {

    },

    afterShow: function(options) {
    },

    onGetData: function() {

    },

    onGetDataAsync: function() {

    },

    onChangeNav: function(nav) {

    },

    getDialogTitle: function() {
        return $.trim(this.$('.modal-title').text());
    },

    initialize: function(options) {
        options = options || {};
        if(!options.filter_type){
            options.filter_type = 'all';
        }
        this.$el = $(this.el);

        var $node = null;
        if (this.templates && this.templates.dialogTmpl) {
            var template = this.getTmpl('dialogTmpl');
            $node = $(template(options));
        } else {
            var template = this.getTemplate();
            $node = $.tmpl(template, options);
        }

        $('body').append($node);
        this.el = $node.get(0);
        this.$el = $(this.el);

        var $titleInput = null;
        var $title = null;
        var $editIcon = null;
        if (options.canEditTitle) {
            this.$('.modal-title').html('<input type="text" name="" class="mr5 form-control xa-titleInput wui-titleInput" style=""/><span class="xa-title xui-titleColor mr5"></span><span class="xa-editTitle  glyphicon glyphicon-edit cursor-pointer"></span>').addClass('form-inline');
            $titleInput = this.$('.xa-titleInput');
            $title = this.$('.xa-title');
            $editIcon = this.$('.xa-editTitle');
            $titleInput.blur(function() {
                var title = $.trim($titleInput.val());
                if (title) {
                    $titleInput.hide();
                    $title.text($titleInput.val()).show();
                    $editIcon.show();
                }
            });
        }

        this.setTitle(options.title);

        this.successCallback = null;
        this.$dialog = this.$el;
        this.$dialog.find('.xa-editTitle').click(function() {
            $title.hide();
            $editIcon.hide();
            $titleInput.show().focus();
        });
        //W.renderValidateIndicator(this.$dialog);

        var _this = this;
        W.createWidgets(_this.$dialog);

        this.$el.on('shown.bs.modal', _.bind(this.afterShow, this));

        this.$el.delegate('.xa-titleNav', 'click', _.bind(this.onClickTitleNav, this));

        this.onInitialize(options);
    },

    onClickTitleNav: function(event) {
        var $nav = $(event.target);
        this.$('.xui-dialog-activeTitleNav').removeClass('xui-dialog-activeTitleNav');
        $nav.addClass('xui-dialog-activeTitleNav');

        var nav = $nav.data('nav');
        this.onChangeNav(nav);
        this.trigger('change-nav', nav);
    },

    clickNav: function(nav) {
        var $nav = this.$dialog.find('[data-nav="'+nav+'"]');
        var event = {target:$nav.get(0)};
        this.onClickTitleNav(event);
    },

    render: function() {
    },

    show: function(options) {
        this.options = options;
        this.successCallback = options.success;

        this.beforeShow(options);

        this.setTitle(options.title);

        this.$dialog.modal('show');

        this.onShow(options);
    },

    reset: function() {
        var title = '';
        if (this.options.canEditTitle) {
            if (this.options.title) {
                title = this.options.title;
            }
        }

        $titleInput = this.$('.xa-titleInput');
        $title = this.$('.xa-title');
        $editIcon = this.$('.xa-editTitle');
        $titleInput.val(title);
        $title.text(title);

        if (this.options.title) {
            $title.show();
            $titleInput.hide();
        } else {
            $title.hide();
            $titleInput.show();
        }
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onClickSubmitButton: function(event) {
        var data = this.onGetData(event);

        if (data) {
            this.$dialog.modal('hide');
            if (this.successCallback) {
                //调用success callback
                var _this = this;
                _.delay(function() {
                    _this.successCallback(data);
                    _this.successCallback = null;
                }, 100);
            }
        }
    },

    setTitle: function(title){     
        if (title) {
            var $title = this.$('.xa-title');
            var $titleInput = this.$('.xa-titleInput');
            if ($title.length > 0) {
                $title.text(title);
                $titleInput.hide().val(title);
            } else {
                //在非编辑模式下，直接修改modal-title
                if (_.isArray(title)) {
                    var buf = [];
                    var counter = 1;
                    _.each(title, function(titleInfo) {
                        if (counter === 1) {
                            buf.push('<span class="xa-titleNav xui-dialog-titleNav xui-dialog-activeTitleNav" data-nav="' + titleInfo.type + '">' + titleInfo.name + '</span>');
                        } else {
                            buf.push('<span class="xa-titleNav xui-dialog-titleNav" data-nav="' + titleInfo.type + '">' + titleInfo.name + '</span>');
                        }
                        counter += 1;
                    });
                    this.$('.modal-title').html(buf.join('<span class="xui-dialog-titleNavBar mr10 ml10">|</span>'));
                } else {
                    this.$('.modal-title').text(title);
                }
            }
        } else {
            var $editIcon = this.$('.xa-editTitle');
            if ($editIcon) {
                $editIcon.hide();
            }
        }   
    }
});

/**
 * showDialog: 显示dialogName指定的dialog
 */
W.dialog.showDialog = function(dialogName, options) {
    var dialog = W.dialog.NAME2DIALOG[dialogName];
    if (dialog) {
        dialog.show(options);
        return;
    }

    //没有dialog，创建之
    xlog('create new dialog: ' + dialogName);
    var obj = window;
    var items = dialogName.split('.');
    var itemCount = items.length;
    // 定位对象?
    for (var i = 0; i < itemCount; ++i) {
        var item = items[i];
        if (obj.hasOwnProperty(item)) {
            obj = obj[item];
        } else {
            obj = [];
            break;
        }
    }

    if (obj !== null) {
        //xlog(options);
        xlog("obj=");
        xlog(obj);
        var dialog = new obj(options);
        W.dialog.NAME2DIALOG[dialogName] = dialog;
        dialog.show(options);
    }
}


/**
 * initDialog: 初始化dialogName指定的dialog
 */
W.dialog.initDialog = function(dialogName, options) {
    var dialog = W.dialog.NAME2DIALOG[dialogName];
    if (dialog) {
        return;
    }

    //没有dialog，创建之
    xlog('create new dialog: ' + dialogName);
    var obj = window;
    var items = dialogName.split('.');
    var itemCount = items.length;
    for (var i = 0; i < itemCount; ++i) {
        var item = items[i];
        if (obj.hasOwnProperty(item)) {
            obj = obj[item];
        } else {
            obj = [];
            break;
        }
    }

    xlog(obj);
    if (obj !== null) {
        var dialog = new obj(options);
        W.dialog.NAME2DIALOG[dialogName] = dialog;
    }
}
