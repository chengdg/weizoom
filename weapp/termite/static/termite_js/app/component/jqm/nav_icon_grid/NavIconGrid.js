/**
 * @class W.component.jqm.Grid
 * 
 */
W.component.jqm.NavIconGrid = W.component.Component.extend({
	type: 'jqm.nav_icon_grid',
	propertyViewTitle: '导航按钮',

    dynamicComponentTypes: [
        {type: 'jqm.nav_icon_grid_button', model: {index: 1, text: '导航1', icon:'', target:'', color:'#F46B41'}},
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'columns',
                type: 'select',
                displayName: '列数',
                source: W.data.getIntegerRanges(2, 5),
                default: '4'
            }, {
                name: 'width',
                type: 'text',
                displayName: '宽度',
                default: '300'
            }, {
                name: 'height',
                type: 'text',
                displayName: '高度',
                default: '205'
            }, {
                name: 'fixed_position',
                type: 'select',
                displayName: '固定？',
                source: W.data.FixedPositions,
                default: "none"
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
        /*
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
        */
    }
}, {
    indicator: {
        name: '导航图标Grid',
        imgClass: 'componentList_component_grid'
    }
});
