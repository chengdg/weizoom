/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 详情影响力
 */

ensureNS('W.webapp.usercenter');
W.webapp.usercenter.Relation = Backbone.Model.extend({

})


/**
 * 详情影响力s
 */

W.webapp.usercenter.Relations = W.ApiCollection.extend({
    model: W.webapp.usercenter.Relation,
    app: 'webapp/user_center',

    initialize: function(models, options) {

    },

    url: function() {
        var _this = this;
        var onlyFans = 0;
        if (_this.onlyFans){
            onlyFans = 1;
        }
        return this.getApiUrl('get_member_follow_relations/'+_this.memberId+'/'+onlyFans);
    },

    parse: function(response){
        var data = response.data;
        if(!data) {
            return [];
        }
        return data.items;
    }
});
