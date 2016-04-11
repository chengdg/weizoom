/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.create_ordinary:action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {

	addOrdinaryRuleInfo: function(data) {
		Dispatcher.dispatch({
			actionType: Constant.CARD_ADD_ORDINARY_RULE_INFO,
			data: data
		});
	},
	saveOrdinaryRule: function(data) {
		Resource.put({
			resource: 'card.create_ordinary',
			data: data,
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.CARD_DATA_SAVE_ORDINARY_RULE
			}
		});	
	}
}

module.exports = Action;