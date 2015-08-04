/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 组件列表视图
 * @class
 */
W.workbench.ComponentListView = Backbone.View.extend({
	el: '',

	events: {
        'mouseenter .xui-component': 'onMouseEnterComponent'
	},

    getTemplate: function() {
        $('#component-list-tmpl-src').template('component-list-tmpl');
        return "component-list-tmpl";
    },
	
	initialize: function(options) {
		this.template = this.getTemplate();
        this.el = $.tmpl(this.template, {components: W.component.COMPONENTS})[0];
        this.$el = $(this.el);

        $(options.el).append(this.$el);
	},

    fitSize: function() {
        var windowHeight = $(window).height();
        var $sectionContainer = this.$('.sectionContainer');
        var sectionContainerTop = $sectionContainer.offset().top;
        var sectionContainerHeight = windowHeight - sectionContainerTop;
        this.$('.sectionContainer').height(sectionContainerHeight);
    },

    render: function() {
        console.log("in ComponentListView.render()");
        this.fitSize();
        this.$('li').draggable();
        var options = { 
            opacity: 0.7, 
            helper: "clone",
            revert: "invalid",
            delay: 10,
            cursorAt: { left: 30, top: -2 },
            start: function(event, ui) {
                xlog('start drag...');
                W.Broadcaster.trigger("component:start_drag");
            },
            drag: function(event, ui) {
                W.Broadcaster.trigger('component:drag', event, ui);
            },
            stop: function(event, ui) {
                xlog('stop drag...');
                W.Broadcaster.trigger("component:stop_drag");
            } 
        }
        $('li').draggable(options);
    },

    onMouseEnterComponent: function(event) {
        xlog('mouse enter');
    }
});