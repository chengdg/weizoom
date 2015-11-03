/*
 * GMU连接拼装参数插件
 * 
 *
 * 使用示例;
 * <body data-ui-role="integralMechanism" data-value="{{ cur_request_member.token }}" data-key="fmt">
 * data-key // 拼装参数名
 * data-value // 拼装参数值
 * window.locationHref //方法，重置HREF。加上对积分的支持
 * author: jiangzhe
 */
 (function( $, undefined ) {

gmu.define('integralMechanism', {
    setting: {
        // isHideShare: function() {
        //     var href = window.location.href;
        //     var isHasArgs = href.indexOf('?sct=')>=0 || href.indexOf('&sct=')>=0;
        //     return isHasArgs;
        // },
        dataValue: function(_this) {
            return _this.$el.data('value');
        },
        dataKey: function(_this) {
            return _this.$el.data('key');
        }
    },
    _create : function() {
        this.setFmt();
        this.$el.data('view', this);
    },

    _bind: function() {

    },
    setFmt: function(value) {
        if(!value){
            value = this.setting.dataValue(this);
        }
        var key = this.setting.dataKey(this);
        KEY_NAME = key;
        DATA_VALUE = value;
        if(!value) {
            return;
        }
        var _this = this;
        $('a').each(function() {
            var href = this.getAttribute('href');
            var host = window.location.host;
            if(href && (href.match(/^(\.\/|\/)\S/g) || href.indexOf(host) >= 0)) {
                href = href.indexOf('?') >= 0 ? href + '&'+key+'=' + value : href + '?'+key+'=' + value;
                this.setAttribute('href', href);
                //xlog('把按钮"'+$(this).text().trim()+'"的href修改为:'+href);
            }
        });
    },
});

$(function() {
    $('[data-ui-role="integralMechanism"]').integralMechanism();
});
})( Zepto );
