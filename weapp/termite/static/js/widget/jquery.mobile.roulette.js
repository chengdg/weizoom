/*
 * Jquery Mobile地址选择插件
 * 
 * author: tianyanrong
 */
(function($, undefined) {
    var RouletteCanvas = function(options) {
        this.el = options.el;
        this.width = options.width;
        this.height = options.height;
        this.imagesUrl = options.imagesUrl;
        this.defaluteValue = parseInt(options.defaluteValue, 10);
        this.ctx = this.el.getContext("2d");
        this.setRoulette();
        this.init();
    };
    RouletteCanvas.prototype = {
        init: function() {
            this.roundTimeout = null;
            this.stopTimeout = null;
            this.angleDeg = 0.4;
            this.angle = 0;
            this.deg = 0;
            this.resulteId = null;
        },
        
        getResulteOptions: {
            0: [1.1, 3.1, 5.2], //谢谢参与
            1: [0], //一等奖
            2: [4.2], //二等奖
            3: [2.1] //三等奖
        },
        
        setRoulette: function() {
            var _this = this;
            
            this.pic = new Image(); 
            this.pic.src = this.imagesUrl;
            
            this.pic.onload = function() {
                _this.ctx.drawImage(_this.pic, 0, 0, _this.width, _this.height);
                if(_this.getResulteOptions[_this.defaluteValue]) {
                    _this.loop(_this.getResulteOptions[_this.defaluteValue][0]);
                }
            };
            
        },
        
        getResulte: function(resulteId) {
            var angleDeg = this.angleDeg;
            var currentDeg = this.deg;
            var options = this.getResulteOptions[parseInt(resulteId, 10)];
            var i, k;
            var isStop = false;
            
            for(i = 0, k = options.length; i < k; i++) {
                if(options[i] === currentDeg) {
                    isStop = true;
                }
            }
            return isStop;
        },

        stop: function(resulteId) {
            var _this = this;
            this.resulteId = resulteId;
            if(this.stopTimeout) {
                clearInterval(this.stopTimeout);
                this.stopTimeout = null;
            }
            
            this.stopTimeout = setTimeout(function() {
                clearInterval(_this.stopTimeout);
                _this.stopTimeout = null;
                var angleDeg = (parseInt(_this.angleDeg*10, 10))/10;
                if(angleDeg > 0.1) {
                    _this.angleDeg = (parseInt(_this.angleDeg*10, 10)-1)/10;
                    _this.stop(resulteId);
                }
            }, 500);
        },
        
        start: function(isStart) {
            var _this = this;
            if(this.roundTimeout) {
                clearInterval(this.roundTimeout);
                this.roundTimeout = null;
            }
            
            if(this.resulteId || 0 === this.resulteId) {
                var isStop = this.getResulte(this.resulteId) && this.angleDeg === 0.1;
                if(isStop) {
                    if(this.stopTimeout) {
                        clearInterval(this.stopTimeout);
                        this.stopTimeout = null;
                    }
                    this.init();
                    $(this.el).trigger('can-start');
                    return false;
                }
            }
            
            this.roundTimeout = setTimeout(function() {
                 clearInterval(_this.roundTimeout);
                _this.roundTimeout = null;
                _this.loop();
                _this.start();
            }, 10)
        },
        
        DegToRad: function(d) {
            return d * this.angleDeg;
        },
        
        loop: function(deg) {
            if(deg) {
                 this.deg = deg;
            }else {
                if(this.deg && this.deg >= 6) {
                    this.angle = 0;
                }
                this.deg = this.DegToRad(this.angle);
            }
            var ctx = this.ctx;
            ctx.save();
            ctx.translate(this.width * 0.5, this.width * 0.5);
            ctx.rotate(this.deg);
            ctx.translate(-this.width * 0.5, -this.width * 0.5);
            ctx.drawImage(this.pic, 0, 0, this.width, this.height);
            ctx.restore();
            this.angle += 1;
        }
    };
    
    $.widget("mobile.roulette", $.mobile.widget, {
        options: {
            passwordText: ['谢谢参与', '一等奖', '二等奖', '三等奖'],
            imagesUrl: {
                box: '/static/img/widget/roulette/box.png',
                roulette: '/static/img/widget/roulette/roulette.png',
                startButton: '/static/img/widget/roulette/startButton.png'
            }
        },
        
        setting: {
            app: '',
            api: '',
            args: {},
            canPlayCount: '',
            defaluteValue: function(_this) {
                return _this.$el.attr('defalute-value');
            }
        },
    
        _create: function() {
            this.$el = this.element;
            this.isStart = false;
            this.setting.api = this.$el.attr('api');
            this.setting.app = this.$el.attr('app');
            this.setting.args = this._evalJson(this.$el.attr('args'));
            this.setting.canPlayCount = this.$el.attr('can-play-count');
            this._buildTemplate();
            this._bindEvents();
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
            this.$el.delegate('.tx_start', 'click', function() {
                _this._startRound();
            });
            this.$el.bind('can-start', function() {
                _this._alert();
                _this.$el.trigger('complate', {
                    integral: _this.integral
                });
            });
        },
        
        _alert: function() {
            var name = ['', '一等奖', '二等奖', '三等奖'];
            var _this = this;
            if(this.prizeRank) {
                $('.ui-page').alert({
                    isShow: true,
                    info: '恭喜您中了' + name[this.prizeRank],
                    isSlide: true,
                    speed: 2000,
                    callBack: function() {
                        _this._setCanPlay();
                    }
                });
            }
            else {
                _this._setCanPlay();
            }            
        },
        
        _startRound: function() {
            if(this.isStart) {
                return;
            }
            this.$el.trigger('start');
            this._setCanPlay('false');
            this.canvasView.start(true);
            var _this = this;
            W.getApi().call({
                api: this.setting.api,
                app: this.setting.app,
                args: this.setting.args,
                timeout: 2000,
                success: function(data) {
                    _this.setting.canPlayCount = parseInt(data.can_play_count, 10) > 0 ? parseInt(data.can_play_count, 10) : 0;
                    _this.prizeRank = parseInt(data.prize_rank, 10);
                    _this.canvasView.stop(_this.prizeRank);
                    _this.integral = data.member_integral;
                },
                error: function(resp) {
                    _this.prizeRank = 0;
                    _this.canvasView.stop(0);
                }
            });
        },
        
        _setCanPlay: function(isCanPlay) {
            if(!isCanPlay) {
                isCanPlay = parseInt(this.setting.canPlayCount, 10) ? true : false;
            }else {
                isCanPlay = isCanPlay === 'true' ? true : false;
            }
            if(!isCanPlay) {
                this.isStart = true;
                this.$startButton.css({
                    'background-position': 'center bottom'
                });
            }
            else {
                this.isStart = false;
                this.$startButton.css({
                    'background-position': 'center 0px'
                });
            }
        },
        
        _buildTemplate: function() {
            var width = this.$el.width() || 100;
            var height = width;
            var html = '<div class="xui-roulette" style="width:'+width+'px; height: '+height+'px;position:relative;">' +
                        '<canvas width="'+width+'" height="'+height+'" class="xui-roulette-roulette"></canvas>'+
                        '<div class="xui-roulette-box"><a class="tx_start" href="javascript:void(0);"></a></div>'+
                        '</div>';
            this.$el.html(html);
            
            this.$roulette = this.$el.find('.xui-roulette-roulette');
            this.$box = this.$el.find('.xui-roulette-box');
            this.$box.css({
                width: width+'px',
                height: height+'px',
                position: 'absolute',
                top:'0px',
                left:'0px',
                background: 'url('+this.options.imagesUrl.box+') no-repeat center center',
                'z-index': '101',
                '-webkit-background-size': '100% auto',
                '-moz-background-size': '100% auto',
                '-o-background-size': '100% auto',
                'background-size': '100% auto'
            });
            this.$startButton = this.$el.find('.xui-roulette-box a.tx_start');
            this.$startButton.css({
                width: '15%',
                height: '15%',
                position: 'absolute',
                top:'50%',
                left:'50%',
                margin: '-7.5% 0 0 -7.5%',
                background: 'url('+this.options.imagesUrl.startButton+') no-repeat center 0',
                'z-index': '101',
                '-webkit-background-size': '100% auto',
                '-moz-background-size': '100% auto',
                '-o-background-size': '100% auto',
                'background-size': '100% auto'
            });
            var _this = this;
            _this.canvasView = new RouletteCanvas({
                el: _this.$el.find('canvas')[0],
                width: width,
                height: height,
                defaluteValue: _this.setting.defaluteValue(_this),
                imagesUrl: _this.options.imagesUrl.roulette
            });
            
            this._setCanPlay();
            
        }
    });
	// taking into account of the component when creating the window
	// or at the create event
    $(document).bind("pagecreate create", function(e) {
        $(":jqmData(ui-role=roulette)", e.target).roulette();
	});
})(jQuery);
