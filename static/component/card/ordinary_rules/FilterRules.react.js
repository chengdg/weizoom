/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.ordinary_rules:OrdinaryCardPage');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var PageAction = Reactman.PageAction;
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

// var Store = require('./Store');
// var Constant = require('./Constant');
// var Action = require('./Action');

var OrdinaryRulesPage = React.createClass({
	onClickDelete: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		Action.deleteProduct(productId, this.refs.table.refresh);
	},

	rowFormatter: function(field, value, data) {
		if (field === 'name') {
			return (
				<a href={'/card/ordinary_cards/?weizoom_card_rule_id='+data.id}>{value}</a>
			)
		}else if (field === 'action') {
			return (
			<div>
				<a className="btn btn-link btn-xs">导出</a>
				<a className="btn btn-link btn-xs mt5">追加</a>
				<a className="btn btn-link btn-xs">备注</a>
			</div>
			);
		} else {
			return value;
		}
	},

	render:function(){
		var productsResource = {
			resource: 'card.ordinary_rules',
			data: {
				page: 1,
				count_per_page: 15
			}
		};

		return (
		<div className="mt15">
			<Reactman.FilterPanel>
				<Reactman.FilterRow>
					<Reactman.FilterField></Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>
		</div>
		)
	}
})
module.exports = OrdinaryRulesPage;