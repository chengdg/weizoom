/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 处理xa-contenteditable
 */
$(document).ready(function() {
    $.fn.editable = function() {
        var $container = $(this);
        var $els = $container.find('.xa-contenteditable');
        $els.each(function() {
            var $el = $(this);
            $el.data('oldValue', $.trim($el.text()));
        });

        $els.addClass('xui-contenteditable').attr('contenteditable', 'true');
    }
    $('body').editable();

    $(document).delegate('.xa-contenteditable', 'blur', function(event) {
        var $el = $(event.currentTarget);
        var value = $.trim($el.text());
        var oldValue = $el.data('oldValue');
        if (value !== oldValue) {
            $el.data('oldValue', value);
            $el.addClass('xui-dirtyContent');
        }
    });

    $(document).delegate('.xa-contenteditable', 'focus', function(event) {
        var $el = $(event.currentTarget);
        var initValue = $el.data('initValue');
        var value = $.trim($el.text());
        if (value === initValue) {
            $el.text('');
        }
    });

    $(document).delegate('.xa-contenteditable', 'keypress', function(event) {
        var keyCode = event.keyCode;
        if(keyCode === 13) {
            $(event.currentTarget).blur();
            event.stopPropagation();
            event.preventDefault();
        }
    });
});
