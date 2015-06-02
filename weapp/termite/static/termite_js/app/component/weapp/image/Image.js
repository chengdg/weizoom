/**
 * @class W.component.weapp.Image
 * 
 */
W.component.weapp.Image = W.component.Component.extend({
	type: 'weapp.image',
    selectable: 'no',
	propertyViewTitle: '图片',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'hidden',
                displayName: '',
                default: '图片',
            }, {
                name: 'size',
                type: 'hidden',
                displayName: '',
                default: 'null',
            }, {
                name: 'title',
                type: 'text',
                displayName: '标题',
                isUserProperty: true,
                default: '',
            },{
                name: 'originalPrice',
                type: 'text',
                displayName: '原价',
                isUserProperty: true,
                default: '原价',
            }, {
                name: 'price',
                type: 'text',
                displayName: '价格',
                isUserProperty: true,
                default: '￥',
            }, 
             {
                name: 'tag',
                type: 'text',
                displayName: '标签',
                isUserProperty: true,
                default: '',
            },
            {
                name: 'image',
                type: 'dialog_select',
                displayName: '图片',
                isUserProperty: true,
                triggerButton: '选择图片...',
                dialog: 'W.workbench.SelectImageDialog',
                default: ''
            }, {
                name: 'target',
                type: 'dialog_select',
                displayName: '链接',
                isUserProperty: true,
                triggerButton: '选择内容...',
                dialog: 'W.dialog.workbench.SelectLinkTargetDialog',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        image: function($node, model, value, $propertyViewNode) {
            var parentComponent = W.component.getComponent(this.pid);
            $propertyViewNode.find('.dynamicComponentControlImgBox img').attr('src', value);
            W.getImgOriginalSize(value, function(width, height) {
                model.set('size', width+":"+height, {silent: true});
            });
            if(parentComponent.type === 'weapp.image_group') {
                //轮播图，刷新design page
                W.Broadcaster.trigger('designpage:refresh');
            } else {
                $node.find('.wa-inner-imgbox').attr('src', value);
            }

            var task = new W.DelayedTask(function() {
                W.Broadcaster.trigger('component:resize', this);
            }, this);
            task.delay(200);
        },
        title: function($node, model, value, $propertyViewNode) {
            var parentComponent = W.component.getComponent(this.pid);
            if(parentComponent.type === 'weapp.image_group') {
                if (parentComponent.model.displayMode === 'swipe') {
                    //轮播图，不做处理
                    return;
                }
            }

            var $title = $node.find('.wa-inner-title');
            $title.text(value);
            if (value) {
                $title.show();
            } else {
                $title.hide();
            } 

            if ($propertyViewNode) {
                if (value.length > 10) {
                    value = value.substring(0, 10) + '...';
                }
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
            }
            var task = new W.DelayedTask(function() {
              W.Broadcaster.trigger('component:resize', this);
            }, this);
            task.delay(200);
        },
        price: function($node, model, value, $propertyViewNode) {
            var parentComponent = W.component.getComponent(this.pid);
            if(parentComponent.type === 'weapp.image_group') {
                if (parentComponent.model.displayMode === 'swipe') {
                    //轮播图，不做处理
                    return;
                }
            }

            var $price = $node.find('.wa-inner-price');
            $price.text(value);
            if (value) {
                $price.show();
            } else {
                $price.hide();
            }

            if ($propertyViewNode) {
                if (value.length > 10) {
                    value = value.substring(0, 10) + '...';
                }
                $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
            }
        },
        originalPrice: function($node, model, value, $propertyViewNode) {
             var parentComponent = W.component.getComponent(this.pid);
             if(parentComponent.type === 'weapp.image_group') {
                 if (parentComponent.model.displayMode === 'swipe') {
                     //轮播图，不做处理
                     return;
                 }
             }

             var $price = $node.find('.wa-inner-originalPrice');
             $price.text(value);
             if (value) {
                 $price.show();
             } else {
                 $price.hide();
             }

             if ($propertyViewNode) {
                 if (value.length > 10) {
                     value = value.substring(0, 10) + '...';
                 }
                 $propertyViewNode.find('.propertyGroup_property_dynamicControlField_title span').text(value);
             }
        },
        target: function($node, model, value, $propertyViewNode) {
            var data = $.parseJSON(value);
            if ($propertyViewNode) {
                $propertyViewNode.find('.x-targetText').text(data.data_path);
            }
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});