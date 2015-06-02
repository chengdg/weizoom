/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 会员二维码view
 * @constructor
 */
W.MemberQrcode = Backbone.View.extend({
	events: {
        'change select[name*="prize_type"]': 'changePrizeType',
        'change [name="reward"]': 'changeRadio',
        'submit form': 'submit'
	},
	
	initialize: function(options) {
        this.nameSplit = '|';
		this.bindRichEidtView();
        
        this.$prizeType = this.$('[name*="prize_type"]');
        this.$prizeSource = this.$('[name*="prize_source"]');
        this.itemClassName = '.tx_prizeItem';
        this.prizeSourceName = 'prize_source';
        this.isEidtPage = this.$el.attr('is_edit_page');
        this.changeRadio();
	},
    
    setPrizeItemInitValue: function($parent) {
        var $prizeSource = $parent.find('[name*="prize_source"]');
        $prizeSource.attr('disabled', true).hide();
        $prizeSource.eq(0).attr('disabled', false).show();
        this.setValidateForPrizeSource('1', $prizeSource, $prizeSource.eq(0));
    },
     
    changePrizeType: function(event) {
        var _this = this;
        var $el = event.currentTarget ? $(event.currentTarget) : event;
        var value = $el.val();
        
        var index = $el.attr('name').split(this.nameSplit)[1];
        var $prizeSource = $('[name="'+this.prizeSourceName+'|'+index+'"]');
        $prizeSource.attr('disabled', true).hide();
        $prizeSource.each(function() {
            if(this.getAttribute('for_type') === value) {
                var $this = $(this);
                $this.attr('disabled', false).show();
                _this.setValidateForPrizeSource(value, $prizeSource, $this);
            }
        });
    },
    
    setValidateForPrizeSource: function(type, $prizeSource, $this) {
        $prizeSource.removeAttr('data-validate');
        $prizeSource.removeAttr('data-validate-max-length');

        switch(type) {
        case '1':

            $this.attr('data-validate', 'require-select');
            break;
        case '2':
            $this.attr('data-validate', 'require-select');
            break;
        case '3':
            $this.attr('data-validate', 'require-int');
            break;
        case '0':
            $this.attr('data-validate', 'required');
            $this.attr('data-validate-max-length', '36');
            break;
        }
    },
    
    changeRadio: function(event) {
        var value = $('.reward:checked').val();
        var $unitedPrizeSource = $('.tx_prizeItem_all').find('[name*="prize_source"]');
        var $unitedPrizeType = $('.tx_prizeItem_all').find('[name*="prize_type"]');
        var $classifiedPrizeSource = $('.tx_prizeItem_member').find('[name*="prize_source"]');
        var $classifiedPrizeType = $('.tx_prizeItem_member').find('[name*="prize_type"]');
		var _this = this;
		
        if(value === '1') {
            this.$('.tx_prizeItem_member').hide();
            this.$('.tx_prizeItem_all').show();
            this.setPrizeItemInitValue($('.tx_prizeItem_all'))
           	$classifiedPrizeSource.attr('disabled', true).removeAttr('data-validate');
           	$classifiedPrizeType.attr('disabled', true).removeAttr('data-validate');
           	$unitedPrizeSource.attr('disabled', false);
           	$unitedPrizeType.attr('disabled', false);
           	
           	$('.tx_prizeItem_all').find('select').each(function() {
                $(this).val(this.getAttribute('value'));
                if(this.name.indexOf('prize_type') >= 0) {
                    _this.changePrizeType($(this));
                }
            })
        }
        else {
            this.$('.tx_prizeItem_all').hide();
            this.$('.tx_prizeItem_member').show();
            $classifiedPrizeSource.attr('disabled', false);
           	$classifiedPrizeType.attr('disabled', false);
           	$unitedPrizeSource.attr('disabled', true).removeAttr('data-validate');
           	$unitedPrizeType.attr('disabled', true).removeAttr('data-validate');

            $('.tx_prizeItem_member').find('select').each(function() {
                $(this).val(this.getAttribute('value'));
                if(this.name.indexOf('prize_type') >= 0) {
                    _this.changePrizeType($(this));
                }
            })
        }
    },
    
    bindRichEidtView: function() {
        this.editor = new W.common.RichTextEditor({
			el: 'textarea#detail',
			type: 'full',
			imgSuffix: "uid="+W.uid,
            width: 320,
	        height: 300,
	        autoHeight: false,
			wordCount: false,
			maxCount: 600
		})
		this.editor.bind('contentchange', function() {
			//this.$textInput.val(this.editor.getContent());
			//this.onChangeText();
		}, this);
		this.editor.render();
        
    },
    
	submit: function() {
		if(!W.validate(this.$el)) {
            return false;
        }
        
        var args = this.$('form').serializeObject();
        args.id = this.options['item_id'] || 0;
        W.getApi().call({
            app: 'market_tools/member_qrcode',
            api: 'member_qrcode/edit',
            method: 'post',
            args: args,
            success: function(data) {
                window.location.href = '/market_tools/member_qrcode/';
            },
            error: function(resp) {
                var msg = resp.errMsg || '保存失败';
                W.getErrorHintView().show(msg);
            }
        });
        return false;
	}
});