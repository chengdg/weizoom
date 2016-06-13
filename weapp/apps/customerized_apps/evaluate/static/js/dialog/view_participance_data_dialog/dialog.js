/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.evaluate');
W.dialog.app.evaluate.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),
	
	templates: {
		dialogTmpl: '#app-evaluate-viewParticipanceDataDialog-dialog-tmpl',
		resultTmpl: '#app-evaluate-viewParticipanceResultDialog-dialog-tmpl'
	},

	onInitialize: function(options) {
		//创建富文本编辑器
        var MyEditor =  W.view.common.RichTextEditor.extend({
			initialize: function(options) {
			        this.$el = $(this.el);
			        this.$textarea = this.$el;
			        this.type = options['type'] || 'text';
			        var maxCount = options.maxCount || 300;
			        var width = options.width;
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
			    }
        });
        editor = new MyEditor({
            el: 'textarea',
            type: 'text',
            width: null,
            height: 100,
            pasteplain: true
        })
		editor.render();
	},
	
	beforeShow: function(options) {
	},
	
	onShow: function(options) {
		this.product_review_id = options.product_review_id;
		if (this.product_review_id) {
			W.getApi().call({
				app: 'apps/evaluate',
				resource: 'evaluate_review',
				scope: this,
				args: {
					id: this.product_review_id
				},
				success: function(data) {
					var context = data.items;
					var source = $("#app-evaluate-viewParticipanceResultDialog-dialog-tmpl").html();
					var template = Handlebars.compile(source);					
					var html = template(context);
					$('.xa-modal-content').html(html);
					editor.setContent(data.items.shop_reply);
				},
				error: function(resp) {
					console.log('error');
				}
			});
		}
	},
	
	afterShow: function(options) {
		var _this = this
		$(".xa-modal-modify").click(function(event){
            var $el = $(event.currentTarget);
            var status = $el.attr("data-status");
            W.getApi().call({
                app: 'apps/evaluate',
                resource: 'evaluate_review',
                method: 'post',
                args: {
                    product_review_id: _this.product_review_id,
                    status: status
                },
                success: function(){
                    W.showHint('success', '操作成功');
                    $('[data-ui-role="advanced-table"]').data('view').reload();
                },
                error: function(){
                    W.showHint('error', '操作失败');
                }
            });
        });	

		$('body').delegate('.xa-update-tag', 'click', function(event){
			var $el = $(event.currentTarget);
			var member_id = $(this).data('id');

			var memberTagsUpdateView = W.getMemberTagsUpdateView({
				width: 260,
				title: '修改分组',
				position:'top',
				isTitle: false,
				privateContainerClass:'xui-updateGradeOrTagBox',
				isPostData: false
			});
			memberTagsUpdateView.show({
				$action: $el,
				isUpdateGrade: false,
				memberId: member_id,
				isPostData: false
			})
	        memberTagsUpdateView.render();
		});
	},

	onClickSubmitButton: function(){
		var member_id = $('.xa-update-tag').data('id');
		var content = editor.getHtmlContent();
		var tag_ids = [];
		$(".tag_id").each(function() {
			tag_ids.push(this.value)
		});
		// if (content.length > 100) {
		// 	W.showHint('error', '内容不能超过100字');
		// 	return;
		// }		
		W.getApi().call({
            app: 'apps/evaluate',
            resource: 'evaluate_review_shop_reply',
            method: 'post',
            args: {
                product_review_id: this.product_review_id,
                content: content,
                tag_ids: JSON.stringify(tag_ids),
                member_id: member_id
            },
            scope: this,
            success: function(){
                W.showHint('success', '操作成功');
            },
            error: function(){
                W.showHint('error', '操作失败');
            }
        });
	},
	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});
