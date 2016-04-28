/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * W.view.common.RichTextEditor: 富文本编辑器
 # @constructor
 */
ensureNS('W.view.common');
W.view.common.RichTextEditor = Backbone.View.extend({
    el: '',

    events: {
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.$textarea = this.$el;
        this.type = options['type'] || 'text';
        var maxCount = options.maxCount || 300;
        var width = options.width || 300;
        var height = options.height || 200;
        var isDebug = options.debug || false;
        var wordCount = true;
        var pasteplain = !!options.pasteplain;
        if (options.hasOwnProperty('wordCount')) {
            wordCount = options.wordCount;
        }
        var imgSuffix = options.imgSuffix || undefined;

        var imageUrl = "/account/upload_richtexteditor_picture/";
        if (imgSuffix) {
            imageUrl += ("?"+imgSuffix);
        }

        var autoHeight = true;
        if (options.hasOwnProperty('autoHeight')) {
            autoHeight = options.autoHeight;
        }

        var onFormatContent = _.bind(this.onFormatContent, this);
        this.editorOptions = {
            initialFrameWidth: width,
            initialFrameHeight: height,
            minFrameHeight: 50,
            wordCount: wordCount,
            autoFloatEnabled: false,
            autoHeightEnabled: autoHeight,
            initialContent: '',
            emotionLocalization:true,
            elementPathEnabled: false,
            pasteplain: pasteplain,
            maximumWords: maxCount,
            wordCountMsg:'<span style="color:#333;">已输入{#count}个字符, 还可输入{#leave}个字符</span>',
            wordOverFlowMsg:'<span style="color:red;">已超出{#overflow}个字符！</span>',
            onFormatContent: onFormatContent,

            imageUrl: imageUrl,
            imagePath: ''
        };

        //根据type确定toolbars
        if (this.type == 'text') {
        	$.extend(this.editorOptions, {
                toolbars: [['link', 'emotion']]
        	});
        } else if (this.type == 'richtext') {
            $.extend(this.editorOptions, {
                toolbars: [["removeformat", 'bold', 'italic', 'underline', "forecolor", "backcolor", '|', "insertunorderedlist","insertorderedlist", '|', 'link', 'emotion', 'insertimage', 'fullscreen']]
            });
        } else if (this.type == 'full') {
            $.extend(this.editorOptions, {
                toolbars: [['bold', 'italic', 'underline', "forecolor", "backcolor", '|', "insertunorderedlist","insertorderedlist", '|', 'link', 'insertframe', 'emotion', 'insertimage', 'fullscreen'],
                            ['justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'paragraph', 'fontfamily', 'fontsize', '|', 'lineheight', '|', "inserttable", '|', "removeformat"]]
            });
        } else if (this.type == 'code') {
            $.extend(this.editorOptions, {
                wordCount: false,
                toolbars: [["highlightcode", "insertcode", 'fullscreen']]
            });
        } else if (this.type == 'onlyLink') {
            $.extend(this.editorOptions, {
                toolbars: [['link']]
            });           
        }

        //设置是否显示源码
        if (isDebug) {
            var firstToolbars = this.editorOptions.toolbars[0];
            if (firstToolbars.length) {
                firstToolbars.splice(0, 0, 'source');
            } else {
                this.editorOptions.toolbars.splice(0, 0, 'source');
            }
        }
        
        //设置焦点时清除文本的配置
        var originalText = $.trim(this.$textarea.val());
        if (originalText.length == 0) {
            this.editorOptions.autoClearinitialContent = true;
        } else {
            this.editorOptions.autoClearinitialContent = false;
        }

        this.editor = null;
        this.shouldFormatContent = true;

        this.htmlEntities = [
            [/&#39;/g, "'"],
            [/&quot;/g, '"'],
            [/&gt;/g, '>'],
            [/&lt;/g, '<'],
            [/&amp;/g, '&'],
        ];

        this.pendingContent = null; //待editor进入ready之后需要set的content
        this.isEditorReady = false; //editor是否已经ready了
    },

    render: function() {
        var _this = this;

        //管理id，解决一个page中不能有多个richtext editor的bug
        var id = this.$el.attr('id');
        var count = 1;
        if (W.view.common.RichTextEditor.ID2COUNT[id]) {
            count = W.view.common.RichTextEditor.ID2COUNT[id]
        }
        W.view.common.RichTextEditor.ID2COUNT[id] = count+1;
        id = id + '_' + count;
        this.$el.attr('id', id);

    	this.editor = UE.getEditor(this.$el.attr('id'), this.editorOptions);
    	this.editor.addListener('blur', function() {
            var content = _this.editor.getContent();
            _this.$textarea.val(content);
    		_this.trigger('blur', content);
    	});
        this.editor.addListener('keyup', function() {
            _this.trigger('contentchange');
        });
        this.editor.addListener('contentchange', function() {
            _this.trigger('contentchange');
        });
        this.editor.addListener('wordcountoverflow', function() {
            _this.trigger('wordcount_overflow');
        });
        this.editor.addListener('wordcountnormal', function() {
            _this.trigger('wordcount_normal');
        });
        this.editor.addListener('fullscreenchanged', function(cmd, isFullscreen) {
            if (isFullscreen) {
                //TODO: 目前只支持页面上有一个rich text editor
                $('.edui-editor').css('top', '0px');
            }
        });
        this.editor.addListener('ready', function() {
            _this.$textarea.parent().children('div.edui-default').show();
            var content = _this.editor.getContent();
            _this.$textarea.val(content);
            if (_this.type == 'code') {
                _this.editor.commands['selectall'].execCommand.call(_this.editor);
                _this.editor.commands['insertcode'].execCommand.call(_this.editor, 'insertcode', 'css');
                _this.focus();

                //禁止切换语言
                $('.edui-for-insertcode .edui-button-body,.edui-for-insertcode .edui-arrow').attr('onclick', 'javascript:void(0);');
            }
            _this.trigger('ready');
        });

        //_this.$el.show();
        //添加errorHint
        if (this.$el.parent().find('.errorHint').length === 0) {
            this.$el.parent().append('<div class="errorHint"></div>');
        }

        // 删除已有的弹框
        $('.edui-dialog.edui-for-link').remove();

        //editor进入ready状态之后，需要将缓冲的content调用setContent
        this.editor.ready(_.bind(function() {
            this.isEditorReady = true;
            if (this.pendingContent) {
                this.setContent(this.pendingContent);
            }
        }, this));
    },

    enableFormatContent: function() {
        this.shouldFormatContent = true;
    },

    disableFormatContent: function() {
        this.shouldFormatContent = false;        
    },

    focus: function() {
        this.editor.focus(true);
    },

    getContent: function() {
        return this.editor.getContent();
    },

    onFormatContent: function(html) {
        if (this.type == 'richtext' || !this.shouldFormatContent || this.type == 'full') {
            return html;
        }

        if (html[0] === '<' && html[1] === 'p' && html[2] === '>') {
            hSource = html.substring(3, html.length-4); //去除首尾的<p></p>
        } else {
            hSource = html;
        }
        hSource = hSource.replace(/<br\s*\/>/g, '\n').replace(/<\/p>/g, '\n').replace(/<p>/g, '').replace(/&nbsp;/g, ' ');

        //替换表情
        var beg = 0;
        while (true){
            //抽取img
            var pos = hSource.indexOf('<img', beg);
            if (pos == -1) {
                break;
            }

            var end = hSource.indexOf('/>', pos);
            var img = hSource.substring(pos, end+2);
            
            //获得图片名
            var nameBeg = img.indexOf('/weixin/')+8;
            var nameEnd = img.indexOf('"', nameBeg);
            var imgName = img.substring(nameBeg, nameEnd);
            var title = W.EMOTIONNAME2TITLE[imgName];

            //替换
            hSource = hSource.replace(img, title);
        }

        //TODO: 改进算法，替换replace
        _.each(this.htmlEntities, function(entity) {
            hSource = hSource.replace(entity[0], entity[1])
        });
        return $.trim(hSource);
    },

    /**
     * 获得没有经过表情处理的内容
     */
    getHtmlContent: function() {
        this.disableFormatContent();
        var content = this.editor.getContent();
        this.enableFormatContent();
        return content;
    },

    ready: function(fn) {
        this.editor.ready(fn);
    },

    /**
     * 调用ueditor的setContent
     */
    setContent: function(content) {
        if (!this.isEditorReady) {
            xlog('pending setContent');
            this.pendingContent = content;
        } else {
            xlog('setContent');
            this.editor.setContent(content);
        }
    }
});
W.view.common.RichTextEditor.ID2COUNT = {};


W.registerUIRole('textarea[data-ui-role="richtext-editor"]', function() {    
    var $textarea = $(this);
    var type = $textarea.attr('data-type');
    var height = parseInt($textarea.attr('data-height'));
    var width = parseInt($textarea.attr('data-width'));
    var editor = new W.view.common.RichTextEditor({
        el: $textarea.get(),
        type: type,
        width: width,
        height:height,
        autoHeight:false,
        imgSuffix: "uid="+W.uid,
        wordCount: false
    });
    editor.render();

    $textarea.data('view', editor);
});