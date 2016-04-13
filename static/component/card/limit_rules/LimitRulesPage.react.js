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

var LimitRulesPage = React.createClass({
	onClickDelete: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		Action.deleteProduct(productId, this.refs.table.refresh);
	},
	onClickShops: function(event){
		var ruleId = parseInt(event.target.getAttribute('data-rule-id'));
		var shop_limit_list = this.refs.table.getData(ruleId).shop_limit_list;
		// var nodes = shop_limit_list.map(function(data,index){
		// 	return (
		// 		'<span class="mr10">'+data+'</span>'
		// 	)
		// })
		var node_strings = '';
		for (var i in shop_limit_list){
			node_strings +='<span class="mr10">'+shop_limit_list[i]+'</span>'
		}

		Reactman.PageAction.showPopover({
			target: event.target,
			content: node_strings
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'name') {
			return (
				<a href={'/card/limit_cards/?weizoom_card_rule_id='+data.id}>{value}</a>
			)
		}else if (field == "shop_limit_list"){
			if (value.length >0){
				return (
					<a className="btn btn-success" href='javascript:void(0);' onClick={this.onClickShops} data-rule-id={data.id}>查看专属商家</a>
				)
			}
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
			resource: 'card.limit_rules',
			data: {
				page: 1,
				count_per_page: 15
			}
		};

		return (
		<div className="mt15">
			<Reactman.TablePanel>
				
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="创建新卡" icon="plus" href="/card/limit/" />
				</Reactman.TableActionBar>
				<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
					<Reactman.TableColumn name="卡名称" field="name" />
					<Reactman.TableColumn name="面值" field="money" />
					<Reactman.TableColumn name="数量" field="count" />
					<Reactman.TableColumn name="库存" field="storage_count"/>
					<Reactman.TableColumn name="卡类型" field="card_kind" />
					<Reactman.TableColumn name="使用限制" field="valid_restrictions" />
					<Reactman.TableColumn name="专属卡" field="shop_limit_list" />
					<Reactman.TableColumn name="卡号区间" field="card_range"/>
					<Reactman.TableColumn name="备注" field="remark" />
					<Reactman.TableColumn name="操作" field="action" width="80px" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = LimitRulesPage;