/*
Copyright (c) 2011-2013 Weizoom Inc
*/

/**
 * 全局插件, vr- prefix stands for 'viper role'
 */
(function($) {
    //处理vr-productCountEditor
    $(document).ready(function() {
        $('.vr-productCountEditor').each(function() {
            var $productCountEditor = $(this);

            //获取plugin数据
            var name = $productCountEditor.attr('name');
            var inputName = 'plugin:'+name+'/1';
            var inputValue = '';
            var $inputData = $('input[name="'+inputName+'"]');
            if ($inputData.length > 0) {
                inputValue = $inputData.val();
            }

            //创建input
            $productCountEditor.append('<input class="hide" type="text" name="' + inputName + '" value="' + inputValue + '" />');
            var $input = $productCountEditor.find('input[type="text"]');

            var $checkedRadio = $productCountEditor.find(':checked');
            if ($checkedRadio.val() === '1') {
                $input.show();
            }

            $productCountEditor.find('input[type="radio"]').click(function(event) {
                var $radio = $(event.currentTarget);
                if ($radio.val() === '1') {
                    $input.show();
                } else {
                    $input.hide().val(0);
                }
            });
        });
    });

    //处理vr-priceSelector
    $(document).ready(function() {
        $('.vr-priceSelector').each(function() {
            var $priceSelector = $(this);
            var name = $priceSelector.attr('name');
            var inputName = 'plugin:'+name+'/1';
            var inputValue = '';
            var $inputData = $('input[name="'+inputName+'"]');
            if ($inputData.length > 0) {
                inputValue = $inputData.val();
            }
            $priceSelector.append("<input class='hide' type='text' name='" + inputName + "' value='" + inputValue + "' />");
            var $input = $priceSelector.find('input[type="text"]');

            var $checkedRadio = $priceSelector.find(':checked');
            if ($checkedRadio.val() === '1') {
                $input.show();
            }

            $priceSelector.find('input[type="radio"]').click(function(event) {
                var $radio = $(event.currentTarget);
                if ($radio.val() === '1') {
                    var options = {
                        success: _.bind(function(data) {
                            $input.val(JSON.stringify(data));
                        }, this),
                    }
                    W.dialog.showDialog('W.dialog.PromotionPriceDialog', options);
                    $input.show();
                } else {
                    $input.hide().val(0);
                }
            });
        });
    });
}(jQuery));