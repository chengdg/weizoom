/*
Copyright (c) 2011-2012 Weizoom Inc
*/

W.levelNames = ['一','二','三','四','五','六','七']

/**
 * 一个会话中多条message的view
 * @constructor
 */
W.ShakePrize = Backbone.View.extend({
	events: {
		'change #lottery_type': 'changeLotteryType',
        'change select[name*="prize_type"]': 'changePrizeType',
        'change [name="can_repeat"]': 'changeRadio',
        'keyup [name="daily_play_count"]': 'keepDailyPlayCount',
        'click .tx_addPrizeItem': 'addPrizeItem',
        'click .tx_removeItem': 'removePrizeItem',
        'submit form': 'submit'
	},
	
	initialize: function(options) {
        xlog('-==============')
        this.nameSplit = '|';
//		this.bindRichEidtView();
        this.bindDateView(this);
        
        this.$prizeType = this.$('[name*="prize_type"]');
        this.$prizeSource = this.$('[name*="prize_source"]');
        this.itemClassName = '.tx_prizeItem';
        this.prizeSourceName = 'prize_source';
        this.isEidtPage = this.$el.attr('is_edit_page');
        
        if(!this.isEidtPage) {
            this.setPrizeItemInitValue(this.$el);
        }
        var _this = this;
        this.updatePrizeItemName();
        this.$('select').each(function() {
            $(this).val(this.getAttribute('value'));
            if(this.name.indexOf('prize_type') >= 0) {
                _this.changePrizeType($(this));
            }
        })
        this.checkCanAdd();
	},
    
    setPrizeItemInitValue: function($parent) {
        $parent.find('input:text:visible').val('');
        $parent.find('select').val('');
        var $prizeSource = $parent.find('[name*="prize_source"]');
        $prizeSource.attr('disabled', true).hide();
        $prizeSource.eq(0).attr('disabled', false).show();
        this.setValidateForPrizeSource('1', $prizeSource, $prizeSource.eq(0));
    },
    
    addPrizeItem: function(event) {
        var $el = $(event.currentTarget);
        this.$prizeItem = this.$(this.itemClassName+':last');
        var  $newItem = $.extend({}, this.$prizeItem); 
        //
        console.log($newItem ,'===================',this.itemClassName)
        //var $newItem = this.$prizeItem.clone();
        this.$prizeItem.after('<div class="tx_prizeItem prizeItem">'+$newItem.html()+'</div>');
        this.updatePrizeItemName();
        this.setPrizeItemInitValue(this.$(this.itemClassName+':last'));
        var _this = this;
        this.bindDateView();
        //_this.bindDateView();

        // this.$('.prizeItem select').each(function() {
        //     $(this).val(this.getAttribute('value'));
        //     if(this.name.indexOf('prize_type') >= 0) {
        //         _this.changePrizeType($(this));
        //     }
        // })
        //this.checkCanAdd();
    },
    
    changeLotteryType: function() {
    	this.checkCanAdd();
    },	
    
    checkCanAdd: function() {
        var type = parseInt($('#lottery_type').val());
        xlog(type)
        if (type == 2) {
        	max_count = 5;
        } else {
        	max_count = 4;
        }
        if ($('.tx_prizeItem').length >= max_count) {
    		$('.tx_addPrizeItem').hide();
    	} else {
    		$('.tx_addPrizeItem').show();
    	}
    },
    
    removePrizeItem: function(event) {
        var $el = $(event.currentTarget);
        var $items = this.$(this.itemClassName);
        if($items.length <= 1) {
            return;
        }
        var $parent = $el.parent();
        $parent.remove();
        this.updatePrizeItemName();
        this.checkCanAdd();
    },
   
    updatePrizeItemName: function() {
        var $item = this.$(this.itemClassName);
        var name;
        $item.each(function(i) {
        	$(this).find('.tx_prize_name').html(W.levelNames[i]+'等奖');
        	$(this).find('.tx_prize_name_input').val(W.levelNames[i]+'等奖');
            $(this).find('[name]').each(function() {
                name = this.getAttribute('name');
                $(this).attr('name', name.split('|')[0]+'|'+(i+1));
                id = this.getAttribute('id');
                if (id){
                    $(this).attr('id', id.split('|')[0]+'|'+(i+1));
                }
            })
        })
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
        var $el = $(event.currentTarget);
        var value = $el.attr('value');
        var $dailyPlayCount = this.$('[name="daily_play_count"]');
        if(value === '1') {
            $dailyPlayCount.attr('data-validate', 'require-int');
            $dailyPlayCount.val('2');
        }
        else {
            $dailyPlayCount.removeAttr('data-validate');
            $dailyPlayCount.val('');
        }
    },
    
    bindDateView: function() {
        $('input[data-ui-role="shakeDatepicker"]').each(function() {
            var _this = this;
            var $datepicker = $(_this);
            console.log()
            var format = $datepicker.attr('data-format');
            var min = $datepicker.attr('data-min');
            var max = $datepicker.attr('data-max');
            var $min_el = $($datepicker.attr('data-min-el'));
            var $max_el = $($datepicker.attr('data-max-el'));
            var options = {};
            options = {
                buttonText: '选择日期',
                currentText: '当前时间',
                hourText: "小时",
                controlType: 'select',
                oneLine: true,
                minuteText: "分钟",
                numberOfMonths: 1,
                dateFormat: 'yy-mm-dd',
                //dateFormat: format,
                closeText: '确定',
                prevText: '&#x3c;上月',
                nextText: '下月&#x3e;',
                monthNames: ['一月','二月','三月','四月','五月','六月',
                    '七月','八月','九月','十月','十一月','十二月'],
                monthNamesShort: ['一','二','三','四','五','六',
                    '七','八','九','十','十一','十二'],
                dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
                dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
                dayNamesMin: ['日','一','二','三','四','五','六'],
                beforeShow: function(e) {
                    if(min === 'now') {
                        $(_this).datepicker('option', 'minDate', new Date());
                    }else if(min){
                        $(_this).datepicker('option', 'minDate', min);
                    }

                    if($min_el){
                        var startTime = $min_el.val();
                        if(startTime) {
                            $(_this).datepicker('option', 'minDate', startTime);
                            $(_this).datepicker('option', 'minDateTime', new Date(startTime));
                        }
                    }

                    if(max === 'now') {
                        $(_this).datepicker('option', 'maxDate', new Date());
                    }else if(max){
                        $(_this).datepicker('option', 'maxDate', max);
                    }

                    if($max_el){
                        var endTime = $max_el.val();
                        if(endTime) {
                            $(_this).datepicker('option', 'maxDate', endTime);
                        }
                    }
                },
                onClose: function() {
                }
            };

            $datepicker.datetimepicker(options);
            //cc.beforeShow();
        });
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
    
    keepDailyPlayCount: function(event) {
        var $el = $(event.currentTarget);
        if(!$el.val() && this.$('[name="can_repeat"][value="1"]')[0].checked) {
            $el.val(2);
        }
    },

	submit: function() {
		xlog('eeee')
		if(!W.validate(this.$el)) {
            return false;
        }

        var args = this.$('form').serializeObject();
        args.id = this.options['item_id'] || 0;
        W.getApi().call({
            app: 'market_tools/shake',
            api: 'shake/edit',
            method: 'post',
            args: args,
            success: function(data) {
                //window.location.href = '/market_tools/shake/';
            },
            error: function(resp) {
                var msg = resp.errMsg || '保存失败';
                W.getErrorHintView().show(msg);
            }
        });
        return false;
	}
});