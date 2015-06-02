/*
Copyright (c) 2011-2013 Weizoom Inc
*/

/**
 * 全局事件响应
 */
(function($) {
    //为需要校验的标签增加 星号提示
    $(document).ready(function() {
        var $labelEL = $('[data-validate^="requir"]').parent().prev();
        $labelEL.addClass("star_show");
        $('[data-validate^="requir"]').prev().addClass("star_show");
    });

    //为wx_delete元素安装删除确认机制
    $(document).ready(function(event) {
        xlog('install hander for wx_delete link')
        $(document).delegate('.wx_delete', 'click', function(event) {
            event.stopPropagation();
            event.preventDefault();
            var $el = $(event.currentTarget);
            var deleteCommentView = W.getItemDeleteView();
            deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
                window.location.href = $el.attr('href');
            });
            deleteCommentView.show({
                $action: $el,
                info: '确定删除吗?'
            });
        });
    });

    $(document).ready(function(event) {
        //实现swip images selector
        $('[data-ui-role="swipe-images-selector"]').each(function() {
            var $selector = $(this);
            var count = $selector.attr("data-count");
            var $targetInput = $($selector.attr('data-target-input'));
            var imageWidth = parseInt($selector.attr('data-image-width'));
            var imageHeight = parseInt($selector.attr('data-image-height'));
            var imagesJson = $selector.attr('data-images-json');
            var images = [];
            if (imagesJson) {
                var images = $.parseJSON($selector.attr('data-images-json'));
            }

            var view = new W.common.SwipeImagesSelectorView({
                el: $selector.get(),
                count: count,
                targetInput: $targetInput,
                images: images,
                selector: {
                    width: imageWidth,
                    height: imageHeight
                }
            });
            view.render();
            $selector.data('view', view);
        });

        //创建simulator
        $('[data-ui-role="embeded-simulator"]').each(function() {
            var $simulatorEl = $(this);
            var url = $simulatorEl.attr('data-url');
            var phone = new W.common.EmbededPhoneView({
                el: $simulatorEl.get(),
                mode: 'webapp',
                initBrowserUrl: url
            });
            $simulatorEl.data('view', phone);
            phone.render();
        });

        //创建image selector
        $('input[data-ui-role="image-selector"]').each(function() {
            var $imageInput = $(this);
            var width = parseInt($imageInput.attr('data-width'))
            var height = parseInt($imageInput.attr('data-height'));
            var $imageView = $imageInput.siblings('div[data-ui-role="image-selector-view"]').eq(0);
            var url = $imageInput.val();
            var view = new W.ImageView({
                el: $imageView.get(),
                picUrl: url,
                height: height,
                width: width,
                autoShowHelp: true
            });
            view.bind('upload-image-success', function(path) {
                $imageInput.val(path);
            });
            view.bind('delete-image', function() {
                $imageInput.val('');
            });
            view.render();
        });

        //创建paginator
        $('div[data-ui-role="paginator"]').each(function() {
            var $node = $(this);
            var el = $node.get(0);
            var pageinfo = $.parseJSON($node.attr('data-pageinfo'));
            var paginationView = new W.PaginationView({
                el: el,
                isHasDetailedPage: true,
                isHasJumpPage: true
            });
            paginationView.bind('goto', function(page) {
                window.location.href = paginationView.getTargetUrl(page);
            });
            paginationView.setPageInfo(pageinfo);
            paginationView.render();
        });

        //创建RichTextEditor
        $('textarea[data-ui-role="richtext-editor"]').each(function() {
            var $textarea = $(this);
            var type = $textarea.attr('data-type');
            var height = parseInt($textarea.attr('data-height'));
            var width = parseInt($textarea.attr('data-width'));
            var editor = new W.common.RichTextEditor({
                el: $textarea.get(),
                type: type,
                width: width,
                height:height,
                autoHeight:false,
                imgSuffix: "uid="+W.uid,
                wordCount: false
            });
            editor.render();
        });

	    //创建datepicker
	    // data-min和data-max可以有两种值：
	    //      一种为‘now’获取当天日期；
	    //      一种为‘2013年09月05日'日期，可以随意设置日期，但格式要和data-format一致。
	    $('input[data-ui-role="datepicker"]').each(function() {
		    var $datepicker = $(this);
		    var format = $datepicker.attr('data-format');
		    var min = $datepicker.attr('data-min');
		    var max = $datepicker.attr('data-max');
		    var $min_el = $($datepicker.attr('data-min-el'));
		    var $max_el = $($datepicker.attr('data-max-el'));
		    var options = {
			    buttonText: '选择日期',
			    numberOfMonths: 1,
			    dateFormat: format,
			    closeText: '关闭',
			    prevText: '&#x3c;上月',
			    nextText: '下月&#x3e;',
			    monthNames: ['一月','二月','三月','四月','五月','六月',
				    '七月','八月','九月','十月','十一月','十二月'],
			    monthNamesShort: ['一','二','三','四','五','六',
				    '七','八','九','十','十一','十二'],
			    dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
			    dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
			    dayNamesMin: ['日','一','二','三','四','五','六'],
			    beforeShow: function(e) {
				    if(min === 'now') {
						$(this).datepicker('option', 'minDate', new Date());
				    }else if(min){
					    $(this).datepicker('option', 'minDate', min);
				    }

                    if($min_el){
					    var startTime = $min_el.val();
					    if(startTime) {
						    $(this).datepicker('option', 'minDate', startTime);
					    }
                    }

				    if(max === 'now') {
					    $(this).datepicker('option', 'maxDate', new Date());
				    }else if(max){
					    $(this).datepicker('option', 'maxDate', max);
				    }

				    if($max_el){
					    var endTime = $max_el.val();
					    if(endTime) {
						    $(this).datepicker('option', 'maxDate', endTime);
					    }
				    }
			    },
			    onClose: function() {
			    }
		    };

		    $datepicker.datepicker(options);
	    });
    });

    $(document).ready(function() {
        //实现预览功能
        $('[data-ui-role="preview-button"]').click(function() {
            if (!W.validate()) {
                return false;
            }

            var $button = $(this);
            var $form = $($button.attr('data-target-form'));
            var data = {};
            $form.find('[name]').each(function() {
                var $field = $(this);
                var value = $field.val ? $field.val() : null;
                if (value) {
                    data[$field.attr('name')] = value;
                }
            });

            
            var app = $button.attr('data-app');
            var apiEntity = $button.attr('data-api-entity');
            W.getLoadingView().show();
            xlog(data);
            W.getApi().call({
                app: app,
                api: 'preview_'+apiEntity+'/create',
                method: 'post',
                args: data,
                success: function(data) {
                    W.getLoadingView().hide();

                    var $simulatorEl = $('[data-ui-role="embeded-simulator"]').eq(0);
                    var phone = $('[data-ui-role="embeded-simulator"]').eq(0).data('view');
                    var url = $simulatorEl.attr('data-url');
                    if (url.indexOf('?') == -1) {
                        url = url + '?is_preview=1';
                    } else {
                        url = url + '&is_preview=1';
                    }
                    phone.refreshBrowser(url);
                },
                error: function(resp) {
                    W.getLoadingView().hide();
                    alert('预览失败');
                }
            })
        });
    });

    //实现sortable-table
    $(document).ready(function(event) {
        /*在拖动时，拖动行的cell（单元格）宽度会发生改变。在这里做了处理就没问题了*/
        function storHelper(e, ui) {
            ui.children().each(function() {
                $(this).width($(this).width());
            });
            return ui;
        }

        /* 拖动结束后，提交排序结果 */
        function submitForSort($table) {
            var app = $table.attr('data-sort-app');
            var api = $table.attr('data-sort-api');
            var ids = [];
            $table.find("tbody tr").each(function() {
                var id = $(this).attr("data-id");
                ids.push(id);
            });

            W.getApi().call({
                app: app,
                api: api,
                args: {
                    ids: ids.join('_')
                },
                success: function(data) {
                    xlog('success');
                },
                error: function(resp) {
                    xlog('fail!');
                },
                scope: this
            });
        }

        $('table[data-ui-role="sortable-table"]').each(function() {
            var $table = $(this);
  
            /*
            $table.css({
                cursor: 'move'
            });
*/
            /*
            $table.find('tr').each(function() {
                //$(this).find('td').eq(0).find('div').prepend('<i class="icon-align-justify icon-white sortHandle"></i>');
                $(this).find('td').eq(0).addClass('sortHandle');
            });
*/

            //拖动排序
            $table.find("tbody").sortable({
                axis: 'y',
                cursor: 'move',
                helper: storHelper,
                handle: '.sortHandle',
                stop: _.bind(function(options) {
                    submitForSort($table);
                }, this)
            });
        });

	    W.common.disableSortable = function() {
		    $('.select_text').unbind('mousedown');
			$('.select_text').mousedown(function(event) {
			    var $tbody = $(event.currentTarget).parents('tbody');
			    $tbody.sortable('disable');
			    try{
				    $tbody.sortable('disable');
				    $('body').data('disableTbody', $tbody);
			    } catch (e) {
				}
		    });
	    }
	    W.common.disableSortable();

	    $('body').mouseup(function(event) {
		    var $tbody = $('body').data('disableTbody');
		    if($tbody){
			    $tbody.sortable('enable');
		    }
	    });
    });    
}(jQuery));