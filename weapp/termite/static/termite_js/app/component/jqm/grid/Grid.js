/**
 * @class W.component.jqm.Grid
 * 
 */
W.component.jqm.Grid = W.component.Component.extend({
	type: 'jqm.grid',
	propertyViewTitle: 'Grid',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'columns',
                type: 'select',
                displayName: 'Columns',
                source: W.data.getIntegerRanges(2, 5),
                default: '2'
            }, {
                name: 'rows',
                type: 'select',
                displayName: 'Rows',
                source: W.data.getIntegerRanges(1, 6),
                default: "1"
            }]
        }
    ],

    propertyChangeHandlers: {
        columns: function($node, model, value) {
            var columns = parseInt(model.get('columns'));
            var rows = parseInt(model.get('rows'));
            this.updateContainers(rows * columns);

            W.Broadcaster.trigger('designpage:refresh');
        },
        rows: function($node, model, value) {
            var columns = parseInt(model.get('columns'));
            var rows = parseInt(model.get('rows'));
            this.updateContainers(rows * columns);
            
            //W.Broadcaster.trigger('workbench:refresh_design_page');
            W.Broadcaster.trigger('designpage:refresh');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);

        if (!obj || !obj.model) {
            //创建新的grid，而非从json parse
            var columns = parseInt(this.model.get('columns'));
            var rows = parseInt(this.model.get('rows'));
            this.updateContainers(rows * columns);    
        }
    },

    updateContainers: function(count) {
        var originalCount = this.components.length;
        if (originalCount == count) {
            return;
        } else if (originalCount > count) {
            //缩减
        } else {
            //增加
            var addedCount = count - originalCount;
            for (var i = 0; i < addedCount; ++i) {
                var container = new W.component.jqm.GridContainer();
                this.addComponent(container);
            }
        }
    }
}, {
    indicator: {
        name: 'Grid',
        imgClass: 'componentList_component_grid'
    }
});
