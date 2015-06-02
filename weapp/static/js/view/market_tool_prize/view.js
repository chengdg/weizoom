/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 营销工具中选择奖项的View
 * 
 * author: chuter
 */
ensureNS('W.view.markettool.prize');
W.view.markettool.prize.PrizeSelector = Backbone.View.extend({
    getSelectorTemplate: function() {
        $('#market-tool-prize-selector-tmpl-src').template('market-tool-prize-selector-tmpl');
        return 'market-tool-prize-selector-tmpl';
    },

    getPrizeListTemplate: function() {
        $('#market-tool-prize-list-tmpl-src').template('market-tool-prize-list-tmpl');
        return 'market-tool-prize-list-tmpl';
    },

    getScoreInputTemplate: function() {
        $('#market-tool-prize-score-input-tmpl-src').template('market-tool-prize-score-input-tmpl');
        return 'market-tool-prize-score-input-tmpl';
    },

    getRealPrizeInputTemplate: function() {
        $('#market-tool-prize-real-prize-input-tmpl-src').template('market-tool-prize-real-prize-input-tmpl');
        return 'market-tool-prize-real-prize-input-tmpl';
    },

    events: {
        'change .xa-selectPrizeType': 'selectPrizeType',
    },

    render: function() {
        var _this = this;
        W.getApi().call({
            app: 'prize',
            api: 'prize_types/get',
            method: 'get',
            args: {},
            success: function(data) {
                _this.prizeTypes = data.items;

                var html = $.tmpl(_this.selectorTemplate, {
                    prize_types: _this.prizeTypes,
                    selected_prize_type: _this.getInitializingPrizeType(),
                });
                _this.$el.append(html);

                _this.selectPrizeType();
            },
            error: function(response) {
                alert('加载奖项列表失败！请刷新页面重试！');
            },
            scope: this
        });
    },
    
    getInitializingPrizeType: function() {
        if (this.initPrizeInfo) {
            return this.initPrizeInfo.type;
        } else {
            return "";
        }
    },

    getInitializingPrizeName: function() {
        if (this.initPrizeInfo) {
            return this.initPrizeInfo.name;
        } else {
            return "";
        }
    },

    getInitializingScoreValue: function() {
        if (this.isInitializingScorePrizeType()) {
            return this.initPrizeInfo.id;
        } else {
            return "";
        }
    },

    getInitializingRealPrizeName: function() {
        if (this.isInitializingRealPrizeType()) {
            return this.initPrizeInfo.name;
        } else {
            return "";
        }
    },

    isInitializingScorePrizeType: function() {
        return this.initPrizeInfo && (this.initPrizeInfo.name == '_score-prize_');
    },

    isInitializingNonPrizeType: function() {
        return this.initPrizeInfo && (this.initPrizeInfo.id == -1);
    },

    isInitializingRealPrizeType: function() {
        return this.initPrizeInfo && (this.initPrizeInfo.id == 0);
    },

    selectPrizeType: function(event) {
    	var _this = this;
    	var value = this.$('.xa-selectPrizeType').val();

        if (value == '积分') {
            this.isNonPrizeType = false;
            this.isScorePrizeType = true;
            this.isRealPrizeType = false;

            this.$('#prizeTypesSelector').nextAll().remove();

            var html = $.tmpl(_this.scoreInputTemplate, {
                score: _this.getInitializingScoreValue()
            });

            this.$('#prizeTypesSelector').after(html);
        } else if (value == '无奖励') {
            this.isNonPrizeType = true;
            this.isScorePrizeType = false;
            this.isRealPrizeType = false;
            this.$('#prizeTypesSelector').nextAll().remove();
        } else if (value == '实物奖励') {
            this.isNonPrizeType = false;
            this.isScorePrizeType = false;
            this.isRealPrizeType = true;

            this.$('#prizeTypesSelector').nextAll().remove();

            var html = $.tmpl(_this.realPrizeInputTemplate, {
                name: _this.getInitializingRealPrizeName()
            });

            this.$('#prizeTypesSelector').after(html);
        } else {
            this.isNonPrizeType = false;
            this.isScorePrizeType = false;
            this.isRealPrizeType = false;

            this.$('#prizeTypesSelector').next().remove();

            var defaultSelectValue = '请选择' + value;

            W.getApi().call({
                app: 'prize',
                api: 'prize_list/get',
                method: 'get',
                args: {
                    name: value
                },
                success: function(data) {
                    var prizeList = data.items;
                    
                    var html = $.tmpl(_this.prizeListTemplate, {
                        defaultSelectValue: defaultSelectValue,
                        prizeList: prizeList,
                        selected_prize_name: _this.getInitializingPrizeName()
                    });

                    this.$('#prizeTypesSelector').after(html);
                    $('body').delegate('.xua-coupon', 'change', function(){
                        var count = $(':selected', this).data('count');
                        if(count || count == 0){
                            $(this).nextAll('p').find('.xua-remainedCount').html('当前库存:'+count).show();
                            $(this).nextAll('p').find('a').attr('href','/mall_promotion/coupon/create/?rule_id='+$(this).val()).show();
                        }
                    })
                },
                error: function(response) {
                },
                scope: this
            });
        }
    },
    
    getPrizeInfo: function() {
        if (this.isNonPrizeType) {
            return {'id':-1, 'name':'non-prize', 'type':'无奖励'};
        } else if (this.isScorePrizeType) {
            var score = parseInt(this.$('#prize_score_input').val());
            return {'id':score, 'name':'_score-prize_', 'type':'积分'};
        } else if (this.isRealPrizeType) {
            var prize_name = this.$('#prize_real_prize_input').val();
            return {'id':0, 'name':prize_name, 'type':'实物奖励'};
        } else {
            var $slectPrizeType = this.$("#prizeTypesSelector option:selected");
            var prizeType = $slectPrizeType.val();

            var $selectedPrize = this.$("#prize_list option:selected");
            var id = parseInt($selectedPrize.val());
            var prizeName = $selectedPrize.html();
            return {'id':id, 'name':prizeName, 'type':prizeType};
        }
    },

    getViewData: function() {
        return JSON.stringify(this.getPrizeInfo());
    },

    setViewData: function(data) {
        this.initPrizeInfo = $.parseJSON(data);
        if (this.$('.xa-selectPrizeType').length > 0) {
            //已经render了，重新设置值
            this.$('.xa-selectPrizeType').val(this.initPrizeInfo['type']);
            this.selectPrizeType();
        }
    },

    initialize: function(options) {
    	this.$el = $(options.el);
        this.initPrizeInfo = options.initPrizeInfo;
        this.isNonPrizeType = true;
        this.isScorePrizeType = false;
        this.isRealPrizeType = false;
        this.selectorTemplate = this.getSelectorTemplate();
        this.prizeListTemplate = this.getPrizeListTemplate();
        this.scoreInputTemplate = this.getScoreInputTemplate();
        this.realPrizeInputTemplate = this.getRealPrizeInputTemplate();
    },
});

W.registerUIRole('div[data-ui-role="prize-selector"]', function() {
    var $div = $(this);

    var initPrizeInfoStr = $div.attr('data-init-prizeinfo');

    if (initPrizeInfoStr) {
        var initPrizeInfo = $.parseJSON(initPrizeInfoStr);
    } else {
        var initPrizeInfo = null;
    }

    var prizeSelector = new W.view.markettool.prize.PrizeSelector({
        el: $div[0],
        initPrizeInfo: initPrizeInfo,
    });
    prizeSelector.render();

    $div.data('view', prizeSelector);
});