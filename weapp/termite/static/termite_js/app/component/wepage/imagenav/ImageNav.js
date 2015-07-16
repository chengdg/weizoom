/**
 * @class W.component.wepage.ImageNav
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.ImageNav = W.component.Component.extend({
	type: 'wepage.image_nav',    
    selectable: 'no',
	propertyViewTitle: '图片导航',

    properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'image',
                type: 'dialog_select',
                isUserProperty: true,
                triggerButton: '选择图片...',
                selectedButton: '重新上传',
                // help:'建议图片尺寸：260*260',
                validate: 'data-validate="require-notempty::请添加一张图片"',
                dialog: 'W.dialog.termite.SelectImagesDialog',
                default: ''
            }, {
                name: 'title',
                type: 'text',
                displayName: '描述',
                isUserProperty: true,
                maxLength: 5,
                default: '',
            }, {
                name: 'target',
                type: 'select_link',
                displayName: '链接到',
                isUserProperty: true,
                validate: 'data-validate="require-notempty::链接地址不能为空"',
                triggerButton: '从微站选择'
            }]
        }
    ],

    propertyChangeHandlers: {
        image: function($node, model, value, $propertyViewNode) {
            var data = $.parseJSON(value);
            var image = data.images[0];
            $node.find('img').attr('src', image.url);

            model.set({
                image: image.url,
                width: image.width,
                height: image.height
            }, {silent: true});


            $propertyViewNode.find('.xa-dynamicComponentControlImgBox img').attr('src', image.url);
            $propertyViewNode.find('.xa-dialogTrigger').removeClass('xui-imgDisplayBtn').addClass('xui-dialogSelectedBtn').html('重新上传');
            $propertyViewNode.find('.xa-dynamicComponentControlImgBox').show();
            $propertyViewNode.find('.xa-dynamicComponentControlImgBox img').parents('.xa-errorHintContainer').find('.errorHint').hide();

            _.delay(function() {
                W.Broadcaster.trigger('component:resize', this);
            }, 100);

            if (data.type === 'newImage') {
                W.resource.termite2.Image.put({
                    data: image,
                    success: function(data) {

                    },
                    error: function(resp) {

                    }
                })
            }

        },
        title: function($node, model, value, $propertyViewNode) {
            var parentComponent = W.component.getComponent(this.pid);
            if(parentComponent.type === 'wepage.image_group') {
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

        target: function($node, model, value, $propertyViewNode) {
            /*
            xwarn(value);
            if (value.length > 0) {
                var linkData = $.parseJSON(value);
                if (linkData.type === 'manualInput') {

                } else {
                    $propertyViewNode.find('.xa-selected-title-box').show();
                    $propertyViewNode.find('.xa-selectLink-url').val(linkData.data).attr('disabled','disabled');
                    $propertyViewNode.find('.xa-selectLink-name').text(linkData.data_path);
                    $propertyViewNode.find('.xa-link-menu').html('修改<span class="glyphicon glyphicon-menu-down"></span>');
                }

                $node.find('a').attr('href', linkData.data);
            }else{
                $propertyViewNode.find('.xa-selected-title-box').hide();
                $propertyViewNode.find('.xa-selectLink-url').val('').removeAttr('disabled');
                $propertyViewNode.find('.xa-selectLink-name').text('');
                $propertyViewNode.find('.xa-link-menu').html('从微站选择<span class="glyphicon glyphicon-menu-down"></span>');

                $node.find('a').attr('href', "#")
            }
            */  
            var parentComponent = W.component.getComponent(this.pid);
            parentComponent.refresh(null, {refreshPropertyView:true});
        }
    }
});