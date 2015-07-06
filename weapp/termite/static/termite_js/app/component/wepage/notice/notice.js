/**
 * @class W.component.wepage.Title
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.Title = W.component.Component.extend({
	type: 'wepage.notice',
	propertyViewTitle: '公告',
    className:'xui-noticeEditor',

	properties: [
        {
            group: '属性1',
            fields: [{
                name: 'title', 
                type: 'text',
                displayName: '公告',
                isUserProperty: true,
                placeholder:'请填写内容，如果过长，将会在手机上滚动显示',
                default: '请填写内容，如果过长，将会在手机上滚动显示'
            }]
        }
    ],

    propertyChangeHandlers: {
    	title: function($node, model, value) {            
            value = this.getDisplayValue(value, 'title');
            $node.find('.wa-inner-title').text("公告："+value);
            W.Broadcaster.trigger('component:resize', this);
        }
    },
    initialize: function(obj) {
        this.super('initialize', obj);
        this.delayWidth();
    },

    delayWidth: function(){
        if( W.editModel){
            return false;
        }
        var _this = this;
        _.delay(function() {
            var $notice = $(window.frames[0].document.body).find('.wui-notice');
            var $title = $(window.frames[0].document.body).find('.wui-notice .wa-inner-title');
            var width = 0;
            var contentWidth = 0;
            if ($notice.length > 0){
                $notice.each(function() {
                    width = $(this).width();
                    contentWidth = $(this).find('.wa-inner-title').width();
                    rollWidth = width*0.9;
                    if( contentWidth == rollWidth || contentWidth > rollWidth){
                        _this.textRollFunction($(this));
                    }
                });
            }
        }, 2500);
    },

    textRollFunction:function($notice){
        var mytimer = null;
        var nowleft = 0;
        var width = 0;
        var contentWidth = 0;
        var $content = $notice.find('.wa-content');
        width = $notice .width();
        contentWidth = $content.width();
            // window.clearInterval(mytimer);

            mytimer = window.setInterval(function(){
                if( nowleft == -contentWidth ){
                    nowleft = width;
                }else{
                    nowleft = nowleft - 1;
                }
                $content.css('left',nowleft);
            },15);
        
    }

}, {
    indicator: {
        name: '标题',
        imgClass: 'componentList_component_notice'
    }
});
