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

var OrdinaryCardPage = React.createClass({
	onClickDelete: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		Action.deleteProduct(productId, this.refs.table.refresh);
	},

	rowFormatter: function(field, value, data) {
		if (field === 'name') {
			return (
				<a href={'/outline/data/?id='+data.id}>{value}</a>
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
				page: 1
			}
		};

		return (
		<div className="mt15">
			<Reactman.TablePanel>
				
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="创建新卡" icon="plus" href="/card/create_ordinary/" />
				</Reactman.TableActionBar>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} countPerPage={2} ref="table">
					<Reactman.TableColumn name="卡名称" field="name" />
					<Reactman.TableColumn name="面值" field="money" />
					<Reactman.TableColumn name="数量" field="count" />
					<Reactman.TableColumn name="库存" field="count"/>
					<Reactman.TableColumn name="卡类型" field="card_kind" />
					<Reactman.TableColumn name="卡号区间" field="card_range"/>
					<Reactman.TableColumn name="备注" field="remark" />
					<Reactman.TableColumn name="操作" field="action" width="80px" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = OrdinaryCardPage;