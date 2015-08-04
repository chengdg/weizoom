/*
 * Jquery Mobile大转盘
 * 
 * author: tianyanrong
 */
(function($, undefined) {    
    $.widget("mobile.roulette", $.mobile.widget, {
        options: {
            lineCount: {
                '1': 3,
                '2': 3,
                '3': 3,
                '4': 4
            },
            lineNames: {
                '1': ['一等奖', '谢谢参与', '谢谢参与', '谢谢参与', '谢谢参与', '谢谢参与'],
                '2': ['一等奖', '谢谢参与', '谢谢参与', '二等奖', '谢谢参与', '谢谢参与'],
                '3': ['一等奖', '谢谢参与', '二等奖', '谢谢参与', '三等奖', '谢谢参与'],
                '4': ['一等奖', '谢谢参与', '二等奖', '谢谢参与', '三等奖', '谢谢参与', '四等奖', '谢谢参与']
            },
            rankInfo: {
                '1': [1, 0, 0, 0, 0, 0],
                '2': [1, 0, 0, 2, 0, 0],
                '3': [1, 0, 2, 0, 3, 0],
                '4': [1, 0, 2, 0, 3, 0, 4, 0]
            },
//	        rotateDeg : {
//		        '1' : '31deg',
//		        '2' : '31deg',
//		        '3' : '31deg',
//		        '4' : '22.5deg'
//	        },
            imagesUrl: {
                startButton: '/markettools_static/lottery/img/roulette/startButton.png'
            }
        },
        
        setting: {
            app: function(_this) {
                return _this.$el.attr('app');
            },
            api: function(_this) {
                return _this.$el.attr('api');
            },
            args: function(_this) {
                return _this._evalJson(_this.$el.attr('args'));
            },
            canPlayCount: function(_this) {
                return _this.$el.attr('can-play-count');
            },
            defaluteValue: function(_this) {
                return _this.$el.attr('defalute-value');
            },
            lotteryCount: function(_this) {
                return _this.$el.attr('lottery-count') || '3';
            },
	        not_win_desc : function(_this){
		        return _this.$el.attr('not_win_desc');
	        }
        },


        _create: function() {
            this.$el = this.element;
            this.isStart = false;
            this.setting.api = this.setting.api(this);
            this.setting.app = this.setting.app(this);
            this.setting.args = this.setting.args(this);
            this.setting.canPlayCount = this.setting.canPlayCount(this);
	        this.setting.not_win_desc = this.setting.not_win_desc(this);
            this._buildTemplate();
            this._bindEvents();
        },

//	    _rotateDeg :'',//存储指针初始位置
        
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
        },
        
        _alert: function(msg) {
            $('.ui-page').alert({
                isShow: true,
                info: msg,
                isSlide: true,
                speed: 2000,
                callBack: function() {
                    
                }
            });        
        },
        
        _setRouletteStart: function() {
            this.$el.addClass('xui-roulette-widget-start');
        },
        _stopRouletteStop: function(deg) {
            this.$el.removeClass('xui-roulette-widget-start');
            this.$content.css({
                'transform':'rotate('+deg+'deg)',
                '-moz-transform':'rotate('+deg+'deg)',
                '-webkit-transform':'rotate('+deg+'deg)',
                'animation': '',
                '-moz-animation': '',
                '-webkit-animation': '',
                '-o-animation': ''
            });
            this._setCanPlay();
            if(this.prizeRank) {
                this._alert('恭喜您中了'+this.prizeName);
            }
            else {
                this._alert(this.setting.not_win_desc);
            }
	        this.$button.css({
                    'background-position': 'center bottom'
                });
	        this.$el.removeClass('xui-roulette-widget-can-play');
            this.$el.trigger('complate', {
                integral: this.integral
            });
        },
        
        _setRouletteStop: function(time) {
            time = time || 0.5;
            time = time + 1;
            var _this = this;
            
            
            
            if(this.stopValue) {
                clearTimeout(this.stopValue);
                this.stopValue = null;
            }
            this.stopValue = setTimeout(function() {
                clearTimeout(_this.stopValue);
                _this.stopValue = null;
                _this.$content.css({
                    'animation': 'roulette '+time+'s linear infinite',
                    '-moz-animation': 'roulette '+time+'s linear infinite',
                    '-webkit-animation': 'roulette '+time+'s linear infinite',
                    '-o-animation': 'roulette '+time+'s linear infinite'
                });
                
                if(time < 1.5) {
                    _this._setRouletteStop(time);
                }
                else {
                    var degs = _this.getResultDeg();
                    _this.getStopPostion(_this.prizeRank, degs);
                }
            }, time * 1000);
        },
        
        getResultDeg: function() {
            var lotteryCount = this.setting.lotteryCount(this);
            var rankInfo = this.options.rankInfo[lotteryCount];
            var maxLength = rankInfo.length;
            var position = {}, i;
            var eachDeg = 360/maxLength;
            for(i = 0; i < maxLength; i++){
                var start = -(i * eachDeg)-10;
                var end  = -(i * eachDeg)+10;
                start = start >= 0 ? start : 360+start;
                end = end >= 0 ? end : 360+end;
                position[rankInfo[i]] = {
                    start: start,
                    end: end
                }
            }
            return position;
        },
        
        getStopPostion: function(rank, degs) {
            var matrix = this.$content.css('transform');
            matrix = matrix.split(',');
//            console.log('=============='+matrix);
            //根据矩阵得到当前的度数
            var currDeg;
            var acos = Math.acos(parseFloat(matrix[0].split('(')[1], 10));
            var asin = Math.asin(parseFloat(matrix[1], 10));
            acos = acos * 180/Math.PI;
            asin = asin * 180/Math.PI;
            if(asin > 0) {
                currDeg = acos;
            }else{
                currDeg = 360-acos;
            }
            var currentDeg = degs[rank];
            if((currDeg > currentDeg.start && currDeg < currentDeg.end) || (currentDeg.start > currentDeg.end && currDeg < currentDeg.end)) {
                this._stopRouletteStop(currDeg);
            }
            else {
                var _this = this;
                setTimeout(function() {
                    _this.getStopPostion(rank, degs);
                }, 0)
            }
        },
        
        _startRound: function() {
            if(this.isStart) {
                return;
            }
            this.isStart = true;
            this.$el.trigger('start');
            this._setCanPlay('false');
            this._setRouletteStart();
            var _this = this;
            this.setting.canPlayCount = this.setting.canPlayCount - 1;
           // $.writeLog('发送请求');
            W.getApi().call({
                api: this.setting.api,
                app: this.setting.app,
                args: this.setting.args,
                timeout: 2000,
                success: function(data) {
                    _this.prizeRank = data.prize ? parseInt(data.prize.level, 10) : 0;
                    _this.prizeName = data.prize ? data.prize.name : '';
                    _this.integral = data.member ? data.member.integral : null;
                    _this._setRouletteStop();
                   // $.writeLog('请求成功, 名次='+_this.prizeRank+'; 中奖名称='+_this.prizeName);
                },
                error: function(resp) {
                    _this.prizeRank = 0;
                    _this.prizeName = '';
                    _this._setRouletteStop();
                   // $.writeLog('请求失败');
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
                this.$button.css({
                    'background-position': 'center bottom'
                });
                this.$el.removeClass('xui-roulette-widget-can-play')
            }
            else {
//                this.isStart = false;
                this.$button.css({
                    'background-position': 'center 0px'
                });
                this.$el.addClass('xui-roulette-widget-can-play');
            }
        },
        
        _bindContent: function() {
            var $content = this.$content;
            var lineCount = this.options.lineCount;
            var lineName = this.options.lineNames;
            var lotteryCount = this.setting.lotteryCount(this);
            var i, k, count = lineCount[lotteryCount];
            var eachTransform = 180/count;
            var marginTop = 0;
            var priseName = lineName[lotteryCount];
            var eachTransformName = 360/priseName.length;
            var name, j, q;
            var spanMarginTop;
            var nameWidth = this.width-20;
            var $line = $('<div style="position:relative;top:50%;"></div>');
            var $name = $('<div style="position:relative;width:'+nameWidth+'px;height:'+nameWidth+'px;left:10px;top:8px;"></div>');

            for(i = 0; i < count; i++) {
                marginTop = (i === 0) ? this.width/2 : 0;
                $line.append('<div style="z-index:3;transform:rotate('+eachTransform*i+'deg);-moz-transform:rotate('+eachTransform*i+'deg);-webkit-transform:rotate('+eachTransform*i+'deg);height:1px;background:#f6cfcf;width:'+this.width+'px"></div>');
            }
            if(4 === count) {
                $line.css({
                    'transform': 'rotate(-22.5deg)',
                    '-moz-transform': 'rotate(-22.5deg)',
                    '-webkit-transform': 'rotate(-22.5deg)'
                })
            }
            
            for(i = 0, k = priseName.length; i < k; i++) {
                name = priseName[i];
                nameSpan = '';
                for(j = 0, q = name.length; j < q; j++) {
                    if(q === 3) {
                        spanMarginTop = j !== 1 ? 1 : 0;
                    }
                    if(q === 4) {
                        spanMarginTop = (j === 0 || j === 3) ? 1 : 0;
                    }
                    nameSpan += '<span style="vertical-align:-'+spanMarginTop+'px;">'+name[j]+'</span>'
                }
                $name.append('<div style="font-size:12px;position:absolute;text-align:center; height:'+nameWidth+'px;width:'+nameWidth+'px;z-index:3;transform:rotate('+eachTransformName*i+'deg);-moz-transform:rotate('+eachTransformName*i+'deg);-webkit-transform:rotate('+eachTransformName*i+'deg);">'+nameSpan+'</div>')
            }
            $content.append($line);
            $content.append($name);
            $name.css({
                'font-family':'微软雅黑',
                'color': '#c36666'
            })
        },
        
        _bindLight: function() {
            var i;
            var lightLength = 24;
            var deg = 360/20;
            var $content = this.$roulette;
            var width = this.width+15;
            var $light = $('<div class="" style="position:relative;top:-7px;left:'+(width/2-8)+'px;z-index:4"></div>');
            var cssName;
            for(i = 0; i < 20; i++) {
                $light.append('<div class="xui-roulette-light-box" style="position:absolute;height:'+width+'px;transform:rotate('+deg*i+'deg);-moz-transform:rotate('+deg*i+'deg);-webkit-transform:rotate('+deg*i+'deg);"><span class="xui-roulette-light" ></span></div>');
            }
            $content.append($light);
        },
        
        _buildTemplate: function() {
            this._setAnimation();
            var width = this.$el.width() || $(window).width() * 0.65;
            this.width = width;
            var borderWidth = 10;
            this.$roulette = $('<div></div>');
            this.$roulette.css({
                'width': width + 'px',
                'height': width + 'px',
                'position': 'relative',
                'border': borderWidth + 'px solid #fc504f',
                'border-radius': '1000px',
                '-moz-border-radius': '1000px',
                '-webkit-border-radius': '1000px',
                'margin': 'auto'
            });
            this.$content = $('<div class="xui-roulette-roulette-box"></div>');
//	        var lotteryCount = this.setting.lotteryCount(this);
//	        this._rotateDeg = this.options.rotateDeg[lotteryCount];
            this.$content.css({
                width: width + 'px',
                height: width + 'px',
                position: 'absolute',
                left: '0px',
                'top': '0px'
//	            'transform': 'rotate('+this._rotateDeg+')',
//                '-moz-transform': 'rotate('+this._rotateDeg+')',
//                '-webkit-transform': 'rotate('+this._rotateDeg+')'
            });
            this.$border = $('<div></div>');
            this.$border.css({
                width: width+2 + 'px',
                height: width+2 + 'px',
                position: 'absolute',
                left: '-1px',
                'top': '-1px',
                'border': '6px solid #e6302f',
                'border-radius': '1000px',
                '-moz-border-radius': '1000px',
                '-webkit-border-radius': '1000px',
                '-moz-box-sizing': 'border-box',
                '-webkit-box-sizing': 'border-box',
                'box-sizing': 'border-box',
                'z-index': 2
            });
            this.$button = $('<a href="javascript:void(0);" class="tx_start"></a>');
            this.$button.css({
                width: '50px',
                height: '60.55px',
                position: 'absolute',
                top:'50%',
                left:'50%',
                margin: '-35px 0 0 -25px',
                background: 'url('+this.options.imagesUrl.startButton+') no-repeat center 0',
                'z-index': '101',
                '-webkit-background-size': '100% auto',
                '-moz-background-size': '100% auto',
                '-o-background-size': '100% auto',
                'background-size': '100% auto',
                'z-index': 7
            });
            this._bindContent();
            this._bindLight();
            this.$el.append(this.$roulette);
            this.$roulette.append(this.$content);
            this.$roulette.append(this.$border);
            this.$roulette.append(this.$button);
            this._setCanPlay();
        },
        
        _setAnimation: function() {
            var style = document.createElement('style');
            document.head.appendChild(style);
            style.innerHTML = '\
            @-keyframes light1{0%{background:#fff;border:1px solid #fff744;box-shadow:0px 0px 2px #f3ef99;}50%{border:1px solid #e6302f;background:#ec605f;}100%{background:#fff;border:1px solid #f3ef99;box-shadow:0px 0px 2px #f3ef99;}}\n\
            @-moz-keyframes light1{0%{background:#fff;border:1px solid #fff744;-moz-box-shadow:0px 0px 2px #f3ef99;}50%{border:1px solid #e6302f;background:#ec605f;}100%{background:#fff;border:1px solid #f3ef99;-moz-box-shadow:0px 0px 2px #f3ef99;}}\n\
            @-webkit-keyframes light1{0%{background:#fff;border:1px solid #fff744;-webkit-box-shadow:0px 0px 2px #f3ef99;}50%{border:1px solid #e6302f;background:#ec605f;}100%{background:#fff;border:1px solid #f3ef99;-webkit-box-shadow:0px 0px 2px #f3ef99;}}\n\
            @-keyframes light2{0%{border:1px solid #e6302f;background:#ec605f;}50%{background:#fff;border:1px solid #fff744;box-shadow:0px 0px 2px #f3ef99;}100%{border:1px solid #e6302f;background:#ec605f;}}\n\
            @-moz-keyframes light2{0%{border:1px solid #e6302f;background:#ec605f;}50%{background:#fff;border:1px solid #fff744;box-shadow:0px 0px 2px #f3ef99;}100%{border:1px solid #e6302f;background:#ec605f;}}\n\
            @-webkit-keyframes light2{0%{border:1px solid #e6302f;background:#ec605f;}50%{background:#fff;border:1px solid #fff744;box-shadow:0px 0px 2px #f3ef99;}100%{border:1px solid #e6302f;background:#ec605f;}}\n\
            @-keyframes roulette{0%{transform:rotate(0deg);}100%{transform:rotate(359deg);}}\n\
            @-moz-keyframes roulette{0%{-moz-transform:rotate(0deg);}100%{-moz-transform:rotate(359deg);}}\n\
            @-webkit-keyframes roulette{0%{-webkit-transform:rotate(0deg);}100%{-webkit-transform:rotate(359deg);}}\n\
            .xui-roulette-light{position:absolute;display:block;width:5px;height:5px;border-radius:5px;-moz-border-radius:5px;-webkit-border-radius:5px;border:1px solid #fff744;background:#fff;box-shadow:0px 0px 2px #f3ef99; }\n\
            .xui-roulette-widget-start .xui-roulette-light-box:nth-child(2n) span{animation: light1 1s ease-in-out infinite; -moz-animation: light1 1s ease-in-out infinite; -webkit-animation: light1 1s ease-in-out infinite; -o-animation: light1 1s ease-in-out infinite;}\n\
            .xui-roulette-widget-start .xui-roulette-light-box:nth-child(2n+1) span{animation: light2 1s ease-in-out infinite; -moz-animation: light2 1s ease-in-out infinite; -webkit-animation: light2 1s ease-in-out infinite; -o-animation: light2 1s ease-in-out infinite;}\n\
            .xui-roulette-widget-start .xui-roulette-roulette-box{animation: roulette 0.5s linear infinite; -moz-animation: roulette 0.5s linear infinite; -webkit-animation: roulette 0.5s linear infinite; -o-animation: roulette 0.5s linear infinite;}\n\
            .xui-roulette-roulette-box{background-color: #fff; background-image: -moz-radial-gradient(#fff8dc 0%, #feeaac 45%, #ffffff 45%, #ffffff 100%); background-image: -webkit-radial-gradient(#fff8dc 0%, #feeaac 45%, #ffffff 45%, #ffffff 100%);background-image: -o-radial-gradient(#fff8dc 0%, #feeaac 45%, #ffffff 45%, #ffffff 100%); background-image: radial-gradient(#fff8dc 0%, #feeaac 45%, #ffffff 45%, #ffffff 100%);border-radius: 1000px;-moz-border-radius: 1000px;-webkit-border-radius: 1000px;-moz-box-sizing: border-box;-webkit-box-sizing: border-box;box-sizing: border-box;z-index: 1;}\n\
            .xui-roulette-widget-can-play .xui-roulette-light-box span{background:#fff;border:1px solid #fff744;box-shadow:0px 0px 2px #f3ef99;}\n\
            ';
        }
    });
	// taking into account of the component when creating the window
	// or at the create event
    $(document).bind("pagecreate create", function(e) {
        $(":jqmData(ui-role=roulette)", e.target).roulette();
	});
})(jQuery);
