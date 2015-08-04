/*
Copyright (c) 2011-2012 Weizoom Inc
*/
W.ImagesSwipe = function(options) {
	this.imgUrls = options.imgUrls;
    this.$el = $(options.el);
    this.$imgs = [];
    this.page = 1;
    this.maxPage = this.imgUrls.length;
    this.initialize(options);
}

W.ImagesSwipe.prototype = {    
    getImgTemplate: function() {
        return '<div class="xui-imagesSwipe-item fl" style="display:none; position:relative;"><img src="" ><div class="tx_loading ico-loading"></div></div>';
    },
    
    initialize: function(options) {
        this.$el.append('<div class="xui-imagesSwipe tx_imagesSwipe-content"></div>')
        this.$content = this.$el.find('.tx_imagesSwipe-content');
        this.render();
    },
    
    show: function(index) {
        index = index || 0;
        this.$imgs[index].find('img').attr('src', this.imgUrls[index].url);
        this.$imgs[index].show();
        this.$imgs[index+1].find('img').attr('src', this.imgUrls[index+1].url);
        this.page = index + 1;
        if(this.changePage) {
            this.changePage({
                currentPage: 1,
                maxPage: this.maxPage,
                $currentImage: this.$imgs[this.page-1]
            });
        }
    },
    
    render: function() {
        var urls = this.imgUrls;
        var i, k;
        var length = urls.length;
        var width = this.$el.width();
        for(i = 0, k = length; i < k; i++) {
            this.$imgs.push($(this.getImgTemplate()));
            this.$content.append(this.$imgs[i]);
            this.removeLoading(this.$imgs[i]);
            this.$imgs[i].css({
                width: width + 'px'
            })
        }
        this.$el.css({
            'positions': 'relative'
        })
        this.$content.css({
            'width': (width * length) + 'px',
            'positions': 'absolute',
            'top': '0',
            'left': '0'
        });
    },
    
    play: function(page, isNext) {
        var i, k;
        for(i = 0, k = this.$imgs.length; i < k; i++) {
            this.$imgs[i].css({
                'display': 'block'
            })
        }
        
        var _this = this;
        if(this.playValue) {
            clearTimeout(this.playValue);
            this.playValue = null;
        }
        this.playValue = setTimeout(function() {
            clearTimeout(_this.playValue);
            _this.playValue = null;
            
            index = page || 0;
            var marginLeft = isNext ? -_this.$imgs[index-1].width() : 0;
            var index = isNext ? index-2 : index-1;
            
            _this.$imgs[index].css({
                'margin-left': marginLeft + 'px',
                '-moz-transition': 'margin-left 1s',
                '-webkit-transition': 'margin-left 1s',
                '-o-transition':  'margin-left 1s',
                'transition':  'margin-left 1s',
            });
            if(_this.changePage) {
                _this.changePage({
                    currentPage: page,
                    maxPage: _this.maxPage,
                    $currentImage: _this.$imgs[page-1]
                });
            }
            var $img = isNext ? _this.$imgs[page-2] : _this.$imgs[page];
            _this.setHide(page-1, false);
        }, 10);
    },
    
    setHide: function(index, isShow) {
        if(this.setHideValue) {
            clearTimeout(this.setHideValue);
            this.setHideValue = null;
        }
        var _this = this;
        this.setHideValue = setTimeout(function() {
            clearTimeout(_this.setHideValue);
            _this.setHideValue = null;
            var i, k;
            for(i = 0, k = _this.$imgs.length; i < k; i++) {
                if(index !== i) {
                    _this.$imgs[i].css({
                        'display':'none'
                    })
                }
            }
        },1000);
        
    },
    
    removeLoading: function($img) {
        console.log($img.find('img')[0]);
        $img.find('img')[0].onload = function() {
            $img.find('.tx_loading').remove();
        };
    },
    
    next: function() {
        if(this.page === this.maxPage) {
            return;
        }
        this.page++;
        this.play(this.page, true);
        
        if(this.$imgs[this.page]) {
            this.$imgs[this.page].find('img').attr('src', this.imgUrls[this.page].url);
        }
    },
    
    previous: function() {
        if(this.page === 1) {
            return;
        }
        this.page--;
        this.play(this.page, false);
    }
}