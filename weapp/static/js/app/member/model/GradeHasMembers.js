/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 会员
 */

W.Member = Backbone.Model.extend({
	is_show: true,
	initialize: function(){
		this.is_show = true;
	}
})


/**
 * 等级对应的会员
 */

W.GradeHasMembers = W.ApiCollection.extend({
    model: W.Member,
    app: 'webapp/user_center',

    initialize: function(models, options) {
    },

    url: function() {
        var _this = this;
        return this.getApiUrl('grade_has_members/get/'+_this.grade_id);
    },

    parse: function(response){
        var data = response.data;
        if(!data) {
            return [];
        }
        return data.items;
    }
});
