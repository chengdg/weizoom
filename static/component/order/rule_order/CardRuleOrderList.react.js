/**
 * Created by cl on 2016/2/24 024.
 */
var React = require('react');
var debug = require('debug')('m:outline.data:DataPage');

var Store = require('./Store');
var Action = require('./Action');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var PageAction = Reactman.PageAction;
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;
var cardRuleOrderList = React.createClass({
	displayName: 'cardRuleOrderList',

	getInitialState: function() {
		return ({
			CardRecharges: [],
			cardRuleOrder:[]
		})
	},
	componentWillMount: function() {
		Action.getCardRuleOrder();
	},
	componentDidMount: function(){
		Store.addListener(this.getCardRuleOrder);
	},
	getCardRuleOrder: function(){
		console.log(Store.getCardRuleOrder());
		this.setState({
			cardRuleOrder:Store.getCardRuleOrder()
		})
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
	onClickActivation:function(orderId,is_activation){
		console.log(orderId,'sssssss')
		var cur_filter = {
			orderId:orderId,
			is_activation:is_activation,
		};
		console.log(cur_filter,66666)
		Action.getCardRuleOrder(cur_filter);
	},
	render: function() {
		_this=this;
		var cardRuleOrder = this.state.cardRuleOrder;
		var cardRechargesNodes = cardRuleOrder.map(function(card_rule_order,index){
			if (card_rule_order.is_activation ==0){
				var card_is_activation =<div><a style={{display:'block'}} onClick={_this.onClickActivation.bind(_this,card_rule_order.id,card_rule_order.is_activation)} >卡激活{card_rule_order.is_activation}</a><a style={{display:'block'}}>编辑订单</a><a style={{display:'block'}} onClick={_this.onClickActivation.bind(_this,card_rule_order.id,-1)}>取消订单</a><a style={{display:'block'}}>备注</a></div>
				var card_rule_order_is_click=<div>{card_rule_order.order_number}</div>
			}else{
				var card_is_activation =<div><a style={{display:'block'}} onClick={_this.onClickActivation.bind(_this,card_rule_order.id,card_rule_order.is_activation)} >停用{card_rule_order.is_activation}</a><a style={{display:'block'}}>编辑订单</a><a style={{display:'block'}}>备注</a></div>
				var card_rule_order_is_click=<div style={{cursor:'pointer'}}><a>{card_rule_order.order_number}</a></div>
			}
			return (
				<tr key={index}>
					<td>{card_rule_order_is_click}</td>
					<td>{card_rule_order.name}</td>
					<td>{card_rule_order.money}</td>
					<td>{card_rule_order.weizoom_card_order_item_num}</td>
					<td>{card_rule_order.total_money}</td>
					<td>{card_rule_order.card_kind}</td>
					<td>001-002</td>
					<td>
						<div>{card_rule_order.order_attribute}</div>
						<div>无</div>
					</td>
					<td>
						<div>{card_rule_order.responsible_person}</div>
						<div>{card_rule_order.company}</div>
					</td>
					<td>{card_rule_order.created_at}</td>
					<td>
						{card_is_activation}
					</td>
				</tr>
			)
		});
		
		return (
			<div>
				<div className="panel panel-default mt20 xb-rightPanel pr">
					<table className="table table-bordered xui-productList xb-stripedTable xb-noTdBorder xb-noBottom xb-noBorder xb-theadBg">
						<thead>
							<tr>
								<th>订单编号</th>
								<th>卡名称</th>
								<th>面值</th>
								<th>数量</th>
								<th>总额</th>
								<th>卡类型</th>
								<th>卡号区间</th>
								<th>
									<div>订单属性</div>
									<div>折扣方式</div>
								</th>
								<th>
									<div>领用人</div>
									<div>申请部门/公司</div>
								</th>
								<th>下单时间</th>
								<th>操作</th>
							</tr>
						</thead>
						<tbody>
							{cardRechargesNodes}
						</tbody>
					</table>

				</div>
				<div style={{clear: "both"}}></div>
				
			</div>
		)
		
	}
});
module.exports = cardRuleOrderList;

