/*
 *
*/
W.BarcodeAnimation = function(options) {
    this.$action = options.$action;
    this.$window = $(window);
    this.windowHeight = this.$window.height();
    this.windowWidth = this.$window.width();
    this.$body = options.$body;
    this.speed = 90;
    this.bindEvents();
}
W.BarcodeAnimation.prototype = {
    bindEvents: function() {
        var _this = this;
        var isZoom = false;
        this.$action.click(function(event) {
            if(isZoom) {
                return false;
            }
            isZoom = true;
            _this.windowHeight = _this.$window.height();
            _this.windowWidth = _this.$window.width();
            _this.rander();
            _this.setRotate(90);
            _this.setZoom(_this.windowWidth);
        });
        this.$body.delegate('.tx_zoom_hide', 'click', function(event) {
            isZoom = false;
            _this.setRotate(-90);
            _this.setZoom(_this.$action.width());
        });
    },
    rander: function() {
        this.$zoom = this.$body.find('.xui-zoom');
        if(!this.$zoom.length){
            this.$body.append('<div class="xui-zoom tx_zoom_hide"></div>');
            this.$zoom = this.$body.find('.xui-zoom');
            this.$zoom.css({
                'background': 'rgba(0,0,0,0.8)',
                'z-index': '99999',
                'position':'absolute',
                'left':'0px',
                'top':'0px',
                'width':'100%',
                'height': '100%',
                'text-align': 'center',
                'line-height': this.windowHeight + 'px'
            });
        }
        this.$zoom.css({'display':'block'});
        this.$rotate = this.$action.find('img');
        var offset = this.$action.offset();
        var height = this.$rotate.height();
        var width = this.$rotate.width();
        this.scale = height/width;
        this.$action.css({
            'display':'block',
            'height':  height + 'px'
        });
        
        this.$rotate.css({
            'width': this.$action.width() + 'px',
            'vertical-align':'middle',
            'background':'#fff',
            'position': 'absolute',
            'top': this.windowHeight/2 + 'px',
            'left': '50%',
            'margin-top': '-' + (height/2) + 'px',
            'margin-left': '-' + (width/2) + 'px',
            'z-index': '100000'
        })
    },
    
    setAnimation: function(doingMothod, name) {
        var _this = this;
        var name  = 'timeout' + name;
        if(this[name]) {
            clearTimeout(this[name]);
            this[name] = null;
        }
        this.timeoutValue = setTimeout(function() {
            clearTimeout(_this[name]);
            _this[name] = null;
            doingMothod();
        }, this.speed)
    },
    setRotate: function(rotate) {
        if(rotate) {
            this.rotate = rotate || 90;
            this.rotateValue = this.rotate/(400/this.speed);
        }
        if(!this.cacheRotate) {
            this.cacheRotate = 0;
        }
        var _this = this;
        this.setAnimation(function() {
            _this.cacheRotate += _this.rotateValue;
            var isEndRotate = _this.rotate > 0 ? _this.cacheRotate >= _this.rotate : _this.cacheRotate <= 0;
            var endRotate = _this.rotate > 0 ? _this.rotate : 0;
            if(isEndRotate) {
                _this.$rotate.css({
                    'transform': 'rotate(' + endRotate + 'deg)',
                    '-moz-transform': 'rotate(' + endRotate + 'deg)',
                    '-o-transform': 'rotate(' + endRotate + 'deg)',
                    '-webkit-transform': 'rotate(' + endRotate + 'deg)'
                });
            }
            else {
                _this.$rotate.css({
                    'transform': 'rotate(' + _this.cacheRotate + 'deg)',
                    '-moz-transform': 'rotate(' + _this.cacheRotate + 'deg)',
                    '-o-transform': 'rotate(' + _this.cacheRotate + 'deg)',
                    '-webkit-transform': 'rotate(' + _this.cacheRotate + 'deg)'
                });
                _this.setRotate();
            }
        }, 'rotate');
    },
    setZoom: function(end) {
        if(end) {
            this.end = end;
            this.start = this.$action.width();
            this.isZoom = this.start < this.end ? true : false;
            this.zoomValue = this.isZoom ? (this.end-this.start)/(400/this.speed) : (this.start-this.end)/(400/this.speed);
            this.cacheZoom = this.start;
        }
            
        var _this = this;
        this.setAnimation(function() {
            if(_this.isZoom) {
                _this.cacheZoom = _this.cacheZoom + _this.zoomValue;
            }
            else {
                _this.cacheZoom = _this.cacheZoom - _this.zoomValue;
            }
            var isEndZoom = _this.isZoom ? _this.cacheZoom >= _this.end : _this.cacheZoom <= _this.end;
            if(isEndZoom) {
                if(_this.isZoom) {
                    _this.$rotate.css({
                        'width': _this.end + 'px',
                        'margin-left': '-'+(_this.end/2) + 'px',
                        'margin-top': '-' + (_this.end*_this.scale/2) + 'px'
                    });
                }
                else {
                    _this.$rotate.css({
                        'width': '100%',
                        'position': 'static',
                        'margin-left': '0px',
                        'margin-top': '0px'
                    });
                    
                    _this.$zoom.css({'display':'none'});
                }
            }
            else {
                _this.$rotate.css({
                    'width': _this.cacheZoom + 'px',
                    'margin-left': '-' + (_this.cacheZoom/2) + 'px',
                    'margin-top': '-' + (_this.cacheZoom*_this.scale/2) + 'px'
                });
                _this.setZoom();
            }
        }, 'zoom');
    }
}