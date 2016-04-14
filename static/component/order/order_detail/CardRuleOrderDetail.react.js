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
			rule_id: 0
		})
	},
	componentWillMount: function() {
		Action.getRuleId(this.state.order_id);
		Store.addListener(this.getRuleId);
	},
	getRuleId: function() {
		rule_id = Store.getRuleId();
		this.setState({
			rule_id: rule_id
		})
	},
	chooseRuleId: function(rule_id) {
		this.setState({
			rule_id: rule_id
		})
	},
	render: function(){
		var rule_id = this.state.rule_id;
		if(rule_id >0 ){
			return(
				<div>
					<CardRuleOrderList orderId={this.state.order_id} chooseRuleId={this.chooseRuleId}/>
					<CardOrderDetailList ruleId={this.state.rule_id}/>
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

	getCardList: function(rule_id){
		console.log(rule_id);
		this.props.chooseRuleId(rule_id);
	},
	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			var rule_id = data['rule_id'];
			return (
				<div><a onClick={this.getCardList.bind(this,rule_id)}>选取</a></div>
			);
		}else if (field == 'card_kind/valid_restrictions'){
			return (
				<span>{data["card_kind"]}/{data["valid_restrictions"]}</span>
			);
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
						<Reactman.TableColumn name="专属商家" field="storage_time" />
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
					<span>激活</span>
					<span>备注</span>
					<span>有效期</span>
				</div>
			);
		}else if (field === 'money/balance') {
			return (
				<div>
					<span>{data["money"]}/{data["balance"]}</span>
				</div>
			);
		}else {
			return value;
		}
	},
	render: function() {
		var rule_id = this.props.ruleId;
		if(rule_id >=0 ){
			var productsResource = {
				resource: 'order.card_detail',
				data: {
					page: 1,
					rule_id: rule_id,
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
							<Reactman.TableColumn name="有效期" field="validate"/>
							<Reactman.TableColumn name="激活时间" field="activated_at" />
							<Reactman.TableColumn name="备注" field="remark"/>
							<Reactman.TableColumn name="操作" field="action" width="80px" />
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