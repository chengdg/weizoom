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

var RemarkCommentDialog = require('./RemarkCommentDialog.react');

var Store = require('./Store');
// var Constant = require('./Constant');
var Action = require('./Action');

var OrdinaryRulesPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		this.refs.table.refresh();
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
					<a className="btn btn-link btn-xs mt5" onClick={this.onClickRemarkComment} data-rule-id={data.id} >备注</a>
				</div>
			);
		} else {
			return value;
		}
	},
	
	onClickRemarkComment: function(event){
		var ruleId = parseInt(event.target.getAttribute('data-rule-id'));
		var rule = this.refs.table.getData(ruleId);
		Reactman.PageAction.showDialog({
			component: RemarkCommentDialog, 
			data: {
				rule: rule
			},
			success: function(inputData, dialogState) {
				var rule = inputData.rule;
				var remark = dialogState.remark;
				Action.updateOrdinaryRemark(rule, remark);
			}
		});
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
			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="创建新卡" icon="plus" href="/card/ordinary/" />
				</Reactman.TableActionBar>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
					<Reactman.TableColumn name="卡名称" field="name" />
					<Reactman.TableColumn name="面值" field="money" />
					<Reactman.TableColumn name="数量" field="count" />
					<Reactman.TableColumn name="库存" field="storage_count"/>
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
module.exports = OrdinaryRulesPage;