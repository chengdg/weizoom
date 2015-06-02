/*
 * Jquery Mobile地图插件
 *
 * 该插件进行地图的相应api支持，支持的功能有：
 * 1. 给出目的地的gps坐标，展现驾车导航路线图
 * 2. 给出目的地的gps坐标进行定位
 *
 * 使用示例;
 * <div data-ui-role="map" data-map-api="driveroute" data-target-lat="39.0" data-target-lng="139.1">
 * </div>
 * 
 * author: chuter
 */
(function($, undefined) {
	// component definition
	$.widget("mobile.map", $.mobile.widget, {
		options : {
    		mapApi : "driveroute", //所使用的api，默认为驾车导航，支持的api包括：driveroute(驾车导航)，
    	                           //locate(定位)
			targetLat : 0.0,       //目的地纬度
			targetLng : 0.0,       //目的地经度
			targetName : "",       //目的地名称
			apiType : "js",        //百度地图api方式，js表示javascript的api，还有mobile，表示移动端使用的api，
			                       //如果需要导航则使用mobiel方式，如果只是在地图中标识目标点简单的显示只需使用js方式即可
		},
		
		settings : {
			
		},
				
		_create : function() {			
			this._bind();
			
			this._valid_target_coordinate();
			
			if ("js" == this.options.apiType) {
				this._js_api();
			} else {
				this._mobile_api();
			}
		},
		
		mobile_drive_route : function() {
			if (navigator.geolocation) {
        		var options = {timeout : 6000, enableHighAccuracy: true, maximumAge: 60000}
        		navigator.geolocation.getCurrentPosition($.proxy(this._mobile_draw_drive_route, this), $.proxy(this._mobile_gps_errorHandler, this), options);
    		} else {
        		$('body').alert({
            		info:'浏览器不支持获取位置信息',
            		speed: 1000
        		});

				this.mobile_locate();
	    	}
		},
		
		_mobile_api : function() {
			if ("driveroute" == this.options.mapApi) {
				this.mobile_drive_route();
			} else if ("locate" == this.options.mapApi) {
				this.mobile_locate();
			} else {
				this._error("不支持api操作"+this.options.mapApi);
			}
		},
		
		_js_api : function() {
			if ("driveroute" == this.options.mapApi) {
				this.js_drive_route();
			} else if ("locate" == this.options.mapApi) {
				this.js_locate();
			} else {
				this._error("不支持api操作"+this.options.mapApi);
			}
		},
		
		_valid_target_coordinate : function() {
			if (this.options.targetLat < -90.0 || this.options.targetLat > -90.0
					|| this.options.targetLng < -180.0	|| this.options.targetLng > -180.0) {
				this._error("目的地gps坐标位置非法");
			}
		},
		
		js_locate : function() {
			var target = new BMap.Point(this.options.targetLng, this.options.targetLat);
			var map = this._create_map();
			
			map.centerAndZoom(target, 15);			
			var marker = new BMap.Marker(target);  // 创建标注
			map.addOverlay(marker);              // 将标注添加到地图中
			marker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画
		},
		
		mobile_locate : function() {
			api_url = "http://api.map.baidu.com/marker?location="+this.options.targetLat+","+this.options.targetLng+"&title="+this.options.targetName+"&content="+this.options.targetName+"&output=html&src=weizoom";
        	
        	this.element.attr('href', api_url);
        	this.element.attr('rel', "external");
		},
		
		_mobile_draw_drive_route : function(pos) {
			origin = "latlng:"+pos.coords.latitude+","+pos.coords.longitude+"|name:我的位置";
			api_url = "http://api.map.baidu.com/direction?destination=latlng:"+this.options.targetLat+","+this.options.targetLng+"|name:"+this.options.targetName+"&mode=driving&region=开封&output=html&src=weizoom&origin=" + origin
			
			this.element.attr('href', api_url);
        	this.element.attr('rel', "external");
		},
		
		_js_draw_drive_route : function(pos) {
			var lat = pos.coords.latitude;
        	var lng = pos.coords.longitude;
        	
        	var from = new BMap.Point(lng, lat);
        	var to = new BMap.Point(this.options.targetLng, this.options.targetLat);

			var map = this._create_map();
			map.centerAndZoom(from, 11);	
			
        	var driving = new BMap.DrivingRoute(map, {renderOptions:{map: map, autoViewport: true}});
        	driving.search(from, to);
		},
		
		js_drive_route : function() {			
			if (navigator.geolocation) {
        		var options = {timeout : 6000, enableHighAccuracy: true, maximumAge: 60000}
        		navigator.geolocation.getCurrentPosition($.proxy(this._js_draw_drive_route, this), $.proxy(this._js_gps_errorHandler, this), options);
    		} else {
        		$('body').alert({
            		info:'浏览器不支持获取位置信息',
            		speed: 1000
        		});

				this.js_locate();
	    	}
		},
		
		_error : function(eventInfo) {
			var $elem = this.element;
			$elem.trigger("errorOccur", [eventInfo]);
		},
		
		_js_gps_errorHandler : function(err) {
      		$('body').alert({
				info:'获取当前位置失败',
            	speed: 1000
          	});

			this.js_locate();
    	},
    	
    	_mobile_gps_errorHandler : function(err) {
      		$('body').alert({
				info:'获取当前位置失败',
            	speed: 1000
          	});

			this.mobile_locate();
    	},

		_bind : function() {
		},
		
		_unbind : function() {
		},
		
		_create_map : function() {
			var map = new BMap.Map("map");
			map.addControl(new BMap.NavigationControl());  //添加默认缩放平移控件
			return map;
		},
		
		destroy : function() {
			// Unbind any events that were bound at _create
			this._unbind();

			this.options = null;
		},
	});

	// taking into account of the component when creating the window
	// or at the create event
	$(document).bind("pagecreate create", function(e) {
		$(":jqmData(ui-role=map)", e.target).map();
	});
})(jQuery);
