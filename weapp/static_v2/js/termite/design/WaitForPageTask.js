 /**
 * cover管理器
 * @class
 */
W.design.requestForPage = function() {
    W.design.isPageReceived = false;
    var task = new W.DelayedTask(function() {
        xlog('[design page]: request for page by trigger designpage:wait_for_page event...');
        W.Broadcaster.trigger('designpage:wait_for_page');
        if (W.design.isPageReceived) {
            //退出
        } else {
            W.design.requestForPage();
        }
    });
    task.delay(50);
}


W.design.receivePage = function() {
    W.design.isPageReceived = true;
}