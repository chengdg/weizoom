/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * app参与结果alert
*/
(function($) {
var alertTimeoutValue = null;
var initDom = function(options) {
    var $result = $('.wui-appParticipantResult-Cover');
    var prize = null;
    if (options && options.prize) {
        if (options.prize.type === 'coupon') {
            prize = '一张优惠券';
        } else if (options.prize.type === 'integral') {
            prize = '积分奖励'
        }
    }
    var actionButtons =[];
    if (prize){
        actionButtons.push({
            text:'个人中心',
            url:'/termite/workbench/jqm/preview/?module=user_center&model=user_info&action=get&workspace_id=mall&webapp_owner_id='+W.webappOwnerId
        });
    }

    if (options.actionButtons) {
        for(var i = 0; i < options.actionButtons.length; ++i) {
            var button = options.actionButtons[i];
            actionButtons.push(button);
        }
    }
    if ($result.length === 0) {
        var $body = $('body');
        var $node = $('\
            <div class="wui-appParticipantResult-Cover">\
                <div class="wui-i-background">\
                    <div class="wui-i-successIcon">&#10003</div>\
                    <div class="wui-i-successText">提交成功</div>\
                    <div class="wui-i-info"><div class="wui-i-info-prize">您获得了<span class="xa-appParticipantResult-prizeContent"></span><br/>赶紧去个人中心查看吧</div></div>\
                    <div class="wui-i-close xa-closeParticipantResult">&#10005</div>\
                </div>\
            </div>');
        $node.height(document.body.scrollHeight);
        if (actionButtons) {
            var $buttonContainer = $('<div>');
            $buttonContainer.addClass('wui-i-buttons-' + actionButtons.length);
            _.each(actionButtons, function(actionButton) {
                var $el = $('<a class="wui-i-button xa-link" data-href="'+ actionButton.url + '" href="javascript:void(0);">' + actionButton.text+ '</a>');
                $buttonContainer.append($el);
            });
            $node.find('.wui-i-info').append($buttonContainer);
        }
        if (prize) {
            $node.find('.xa-appParticipantResult-prizeContent').text(prize);
        } else {
            $node.find('.wui-i-info-prize').remove();
        }
        $body.append($node);

        $('.xa-closeParticipantResult').on('click', function(event) {
            $('.wui-appParticipantResult-Cover').hide();
        });
        $('.xa-link').on('click', function(event) {
            var $link = $(event.currentTarget);
            var url = $link.data('href');
            var text = $link.text();
            if (text.replace(/(^\s*)|(\s*$)/g,'') === '个人中心' && !W.member_id){
                $('.wui-appParticipantResult-Cover').html('<div class="wui-qrcode">' +
                '<img height="195px" width="195px" src="{% if auth_appid_info %}{{auth_appid_info.qrcode_url}}{% endif %}">' +
                '</div><div>');
            }
            else{
                $('.wui-appParticipantResult-Cover').hide();
                redirectTo(url);
            }



        });
    } else {
        $('.xa-appParticipantResult-prizeContent').text(prize);
        $result.show();
    }
}

$.fn.alertParticipantResult = function(options) {
    initDom(options);
};
} (Zepto))