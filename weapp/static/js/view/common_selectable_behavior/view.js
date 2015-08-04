/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * AdvancedTable: 拥有searchable, column sortable, item sortable功能的高级table
 */
ensureNS('W.view.common');
W.view.common.SelectableBehavior = Backbone.View.extend({
    events:{
        'click [data-can-select="true"]': 'onClickSelectableItem'
    },

    initialize: function(options) {
        this.$el = $(options.el);
        this.selectedCoverHtml = '<span class="selected_cover"><span class="selected_cover_inner"></span></span>';
        this.$el.addClass('xb-selectable');
        this.$('[data-can-select="true"]').css('position', 'relative');

        //isRadio 为true是单选，false是多选
        this.isRadio = options.isRadio || false;
    },

    /**
     * onClickSelectableItem: selectable item点击后的响应函数
     */
    onClickSelectableItem: function(event) {
        var $el = $(event.currentTarget);
        var $selectedCover = $el.find('.selected_cover');

        if($el.attr('is_checked') && 'false' !== $el.attr('is_checked')) {
            $selectedCover.hide();
            $el.attr('is_checked', false);
            $el.css({
                'opacity': 1
            })
        }
        else {
            this.clearSelectedItem();
            $el.attr('is_checked', true);
            if($selectedCover.length === 0) {
                $el.append(this.selectedCoverHtml);
                $selectedCover = $el.find('.selected_cover');
            }
            $selectedCover.css({
                'width': '93.5%',
                'height': $el.height()
            }).show();

            // $el.css({
            //     'opacity':0.5
            // });
        }
    },

    /**
     * clearSelectedItem: 清空已选择的item
     */
    clearSelectedItem: function() {
        if(this.isRadio){
            this.$('[data-can-select="true"]').each(function() {
                var $item = $(this);
                $item.attr('is_checked', false);
                $item.find('.selected_cover').hide();
                $item.css({
                    'opacity': 1
                })
            });
        }
    },

    getSelectedItems: function() {
        return this.$('[is_checked="true"]');
    }
})