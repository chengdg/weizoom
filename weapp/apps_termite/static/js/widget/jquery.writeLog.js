//
$.writeLog = function(msg) {
    var isUnderDevelop = $('body').attr('is-under-develop') ? true : false;
    if(!isUnderDevelop) {
        return;
    }
    var $pageStatusLog = $('#pageStatusLog');
    if(!$pageStatusLog.length) {
        $('[data-role="page"]').append('<div id="pageStatusLog"></div>');
        $pageStatusLog = $('#pageStatusLog');
        $pageStatusLog.css({
            'font-size':'12px',
            'margin-bottom': '80px'
        });
    }
    
    var html = $pageStatusLog.html();
    var date = (new Date());
    var dataString = date.getHours() + ":" + date.getMinutes() + ':'+date.getSeconds();
    $pageStatusLog.html('<div style="border-top:1px dotted #ddd; padding:5px;">'+dataString+':&nbsp;&nbsp;'+msg+'</div>'+html);
};