//依赖jquery.js和system.js,扩展W
(function(W){
	/**
	 * 列表末尾加载更多的按钮
	 * params是一个对象，格式为
	 * {
	 * 	'url' : ..., 请求的地址，但page暂不需要给数值，也会作为参数传进来
	 * 	'css_id' : ..., id，不能包含#
	 * 	'fn' : ...   该函数在jsonp的success中执行，所以需要一个参数接收response
	 *  'page' : ... 自定义的当前页的变量名,即config.js中的全局变量
	 * }
	 */
	W.loadNextPageBtn = (function(){
		var startLoading = function(obj){
			$('#'+obj.el_id).children().html('<span class="mui-spinner" style="height:20px;width:20px;"></span> 加载中....</span>');
			W.getJsonP(obj.url+window[obj.page],function(response){
					obj.hasNext = obj.innerFn(response);//执行传入的函数，将返回状态赋值给属性
					finishLoding(obj);
				},function(){
					mui.toast("网络或服务器错误，请稍后再试");
					finishLoding(obj);
				}
			);
		};
		var finishLoding = function(obj){
			$('#'+obj.el_id).remove();
			if(obj.hasNext ){
				obj.appendToTail();
			}
		};
		var appendElement = function(obj) {
			var el;
			var elId = obj.el_id;
			var css_id = obj.el_id.substring(0,obj.el_id.lastIndexOf('_btn'));
			el = "<ul id='"+elId+"' style='list-style:none;padding-left:0px;'><li class='mui-btn mui-btn-outlined'  style='text-align:center;width:100%;border:0px;'>点击加载更多</li></ul>";
			$('#'+css_id).append(el);
		};
		return function(params){
			this.hasNext = true;
			this.url = params.url;
			this.el_id = params.css_id+"_btn";
			this.innerFn = params.fn;
			this.page = params.page_name;
			this.appendToTail = function(){
				appendElement(this);
				var that = this;
				$('#'+this.el_id).one('click',function(){
					startLoading(that);
				});
			};
		};
	})();
})(W);
