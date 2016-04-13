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
			resource: 'order.order_data',
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
			resource: 'order.card_rule',
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
	resetProduct: function() {
		Dispatcher.dispatch({
			actionType: Constant.CARD_DATA_RESET_PRODUCT,
			data: {

			}
		});
	},
	updateAddProduct: function(index, property, value) {
		Dispatcher.dispatch({
			actionType: Constant.CARD_DATA_UPDATE_ADD_PRODUCT,
			data: {
				index: index,
				property: property,
				value: value
			}
		});
	},
	addCardLines:function() {
		Dispatcher.dispatch({
			actionType:Constant.ADD_CARD_LINES,
		})
	},
	getCardRuleOrder: function(){
		Resource.get({
			resource: 'order.rule_order',
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.CARD_RULE_ORDER,
			}
		});
	},
	// getLimitAndCommonCard:function(argument) {
	// 	Resource.get({
	// 		resource:'order.approval_card',
	// 		dispatch: {
	// 			dispatcher: Dispatcher,
	// 			actionType: Constant.GET_LIMIT_AND_COMMON_CARD,
	// 		}
	// 	})
	// },
	updateOrderStaus:function(filter){
		var that = this
		Resource.post({
			resource: 'order.rule_order',
			data: filter,
			success: function(data) {
				that.getCardRuleOrder()
			}

		})
	}
}
module.exports = Action;