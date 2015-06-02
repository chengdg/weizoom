/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 选择奖项的View
 * 
 * author: likunlun
 */
ensureNS('W.view.markettool');
W.view.markettool.ChoosePrizeView = Backbone.View.extend({
    getChoosePrizeTemplate: function() {
        $('#market-too-choose-prize-tmpl-src').template('choose-prize-tmpl');
        return 'choose-prize-tmpl';
    },

    events: {
        'change select[name="prize_type"]': 'changePrizeType',
    },

    render: function() {
		var html = $.tmpl(this.choosePrizeTemplate, {
			items: this.items,
			prize_type: this.prize_type,
			prize_source: this.prize_source
        });
        this.$el.append(html);
        this.initSelect();
        
        $('body').delegate('.xua-coupon', 'change', function(){
            var count = $(':selected', this).data('count');
            if(count || count == 0){
                $(this).nextAll('p').find('.xua-remainedCount').html('当前库存:'+count).show();
                $(this).nextAll('p').find('a').attr('href','/mall_promotion/coupon/create/?rule_id='+$(this).val()).show();
            }
        })
    },
    
    initSelect: function() {
    	var value = $('[name=prize_type]').attr('default-value');
        $('[name=prize_type]').val(value)
    	this.changePrizeType();
    },
    
    changePrizeType: function(event) {
    	var _this = this;
    	var value = $('[name=prize_type]').val();
        var $prizeSource = $('[name=prize_source]');
        $prizeSource.attr('disabled', true).hide();
        $prizeSource.removeAttr('data-validate');
        $prizeSource.removeAttr('data-validate-max-length');
        $prizeSource.each(function() {
            if(this.getAttribute('for_type') === value) {
                var $this = $(this);
                $this.attr('disabled', false).show();
                _this.setValidateForPrizeSource(value, $this);
            }
        });
    },
    
    setValidateForPrizeSource: function(type, $this) {
        $('[name=prize_source]:visible').val($('[name=prize_source]:visible').attr('default-value'))
    	
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

    initialize: function(options) {
    	this.$el = $(this.el);
        this.choosePrizeTemplate = this.getChoosePrizeTemplate();
        this.items = options.items || [];
        this.prize_type = options.prize_type || '';
        this.prize_source = options.prize_source || '';
    },
    
    hide: function() {
    	this.$el.addClass('hide');
    	var _this = this;
    	var value = $('[name=prize_type]').val();
        var $prizeSource = $('[name=prize_source]');
        $prizeSource.attr('disabled', true).hide();
        $prizeSource.removeAttr('data-validate');
        $prizeSource.removeAttr('data-validate-max-length');
        $prizeSource.each(function() {
            if(this.getAttribute('for_type') === value) {
                var $this = $(this);
                $this.attr('disabled', false).show();
                _this.setNullValidateForPrizeSource(value, $this);
            }
        });
    },
    
    setNullValidateForPrizeSource: function(type, $this) {
        $('[name=prize_source]:visible').val($('[name=prize_source]:visible').attr('default-value'))
    	
        switch(type) {
        case '1':
            $this.attr('data-validate', '');
            break;
        case '2':
            $this.attr('data-validate', '');
            break;
        case '3':
            $this.attr('data-validate', '');
            break;
        case '0':
            $this.attr('data-validate', '');
            $this.attr('data-validate-max-length', '');
            break;
        }
    },
    
     show: function() {
     	this.$el.removeClass('hide');
     	this.initSelect();
    }

});


W.registerUIRole('[data-ui-role="prize-selector-control"]', function() {
    var $div = $(this);
    var couponRuleData = $div.attr('data-coupon-rules');
    if (couponRuleData) {
	    couponRuleData = $.parseJSON(couponRuleData);
    } else {
    	couponRuleData = null;
    }
    var prizeType = $div.attr('data-prize-type');
    var prizeSource = $div.attr('data-prize-source');

    var view = new W.view.markettool.ChoosePrizeView({
        el: $div[0],
        items: couponRuleData,
        prize_type: prizeType,
        prize_source: prizeSource,
    });
    view.render();
   	$div.data('view', view);
});