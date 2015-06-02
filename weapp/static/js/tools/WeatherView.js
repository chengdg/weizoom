/*
*Copyright (c) 2011-2012 Weizoom Inc
*属性:language -- 语言设置 [Chinese || English]
*/
W.WeatherView = function(options) {
	this.$el = $(options.el);
	this.templateId = options.templateId;
	this.render = options.render || this.render;
    this.language = options.language || 'Chinese';
	this.initialize();
	return this;
}

W.WeatherView.prototype = {
    languages: {
        Chinese: {
            today: '今天',
            loading: '加载中...'
        },
        English: {
            today: 'Today',
            loading: 'loading...',
            weeks: {
                '周日': 'Sun',
                '周一': 'Mon',
                '周二': 'Tues',
                '周三': 'Wed',
                '周四': 'Thur',
                '周五': 'Fri',
                '周六': 'Sat'
            },
            weathers:{
                '1': 'sunny',
                '2': 'cloudy',
                '3': 'overcast',
                '4': 'shower',
                '5': 'thundershower',
                '6': 'thundershower and hail',
                '7': 'sleety',
                '8': 'light rain',
                '9': 'moderate rain',
                '10': 'heavy rain',
                '11': 'rainstorm',
                '12': 'downpour',
                '13': 'extraordinary rainstorm',
                '14': 'hail',
                '15': 'showery snow',
                '16': 'light snow',
                '17': 'moderate snow',
                '18': 'heavy snow',
                '19': 'snowstorm',
                '20': 'foggy',
                '21': 'ice rain',
                '22': 'sand storm',
                '23': 'light rain/moderate rain',
                '24': 'moderate rain/heavy rain',
                '25': 'heavy rain/rainstorm',
                '26': 'rainstorm/downpour',
                '27': 'downpour/extraordinary rainstorm',
                '28': 'light snow/moderate snow',
                '29': 'moderate snow/heavy snow',
                '30': 'heavy snow/snowstorm',
                '31': 'dusty',
                '32': 'sand blowing',
                '33': 'severe sand and dust storm'
            }
        }
    },
    
	model: {
		app: 'tool',
		api: 'weather/info'
	},
	
	initialize: function() {
		this.fetch();
	},
	
	weatherClassNames: {
		'晴': '1',
		'多云': '2',
		'阴': '3',
		'阵雨': '4',
		'雷阵雨': '5',
		'雷阵雨伴有冰雹': '6',
		'雨夹雪': '7',
		'小雨': '8',
		'中雨': '9',
		'大雨': '10',
		'暴雨': '11',
		'大暴雨': '12',
		'特大暴雨': '13',
		'冰雹': '14',
		'阵雪': '15',
		'小雪': '16',
		'中雪': '17',
		'大雪': '18',
		'暴雪': '19',
		'雾': '20',
		'冻雨': '21',
		'沙尘暴': '22',
		'小雨-中雨': '23',
		'中雨-大雨': '24',
		'大雨-暴雨': '25',
		'暴雨-大暴雨': '26',
		'大暴雨-特大暴雨': '27',
		'小雪-中雪': '28',
		'中雪-大雪': '29',
		'大雪-暴雪': '30',
		'浮尘': '31',
		'扬沙': '32',
		'强沙尘暴': '33'
	},
	
	fetch: function(event) {
		var _this = this;
		if(this.itemIndex) {
			this.args.item_index = this.itemIndex;
		}
		this.$el.alert({
			'info': this.languages[this.language].loading,
			'top': '.ui-header'
		});
		W.getApi().call({
			api: this.model.api,
			app: this.model.app,
			success: function(data) {
				_this.parse(data);
				_this.render(_this.cacheData);
				_this.$el.alert({
					isShow: false
				});
			},
			error: function(resp) {
				var msg = '更新失败';
				if(!_this.isFirstLoading) {
					msg = '加载失败';
					_this.isFirstLoading = true;
				}
				_this.$el.alert({
					info: msg,
					speed: 2000
				});
			}
		});
	},
	
	render: function(data) {
		var tmplId = this.templateId + '-tmpl';
		$('#' + this.templateId).template(tmplId);
        data.language = this.language;
		this.$el.html($.tmpl(tmplId, data));
	},
	
	splitTemp: function(temp) {
		temp = temp.split('~');
		return {
			temp_lowest: temp[1].replace('℃', ''),
			temp_highest: temp[0].replace('℃', '')
		}
	},
	
	splitDate: function(date, isTime) {
		date = date.split(/\D+/);
		var time = '';
		if(isTime) {
			time = ' ' + date[3] + ':' + date[4];
		}
		return date[1] + '/' + date[2] + time;
	},
	
	getWeatherCssName: function(weather) {
		if(weather.indexOf('转')) {
			weather = weather.split('转');
		}
		else {
			weather = [weather];
		}
		
		if(weather[1]) {
			return [this.weatherClassNames[weather[1]]];
		}
		else {
			return [this.weatherClassNames[weather[0]]];
		}
	},
	
	parse: function(data) {
		var i, k;
		var temp;
		var themeCss;//
		var weatherCss;
        var newWeekName;
        var newWeatherName;
		data.weather_infos = data.weather_info;
		delete data.weather_info;
        
		
		if(data.create_time.indexOf(data.today_date) >= 0) {
			data.create_time = data.create_time.replace(data.today_date, this.languages[this.language].today);
		}
		else {
			data.create_time = this.splitDate(data.create_time, true);
		}
		
		var weatherInfos = data.weather_infos;
		for(i = 0, k = weatherInfos.length; i < k; i++) {
			weatherCss = this.getWeatherCssName(weatherInfos[i].weather);
			weatherInfos[i].daytime = data.is_daytime ? 'day' : 'night';
			weatherInfos[i].status = weatherCss[0];
			if(data.today_date === weatherInfos[i].date) {
				weatherInfos[i].is_today = true;
				weatherInfos[i].week = this.languages[this.language].today;
				data.current_weather_info = weatherInfos[i];
			}
			weatherInfos[i].date = this.splitDate(weatherInfos[i].date);
			temp = this.splitTemp(weatherInfos[i].temp);
			weatherInfos[i].temp_lowest = temp.temp_lowest;
			weatherInfos[i].temp_highest = temp.temp_highest;
            
            //多语方处理
            newWeekName = this.languages[this.language].weeks ? this.languages[this.language].weeks[weatherInfos[i].week] : false;
            if(weatherInfos[i].week && newWeekName) {
                weatherInfos[i].week = newWeekName;
            }
            newWeatherName = this.languages[this.language].weathers ? this.languages[this.language].weathers[weatherCss]: false;
            if(weatherInfos[i].weather && newWeatherName) {
                weatherInfos[i].weather = newWeatherName
            }
		}
		this.cacheData = data;
	}
}