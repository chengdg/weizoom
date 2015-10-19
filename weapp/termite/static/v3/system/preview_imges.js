/**
 * 使用微信浏览器内置图片预览接口对页面中的图片进行预览，
 * 目前支持页面中的所有不可点击的图片
 */
W.ImagePreview = function(Api) {
    this.author = "chuter";
    this.version = "1.0";

    if (typeof String.prototype.startsWith != 'function') {
        // see below for better implementation!
        String.prototype.startsWith = function (str){
            return this.indexOf(str) == 0;
        };
    }

    this.isCanClickImgEle = function(imgEle) {
        var fatherEles = $(imgEle).parents('a');
        return (fatherEles && fatherEles.length > 0);
    };

    this.isAllowAutoPlay = function(imgEle) {
        var $imgEle = $(imgEle);
        if (typeof($imgEle.data('allow-autoplay')) == "undefined" || $imgEle.data('allow-autoplay') == null) {
            return true;
        } else {
            return $(imgEle).data('allow-autoplay') == "true";
        }
    };

    this.unifyUrl = function(el) {
        var url ="";
        if($(el).data('url')){
            url = $(el).data('url');
        }else{
            url = $(el).attr('full-src');
        }
        if(!url)
            url = $(el).attr('src');
        if (url.startsWith('http://')) {
            return url;
        } else if (url.startsWith('data:')) {
            return url;
        } else if (url.startsWith('/')) {
            return 'http://' + window.location.hostname + url;
        } else {
            return 'http://' + window.location.hostname + '/' + url;
        }
    };

    this.cannotClickedImageLinks = [];

    var _this = this;
    $("img").each(function(index, element) {
        if ((!_this.isCanClickImgEle(element)) && _this.isAllowAutoPlay(element)) {
            var absoluteUrl = _this.unifyUrl(element);
            _this.cannotClickedImageLinks.push(absoluteUrl); 
        }
    });
            
    $('body').undelegate('img','click');
    $('body').delegate('img', 'click', function(event) {
        var targetEle = event.currentTarget;
        if ((!_this.isCanClickImgEle(targetEle)) && _this.isAllowAutoPlay(targetEle)) {
            var absoluteUrl = _this.unifyUrl(targetEle);
            Api.previewImage({
                'current':absoluteUrl, 
                'urls':_this.cannotClickedImageLinks
            });
        }
    });
}  