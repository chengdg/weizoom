/**
 * @class W.component.wepage.Image
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.ImageGroupImage = W.component.Component.extend({
    type: 'wepage.imagegroup_image',    
    selectable: 'no',
    propertyViewTitle: '一个广告',

    properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'image',
                type: 'dialog_select',
                isUserProperty: true,
                triggerButton: '选择图片...',
                selectedButton: '重新上传',
                validate: 'data-validate="require-notempty::请添加一张图片"',
                dialog: 'W.dialog.termite.SelectImagesDialog',
                dialogParameter: '{"multiSelection": false}',
                default: ''
            }, {
                name: 'title',
                type: 'text',
                displayName: '标题',
                isUserProperty: true,
                maxLength: 20,
                default: ''
            }, {
                name: 'target',
                type: 'select_link',
                displayName: '链接到',
                isUserProperty: true,
                validate: 'data-validate="require-notempty::链接地址不能为空"',
                triggerButton: '从微站选择'
            }, {
                name: 'width',
                type: 'hidden',
                displayName: '宽度',
                isUserProperty: false
            }, {
                name: 'height',
                type: 'hidden',
                displayName: '高度',
                isUserProperty: false
            }]
        }
    ],

    propertyChangeHandlers: {
        image: function($node, model, value, $propertyViewNode) {
            var data = $.parseJSON(value);
            var image = data.images[0];
            
            if ($node.get(0).tagName.toLowerCase() === 'body') {
                //图片对应的node没有被渲染，不修改图片
            } else {
                var $img = $node.find('img');
                $img.attr('src', image.url);
                $node.find('.xa-placeholder').hide();
                if (!$img.is(':visible')) {
                    $img.show();
                }
            }

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
            if ($node.get(0).tagName.toLowerCase() === 'body') {
                //图片对应的node没有被渲染，直接返回
                return;
            }

            var $title = $node.find('.wa-inner-title');
            $title.text(value);
            if (value) {
                $title.show();
            } else {
                $title.hide();
            } 

            _.delay(function() {
                W.Broadcaster.trigger('component:resize', this);  
            }, 100);
        },

        target: function($node, model, value, $propertyViewNode) {            
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
            /*
            var parentComponent = W.component.getComponent(this.pid);
            parentComponent.refresh(null, {refreshPropertyView:true});
            */
        }
    }
});