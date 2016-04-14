/*
Copyright (c) 2011-2012 Weizoom Inc
*/
var Constant = require('./Constant');
var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Action = {
	getRuleId: function(order_id){
		Resource.get({
			resource: 'order.rule_id_list',
			data: {
				'order_id':order_id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.GET_RULE_ID,
			}
		})
	}
}
module.exports = Action;