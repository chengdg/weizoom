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
	$.widget("mobile.uploadImage", $.mobile.widget, {
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
            this.$img = $('<img name="file_img" file_name="'+this.$input.attr('name')+'" src="" style="display:none;">');
            this.$parent.append(this.$img);
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
                    _this.$img[0].src = this.result.replace('data:base64,', 'data:'+file.type+';base64,');
                    _this.$img[0].style.display = '';
                    _this.$parent.removeClass(_this._loadingClassName);
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
		}
	});

	// taking into account of the component when creating the window
	// or at the create event
	$(document).bind("pagecreate create", function(e) {
		$(":jqmData(ui-role=uploadImage)", e.target).uploadImage();
	});
    
})(jQuery);
