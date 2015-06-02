/**
 * Backbone View in Mobile
 */
W.page.InputablePage = BackboneLite.View.extend({
    events: {
        'input input[type="text"]': 'onChangeTextInputValue',
        'input input[type="tel"]': 'onChangeTextInputValue',
        'input textarea': 'onChangeTextInputValue',
        'focus input': 'onChangeTextInputValue',
        'focus textarea': 'onChangeTextInputValue',
        'blur input': 'onBlurInput',
        'blur textarea': 'onBlurInput',
        'touchstart .xui-clearBtn': 'onClickClearBtn',
    },
    
    initialize: function(options) {
        xlog('in EditAddressPage');
        this.redirectUrlQueryString = options.redirectUrlQueryString;
    },

    /**
     * onChangeTextInputValue: 输入框中内容改变的响应函数
     */
    onChangeTextInputValue: function(event) {
        var $input = $(event.target);
        var $clearBtn = $input.parents('.xa-clearBtnContainer').find('.xui-clearBtn');
        if($input.val() === ""){
            $clearBtn.hide();
        }else{
            $clearBtn.show();
        }
    },
    /**
     * onBlurInput: 输入框失去焦点时的响应函数
     */
    onBlurInput: function(event) {
        _.delay(function() {
            var $input = $(event.target);
            var $clearBtn = $input.parents('.xa-clearBtnContainer').find('.xui-clearBtn');
            if ($clearBtn.length > 0) {
                $clearBtn.hide();
            }
        }, 100);
    },

    /**
     * onClickClearBtn: 点击clear button的响应函数
     */
    onClickClearBtn: function(event) {
        var $clearBtn = $(event.target);
        var $input = $clearBtn.parent().find('textarea');
        if($input.length != 0){
            $input.val('');  
        }else{
            var $input = $clearBtn.parent().find('input');
            $input.val('');  
        }
        $clearBtn.hide();
        
    }
});
