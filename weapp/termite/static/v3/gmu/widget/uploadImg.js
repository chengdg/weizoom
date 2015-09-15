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
            $('.ui-page').alert({
                isShow: true,
                info: msg,
                isSlide: true,
                speed: 2000,
                callBack: function() {}
            });
        },

        _create : function() {
            this.$input = this.$el;
            this.$parent = this.$input.parent();
            this.$parent.addClass(this._uploadImageClassName);
            this.$img = $('<img class="xui-uploadImg pa" name="file_img" file_name="'+this.$input.attr('name')+'" src="" style="display:none;width:45px;height:45px;top:0;left:0;" data-allow-autoplay="false">');
            this.$parent.append('<span class="pa xa-remove xui-remove" style=""><i class="pa"></i></span>')
            this.$parent.append('<input type="hidden" id="storeSrc_'+this.$input.attr('name')+'" name="storeSrc_'+this.$input.attr('name')+'"')
            this.$parent.append(this.$img);
            this.$parent.find('.xa-remove').hide();
            this._bind();
        },

        _bind : function() {
            var _this = this;
            this.$input.bind('change', function(event) {
                _this.$parent.addClass(_this._loadingClassName);

                var file = this.files[0];

                //判断图片格式
                var isErrorByType = (file && file.type !== 'image/jpeg' && file.type !== 'image/gif' && file.type !== 'image/png');
                var isErrorByName = (file && file.name && !file.name.match(/\.(jpg|gif|png)$/));
                if(!file || (file && file.type && isErrorByType) || (file && file.name && isErrorByName)) {
                    _this._alert('图片格式不正确');
                }

                //读取图片信息,预览图片
                var reader = new FileReader();
                reader.onload = function() {
                    var content = this.result.replace('data:base64,', 'data:'+file.type+';base64,');
                    _this.$img[0].src = content;
                    $('#storeSrc_'+_this.$input.attr('name')).val(content);
                    _this.$img[0].style.display = '';
                    _this.$parent.removeClass(_this._loadingClassName);
                    _this.addedImgFun(event);
                    // _this.showDelete();
                    _this.finishEdit();
                    _this.removeImgFun(event);
                }
                reader.onerror=function(){
                    _this._alert('手机不支持图片预览');
                    _this.$parent.removeClass(_this._loadingClassName);
                }
                reader.readAsDataURL(file);
            });
        },

        upload: function() {

        },

        _unbind : function() {

        },

        destroy : function() {
            // Unbind any events that were bound at _create
            this._unbind();

            this.options = null;
        },

        addedImgFun: function(event) {
            var $uploadImage = $(event.target).parent().parent().find('.xui-uploadImage');
            if($uploadImage.length < 6){
                var imgLength = this.$img[0].src.length;
                if(imgLength >0){
                    this.$parent.parent('.xui-productPhoto').find('.xa-deletePhoto').before('<div class="xui-addPhoto fl pr">'
                                                                                                +'<span class="xui-i-box"></span>'
                                                                                                +'<input id="" name="imgFile'+imgLength+'"  data-ui-role="uploadImage" type="file" style="opacity:0;top:0;left:0;width:45px;height:45px;" class="pa">'
                                                                                            +'</div>');

                    $('[name="imgFile'+imgLength+'"]').uploadImage();
                    $(event.target).parent().parent().find('.xa-text').hide();
                    $($(event.target).parent('.xui-uploadImage img')[$uploadImage.length-1]).data('allow-autoplay','true')
                    W.ImagePreview(wx)
                }
            };
            this.showDelete();
            if($uploadImage.length == 5){
                $uploadImage.parent().children('*:nth-child(6)').css('display','none');
            }
        },

        showDelete:function(){
             var imgLength = this.$img[0].src.length;
             if( imgLength > 0 ){
               $('.xa-deletePhoto').show().unbind('click').click(function(){
                    $(this).siblings().find('.xa-remove').show();
                    $(this).siblings('.xui-addPhoto').last().hide();
                    $(this).siblings('.xa-deletePhoto').hide();
                    $(this).siblings('.xa-finishEdit').show();
               });
           }
        },

        finishEdit:function(){
            $('.xa-finishEdit').click(function(event) {
               $(this).siblings().find('.xa-remove').hide();
               var photoLength = $(this).siblings('.xui-addPhoto').length;
               $(this).siblings('.xui-addPhoto').find('.xa-remove').hide();
               $(this).siblings('.xa-deletePhoto').show();
               $(this).hide();
               if( photoLength < 6){
                   $(this).siblings('.xui-addPhoto').last().show();
               }
            });
        },

        removeImgFun:function(event){
            var _this = this;
            var $uploadImage = $(event.target).parent().parent().find('.xui-uploadImage');
            console.log($(event.target).parent().parent().find('.xui-uploadImage'));
            $(event.target).siblings('.xa-remove').click(function(){
                $(this).parent().remove();
                console.log($(this).parent());
                console.log($uploadImage.length);
                if($uploadImage.length == 2){

                    $('.xa-finishEdit').hide();
                    $('.xui-addPhoto').show();
                    $('.xui-addPhoto').find('.xa-remove').hide();
                    // $('.xa-deletePhoto').show();
                    $('.xa-text').show();
                }else if($uploadImage.length == 6){
                    // $('.xui-productPhoto').children('*:nth-child(5)').css('display','inline-block');
                    // $('.xui-productPhoto').children('*:nth-child(5)').find('.xa-remove').hide();
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
