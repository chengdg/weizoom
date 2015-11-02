/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.GlobalNav widget
 */
(function( $, undefined ) {
gmu.define('GlobalNav', {
	options: {
	},
	
	_create: function() {
		var $el = this.$el;
		var is_member = $el.attr('data-member')
		var $globalNavBtn = $('<div class="wui-globalNavBtn"></div>');
		if (is_member == 'true') {
			var $globalLink = $('<div class="wui-globalLink em75">'
								+'<ul class="disF">'
									+'<li><a href="./?woid='+W.webappOwnerId+'&module=mall&model=homepage" class="wui-globalHome"><span class="disBl">返回首页</span></a></li>'
									+'<li><a class="wui-userCenter" href="./?module=user_center&model=user_info&action=get&workspace_id=mall&webapp_owner_id='+W.webappOwnerId+'"><span class="disBl">个人中心</span></a></li>'
									+'<li><a href="./?woid='+W.webappOwnerId+'&module=mall&model=shopping_cart&action=show" class="wui-shoppingCart"><span class="disBl">购物车</span></a></li>'
								+'</ul>'
							+'</div>');
		} else {
			var $globalLink = $('<div class="wui-globalLink em75">'
								+'<ul class="disF">'
									+'<li><a href="./?woid='+W.webappOwnerId+'&module=mall&model=homepage" class="wui-globalHome"><span class="disBl">返回首页</span></a></li>'
									+'<li><a href="./?woid='+W.webappOwnerId+'&module=mall&model=shopping_cart&action=show" class="wui-shoppingCart"><span class="disBl">购物车</span></a></li>'
									+'</ul>'
							+'</div>');
		}

        this.$el.append($globalNavBtn).append($globalLink);
	},
	show: function() {
		this.$el.find('.wui-globalLink').css({
            'display': 'inline-block'
        });
	},

	hide: function() {
		this.$el.find('.wui-globalLink').css({
            'display': 'none'
        });
	},
	delay:function(){
		var _this = this;
		setTimeout(function(){
        	_this.$el.globalNav('hide');
        },2000);
	},
	clickShow:function(){
		if($('.wui-globalLink').eq(0).css('display')=='none'){
        	this.$el.globalNav('show');
       	}else{
       		this.$el.globalNav('hide');
       	}
	}
});

$(function() {
	$('[data-ui-role="global-nav"]').each(function() {
		var $globalNav = $(this);
		$globalNav.globalNav('hide');
	});

    $('body').bind('touchstart', function(event){
        if(!$(event.target).is('.wui-globalNavBtn')){
            $('[data-ui-role="global-nav"]').globalNav('delay');
        }
    });
    $('body').bind('touchmove',function(){
        $('[data-ui-role="global-nav"]').globalNav('delay');
    });

    $('.xa-globalNav').click(function(){
       $(this).globalNav('clickShow');
    });
})
})( Zepto );