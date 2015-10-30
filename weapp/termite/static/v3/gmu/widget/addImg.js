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
            // this.$parent = this.$input.parent();
            this.$parents = this.$input.parents('.xui-productPhoto');
            this.$parents.prepend('<ul class="xui-imgList xa-imgList"></ul>');
            this.canvas = document.createElement("canvas");
            this.ctx = this.canvas.getContext('2d');

            //    瓦片canvas
            this.tCanvas = document.createElement("canvas");
            this.tctx = this.tCanvas.getContext("2d");
            // this.$parent.addClass(this._uploadImageClassName);
            // this.$img = $('<img class="xui-uploadImg pa" name="file_img" file_name="'+this.$input.attr('name')+'" src="" style="display:none;width:45px;height:45px;top:0;left:0;" data-allow-autoplay="false">');
            // this.$parent.append('<span class="pa xa-remove xui-remove" style=""><i class="pa"></i></span>')
            // this.$parent.append('<input type="hidden" id="storeSrc_'+this.$input.attr('name')+'" name="storeSrc_'+this.$input.attr('name')+'"')
            // this.$parent.append(this.$img);
            // this.$parent.find('.xa-remove').hide();
            this._bind();
        }, 
        addImg:function(imgSrc){
            var li = "<li class='xa-img'><img src='" + imgSrc +"' data-allow-autoplay = 'true'><span class='pa xa-remove xui-remove' style='display:none;'><i class='pa'></i></span></li>";            
            $('.xa-imgList').append(li);
            if($('.xa-imgList').children('li').length == 5){
                $('.xa-addPhoto').hide();
            }
            $('.xa-text').hide();
            W.ImagePreview(wx)
        },
        _bind : function() {
            var _this = this;
            var maxsize = 200 * 1024;
            this.$input.bind('change', function(event) {
                if(!this.files.length) return;
                var files = Array.prototype.slice.call(this.files);
                var hasImgLength = $('.xa-imgList').children('li').length;
                var imgLength = hasImgLength + files.length;
                if(imgLength > 5){
                    _this._alert('最多同时可上传5张');
                    files.splice(5 - hasImgLength, imgLength - 5);
                }
                var $files = $(files);
                $files.each(function(i, file) {
                    //todo验证格式不正确的交互
                    console.log("_______>>>>>",file.type);
                    var isErrorByType = (file && file.type !== 'image/jpeg' && file.type !== 'image/gif' && file.type !== 'image/png');
                    var isErrorByName = (file && file.name && !file.name.match(/\.(jpg|gif|png|jpeg)$/));
                    if(!file || (file && file.type && isErrorByType) || (file && file.name && isErrorByName)) {
                        _this._alert('图片格式不正确');
                        return;
                    }
                    var reader = new FileReader();
                    reader.onload = function() {
                        var result = this.result;
                        var img = new Image();
                        img.src = result;
                        imgSrc = result;
                        //图片显示在页面上
                        _this.addImg(imgSrc);
                        console.log("<<<<<<<",result);
                        //如果图片大小小于200kb，则直接上传
                        if (result.length <= maxsize) {
                            img = null;

                            _this.upload(result);

                            return;
                        }
                        if (img.complete) {
                            callback();
                        } else {
                            img.onload = callback;
                        }

                        function callback() {
                            var data = _this.compress(img);
                            console.log("____",data);
                            _this.upload(data);

                            img = null;
                        }
                    }
                    reader.readAsDataURL(file);
                    
                });

                _this.showDelete();
                _this.finishEdit();
                _this.removeImgFun();
                //读取图片信息,预览图片
                // var reader = new FileReader();
                // reader.onload = function() {
                //     var content = this.result.replace('data:base64,', 'data:'+file.type+';base64,');
                //     _this.$img[0].src = content;
                //     $('#storeSrc_'+_this.$input.attr('name')).val(content);
                //     _this.$img[0].style.display = '';
                //     _this.$parent.removeClass(_this._loadingClassName);
                //     _this.addedImgFun(event);
                //     // _this.showDelete();
                
                // }
                // reader.onerror=function(){
                //     _this._alert('手机不支持图片预览');
                //     _this.$parent.removeClass(_this._loadingClassName);
                // }
                // reader.readAsDataURL(file);
            });
        },
        
        upload: function(basestr) {
                W.getApi().call({
                 app: 'webapp',
                 api: 'project_api/call',
                 method: 'post',
                 args: _.extend({
                     target_api: 'product_review2/create',
                     module: 'mall',
                     woid: W.webappOwnerId,
                     basestr: JSON.stringify(basestr),
                 }),
                 success: function (data) {
                    console.info()
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
                $('.xa-addPhoto, .xa-deletePhoto').hide();
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
