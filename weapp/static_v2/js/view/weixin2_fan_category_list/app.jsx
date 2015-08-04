// TODO: 用React重构粉丝分类列表
ensureNS('W.view.weixin');
var app = app || {};

xlog("in fan_category_list app.jsx");

(function() {
	xlog("in function()");
	'use strict';

	app.FanCategoryModel = function(key) {
		xlog("in FanCategoryModel()");
		this.key = key;
		obj = JSON.parse('{"errMsg": "", "code": 200, "data": {"fan_has_category_id": 0, "categories": [{"is_editable": false, "name": "\u672a\u5206\u7ec4", "id": 0}, {"is_editable": true, "name": "\u661f\u6807\u7ec42", "id": 33}, {"is_editable": true, "name": "aaaa", "id": 36}, {"is_editable": true, "name": "\u4e00\u4e8c\u4e09\u56db", "id": 37}, {"is_editable": true, "name": "111122", "id": 38}, {"is_editable": true, "name": "222233", "id": 39}]}, "success": true, "innerErrMsg": ""}');
		this.categories = obj['data']['categories'];
		this.onChanges = [];
	};

	app.FanCategoryModel.prototype.subscribe = function(onChange) {
		xlog("in FanCategoryModel.subscribe()");
		this.onChanges.push(onChange);
	};

	app.FanCategoryModel.prototype.inform = function(onChange) {
		xlog("in FanCategoryModel.inform()");
		this.onChanges.forEach(function(cb) {xlog("in inner call-back function of inform()"); cb(); });
	};


	app.CategoryItem = React.createClass({
		getInitialState: function() {
			//xlog("in CategoryItem.getInitialState()");
			return {};
		},

		render: function() {
			//xlog("in CategoryItem.render()");
			return (
                    	<li className="xa-hoverEditor pl20" data-id="{{this.props.id}}" data-name={this.props.name}><span className="xui-i-categoryName">{this.props.name}</span>（{this.props.fanCount}）
                    	</li>
			);
		},
	});

	var CategoryItem = app.CategoryItem;


	var FanCategoryList = React.createClass({
		getInitialState: function() {
			xlog("in getInitialState()");
			return {
				editing: null
			};
		},

		componentDidMount: function() {
			xlog("in componentDidMount()");
		},

		render: function() {
			xlog("in render()");
			var main;
			var categories = this.props.model.categories;

			var showCategories = categories.filter(function (category) {
				return true;
			}, this);

			var categoryItems = showCategories.map(function (category) {
				return (
					<CategoryItem
						key={category.id}
						id={category.id}
						name={category.name}
						fanCount={0}  />
					)
			});

			main = (
				<div>
				<ul className='xui-i-addLi pa'>	
				{categoryItems}
				</ul>
				</div>
				);

			return (
				<div>
				{main}
				</div>
			);
		},
	});
	
	var model = new app.FanCategoryModel('fan-category-list');

	function render() {
		xlog("in FanCategoryList render()");
		React.render(
			<FanCategoryList model={model}/>,
			document.getElementById('fan-category-list-app')
			);
	};

	model.subscribe(render);
	render();
})();
