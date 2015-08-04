/*
 * 地址选择插件(弹出)
 * 
 *
 * 使用示例;
 * <input name="area" data-ui-role="areaPop" type="text" value="1_1_2">
 * value属性的值:省_城市_区
 * author: guoliyan
 */
 (function( $, undefined ) {
gmu.define('AreaPop', {
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

    _create: function() {
       // FastClick.attach(document.body);
        var $el = this.$el;
        this.$input = this.$el;
        xlog(this.$input);
        this.$input.attr('type', 'hidden');
        this.domList = {
            province: $('<ul type="province" to-type="city" id="areaWidget-province" class="xui-popAddress xui-provice"></ul>'),
            city: $('<ul type="city" to-type="district" id="areaWidget-city" class="xui-popAddress xui-city"></ul>'),
            district: $('<ul type="district" id="areaWidget-district" class="xui-popAddress xui-district"></ul>')
        }

        this.$el = this.$input.parent('.xa-areaPopContainer');
        this.$el.attr('class', 'wui-area');

        var area_str = this.$input.attr('data-area-str') || '请选择省市区';
        var $infoBox = $('<div class="xa-openSelect pl5" style="color:#888;font-size:0.9em;" >'+area_str+'<i></i></div>');
        var $outer = $('<div class="hidden xui-outer" >'+
                            '<div class="pr xui-inner" id="xa-wrapper">'+
                                '<div class="xui-proviceTag xa-proviceTag hidden" style="color:#888;"></div>'+
                                '<div class="xui-cityTag xa-cityTag hidden" style="color:#888;"></div>'+
                            '</div>'+
                        '</div>');

        if($infoBox.text() == '请选择省市区'){
            $infoBox.addClass('xui-openSelect');
            $infoBox.css('color','#C7C7CC')
        }

        this.$el.append($infoBox).append($outer);

        var $inner = this.$el.find('.xui-inner');
        var $proviceTag = this.$el.find('.xa-proviceTag');
        var $cityTag = this.$el.find('.xa-cityTag');

        var height = window.document.body.clientHeight;
        var width = window.document.body.clientWidth;
        //var $iscrollUl = this.$el.find(".xui-popAddress");
        
        $outer.css({
             width: width,
             height: height
         });
        $inner.css({
           width: width,
           height: "1730px"
        });
        $('body').swipeMask('hide');
        this.cachData = {};
        // //绑定change事件
        var _this = this;
        this.$el.delegate('.xa-openSelect', 'click', function(event) {
            $outer.fadeIn(100);
            $infoBox.removeClass('xui-openSelect');
           _this._select_btn_click(event)
        });


         this.$el.delegate('.xa-proviceTag', 'click', function(event) {
         _this._selectProvice();
         
        });

        this.$el.delegate('.xa-cityTag', 'click', function(event) {
         _this._selectCity();
         
        });


        this.$el.delegate('ul li', 'click', function(event) {
            event.stopPropagation();
            $('body').swipeMask('show');
            var $ul = $(this).parent('ul');
            var value = $(this).attr('data-value');
            $ul.attr('data-value', value);
            var value_str = $(this).text();
            
            $ul.attr('data-value-str', value_str)
            _this._triggerFetch($ul, value);

            var type = $ul.attr("type");            
            if(type === "province"){
                _this.$el.find('ul[type="province"]').addClass('hidden');
                _this.$el.find('.xa-proviceTag').removeClass('hidden');
                _this.$el.find('.xa-proviceTag').text(value_str);
            }else if(type === "city"){
                _this.$el.find('ul[type="city"]').addClass('hidden');
                _this.$el.find('.xa-cityTag').removeClass('hidden');
                _this.$el.find('.xa-cityTag').text(value_str);
            }else{
                $(this).parents('.xui-outer').fadeOut(50);
                $('body').swipeMask('hide');
                _this.$el.find('ul').addClass('hidden');
                _this._set_div_value();
                _this.$input.trigger('changed-province');
                _this.$el.find('.xa-proviceTag').addClass('hidden');
                _this.$el.find('.xa-cityTag').addClass('hidden');
                _this.$el.find('.xui-provice').css({'top':0});
            }
        });
        

        //在DOM中缓存this
        $el.data('view', this);
        
        //myScroll = new iScroll('xa-wrapper',{checkDOMChanges:true});
        //解决异步加载dom,引起的iscroll失效
        // var initScroll = function () {
        // intervalTime = setInterval(function () {
        //         var resultContentH = $(".xui-outer").height();
        //         if (resultContentH > 0) {  //判断数据加载完成的条件
        //             //console.log("此时showResult的高度是:" + resultContentH);
        //             $(".xui-outer").height(resultContentH);
        //             setTimeout(function () {
        //                 clearInterval(intervalTime);
        //                 myScroll = new iScroll('xa-wrapper',{checkDOMChanges:true});
        //             }, 100)
        //         }
        //     }, 10);
        // }
        // initScroll();
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
        this.$el.find('.xa-openSelect').text( info_str.join(' ')).css('color', '#888');
        this.$el.find('.xa-openSelect').attr('data-value', info.join('_'));
        $('[name="area"]').val(info.join('_'));
    },
    _select_btn_click: function(event){
        var $ul = $('ul[type=province]');
        //$ul.removeClass('hidden').addClass('lightScale');
        this._fetch('province');
        this._changeTop();

    },
    // _setDefalut: function($el) {
    //     var type = $el.attr('to-type');
    //     if(!type) {
    //         return;
    //     }
    //     this.domList[type].html(this._createDefaulteOption(type));
    //     this.domList[type].selectmenu('refresh');
    //     if('city' === type) {
    //         this.domList.district.html(this._createDefaulteOption('district'));
    //         this.domList.district.selectmenu('refresh');
    //     }
    // },
    
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
            optionHtml += '<li data-value="'+keyName+'"><div class="liInner">'+data[keyName]+'</div></li>'
        }
        if (!optionHtml) {
            $('ul[type=district]').attr('data-value', '');
            $('ul[type=district]').attr('data-value-str', '');
            this.$el.find('.xui-outer').fadeOut(50);
            this.$el.find('ul').addClass('hidden');
            this._set_div_value();
            return;
        }

        $select.html(optionHtml);

        $select.removeClass('hidden');

        var $inner = this.$el.find('.xui-inner');
        $inner.append($select);
        var $activeUl = $('.xui-inner ul:last-child');
        var height = window.document.body.clientHeight;
        if($activeUl.height() < height){
            $activeUl.parent('.xui-inner').height(height);
        }else{
            $activeUl.parent('.xui-inner').height($activeUl.height());
        }
    },

    _fetch: function(type, value) {
        if('-1' === value) {
            return;
        }
        var _this = this;
        var key = value ? type + '_' + value : type;
        if(this.cachData[key]) {//判断是否缓存        
            $('body').swipeMask('hide');
            _this._setOptions(type, value);
            return;
        }

        var url = value ? this._options.api[type] + value + '/' : this._options.api[type];
        $.ajax({
            url: url,
            success: function(data) {
                $('body').swipeMask('hide');
                data = data.data;
                _this.cachData[key] = data;
                _this._setOptions(type, value);       
                if(_this.selectData) {
                    _this._setValue();                    
                }
            },
            error: function(e) {
                $('body').swipeMask('hide');
            }
        })
    },

    // 判断是否改变provice高度
    _changeTop:function(){
        var $el = this.$el;
        var $proviceTag = this.$el.find('.xui-proviceTag');
        if($proviceTag && !$proviceTag.hasClass('hidden')){
            this.$el.find('.xui-provice').css('top','74px;')
        }
    },

    // 点击返回选择省份
    _selectProvice:function(){
        var $el = this.$el;
        var $provice = $el.find('.xui-provice');
        var $district = $el.find('.xui-district');
        var $city = $el.find('.xui-city');
        $el.find('.xa-proviceTag').addClass('hidden');
        $el.find('.xa-cityTag').addClass('hidden');
        $provice.removeClass('hidden').css({'top':0});
        $district.addClass('hidden');
        $city.addClass('hidden');


    },

    //点击返回选择城市
      _selectCity:function(){
        var $el = this.$el;
        var $provice = $el.find('.xui-provice');
        var $district = $el.find('.xui-district');
        var $city = $el.find('.xui-city');
        $el.find('.xa-cityTag').addClass('hidden');
        $city.removeClass('hidden');
        $district.addClass('hidden');
        $provice.addClass('hidden');
    }
})

$(function() {
    $('[data-ui-role="areaPop"]').each(function() {
        var $input = $(this);
        $input.areaPop();
    });
})
})( Zepto );
