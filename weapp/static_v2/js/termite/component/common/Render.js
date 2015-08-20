/**
 * @class W.component.Component
 * 组件的基类
 *
 */
ensureNS('W.component');
W.component.Render = function(obj) {
	this.initialize(obj);
}


// 相当于让Render继承自Backbone.Events，并增加了若干函数
_.extend(W.component.Render.prototype, Backbone.Events, {
	initialize: function(obj) {
		//编译handlebar模板
		this.template = null;
		this.compileTemplates();
	},

	compileTemplates: function() {
		var $templates = $('[data-component-template="true"]');
		this.$templates = $templates;

		var contents = []
		if ($templates.length == 0) {
			xwarn('no component template');
			return;
		}

		if ($templates.length > 0) {
			for (var i = 0; i < $templates.length; ++i) {
				var $template = $templates.eq(i);
				contents.push($template.html());
			}	
		}

		this.template = Handlebars.compile(contents.join("\n"));
		this.template({}); //第一次渲染，加速后续的渲染
	},

	refresh: function(component) {
		return this.__do_render(component);
	},

	render: function(component) {
		var componentContainer = {
			type: 'wepage.runtime_component_container',
			components: [component]
		}
		component = componentContainer;

		return this.__do_render(component);
	},

	__do_render: function(component) {
		//先渲染sub component
		var subComponents = component.components;
		subComponents = _.sortBy(subComponents, function(subComponent) { return subComponent.model.index; });
		var subComponentCount = subComponents.length;
		for (var i = 0; i < subComponentCount; ++i) {
			var subComponent = subComponents[i];
			subComponent.parent_component = component;
			subComponent.html = this.__do_render(subComponent);
		}

		//渲染component自身
		var context = {
			in_design_mode: true,
			in_product_mode: false,
			component: component
		}
		if (!this.template) {
			this.compileTemplates();
		}
		var html = '<div>'+$.trim(this.template(context))+'</div>';
		var $node = $(html);
		$node.find('a').attr('href', 'javascript:void(0);');
		return $node.html();
	}
});


$(document).ready(function() {
	W.Render = new W.component.Render();
})
/*
_.delay(function() {
	W.Render = new W.component.Render();	
}, 200);
*/
