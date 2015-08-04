/*
 * Jquery Mobile地址选择插件(弹出)
 * 
 *
 * 使用示例;
 * <input name="area" data-ui-role="areaPop" type="text" value="1_1_2">
 * value属性的值:省_城市_区
 * author: guoliyan
 */
(function($, undefined) {
	// component definition
	$.widget("mobile.areaPop", $.mobile.widget, {
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
            return '<li value="-1">'+this.settings.defaultValue[type]+'</li>'
        },
				
		_create : function() {
            this._bind();
			this.$input = this.element;
            this.$input.attr('type', 'hidden');
            this.domList = {
                province: $('<ul type="province" to-type="city" id="areaWidget-province" class="xui-popAddress"></ul>'),
                city: $('<ul type="city" to-type="district" id="areaWidget-city" class="xui-popAddress"></ul>'),
                district: $('<ul type="district" id="areaWidget-district" class="xui-popAddress"></ul>')
            }
            this.$el = this.$input.parent('.ui-input-text');
            this.$el.attr('class', 'wui-area');

            var area_str = this.$input.attr('data-area-str') || '地区信息';
            var $div = $('<div class="xa-openSelect pl5" style="color:#576b95;">'+area_str+'</div>');
            this.$el.append($div);
            this.cachData = {};
            // //绑定change事件
            var _this = this;

            this.$el.delegate('.xa-openSelect', 'click', function(event) {
               _this._select_btn_click(event)
            });
            this.$el.delegate('ul li', 'click', function(event) {
            	event.stopPropagation();
            	var $ul = $(this).parent('ul');
                var value = $(this).attr('data-value');
                $ul.attr('data-value', value);
                var value_str = $(this).text();
                $ul.attr('data-value-str', value_str)
                _this._triggerFetch($ul, value);
                var type = $ul.attr("type");
                if(type === "district"){
                    _this.$el.find('ul').addClass('hidden');
                    _this._set_div_value();
                    _this.$input.trigger('changed-province');
                }
            });
		},

		_set_div_value: function() {
            var info = [];
			var province = this.$el.find('ul[type=province]').attr('data-value');
            if (province ) {
                info.push(province);
            }
			var city = this.$el.find('ul[type=city]').attr('data-value');
            if (city ) {
                info.push(city);
            }
			var district = this.$el.find('ul[type=district]').attr('data-value');
            if (district ) {
                info.push(district);
            }
             var info_str = [];
			var province_str = this.$el.find('ul[type=province]').attr('data-value-str');
            if (province_str ) {
                info_str.push(province_str);
            }
			var city_str = this.$el.find('ul[type=city]').attr('data-value-str');
            if (city_str ) {
                info_str.push(city_str);
            }
			var district_str = this.$el.find('ul[type=district]').attr('data-value-str');
             if (district_str ) {
                info_str.push(district_str);
            }
			this.$el.find('.xa-openSelect').text( info_str.join(' ')).css('color', '#576b95');
			this.$el.find('.xa-openSelect').attr('data-value', info.join('_'));
            $('[name="area"]').val(info.join('_'));
		},
		_select_btn_click: function(event){
            var $ul = $('ul[type=province]')
            $ul.removeClass('hidden').addClass('lightScale');
     		this._fetch('province');
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
                    valueName = this.domList[keyName].find('li[value="'+value+'"]').text();
                    valueNames.push(valueName);
                }
            }
            this.$input.val(values.join('_'));
            this.$input.attr('area-value', valueNames.join(' '));
            this.$input.trigger('change');
        },
        
        _triggerFetch: function($el, value) {
            var type = $el.attr('to-type');
             if(type && value) {
                this._fetch(type, value);
            }
        },
        
        _setOptions: function(type, value) {
            var $select = this.domList[type];
            var key = value ? type + '_' + value : type;
            var data = this.cachData[key];
            optionHtml = '';
            
            for(keyName in data) {
                optionHtml += '<li data-value="'+keyName+'"><div class="ml15 liInner">'+data[keyName]+'</div></li>'
            }
            if (!optionHtml) {
                $('ul[type=district]').attr('data-value', '');
                $('ul[type=district]').attr('data-value-str', '');
                this.$el.find('ul').addClass('hidden');
                this._set_div_value();
                return;
            }
            $select.html(optionHtml);
            $select.removeClass('hidden').addClass('lightScale');
            this.$el.append($select);
        },
        _fetch: function(type, value) {
            if('-1' === value) {
                return;
            }
            var _this = this;
            var key = value ? type + '_' + value : type;
            if(this.cachData[key]) {
                _this._setOptions(type, value);
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
		$(":jqmData(ui-role=areaPop)", e.target).areaPop();
	});
})(jQuery);
