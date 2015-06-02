/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * css editor
 * @class
 */
W.workbench.CssEditorView = Backbone.View.extend({
	el: '',

	events: {
        'click [data-action="collapseEditor"]': 'onClickCollapseEditorButton',
        'keypress #cssEditor_codeEditor': 'onCodeEditorKeypress'
	},

    getTemplate: function() {
    },
	
	initialize: function(options) {
		this.$el = $(this.el);

        $('#cssEditorIndicator').click(_.bind(this.onClickCssEditorIndicator, this));
        this.isCodeLoaded = false;
        this.editorWidth = 0;
        this.codeEditor = null;
	},

    render: function() {
        return;
    },

    /**
     * setDimension: 设置editor的dimension
     */
    setDimension: function() {
        var $phone = $('#phone');
        this.editorWidth = $phone.offset().left - 30;
        xlog('[css editor]: set dimension to ' + this.editorWidth);
        this.$el.css({
            width: this.editorWidth,
            left: 0-this.editorWidth + 'px'
        });

        //设置code editor height
        var cssEditorHeight = this.$el.outerHeight();
        //42是sectionHeader的高度，10是margin top的高度，3是底部空白空间
        this.$('#cssEditor_codeEditor').height(cssEditorHeight - 70 - 5);
    },

    /**
     * loadCode: 加载代码
     */
    loadCode: function() {
        W.getApi().call({
            app: 'workbench', 
            api: 'css/get',
            args: {
                project_id: W.projectId
            },
            success: function(data) {
                this.codeEditor = ace.edit("cssEditor_codeEditor");
                this.codeEditor.setTheme("ace/theme/monokai");
                this.codeEditor.getSession().setMode("ace/mode/css");
                this.codeEditor.setValue(data);
            },
            error: function(resp) {
                alert('加载CSS失败！');
            },
            scope: this
        });
    },

    /**
     * onClickCssEditorIndicator: 点击css editor indicator的响应函数
     */
    onClickCssEditorIndicator: function(event) {
        if (!this.isCodeLoaded) {
            this.setDimension();
        }
        var left = this.$el.css('left');
        var _this = this;
        if (left.indexOf('-') == -1) {
            this.$el.animate({
                left: 0-this.editorWidth+'px'
            }, 200, function() {
                xlog('done!');
            });
        } else {
            this.$el.animate({
                left: '0px'
            }, 200, function() {
                xlog('done!');
                if (!_this.isCodeLoaded) {
                    _this.loadCode();
                    _this.isCodeLoaded = true;
                }
            });
        }
    },

    /**
     * onClickCollapseEditorButton: 点击隐藏editor按钮的响应函数
     */
    onClickCollapseEditorButton: function(event) {
        this.onClickCssEditorIndicator();
    },

    /**
     * onCodeEditorKeypress: 在code editor中按下键盘的响应函数
     */
    onCodeEditorKeypress: function(event) {
        if (event.ctrlKey && event.which === 115) {
            event.preventDefault();
            event.stopPropagation();

            W.getApi().call({
                app: 'workbench', 
                api: 'css/update',
                method: 'post',
                args: {
                    project_id: W.projectId,
                    content: this.codeEditor.getValue().trim()
                },
                success: function(data) {
                    W.Broadcaster.trigger('workbench:refresh_design_page');
                },
                error: function(resp) {
                    alert('保存CSS失败！');
                }
            });
        }    
    }
});