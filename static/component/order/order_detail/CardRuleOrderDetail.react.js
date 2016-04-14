/**
 * Created by cl on 2016/2/24 024.
 */
var React = require('react');
var debug = require('debug')('m:outline.data:DataPage');

var Store = require('./Store');
var Action = require('./Action');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');
var FormInput = Reactman.FormInput;
var FormSubmit = Reactman.FormSubmit;
var Dispatcher = Reactman.Dispatcher;

var CardRuleOrderDetail = React.createClass({
	displayName: 'CardRuleOrderDetail',
	getInitialState: function() {
		return ({
			order_id: W.card_rule_order_id,
			rule_id: 0,
			order_item_id: 0
		})
	},
	componentWillMount: function() {
		Action.getRuleId(this.state.order_id);
		Store.addListener(this.getRuleId);
	},
	getRuleId: function() {
		rule_order = Store.getRuleId();
		this.setState({
			rule_id: rule_order.rule_id,
			order_item_id: rule_order.order_item_id
		})
	},
	chooseRuleId: function(rule_id,order_item_id) {
		this.setState({
			rule_id: rule_id,
			order_item_id: order_item_id
		})
	},
	render: function(){
		var rule_id = this.state.rule_id;
		if(rule_id >0 ){
			return(
				<div>
					<CardRuleOrderList orderId={this.state.order_id}/>
					<CardOrderDetailList ruleId={this.state.rule_id} orderItemId={this.state.order_item_id}/>
				</div>
			)
		}else{
			return(
				<div>
					<CardRuleOrderList orderId={this.state.order_id}/>
				</div>
			)
		}
		
	}
})

var CardRuleOrderList = React.createClass({
	displayName: 'CardRuleOrderList',

	getCardList: function(rule_id,order_item_id){
		this.props.chooseRuleId(rule_id,order_item_id);
	},
	onClickShops: function(shop_limit_list,event){
		var node_strings = '';
		for (var i in shop_limit_list){
			node_strings +='<div class="fl">'+shop_limit_list[i]+'&nbsp;</div>'
		}
		Reactman.PageAction.showPopover({
			target: event.target,
			content: node_strings
		});
	},
	rowFormatter: function(field, value, data) {
		var _this = this;
		if (field === 'action') {
			var rule_id = data['rule_id'];
			var order_item_id = data['order_item_id'];
			return (
				<div><a onClick={_this.getCardList.bind(_this,rule_id,order_item_id)}>选取</a></div>
			);
		}else if (field == 'card_kind/valid_restrictions'){
			return (
				<span>{data["card_kind"]}/{data["valid_restrictions"]}</span>
			);
		}else if (field == 'shop_limit_list'){
			var shop_limit_list = data['shop_limit_list'];
			console.log(shop_limit_list);
			if(shop_limit_list && shop_limit_list.length>0){
				return (
					<span className="xi-td-span"><a className="btn btn-success" href='javascript:void(0);' onClick={_this.onClickShops.bind(_this,shop_limit_list)} data-rule-id={data.rule_id}>查看专属商家</a><br></br></span>
				)
			}
		}else {
			return value;
		}
	},
	render: function() {
		var order_id = this.props.orderId;
		var productsResource = {
			resource: 'order.order_detail',
			data: {
				page: 1,
				order_id: this.props.orderId,
				count_per_page: 15
			}
		};
		return (
			<div className="order_detail">		
				<Reactman.TablePanel>
					<Reactman.TableActionBar></Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table1">
						<Reactman.TableColumn name="卡名称" field="name" />
						<Reactman.TableColumn name="面值" field="money" />
						<Reactman.TableColumn name="数量" field="count" />
						<Reactman.TableColumn name="总额" field="total_money" />
						<Reactman.TableColumn name="卡类型/使用限制" field="card_kind/valid_restrictions"/>
						<Reactman.TableColumn name="专属商家" field="shop_limit_list" />
						<Reactman.TableColumn name="卡号区间" field="card_range"/>
						<Reactman.TableColumn name="操作" field="action" width="80px" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
});

var CardOrderDetailList = React.createClass({
	displayName: 'CardOrderDetail',

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<span>激活</span><br></br>
					<span>备注</span><br></br>
					<span>有效期</span>
				</div>
			);
		}else if (field === 'money/balance') {
			return (
				<div>
					<span>{data["money"]}/{data["balance"]}</span>
				</div>
			);
		}else if (field === 'validate_from/validate_to') {
			return (
				<div>
					<span>{data["validate_from"]}<br></br>{data["validate_to"]}</span>
				</div>
			);
		}else {
			return value;
		}
	},
	render: function() {
		var rule_id = this.props.ruleId;
		var order_item_id = this.props.orderItemId;
		if(rule_id >=0 ){
			var productsResource = {
				resource: 'order.card_detail',
				data: {
					page: 1,
					rule_id: rule_id,
					order_item_id: order_item_id,
					count_per_page: 15
				}
			};
			return (
				<div className="card_detail">		
					<Reactman.TablePanel>
						<Reactman.TableActionBar></Reactman.TableActionBar>
						<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table2">
							<Reactman.TableColumn name="卡号" field="card_num" />
							<Reactman.TableColumn name="密码" field="password" />
							<Reactman.TableColumn name="状态" field="card_status" />
							<Reactman.TableColumn name="面值/余额" field="money/balance" />
							<Reactman.TableColumn name="有效期" field="validate_from/validate_to"/>
							<Reactman.TableColumn name="激活时间" field="activated_at" />
							<Reactman.TableColumn name="备注" field="remark"/>
							<Reactman.TableColumn name="操作" field="action" width="100px" />
						</Reactman.Table>
					</Reactman.TablePanel>
				</div>
			)
		}else{
			<div></div>
		}
		
	}
});
module.exports = CardRuleOrderDetail;