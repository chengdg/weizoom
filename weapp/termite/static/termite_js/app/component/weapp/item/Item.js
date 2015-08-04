/**
 * @class W.component.weapp.Item
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.Item = W.component.Component.extend({
	type: 'weapp.item',
	selectable: 'no',
	propertyViewTitle: '商品',

	properties: [
        {
            group: '属性1',
            fields: [{
            	name: 'title',
            	type: 'hidden',
                isUserProperty: true,
            	default: '选择商品'
            },{
                name: 'target',
                type: 'dialog_select',
                displayName: '商品',
                isUserProperty: true,
                dialogParameter: 'W.component.weapp.Item.getTarget',
                triggerButton: '选择商品...',
                dialog: 'W.dialog.workbench.SelectLinkTargetDialog'
            }]
        }
    ],

    propertyChangeHandlers: {
        target: function($node, model, value, $propertyViewNode) {
            var data = $.parseJSON(value);
            var $innerPic = $node.find('.wui-inner-pic');
            var $img = $innerPic.find('img');
            var imgSrc = data['meta']['pic_url'];
            if ($img.length === 0) {
                $img=$innerPic.empty().append($('<img/>').attr('src',imgSrc));
            } else {
                $img.attr('src', imgSrc);
            }

            $node.find('.wa-inner-title').text(data['meta']['name']);
            $node.find('.wa-inner-price').text('¥'+data['meta']['price']);

            var productName = data['meta']['name'];
            if ($propertyViewNode) {
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(productName);
                $propertyViewNode.find('.x-targetText').text(data.data_path);
            }
            model.set('title', productName, {silent:true});
            W.Broadcaster.trigger('component:resize', this);
        }
    }
});

W.component.weapp.Item.getTarget = function(component, $button) {
    var $el = $button.parents('.propertyGroup_property_dynamicControlField_control');
    if ($el.length === 0) {
        return {frozen: true};
    }

    var cid = $el.attr('data-dynamic-cid');
    var itemComponent = W.component.getComponent(cid)
    if (itemComponent.model.get('target')) {
        return {frozen: true};
    } else {
        return {"frozen":true, "currentLinkTarget": {"workspace":"innerName:mall","data_category":"商品"}}
    }
}