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
            wuiAlert(msg, 2000);
        },

        _create : function() {
            this.$input = this.$el;
            this.$parents = this.$input.parents('.xui-productPhoto');
            this.$uploadImg = this.$parents.parents('.wui-UploadImg')|| "";
            this.uploadImg_id = '';
            if (this.$uploadImg != ""){
                this.uploadImg_id = this.$uploadImg.attr('data-component-cid');
            }
            this.$parents.prepend('<ul class="xui-imgList xa-imgList"></ul>');
            this.canvas = document.createElement("canvas");
            this.ctx = this.canvas.getContext('2d');

            this._bind();
        },
        _bind : function() {
            var _this = this;
            var maxsize = 200 * 1024;
            this.$input.bind('change', function(event) {
                if(!this.files.length) return;
                _this.$parents.find('.xa-text').hide();
                var files = Array.prototype.slice.call(this.files);
                var hasImgLength = _this.$parents.find('.xa-imgList').children('li').length;
                var preLength = hasImgLength + files.length;
                if(preLength >= 5){
                    _this.$parents.find('.xa-addPhoto').hide();
                }
                if(preLength > 5){
                    _this._alert('最多可上传5张图片');
                    files.splice(5 - hasImgLength, preLength - 5);
                }
                var $files = $(files);
                $files.each(function(i, file) {
                    if(file.type !== "" && file.name !== ""){
                        var isErrorByType = (file && file.type !== 'image/jpeg' && file.type !== 'image/gif' && file.type !== 'image/png');
                        var name = file.name.toLowerCase();
                        var isErrorByName = (file && file.name && !name.match(/\.(jpg|gif|png|jpeg)$/));
                        if(!file || (file && file.type && isErrorByType) || (file && file.name && isErrorByName)) {
                            _this._alert('图片格式不正确');
                            return;
                        }
                    }else{
                        JSAnalysis('userAddImg','',W.webappOwnerId);
                    }
                    var reader = new FileReader();
                    var $li = $("<li class='xa-img'><span class='pa xa-remove xui-remove' style='display:none;'><i class='pa'></i></span><div class='xui-progress xa-progress'><span></span></div></li>");
                    _this.$parents.find('.xa-imgList').append($li);

                    var imglength = _this.$parents.find('.xa-imgList').children('li').length;
                    var orientation;

                    EXIF.getData(file, function() {
                        EXIF.getAllTags(this);   
                        orientation = EXIF.getTag(this, 'Orientation'); 
                        reader.onload = function() {
                            var result = this.result;
                            var img = new Image();
                            img.src = result;                        
                            //如果图片大小小于200kb，则直接上传
                            if (result.length <= maxsize) {
                                img = null;
                                _this.upload(result, imglength,$li);

                                return;
                            }
                            if (img.complete) {
                                callback(orientation);
                            } else {
                                img.onload = function(){
                                    callback(orientation);
                                };
                            }
                            function callback() {
                                var data = _this.compress(img,orientation);
                                _this.upload(data, imglength,$li);

                                img = null;
                            }
                        }
                        reader.readAsDataURL(file);
                    });
                   
                });

                _this.showDelete();
                _this.finishEdit();
            });
        },

        upload: function(basestr,imglength,$li) {
            W.is_pic_up = false;
            var _this = this;
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
                    var img ="<img src='" + data.path + "' id='"+_this.uploadImg_id+"pro_reivew"+imglength+"' data-src="+ data.path +" full-src='" + data.path + "'>";
                    $li.append(img);
                    $li.children('img').data('allow-autoplay','true');
                    W.ImagePreview(wx);
                    clearInterval(loop);
                    $bar.css('width',"100%");
                    setTimeout(function(){
                        $bar.parent().css('opacity','0');
                    },300);
                    W.is_pic_up = true;
                },
                error: function (data) {
                    _this._alert('图片格式不正确，请重新上传');
                    clearInterval(loop);
                }
            });
        },
        compress:function(img, orientation){
            var initSize = img.src.length;
            var width,
                height,
                ratio,
                ndata;
            width = img.width;
            height = img.height;
            var needCompress = (ratio = width * height / 4000000)>1;
            //如果图片大于四百万像素，计算压缩比并将大小压至400万以下
            if (needCompress) {
                ratio = Math.sqrt(ratio);
                width /= ratio;
                height /= ratio;
            }else {
                ratio = 1;
            }
            //当竖着手机拍照时为6
            if(orientation == 6){
                this.canvas.width = height;
                this.canvas.height = width;
            }else{
                this.canvas.width = width;
                this.canvas.height = height;
            }
            //铺底色
            this.ctx.fillStyle = "#fff";
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

            
            if(orientation == 6){
                this.ctx.rotate(0.5 * Math.PI);
                this.ctx.translate(0, -height);
            }
            this.ctx.drawImage(img, 0, 0, width, height);

            ndata = this.canvas.toDataURL('image/jpeg', 0.3);

            this.canvas.width = this.canvas.height = 0;

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
            var _this = this;
            _this.$parents.find('.xa-deletePhoto').show().unbind('click').click(function(){
                _this.$parents.find('.xa-remove, .xa-finishEdit').show();
                _this.$parents.find('.xa-addPhoto, .xa-deletePhoto,.xa-text').hide();
                _this.removeImgFun();
            });
        },

        finishEdit:function(){
            var _this = this;
            this.$parents.find('.xa-finishEdit').click(function(event) {
               _this.$parents.find('.xa-remove,.xa-finishEdit').hide();
               _this.$parents.find('.xa-deletePhoto').show();
               var length = $('.xa-imgList').children('li').length;
               if(length < 5){
                    _this.$parents.find('.xa-addPhoto').show();
                    _this.$parents.find('.xa-finishEdit').hide();
                }
                _this.$parents.find('.xa-remove').unbind('click');
            });
        },
        removeImgFun:function(){
            var _this = this;
            this.$parents.find('.xa-remove').click( function(event) {
                $(event.target).parents('li').remove();
                var length = _this.$parents.find('.xa-imgList').children('li').length;
                if(length == 0){
                    _this.$parents.find('.xa-addPhoto,.xa-text').show();
                    _this.$parents.find('.xa-finishEdit').hide();
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
