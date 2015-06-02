/**
 * @class W.component.jqm.Grid
 * 
 */
W.component.jqm.NavGrid = W.component.Component.extend({
	type: 'jqm.nav_grid',
	propertyViewTitle: '导航Grid',

    dynamicComponentTypes: [
        {type: 'jqm.nav_grid_button', model: {index: 1, text: '导航1', image:'', target:''}},
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'columns',
                type: 'select',
                isUserProperty: true,
                displayName: 'Columns',
                source: W.data.getIntegerRanges(2, 5),
                default: '3'
            }, {
                name: 'is_image_shadow',
                type: 'boolean',
                isUserProperty: true,
                displayName: '图片阴影？',
                default: 'yes'
            }]
        }, {
            group: '选项集',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
        items: function($node, model, value) {
            var index = 1;
            var orderedCids = value;
            _.each(orderedCids, function(cid) {
                W.component.CID2COMPONENT[cid].model.set('index', index++, {silent: true});
            });

            var task = new W.DelayedTask(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this);
            task.delay(100);
        },
        columns: function($node, model, value) {
            var columns = parseInt(model.get('columns'));
            var rows = parseInt(model.get('rows'));
            this.updateContainers(rows * columns);

            W.Broadcaster.trigger('designpage:refresh');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);

        /*
        if (!obj || !obj.model) {
            //创建新的grid，而非从json parse
            var columns = parseInt(this.model.get('columns'));
            var rows = parseInt(this.model.get('rows'));
            this.updateContainers(rows * columns);    
        }
        */
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
        name: '导航Grid',
        imgClass: 'componentList_component_grid'
    }
});
