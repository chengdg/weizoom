/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * <input name="area" data-ui-role="area" type="text" value="1_1_2">
 * value属性的值:省_城市_区
 * author: tianyanrong
 */
(function($, undefined) {
	// component definition
	$.widget("mobile.area", $.mobile.widget, {
		options : {
            api: {
                province: '/tools/api/regional/provinces/ ', //获取省份的API
                city: '/tools/api/regional/cities/', //获取城市的API
                district: '/tools/api/regional/districts/' //获取区的API
            }
		},
		
		settings : {
			defaultProvince: '北京市',
            defaultValue: {
                province: '请选择',
                city: '请选择',
                district: '请选择'
            }
		},
        
        _createDefaulteOption: function(type) {
            return '<option value="-1">'+this.settings.defaultValue[type]+'</option>'
        },
				
		_create : function() {
            this._bind();
			this.$input = this.element;
            this.$input.attr('type', 'hidden');
            this.domList = {
                province: $('<select to-type="city">'+this._createDefaulteOption('province')+'</select>'),
                city: $('<select to-type="district">'+this._createDefaulteOption('city')+'</select>'),
                district: $('<select>'+this._createDefaulteOption('district')+'</select>')
            }
            this.$el = this.$input.parent('.ui-input-text');
            this.$el.attr('class', 'xui-area');
            this.$el.append(this.domList.province);
            this.$el.append(this.domList.city);
            this.$el.append(this.domList.district);
            this.defaultProvince = this.settings.defaultProvince;
            this.cachData = {};
            this._fetch('province');
            this.domList.province.selectmenu();
            this.domList.city.selectmenu();
            this.domList.district.selectmenu();
            this.selectData = {};
            
            //得到默认值
            var data = this.$input.val();
            if(data) {
                data = data.indexOf('_') > 0 ? data.split('_') : [data];
                this.selectData = {
                    province: data[0],
                    city: data[1],
                    district: data[2]
                }
            }
            
            //绑定change事件
            var _this = this;
            this.$el.delegate('select', 'change', function(event) {
                var $el = $(event.currentTarget);
                _this._setDefalut($el);
                _this._triggerFetch($el);
                _this._setValue();
            });
		},
        
        _setDefalut: function($el) {
            var type = $el.attr('to-type');
            if(!type) {
                return;
            }
            this.domList[type].html(this._createDefaulteOption(type));
            this.domList[type].selectmenu('refresh');
            if('city' === type) {
                this.domList.district.html(this._createDefaulteOption('district'));
                this.domList.district.selectmenu('refresh');
            }
        },
        
        _setValue: function() {
            var keyName;
            var values = [];
            var value;
            var valueNames = [];
            for(keyName in this.domList) {
                value = this.domList[keyName].val();
                
                if(value && value !== '-1') {
                    values.push(value);
                    valueName = this.domList[keyName].find('option[value="'+value+'"]').text();
                    valueNames.push(valueName);
                }
            }
            this.$input.val(values.join('_'));
            this.$input.attr('area-value', valueNames.join(' '));
            this.$input.trigger('change');
        },
        
        _triggerFetch: function($el) {
            var type = $el.attr('to-type');
            var value = $el.val();
            if(type && value) {
                this._fetch(type, value);
            }
        },
        
        _setOptions: function(type, value) {
            var $select = this.domList[type];
            var key = value ? type + '_' + value : type;
            var data = this.cachData[key];
            var keyName, optionHtml = '<option value="-1">'+this.settings.defaultValue[type]+'</option>';
            for(keyName in data) {
                optionHtml += '<option value="'+keyName+'">'+data[keyName]+'</option>'
            }
            $select.html(optionHtml);
            $select.val(this.selectData[type]);
            $select.selectmenu('refresh');
            this._triggerFetch($select);
        },
        
        _fetch: function(type, value) {
            if('-1' === value) {
                return;
            }
            var _this = this;
            var key = value ? type + '_' + value : type;
            if(this.cachData[key]) {
                this._setOptions(type, value);
                return;
            }
            var url = value ? this.options.api[type] + value + '/' : this.options.api[type];
            $.ajax({
                url: url,
                success: function(data) {
                    data = data.data;
                    _this.cachData[key] = data;
                    _this._setOptions(type, value);
                    if(_this.selectData) {
                        _this._setValue();
                    }
                },
                error: function(e) {
                    
                }
            })
        },

		_bind : function() {
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
		$(":jqmData(ui-role=area)", e.target).area();
	});
})(jQuery);
