/*
Copyright (c) 2011-2013 Weizoom Inc
*/

/**
 * 全局事件响应
 */
$(document).ready(function(event) {
    //为需要校验的标签增加 星号提示
    $(document).ready(function() {
        $('[data-validate^="requir"]').each(function() {
            var $input = $(this);
            $controlGroup = $input.parents('.form-group');
            if ($controlGroup.length > 0 && !$input.parents('.form-group').hasClass('nostar')) {
                $controlGroup.find('label').eq(0).addClass('star_show');
            }
        });
    });

    //为wx_delete元素安装删除确认机制
    xlog('install hander for wx_delete link')
    // $(document).delegate('.wx_delete', 'click', function(event) {
    //     event.stopPropagation();
    //     event.preventDefault();
    //     var $el = $(event.currentTarget);
    //     var deleteCommentView = W.getItemDeleteView();
    //     deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
    //         window.location.href = $el.attr('href');
    //     });
    //     deleteCommentView.show({
    //         $action: $el,
    //         info: '确定删除吗?'
    //     });
    // });
});