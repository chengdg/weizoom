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

var OrdinaryCardsPage = React.createClass({
	onClickDelete: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		Action.deleteProduct(productId, this.refs.table.refresh);
	},

	rowFormatter: function(field, value, data) {
		if(field == "storage_status_text"){
			var style = {
				color: "#00CC00"
			}
			if(data.storage_status_text == "已出库"){
				style={
					color: "#FF0000"
				}
			}
			return(
				<div style={style}>{data.storage_status_text}</div>
			)
		}else if (field == "rule_money/money"){
			return (
				<div>
					<span>{data.rule_money}</span>/<span>{data.money}</span>
				</div>
			)
		}else if (field=="activated_to-department"){
			return (
				<div>
					<div>{data.activated_to}</div>
					<div>{data.department}</div>
				</div>
			);
		}else if (field === 'action') {
			return (
			<div>
				<a className="btn btn-link btn-xs">备注</a>
			</div>
			);
		} else {
			return value;
		}
	},

	render:function(){
		var productsResource = {
			resource: 'card.ordinary_cards',
			data: {
				weizoom_card_rule_id: W.weizoom_card_rule_id,
				page: 1,
				count_per_page: 15
			}
		};

		return (
		<div className="mt15">
			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="导出" icon="plus" href="#" />
					<Reactman.TableActionButton text="创建新卡" icon="plus" href="/card/create_ordinary/" />
				</Reactman.TableActionBar>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
					<Reactman.TableColumn name="卡号" field="weizoom_card_id" />
					<Reactman.TableColumn name="密码" field="password" />
					<Reactman.TableColumn name="状态" field="storage_status_text" />
					<Reactman.TableColumn name="面额/余额" field="rule_money/money"/>
					<Reactman.TableColumn name="出库时间" field="storage_time" />
					<Reactman.TableColumn name="备注" field="remark"/>
					<Reactman.TableColumn name="领用人</br>申请部门/公司" field="activated_to-department" />
					<Reactman.TableColumn name="操作" field="action" width="80px" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = OrdinaryCardsPage;