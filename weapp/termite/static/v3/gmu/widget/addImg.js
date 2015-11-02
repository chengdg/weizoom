/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * <input id="" name=""  data-ui-role="uploadImage" type="file" >
 * _uploadImageClassName--模块样式
 * _loadingClassName--加载时样式
 * _alert--提示方法
 */
(function($, undefined) {
    gmu.define("UploadImage", {
        _loadingClassName: 'upLoadImageLoadding',

        _uploadImageClassName: 'xui-uploadImage',

        _alert: function(msg) {
            $('body').alert({
                isShow: true,
                info: msg,
                isSlide: true,
                speed: 2000,
                callBack: function() {
                }
            });
        },

        _create : function() {
            this.$input = this.$el;
            this.$parents = this.$input.parents('.xui-productPhoto');
            this.$parents.prepend('<ul class="xui-imgList xa-imgList"></ul>');
            this.canvas = document.createElement("canvas");
            this.ctx = this.canvas.getContext('2d');

            //瓦片canvas
            this.tCanvas = document.createElement("canvas");
            this.tctx = this.tCanvas.getContext("2d");
            this._bind();
        },
        _bind : function() {
            var _this = this;
            var maxsize = 200 * 1024;
            this.$input.bind('change', function(event) {
                if(!this.files.length) return;
                $('.xa-text').hide();
                var files = Array.prototype.slice.call(this.files);
                var hasImgLength = $('.xa-imgList').children('li').length;
                var preLength = hasImgLength + files.length;
                if(preLength >= 5){
                    $('.xa-addPhoto').hide();
                }
                if(preLength > 5){
                    _this._alert('最多可上传5张图片');
                    files.splice(5 - hasImgLength, preLength - 5);
                }
                var $files = $(files);
                $files.each(function(i, file) {
                    //todo验证格式不正确的交互
                    var isErrorByType = (file && file.type !== 'image/jpeg' && file.type !== 'image/gif' && file.type !== 'image/png');
                    var name = file.name.toLowerCase();
                    var isErrorByName = (file && file.name && !name.match(/\.(jpg|gif|png|jpeg)$/));

                    if(!file || (file && file.type && isErrorByType) || (file && file.name && isErrorByName)) {

                        _this._alert('图片格式不正确');
                        return;
                    }
                    var reader = new FileReader();
                    var $li = $("<li class='xa-img'><span class='pa xa-remove xui-remove' style='display:none;'><i class='pa'></i></span></li>");
                    $('.xa-imgList').append($li);

                    var imglength = $('.xa-imgList').children('li').length;
                    reader.onload = function() {
                        var result = this.result;
                        var img = new Image();
                        img.src = result;

                        var innerHtml = "<img src="+ result +" data-allow-autoplay = 'true' id=pro_reivew"+imglength+"><div class='xui-progress xa-progress'><span></span></div>";
                        $li.append(innerHtml);
                        //如果图片大小小于200kb，则直接上传
                        if (result.length <= maxsize) {
                            img = null;

                            _this.upload(result, imglength,$li);

                            return;
                        }
                        if (img.complete) {
                            callback();
                        } else {
                            img.onload = callback;
                        }

                        function callback() {
                            var data = _this.compress(img);
                            _this.upload(data, imglength,$li);

                            img = null;
                        }
                    }
                    reader.readAsDataURL(file);
                    
                });

                _this.showDelete();
                _this.finishEdit();
                _this.removeImgFun();
            });
        },
        upload: function(basestr,imglength,$li) {
            var $bar = $li.find('.xa-progress span');
            var percent = 0;
            var loop = setInterval(function () {
                percent++;
                $bar.css('width', percent + "%");
                if (percent == 99) {
                    clearInterval(loop);
                }
            },100);
            W.getApi().call({
                app: 'webapp',
                api: 'project_api/call',
                method: 'post',
                args: _.extend({
                    target_api: 'product_review_pic/create',
                    module: 'mall',
                    woid: W.webappOwnerId,
                    basestr: JSON.stringify(basestr)
                }),
                success: function (data) {
                    $("#pro_reivew"+imglength).attr('data-src',data.path)
                    clearInterval(loop);
                    $bar.css('width',"100%");
                    setTimeout(function(){
                        $bar.parent().css('opacity','0');
                    },300)                
                },
                error: function (data) {
                    alert('没有可连接的网络');
                    return;
                }
            });
        },
        compress:function(img){
            var initSize = img.src.length;
            var width = img.width;
            var height = img.height;

            //如果图片大于四百万像素，计算压缩比并将大小压至400万以下
            var ratio;
            if ((ratio = width * height / 4000000)>1) {
                ratio = Math.sqrt(ratio);
                width /= ratio;
                height /= ratio;
            }else {
                ratio = 1;
            }

            this.canvas.width = width;
            this.canvas.height = height;

            //铺底色
            this.ctx.fillStyle = "#fff";
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

            //如果图片像素大于100万则使用瓦片绘制
            var count;
            if ((count = width * height / 1000000) > 1) {
                count = ~~(Math.sqrt(count)+1); //计算要分成多少块瓦片

            //计算每块瓦片的宽和高
                var nw = ~~(width / count);
                var nh = ~~(height / count);

                this.tCanvas.width = nw;
                this.tCanvas.height = nh;

                for (var i = 0; i < count; i++) {
                    for (var j = 0; j < count; j++) {
                        this.tctx.drawImage(img, i * nw * ratio, j * nh * ratio, nw * ratio, nh * ratio, 0, 0, nw, nh);

                        this.ctx.drawImage(this.tCanvas, i * nw, j * nh, nw, nh);
                    }
                }
            } else {
                this.ctx.drawImage(img, 0, 0, width, height);
            }

            //进行最小压缩
            var ndata = this.canvas.toDataURL('image/jpeg', 0.3);

            console.log('压缩前：' + initSize);
            console.log('压缩后：' + ndata.length);
            console.log('压缩率：' + ~~(100 * (initSize - ndata.length) / initSize) + "%");

            this.tCanvas.width = this.tCanvas.height = this.canvas.width = this.canvas.height = 0;

            return ndata;
        },
        _unbind : function() {
            
        },
        
        destroy : function() {
            // Unbind any events that were bound at _create
            this._unbind();

            this.options = null;
        },

        showDelete:function(){
            $('.xa-deletePhoto').show().unbind('click').click(function(){
                $('.xa-remove, .xa-finishEdit').show();
                $('.xa-addPhoto, .xa-deletePhoto,.xa-text').hide();
            });
        },

        finishEdit:function(){
            $('.xa-finishEdit').click(function(event) {
               $('.xa-remove,.xa-finishEdit').hide();
               $('.xa-deletePhoto').show();
               var length = $('.xa-imgList').children('li').length;
               if(length < 5){
                    $('.xa-addPhoto').show();
                    $('.xa-finishEdit').hide();
                }
            });
        },
        removeImgFun:function(){
            $('body').delegate($('.xa-remove'), 'click', function(event) {
                $(event.target).parents('li').remove();
                var length = $('.xa-imgList').children('li').length;
                if(length == 0){
                    $('.xa-addPhoto,.xa-text').show();
                    $('.xa-finishEdit').hide();
                }
            });
        }
    });
    


    // taking into account of the component when creating the window
    // or at the create event
    $(function(){
        $('[data-ui-role="uploadImage"]').each(function(){
            var $uploadImage = $(this);
            $uploadImage.uploadImage();
        })
    });
    
})(Zepto);
