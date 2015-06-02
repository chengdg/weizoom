/*
 * Jquery Mobile地址选择插件
 * 
 * <div class="xui-scratchcard-card-widget" data-ui-role="scratchCard" app="m/health" api="scratch_card_record/{{ webapp_id }}" args="{id: '{{ scratch_card.id}}', is_prize: '{{ is_can_prize }}', prize_rank: '{{ prize_rank }}'}" is-had-scratched="{% if is_can_prize %}{% else %}true{% endif %}" is-mobile="true" is-can-play="{% if is_can_play %}true{% endif %}" not-play-reason="{{not_play_reason}}" scratch-rank="{{ prize_rank }}"></div>
 * app:
 * api:
 * args:
 * is-had-scratched: 'true' || '' //是否已被刮过
 * is-mobile: 'true' || '' //是否为手机端--(已升级，这个参数不需要了)
 * is-can-play: 'true' || ''  //是否能玩
 * not-play-reason: '不能玩的原因'
 * scratch-rank: '1' //中奖[0, 1, 2, 3]==['谢谢参与', '一等奖', '二等奖', '三等奖']
 *
 * author: tianyanrong
 */
(function($, undefined) {
    var ScratchCard = function(options) {
        this.el = options.el;
        this.width = options.width;
        this.height = options.height;
        this.isMobile = this.browser.versions.mobile;
        this.isCanPlay = options.isCanPlay;
        this.lastX = 0;
        this.lastY = 0;
        var canvasOffset = $(this.el).offset();
        this.offsetX = canvasOffset.left;
        this.offsetY = canvasOffset.top;
        this.isMouseDown = false;
        this.ctx = this.el.getContext("2d");
        this.setBackground();
        this.bindEvent(this.isMobile);
    };
    ScratchCard.prototype = {
        browser: {
            versions : function() {
                var u = navigator.userAgent, app = navigator.appVersion;
                return {//移动终端浏览器版本信息                                
                    trident : u.indexOf('Trident') > -1, //IE内核                                
                    presto : u.indexOf('Presto') > -1, //opera内核                                
                    webKit : u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核                                
                    gecko : u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1, //火狐内核                               
                    mobile : !!u.match(/AppleWebKit.*Mobile.*/)
                    || !!u.match(/AppleWebKit/), //是否为移动终端                                
                    ios : !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端                
                    android : u.indexOf('Android') > -1 || u.indexOf('Linux') > -1, //android终端或者uc浏览器                                
                    iPhone : u.indexOf('iPhone') > -1 || u.indexOf('Mac') > -1, //是否为iPhone或者QQHD浏览器                   
                    iPad: u.indexOf('iPad') > -1, //是否iPad      
                    webApp : u.indexOf('Safari') == -1,//是否web应该程序，没有头部与底部
                    google:u.indexOf('Chrome')>-1
                };
            }(),
            language : (navigator.browserLanguage || navigator.language).toLowerCase()
        },
    
        setBackground: function() {
            var ctx = this.ctx;
            var grd = ctx.createLinearGradient(0,0,this.width,this.height);
            grd.addColorStop(0,"#9F9F9F");
            ctx.fillStyle = grd;
            ctx.fillRect(0,0,this.width,this.height);
        },
        
        bindEvent: function(isMobile) {
            var _this = this;
            if(isMobile) {
                this.el.addEventListener("touchstart", function(event) {
                    _this.touchstart(event);
                }, false);
                this.el.addEventListener("touchend", function(event) {
                    _this.touchend(event);
                }, false);
                this.el.addEventListener("touchmove", function(event) {
                    _this.touchmove(event);
                }, false);
            }
            else {
                this.el.addEventListener("mousedown", function(event) {
                    _this.touchstart(event);
                }, false);
                this.el.addEventListener("mouseup", function(event) {
                    _this.touchend(event);
                }, false);
                this.el.addEventListener("mousemove", function(event) {
                    _this.touchmove(event);
                }, false);
            }
        },
        
        touchstart: function(event){
            event = event.touches && event.touches[0] ? event.touches[0] : event;
            mouseX=parseInt(event.clientX - this.offsetX);
            mouseY=parseInt(event.clientY - this.offsetY);

            // Put your mousedown stuff here
            this.lastX=mouseX;
            this.lastY=mouseY;
            if(this.isCanPlay) {
                this.isMouseDown = true;
                $(this.el).trigger('start');
            }
            else {
                $(this.el).trigger('notCanPlay');
                //this.alertError();
            }
        },        
        
        touchend: function(event){
            event = event.touches && event.touches[0] ? event.touches[0] : event;
            mouseX=parseInt(event.clientX - this.offsetX);
            mouseY=parseInt(event.clientY - this.offsetY);

            // Put your mouseup stuff here
            this.isMouseDown = false;
        },
        
        touchmove: function(event){
            event.preventDefault(); //阻止滚动  
            event = event.touches && event.touches[0] ? event.touches[0] : event;
            mouseX=parseInt(event.clientX - this.offsetX);
            mouseY=parseInt(event.clientY - this.offsetY);
            var differValue = this.isMobile ? 0 : 0;
            var lastX = this.lastX;
            var lastY = this.lastY;
            var ctx = this.ctx;
            // Put your mousemove stuff here
            if(this.isMouseDown){
                ctx.beginPath();
                ctx.lineJoin = "miter";
                ctx.globalCompositeOperation="destination-out";
                ctx.arc(lastX, lastY-differValue, 10, 0, Math.PI*2, false);
                ctx.fill();
                this.lastX = mouseX;
                this.lastY = mouseY;
            }
        }
    };
    
    
    $.widget("mobile.scratchCard", $.mobile.widget, {
        options: {
            passwordText: ['谢谢参与', '一等奖', '二等奖', '三等奖']
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
            scratchRank: function(_this) {
                return _this.$el.attr('scratch-rank') || 0;
            },
            //是否已刮过
            isHadScratched: function(_this) {
                return _this.$el.attr('is-had-scratched') ? true : false;
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
    
        _create: function() {
            this.$el = this.element;
            this._buildTemplate();
            this._bindEvents();
        },
        
        _bindEvents: function() {
            var _this = this;
            
            //绑定不能玩的事件
            this.$el.bind('notCanPlay', function() {
                _this._alertError();
            });
            
            //绑定开始划的事件
            this.$el.bind('start', function() {
                if(_this.isSart) {
                    return;
                }
                _this.isSart = true;
//                W.getApi().call({
//                    api: _this.setting.api(_this),
//                    app: _this.setting.app(_this),
//                    args: _this.setting.args(_this),
//                    success: function(data) {
//                        if(data.member_integral) {
//                            _this.$el.trigger('complate', {integral: data.member_integral});
//                        }
//                    },
//                    error: function(resp) {
//
//                    }
//                });
	             _this.$el.trigger('complate', {});
            });
        },
        
        _buildTemplate: function() {
            var width = this.$el.width() || 80;
            var height = this.$el.height() || 40;
            var scratchRank = this.setting.scratchRank(this);
            var isHadScratched = this.setting.isHadScratched(this);
            var canvasCss = isHadScratched ? 'display:none' : '';
            
            var html = '<div class="xui-scratchCard" style="width:'+width+'px; height: '+height+'px; line-height:'+height+'px; text-align:center; position:relative;">' +
                        '<span class="tx_rank_lay"></span>'+
                        '<canvas width="'+width+'" height="'+height+'" style="position:absolute; top:0px; left:0px; '+canvasCss+'"></canvas>'+
                        '</div>';
            this.$el.html(html);
            
            var _this = this;
            setTimeout(function() {
                _this.canvasView = new ScratchCard({
                    el: _this.$el.find('canvas')[0],
                    width: width,
                    height: height,
                    isMobile: _this.setting.isMobile(_this),
                    isCanPlay: _this.setting.isCanPlay(_this),
                    textContent: _this.options.passwordText[scratchRank]
                });
                _this.$el.find('.tx_rank_lay').text(_this.options.passwordText[scratchRank]);
                _this.$el.find('.xui-scratchCard').css({
                    background: '#FEE301'
                })
            }, 0)
            
        },
        
        _alertError: function() {
            $('.ui-page').alert({
                isShow: true,
                info: this.setting.notPlayReason(this),
                isSlide: true,
                speed: 2000
            });
        }
    });
	// taking into account of the component when creating the window
	// or at the create event
    $(document).bind("pagecreate create", function(e) {
        $(":jqmData(ui-role=scratchCard)", e.target).scratchCard();
	});
})(jQuery);
