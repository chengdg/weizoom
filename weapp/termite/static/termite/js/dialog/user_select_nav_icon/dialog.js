/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.workbench');
W.dialog.workbench.SelectNavIconDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .selectNavIconDialog_iconBox': 'onClickIcon',
        'click .tx_toggleIconMenu': 'toggleIcoMenu'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#user-select-nav-icon-dialog-tmpl-src').template('user-select-nav-icon-dialog-tmpl-tmpl');
        return "user-select-nav-icon-dialog-tmpl-tmpl";
    },

    getOneIconTemplate: function() {
        $('#user-select-nav-icon-dialog-one-icon-tmpl-src').template('user-select-nav-icon-dialog-one-icon-tmpl');
        return "user-select-nav-icon-dialog-one-icon-tmpl";
    },

    makeRadios: function(templates, targetTemplateProjectId) {
        var buf = [];
        var length = templates.length;
        for (var i = 0; i < length; ++i) {
            var template = templates[i];
            if (template.id === targetTemplateProjectId) {
                buf.push('<label class="radio">' + 
                            '<input type="radio" checked="checked" name="template" data-id="' + template.id + '" value="' + template.innerName + '" />' + template.name +
                        '</label>');
            } else {
                buf.push('<label class="radio">' + 
                            '<input type="radio" name="template" data-id="' + template.id + '" value="' + template.innerName + '" />' + template.name +
                        '</label>');
            }
        }

        return $(buf.join(''));
    },

    onInitialize: function(options) {
        this.isIconLoaded = false;
        this.cacheIconData = null;
        this.$iconContainer = this.$('.tx_iconContainer');
        this.oneIconTemplate = this.getOneIconTemplate();
    },

    /**
     * 初始化图片上传器
     */
    initImageUploader: function() {
        var _this = this;
        var fileUploader = this.$('#iconUploader');
        var _path = null;
        fileUploader.each(function() {
            $(this).uploadify({
                swf: '/static/uploadify.swf',
                multi: false,
                removeCompleted: true,
                uploader: '/account/upload_icon/',
                cancelImg: '/static/img/cancel.png',
                buttonText: '上传60*60图标...',
                fileTypeDesc: '图标文件',
                fileTypeExts: '*.jpg; *.png; *.gif; *.ico',
                method: 'post',
                formData: {
                    uid: W.uid
                },
                removeTimeout: 0.0,
                onUploadSuccess : function(file, path, response) {
                    xlog('icon path: ' + path);
                    _path = path;
                    _this.onFinishUpload(path);
                },
                onUploadComplete: function() {
                    //在onUploadComplete中隐藏uploadZone，防止queue不清空的bug
                    _path = null;
                },
                onUploadError: function(file, errorCode, errorMsg, errorString) {
                    xlog(errorCode);
                    xlog(errorMsg);
                    xlog(errorString);
                    W.getErrorHintView().show('图片数据损坏，无法在Android平台显示，请处理图片，再次上传');
                }
            });
        });
    },

    onShow: function(options) {
        if (!this.isImageFetched) {
            var _this = this;
            this.isImageFetched = true;
            var task = new W.DelayedTask(function() {
                W.getApi().call({
                    app: 'workbench',
                    api: 'nav_icons/get',
                    args: {
                        project_id: W.projectId
                    },
                    scope: this,
                    success: function(data) {
                        _this.cacheIconData = data;
                        _this.renderIconMenus(data);
                        _this.$('.selectNavIconDialog_body_loading').hide();
                    },
                    error: function(resp) {
                        alert('获取图片失败');
                    }
                });
            }, this)
            task.delay(1000);
        }
    },

    /**
     * onFinishUpload: 上传图标结束后的响应函数
     */
    onFinishUpload: function(path) {
        var menuId = '我上传的';
        this.cacheIconData[menuId].push(path);
        var $icoContent = this.$('.tx_iconContent'+menuId);
        var $emptyIndicator = $icoContent.find('.xa-inner-emptyIndicator');
        if ($emptyIndicator.length > 0) {
            $emptyIndicator.remove();
        }
        $icoContent.append(this.onAddImage(path));
        this.toggleIcoMenu(null, menuId);

        var event = {currentTarget: $icoContent.find('.selectNavIconDialog_iconBox').last().get(0)};
        this.onClickIcon(event);
    },
    
    renderIconMenus: function(data) {
        var menuName;
        var li = '';
        var firstName;
        for(menuName in data) {
            firstName = firstName || menuName;
            li += '<li><a href="javascript:void(0);" class="tx_toggleIconMenu" to="'+menuName+'">'+menuName+'</a></li>'
        }
        li += ('<div style="position: absolute; right: 40px; bottom: -8px;">' 
                + '<button class="btn btn-primary" id="iconUploader">上传图片</button>'
                + '</div>');
        this.$('.tx_iconMenus').html(li);

        this.initImageUploader();

        this.toggleIcoMenu(null, firstName);
    },
    
    toggleIcoMenu: function(event, menuId) {
        var menuId = event ? $(event.currentTarget).attr('to') : menuId;
        this.renderIcons(menuId, this.cacheIconData[menuId]);
    },
    
    renderIcons: function(id, data) {
        var $currentIconContent = this.$iconContainer.find('.tx_iconContent'+id+'');
        var isHasIconContent = $currentIconContent.length;
        this.$('.tx_iconContent').hide();
        if(isHasIconContent) {
            $currentIconContent.show();
        }
        else {
            var $icoContent = $('<div class="tx_iconContent'+id+' tx_iconContent"></div>');
            this.$iconContainer.append($icoContent);
            if (data.length > 0) {
                _.each(data, function(path) {
                    $icoContent.append(this.onAddImage(path));
                }, this);
            } else {
                $icoContent.append('<div class="xa-inner-emptyIndicator">您还没有上传过图标</div>');
            }
            
        }
        this.$('.tx_toggleIconMenu').parent('li').removeClass('active');
        this.$('.tx_toggleIconMenu[to="'+id+'"]').parent('li').addClass('active');
    },

    /**
     *
     */
    onAddImage: function(path) {
        var $node = $.tmpl(this.oneIconTemplate, {url: path});
        return $node;
    },

    /**
     * onClickIcon: 点击图片后的响应函数
     */
    onClickIcon: function(event) {
        this.$('.activeImg').hide().removeClass('activeImg');
        var imgBox = $(event.currentTarget);
        imgBox.find('.selectNavIconDialog_iconBox_cover').addClass('activeImg').show();
    },

    /**
     * onGetData: 获取数据
     */
    onGetData: function(event) {
        var activeImage = this.$('.activeImg').parent().find('img');
        var imageUrl = activeImage.attr('src');

        this.$dialog.find('.activeImg').hide().removeClass('activeImg');

        return imageUrl;
    }
});