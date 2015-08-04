/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * <div data-ui-role="countdown" now-time="2013-12-19 17:20:00" end-time="2013-12-22 15:20:00" start-time="2013-12-18 15:20:00" countdown-name="团购"></div>
 * value属性的值:省_城市_区
 * author: tianyanrong
 */
(function($, undefined) {
	// component definition
	$.widget("mobile.countdown", $.mobile.widget, {
        _setting: {
            startTime: function(_this) {
                return _this._formatTime(_this.$el.attr('start-time'));
            },
            endTime: function(_this) {
                return _this._formatTime(_this.$el.attr('end-time'));
            },
            nowTime: function(_this) {
                return _this._formatTime(_this.$el.attr('now-time') || (+new Date()));
            },
            name: function(_this) {
                return _this.$el.attr('countdown-name');
            },
            getButtonElement: function(_this) {
                return $('#'+_this.$el.attr('button-id'));
            }
        },
        
        _getTipInfo: function() {
            var name = this._setting.name(this);
            return [name+'已经结束了，敬请期待新一轮'+name+'！', '距离'+name+'开始还有：', '距离'+name+'结束仅剩：'];
        },
        
        _formatTime: function(time) {
            time = time.split(/\D+/g);
            return (+new Date(time[0], time[1]-1, time[2], (time[3] || 0), (time[4] || 0), (time[5] || 0)))/1000;
        },
        
		_create : function() {
            this.$el = this.element;
            this.$el.html(this._getTimplate());
            this.$el.css({'display':'none'});
            this._setting.getButtonElement(this).css({'display':'none'});
            this._countDown(this._setting.nowTime(this), this._setting.startTime(this), this._setting.endTime(this), this.$el[0], 'p', 'span', 'b', this._getTipInfo());
        },
        
        _getTimplate: function() {
            return '<b class="koInfo tx_title"></b>\
                    <p class="time tx_time">\
                        <span class="num tx_num">00</span>日\
                        <span class="num tx_num">00</span>时\
                        <span class="num tx_num">00</span>分\
                        <span class="num tx_num">00</span>秒\
                    </p>';
        },
        
        _countDown: function(nowtime,starttime,endtime,container,timeTag,numTag,infoTag,tipInfo) {
            var _this = this;
            var obj = container;
            var aTime = obj.getElementsByTagName(timeTag)[0];
            var aNum = aTime.getElementsByTagName(numTag);
            var aInfo = obj.getElementsByTagName(infoTag)[0];
            window.nowtime = nowtime;
            //秒杀主函数
            function count()
            {
                nowtime  = ++window.nowtime;
                if(nowtime > endtime)
                {
                    _this._setDisable(true);
                    aInfo.innerHTML = tipInfo[0];
                    aTime.style.display = "none";
                    return;
                    
                }else if(starttime > nowtime){
                    _this._setDisable(true);
                    var d = calculateTime(starttime,nowtime);
                    aInfo.innerHTML = tipInfo[1];
                    
                    aNum[0].innerHTML = d.day;
                    aNum[1].innerHTML = d.hour;
                    aNum[2].innerHTML = d.min;
                    aNum[3].innerHTML = d.sec;
                    
                    return;
                    
                }else if(nowtime >= starttime){
                    _this._setDisable(false);
                    var d = calculateTime(endtime,nowtime);
                    aInfo.innerHTML = tipInfo[2];
                    
                    aNum[0].innerHTML = d.day;
                    aNum[1].innerHTML = d.hour;
                    aNum[2].innerHTML = d.min;
                    aNum[3].innerHTML = d.sec;
                    
                    return;
                }else{
                        
                }
            }
            //秒杀时间的判断
            function calculateTime(bigTime,smallTime)
            {
                var c = Math.floor(bigTime-smallTime);
                var d,h,m,s;
                
                d = Math.floor(c/24/3600);
                
                if(d<=0){
                    h = Math.floor(c/3600);	
                }else{
                    h=Math.floor((c-d*24*3600)/3600);
                }
                m=Math.floor((c-d*24*3600-h*3600)/60);
                s=Math.floor(c-d*24*3600-h*3600-m*60);
                
                return {
                        day:addZero(d),
                        hour:addZero(h),
                        min:addZero(m),
                        sec:addZero(s)
                    };
            };

            //给一位数的数字前增加"0"
            function addZero(num)
            {
                return parseInt(num) < 10 ? ("0"+num) : (num);
            }
            
            //循环
            setInterval(count,1000);
        },
        
        //设置按钮状态
        _setDisable: function(isDisable) {
            var $button = this._setting.getButtonElement(this);
            this.$el.show();
             if (isDisable) {
                $button.hide();
            }else{
                $button.show();
            };
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
		$(":jqmData(ui-role=countdown)", e.target).countdown();
	});
})(jQuery);
