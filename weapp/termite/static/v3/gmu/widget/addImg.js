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
            // this.$parent.addClass(this._uploadImageClassName);
            // this.$img = $('<img class="xui-uploadImg pa" name="file_img" file_name="'+this.$input.attr('name')+'" src="" style="display:none;width:45px;height:45px;top:0;left:0;" data-allow-autoplay="false">');
            // this.$parent.append('<span class="pa xa-remove xui-remove" style=""><i class="pa"></i></span>')
            // this.$parent.append('<input type="hidden" id="storeSrc_'+this.$input.attr('name')+'" name="storeSrc_'+this.$input.attr('name')+'"')
            // this.$parent.append(this.$img);
            // this.$parent.find('.xa-remove').hide();
            this._bind();
        }, 
        addImg:function(imgSrc){
            var li = "<li class='xui-addPhoto mb10 fl pr'><img src='" + imgSrc +"' data-allow-autoplay = 'true'><span class='pa xa-remove xui-remove' style='display:none;'><i class='pa'></i></span></li>";            
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
                    //todo隐藏添加图片按钮
                }
                var $files = $(files);
                $files.each(function(i, file) {
                    //todo验证格式不正确的交互
                    var isErrorByType = (file && file.type !== 'image/jpeg' && file.type !== 'image/gif' && file.type !== 'image/png');
                    var isErrorByName = (file && file.name && !file.name.match(/\.(jpg|gif|png)$/));
                    if(!file || (file && file.type && isErrorByType) || (file && file.name && isErrorByName)) {
                        _this._alert('图片格式不正确');
                        return;
                    }
                    var reader = new FileReader();
                    reader.onload = function() {
                        var result = this.result;
                        var img = new Image();
                        imgSrc = result;
                        //图片显示在页面上
                        _this.addImg(imgSrc);

                        //如果图片大小小于200kb，则直接上传
                        if (result.length <= maxsize) {
                            img = null;

                            // _this.upload(result, file, $(li));

                            return;
                        }
                        if (img.complete) {
                            callback();
                        } else {
                            img.onload = callback;
                        }

                        function callback() {
                            var data = compress(img);
                            
                            //_this.upload(data, file, $(li));

                            img = null;
                        }
                    }
                    reader.readAsDataURL(file);
                    
                });
                // var hasImgLength = $('.xa-imgList').children('li').length;
                
                //todo图片出现再出现删除按钮
                _this.showDelete();
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
                _this.finishEdit();
                _this.removeImgFun(event);
                // }
                // reader.onerror=function(){
                //     _this._alert('手机不支持图片预览');
                //     _this.$parent.removeClass(_this._loadingClassName);
                // }
                // reader.readAsDataURL(file);
            });
        },
        
        upload: function() {
            
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

            canvas.width = width;
            canvas.height = height;

    //        铺底色
            ctx.fillStyle = "#fff";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            //如果图片像素大于100万则使用瓦片绘制
            var count;
            if ((count = width * height / 1000000) > 1) {
                count = ~~(Math.sqrt(count)+1); //计算要分成多少块瓦片

    //            计算每块瓦片的宽和高
                var nw = ~~(width / count);
                var nh = ~~(height / count);

                tCanvas.width = nw;
                tCanvas.height = nh;

                for (var i = 0; i < count; i++) {
                    for (var j = 0; j < count; j++) {
                        tctx.drawImage(img, i * nw * ratio, j * nh * ratio, nw * ratio, nh * ratio, 0, 0, nw, nh);

                        ctx.drawImage(tCanvas, i * nw, j * nh, nw, nh);
                    }
                }
            } else {
                ctx.drawImage(img, 0, 0, width, height);
            }

            //进行最小压缩
            var ndata = canvas.toDataURL('image/jpeg', 0.3);

            console.log('压缩前：' + initSize);
            console.log('压缩后：' + ndata.length);
            console.log('压缩率：' + ~~(100 * (initSize - ndata.length) / initSize) + "%");

            tCanvas.width = tCanvas.height = canvas.width = canvas.height = 0;

            return ndata;
        },
        _unbind : function() {
            
        },
        
        destroy : function() {
            // Unbind any events that were bound at _create
            this._unbind();

            this.options = null;
        },

        // addedImgFun: function(event) {
        //     var $uploadImage = $('.xui-uploadImage');
        //     if($uploadImage.length < 6){
        //         var imgLength = this.$img[0].src.length;
        //         if(imgLength >0){
        //             this.$parent.parent('.xui-productPhoto').find('.xa-deletePhoto').before('<div class="xui-addPhoto fl pr">'
        //                                                                                         +'<span class="xui-i-box"></span>'
        //                                                                                         +'<input id="" name="imgFile'+imgLength+'"  data-ui-role="uploadImage" type="file" style="opacity:0;top:0;left:0;width:45px;height:45px;" class="pa">'
        //                                                                                     +'</div>');
               
        //             $('[name="imgFile'+imgLength+'"]').uploadImage();
        //             $('.xa-text').hide();
        //             $($('.xui-uploadImage img')[$uploadImage.length-1]).data('allow-autoplay','true')
        //             W.ImagePreview(wx)
        //         }
        //     };
        //     this.showDelete();
        //     if($uploadImage.length == 5){
        //         $uploadImage.parent().children('*:nth-child(6)').css('display','none');
        //     }
        // },

        showDelete:function(){
            $('.xa-deletePhoto').show().unbind('click').click(function(){
                $('.xa-remove').show();
                $('.xa-addPhoto').hide();
                $('.xa-deletePhoto').hide();
                $('.xa-finishEdit').show();
            });
        },

        finishEdit:function(){
            $('.xa-finishEdit').click(function(event) {
               $('.xa-remove').hide();
               $('.xa-deletePhoto').show();
               $('.xa-finishEdit').hide();
            });
        },

        removeImgFun:function(event){
        //     var _this = this;
        //     var $uploadImage = $('.xui-uploadImage');
        //     $(event.target).siblings('.xa-remove').click(function(){
        //         $(this).parent().remove();
        //         if($uploadImage.length == 2){
        //             $('.xa-finishEdit').hide();
        //             $('.xui-addPhoto').show();
        //             $('.xui-addPhoto').find('.xa-remove').hide();
        //             $('.xa-text').show();
        //         }
        //     });

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
