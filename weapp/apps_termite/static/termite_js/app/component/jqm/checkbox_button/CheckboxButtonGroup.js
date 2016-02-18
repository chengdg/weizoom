/**
 * @class W.component.jqm.CheckboxButtonGroup
 * 
 */
W.component.jqm.CheckboxButtonGroup = W.component.Component.extend({
	type: 'jqm.checkbox_button_group',
	propertyViewTitle: 'Checkbox Button Group',

    dynamicComponentTypes: [
        {type: 'jqm.checkbox_button', model: {name: '', text: 'Checkbox', value: '', theme: 'c'}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'title',
                type: 'text',
                displayName: 'Title',
                default: '选择'
            }, {
                name: 'is_mini',
                type: 'boolean',
                displayName: 'Mini? ',
                default: "no"
            }, {
                name: 'orientation',
                type: 'select',
                displayName: '排列',
                source: W.data.RadioButtonOrientations,
                default: 'vertical'
            }]
        }, {
            group: '选项集',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
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
        title: function($node, model, value) {
            $node.find('legend').text(value+':');
        },
        is_mini: function($node, model, value) {
            if (value === 'yes') {
                $node.find('label').removeClass('ui-fullsize').addClass('ui-mini');
                $node.find('fieldset').addClass('ui-mini');
            } else {
                $node.find('fieldset').removeClass('ui-mini');
                $node.find('label').removeClass('ui-mini').addClass('ui-fullsize');
            }

            W.Broadcaster.trigger('component:resize', this);
        },
        orientation: function($node, model, value) {
            var oldClass = '';
            var newClass = '';
            if (value === 'vertical') {
                oldClass = "ui-controlgroup-horizontal";
                newClass = "ui-controlgroup-vertical";
            } else {
                newClass = "ui-controlgroup-horizontal";
                oldClass = "ui-controlgroup-vertical";
            }
            
            $node.find('fieldset').removeClass(oldClass).addClass(newClass);
            W.Broadcaster.trigger('component:resize', this);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'Checkboxes',
        imgClass: 'componentList_component_checkbox'
    }
});