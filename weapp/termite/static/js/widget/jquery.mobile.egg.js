/*
 * Jquery Mobile地址选择插件
 * 
 * author: tianyanrong
 */
(function($, undefined) {
    $.widget("mobile.egg", $.mobile.widget, {
        options: {
            rankText: ['谢谢参与', '一等奖', '二等奖', '三等奖'],
            imagesUrl: {
                egg: '/static/img/widget/egg/egg.png',
                egged: '/static/img/widget/egg/egged.png',
                hammer: '/static/img/widget/egg/hammer.png'
            }
        },
        
        setting: {
            //应用名
            app: function(_this) {
                return _this.$el.attr('app');
            },
            //应用api
            api: function(_this) {
                return _this.$el.attr('api');
            },
            //参数
            args: function(_this) {
                return _this._evalJson(_this.$el.attr('args')) || {};
            },
            //名次
            rankNumber: function(_this) {
                return _this.$el.attr('rank-number') || 0;
            },
            //是否已刮过
            isHadPlay: function(_this) {
                return _this.$el.attr('is-had-play') ? true : false;
            },
            //是否是移动端
            isMobile: function(_this) {
                return _this.$el.attr('is-mobile') ? true : false;
            },
            //是否能玩
            isCanPlay: function(_this) {
                return _this.$el.attr('is-can-play') ? true : false;
            },
            //不能玩的原因
            notPlayReason: function(_this) {
                return _this.$el.attr('not-play-reason');
            },
            //上次被砸金蛋的位置
            lastEggPosition: function(_this) {
                return _this.$el.attr('last-egg-position') || '0';
            },
        },
    
        _create: function() {
            this.$el = this.element;
            this.isHadPlay = false;
            this._buildTemplate();
            this._bindEvents();
            this._setStyle();
            
            //判断金蛋是否被砸
            if(this.setting.isHadPlay(this)) {
                this._setSmashedEgg(this.setting.lastEggPosition(this));
            }
            else {
                this._setAnimation();
                var _this = this;
                setTimeout(function() {
                    _this._playAnimation();
                }, 10)
            }
            
        },
        
        _evalJson: function(x) {
            try{
                x = (new Function('return (' + x +')'))();
            }catch(e){
                if('string' === typeof x && x.indexOf('":')){
                    
                }
            }
            return x;
        },
        
        _bindEvents: function() {
            var _this = this;
            this.$el.delegate('.tx_btnEgg', 'click', function(event) {
                _this._smashEgg(event);
            });
        },
        
        _alert: function(msg, speed) {
            if(msg) {
                $('.ui-page').alert({
                    isShow: true,
                    info: msg,
                    isSlide: true,
                    speed: speed || 2000,
                    callBack: function() {
                        
                    }
                });
            }  
        },
        
        
        _smashEgg: function(event) {
            if(!this.setting.isCanPlay(this)) {
                this._alert(this.setting.notPlayReason(this))
                return;
            }
            
            if(this.isHadPlay) {
                return;
            }
            
            var value = $(event.currentTarget).attr('value');
            this._setSmashedEgg(value);
            
            this.$el.trigger('start');
            
            var args = this.setting.args(this);
            args['last_egg_position'] = value;
            var _this = this;
            W.getApi().call({
                api: this.setting.api(this),
                app: this.setting.app(this),
                args: args,
                success: function(data) {
                    _this.$el.trigger('complate', {integral: data.member_integral});
                   
                },
                error: function(resp) {
                    
                }
            });
            var rankNumber = this.setting.rankNumber(this);
            if(rankNumber > 0) {
                this._alert('恭喜您中了' + this.options.rankText[rankNumber], 5000)
            }
        },
                
        _setSmashedEgg: function(value) {
            this.isHadPlay = true;
            this.$el.find('.tx_btnEgg[value="'+value+'"]').css({
                'background': 'url('+this.options.imagesUrl.egged+') no-repeat',
            });
            
            this.$hammer.remove();
        },
        
        _setStyle: function() {
            this.$hammer = this.$hammer || this.$el.find('.tx_hammer');
            this.$el.css({
                'position': 'relative',
                'margin': '0 auto',
                'width': '250px',
                'height': '120px'
            })
            this.$el.find('.tx_btnEgg').css({
                'display': 'inline-block',
                'width': '80px',
                'height': '94px',
                'background': 'url('+this.options.imagesUrl.egg+') no-repeat',
                'color': '#FFCC22',
                'font-size': '30px',
                'line-height': '90px',
                'font-weight': 'bold',
                'text-align': 'center',
                'margin-top': '25px'
            });
            this.$hammer.css({
                'display': 'inline-block',
                'width': '50px',
                'height': '58px',
                'background': 'url('+this.options.imagesUrl.hammer+') no-repeat',
                'position': 'absolute',
                'top': '0px',
                'left': '55px',
                'z-index': 2
            });
        },
        
        _setAnimation: function() {
            var style = document.createElement('style');
            document.head.appendChild(style);
            style.innerHTML = '\
            @-keyframes egg{0%{transform: translate(0,0px);}20%{transform: translate(0,5px);}50%{transform: translate(0,0px);}70%{transform: translate(0,5px);}100%{transform: translate(0,0px);}}\
            @-moz-keyframes egg{0%{-moz-transform: translate(0,0px);}20%{-moz-transform: translate(0,5px);}50%{-moz-transform: translate(0,0px);}70%{-moz-transform: translate(0,5px);}100%{-moz-transform: translate(0,0px);}}\
            @-webkit-keyframes egg{0%{-webkit-transform: translate(0,0px);}20%{-webkit-transform: translate(0,5px);}50%{-webkit-transform: translate(0,0px);}70%{-webkit-transform: translate(0,5px);}100%{-webkit-transform: translate(0,0px);}}\
            @-keyframes hammer{0%{transform:rotate(0deg);transform-origin:bottom;}20%{transform:rotate(-20deg);transform-origin:bottom;}50%{transform:rotate(-10deg);transform-origin:bottom;}70%{transform:rotate(-5deg);transform-origin:bottom;}100%{transform:rotate(0deg);transform-origin:bottom;}}\
            @-moz-keyframes hammer{0%{-moz-transform:rotate(0deg);-moz-transform-origin:bottom;}20%{-moz-transform:rotate(-20deg);-moz-transform-origin:bottom;}50%{-moz-transform:rotate(-10deg);-moz-transform-origin:bottom;}70%{-moz-transform:rotate(-5deg);-moz-transform-origin:bottom;}100%{-moz-transform:rotate(0deg);-moz-transform-origin:bottom;}}\
            @-webkit-keyframes hammer{0%{-webkit-transform:rotate(0deg);-webkit-transform-origin:bottom;}20%{-webkit-transform:rotate(-20deg);-webkit-transform-origin:bottom;}50%{-webkit-transform:rotate(-10deg);-webkit-transform-origin:bottom;}70%{-webkit-transform:rotate(-5deg);-webkit-transform-origin:bottom;}100%{-webkit-transform:rotate(0deg);-webkit-transform-origin:bottom;}}\
            ';
        },
        
        _playAnimation: function() {
            this.$egg = this.$egg || this.$el.find('.tx_btnEgg');
            this.$hammer = this.$hammer || this.$el.find('.tx_hammer');
            this.$egg.css({
                'animation': 'egg 1s ease-in-out infinite',
                '-moz-animation': 'egg 1s ease-in-out infinite',
                '-webkit-animation': 'egg 1s ease-in-out infinite',
                '-o-animation': 'egg 1s ease-in-out infinite'
            });
            this.$hammer.css({
                'animation': 'hammer 0.8s ease-in-out infinite',
                '-moz-animation': 'hammer 0.8s ease-in-out infinite',
                '-webkit-animation': 'hammer 0.8s ease-in-out infinite',
                '-o-animation': 'hammer 0.8s ease-in-out infinite'
            })
        },
        
        _buildTemplate: function() {
            var width = 240;
            var height = 120;
            var html = '<span class="tx_hammer"></span>\
                        <a href="javascript:void(0);" class="tx_btnEgg" value="1">1</a>\
                        <a href="javascript:void(0);" class="tx_btnEgg" value="2">2</a>\
                        <a href="javascript:void(0);" class="tx_btnEgg" value="3">3</a>';
            this.$el.html(html);            
        }
    });
	// taking into account of the component when creating the window
	// or at the create event
    $(document).bind("pagecreate create", function(e) {
        $(":jqmData(ui-role=egg)", e.target).egg();
	});
})(jQuery);
