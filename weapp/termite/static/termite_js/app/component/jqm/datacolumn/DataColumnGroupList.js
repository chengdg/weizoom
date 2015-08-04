/**
 * @class W.component.jqm.DataColumnGroupList
 * 
 */
W.component.jqm.DataColumnGroupList = W.component.Component.extend({
	type: 'jqm.datacolumn_group_list',
	propertyViewTitle: 'Data Column Group List',

    dynamicComponentTypes: [
        {type: 'jqm.datacolumn_group', model: {index: 1, text: '数据分类1', columns: '3'}},
    ],

	properties: [
        {
            group: 'Model属性',
            fields: []
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
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Data Column',
        imgClass: 'componentList_component_grid'
    }
});