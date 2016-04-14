/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.ordinary_rules:action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	updateOrdinaryRemark: function(rule, remark) {
		Dispatcher.dispatch({
			actionType: Constant.CARD_ORDINARY_UPDATE_REMARK,
			data: {
				rule: rule,
				remark: remark
			}
		});
	}
}

module.exports = Action;