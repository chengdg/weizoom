/*
Copyright (c) 2011-2012 Weizoom Inc
*/
var Constant = require('./Constant');
var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Action = {
	saveCardRuleOrder: function(filter) {
		Resource.post({
			resource: 'order.create_rule_order',
			data: {
				rule_order: filter.rule_order,
				card_rule_num: filter.card_rule_num,
				valid_time_from: filter.valid_time_from,
				valid_time_to: filter.valid_time_to,
				company_info: filter.company_info,
				responsible_person: filter.responsible_person,
				contact: filter.contact,
				sale_name: filter.sale_name,
				sale_departent: filter.sale_departent,
				order_attributes: filter.order_attributes,
				remark:filter.remark
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.CREATE_CRAD_RULE_ORDER,
			}
		});
	},
	getCardRule: function(){
		Resource.get({
			resource: 'order.get_card_cule',
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.GET_CARD_RULE,
			}
		});
	},
	updateProduct: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.CARD_DATA_UPDATE_PRODUCT,
			data: {
				property: property,
				value: value
			}
		});
	},
	getCardRuleOrder: function(filter){
		console.log(filter,12345)
		Resource.get({
			resource: 'order.rule_order',
			data: filter,
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.CARD_RULE_ORDER,
			}
		});
	},
}
module.exports = Action;