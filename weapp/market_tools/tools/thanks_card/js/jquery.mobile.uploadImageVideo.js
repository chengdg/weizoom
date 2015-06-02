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
    // component definition
    $.widget("mobile.uploadImageVideo", $.mobile.widget, {
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
            this.$input = this.element;
            this.$parent = this.$input.parent();
            this.$parent.addClass(this._uploadImageClassName);
            this.$img = $('<img name="file_img" type="" file_name="'+this.$input.attr('name')+'" src="" style="display:none;">');
            this.$parent.append(this.$img);            
            this._bind();
        },  

        _bind : function() {
            var _this = this;
            
            this.$input.bind('change', function(event) {
                _this.$parent.addClass(_this._loadingClassName);

                var file = this.files[0];

                var fileType = file.type.toString();
                var is_image = false;
                var is_video = false;
                if (fileType.indexOf('image') == 0) {
                    is_image = true;
                }
                if (fileType.indexOf('video') == 0) {
                    is_video = true;
                } 
                if (!is_image && !is_video) {
		            is_image = (file && file.name && file.name.match(/\.(jpg|gif|png|png-8|png-24|jpeg|JPG|GIF|PNG|PNG-8|PNG-24|JPEG)$/));
               	    is_video = (file && file.name && file.name.match(/\.(mp4|ogg|wmv|rmbv|mkv|3gp|MP4|OGG|WMV|RMVB|MKV|3GP)$/));
        		    if (!is_image && !is_video) {
                    	_this._alert('格式不正确');
                    	return;
        		    }
                }

                //读取图片信息,预览图片
                var reader = new FileReader();
                reader.onload = function() {
                    content = this.result.replace('data:base64,', 'data:'+file.type+';base64,');
                    $("#thanks_card_img").attr('value', content);
                    _this.$img[0].style.display = '';
                    _this.$parent.removeClass(_this._loadingClassName);

                    if (is_image) { 
                        _this.$img[0].src = content;                       
                        $('#thanks_card_att_type').attr('value', 'image');
                    } else {
                        _this.$img[0].src = "/markettools_static/thanks_card/img/ready.png";
                        $('#thanks_card_att_type').attr('value', 'video');
                    }
                }
                reader.onerror=function(){
                    _this._alert('手机不支持预览');
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
        }
    });

    // taking into account of the component when creating the window
    // or at the create event
    $(document).bind("pagecreate create", function(e) {
        $(":jqmData(ui-role=uploadImageVideo)", e.target).uploadImageVideo();
    });
    
})(jQuery);
