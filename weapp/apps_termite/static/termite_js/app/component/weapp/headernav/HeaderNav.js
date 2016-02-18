/**
 * @class W.component.weapp.HeaderNav
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.HeaderNav = W.component.Component.extend({
	type: 'weapp.headernav',
	selectable: 'no',
	propertyViewTitle: '页头导航',

	properties: [
        {
            group: '属性1',
            fields: [{
            	name: 'title',
            	type: 'text',
            	displayName: '导航名称',
                isUserProperty: true,
            	default: '全部'
            },{
                name: 'tag',
                type: 'text',
                displayName: '标签',
                isUserProperty: true,
                default: 'all'
            }]
        }
    ],

    propertyChangeHandlers: {
        title: function($node, model, value, $propertyViewNode) {
        	$node.find('div').html(value);
        	$propertyViewNode.find('h3 span').html(value);
        },
        target: function($node, model, value, $propertyViewNode) {
            var data = $.parseJSON(value);
            if ($propertyViewNode) {
                $propertyViewNode.find('.x-targetText').text(data.data_path);
            }
        }
    }
});
