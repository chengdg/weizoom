ensureNS('W.dialog.mall');

W.dialog.mall.MemberPageSelectCouponDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectCoupon': 'onSelectCoupon',
        'click .xa-up': 'upCounter',
        'click .xa-down': 'downCounter'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#member-page-select-coupon-dialog-tmpl-src').template('member-page-select-coupon-dialog-tmpl');
        return "member-page-select-coupon-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');

    },

    beforeShow: function() {
        this.table.reset();
        $(".xa-member-coupon-send").removeClass('disabled');
        $(".xa-member-info-block").addClass('hide');
        $(".xa-member-coupon-send").css('background-color',"#207cbe");
    },

    onShow: function(options) {
        this.enableMultiSelection = false;
        this.member_count = options.member_count;
        if (options.hasOwnProperty('enableMultiSelection')) {
            this.enableMultiSelection = options.enableMultiSelection;
        }
        if (options.member_name){
            $('.xa-member-info').html('<img class="mr10 " src="/static_v2/img/editor/hint.png" />'+"您将为"+options.member_name+"发放优惠券");
        }
        if (options.member_count > 1){
            $('.xa-member-info').html('<img class="mr10 " src="/static_v2/img/editor/hint.png" />'+"您将为"+options.member_count+"人发放优惠券");
        }
        this.table.reload({
            "member_count": this.member_count
        });
    },

    afterShow: function(options) {
        if(!$('.xa-member-couponTable').data('length')){
            $(".xa-member-coupon-send").addClass('disabled');
            $(".xa-member-coupon-send").css('background-color',"#ccc");
        }else{
            $(".xa-member-info-block").removeClass('hide');
        }
    },

    onSelectCoupon: function(event) {
        var $checkbox = $(event.currentTarget);
        if (!this.enableMultiSelection) {
            var $label = this.$('label.checked');
            $label.find('input').prop('checked', false);
            $label.removeClass('checked');
            if($checkbox.parent().hasClass('checked')){
                $checkbox.parent('.checked').find('span').text('已选择');
            }else{
                $checkbox.parents('tr').siblings().find('label span').text('选取');
            }
        }
        if ($checkbox.is(':checked')) {
            $checkbox.parent().addClass('checked');
            $checkbox.parent('.checked').find('span').text('已选择');
        } else {
            $checkbox.parent().removeClass('checked');
            $checkbox.parent().find('span').text('选取');
        }
    },

    upCounter: function(event) {
        var $cur_up = $(event.currentTarget);
        var is_limit = true;
        var max_count = $cur_up.parent().prev().data('max-count');
        var limit_count = parseInt($cur_up.parent().prev().data('min-limit'));
        var remained_count = parseInt($cur_up.parent().prev().data('remained-count'));
        if (!max_count){
            max_count = remained_count;
            is_limit = false;
        }
        var cur_count = parseInt($cur_up.prevAll('.xa-counterText').text());

        if($cur_up.hasClass("xui-btn")){
            if(is_limit){
                if (this.member_count == 1){
                    if(limit_count <= remained_count){
                        return;
                    }
                    if(limit_count > remained_count){
                        $cur_up.parent().next().removeClass('hide');
                    }
                    return;
                }
                if (this.member_count > 1){
                    if(limit_count <= remained_count){
                        if(cur_count < limit_count){
                            $cur_up.parent().next().removeClass('hide');
                        }
                        if(cur_count == limit_count){
                            return;
                        }
                        return;
                    }
                    if(limit_count > remained_count){
                        $cur_up.parent().next().removeClass('hide');
                        return;
                    }
                }
            }else{
                //只考虑库存不足的情况
                if(remained_count <= (cur_count + 1) * this.member_count){
                    $cur_up.parent().next().removeClass('hide');
                }
                return;
            }
        }

        if (this.member_count == 1){
            if((cur_count+1)<=max_count){
                $cur_up.prevAll('.xa-down').removeClass("xui-btn");
                $cur_up.prevAll('.xa-counterText').text(cur_count+1);
            }
            if((cur_count+1) == max_count){
                $cur_up.addClass("xui-btn");
            }
        }else if (this.member_count > 1){
            if (limit_count == max_count && limit_count != remained_count){
                if((cur_count+1) <= limit_count && (cur_count+1)*this.member_count < remained_count){
                    $cur_up.prevAll('.xa-down').removeClass("xui-btn");
                    $cur_up.prevAll('.xa-counterText').text(cur_count+1);
                }
                if((cur_count+1) == max_count){
                    $cur_up.addClass("xui-btn");
                }
                if((cur_count+2)*this.member_count > remained_count){
                    $cur_up.addClass("xui-btn");
                }
            }else{
                if((cur_count+1)*this.member_count <= max_count){
                    $cur_up.prevAll('.xa-down').removeClass("xui-btn");
                    $cur_up.prevAll('.xa-counterText').text(cur_count+1);
                }
                if((cur_count+2)*this.member_count > max_count){
                    $cur_up.addClass("xui-btn");
                }
            }
        }

    },

    downCounter: function(event) {
        var $cur_down = $(event.currentTarget);
        var cur_count = parseInt($cur_down.nextAll('.xa-counterText').text());
        if($cur_down.hasClass("xui-btn")){
            return;
        }else{
            if (cur_count > 1){
                $cur_down.nextAll('.xa-counterText').text(cur_count-1);
                $cur_down.nextAll('.xa-up').removeClass("xui-btn");
                $cur_down.parent().next().addClass("hide");
                if (cur_count == 2){
                    $cur_down.addClass("xui-btn");
                }
            }
        }
    },

    onGetData: function(options) {
        var data = {};
        var _this = this;

        this.$('tbody tr').each(function() {
            var $tr = $(this);
            if ($tr.find('.xa-selectCoupon').is(':checked')) {
                data.couponRuleId = $tr.data('id');
                data.prePersonCount = parseInt($tr.find('.xa-counterText').text())

            }
        })
        return data;
    }
})