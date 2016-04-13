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
	getAttributeValue :function(value,data){
		var order_item_list = JSON.parse(data['order_item_list']);
		var order_items = order_item_list.map(function(order_item,index){
			if (value == 'card_kind/valid_restrictions'){
				return (
					<span key={index}>{order_item["card_kind"]}/{order_item["valid_restrictions"]}<br></br></span>
				)
			}else if (value == 'weizoom_card_id_first/weizoom_card_id_last'){
				return (
					<span key={index}>{order_item["weizoom_card_id_first"]}-{order_item["weizoom_card_id_last"]}<br></br></span>
				)
			}else if (value == 'name'){
				return (
					<span key={index}><a href={'/order/detail?order_id='+data['id']}>{order_item['name']}</a><br></br></span>
				)
			}else{
				return (
					<span key={index}>{order_item[value]}<br></br></span>
				)
			}
		})

		
		console.log(value);
		console.log("---------");
		console.log(JSON.parse(data['order_item_list']));
		
		return order_items;
	},
	// componentWillMount: function() {
	// 	Action.getCardRuleOrder();
	// },
	// componentDidMount: function(){
	// 	Store.addListener(this.getCardRuleOrder);
	// },
	// getCardRuleOrder: function(){
	// 	this.setState({
	// 		cardRuleOrder:Store.getCardRuleOrder()
	// 	})
	// },
	rowFormatter: function(field, value, data) {
		if (field === 'name') {
			var order_items = this.getAttributeValue('name',data);
			return (
				<div>{order_items}</div>
			);
		}else if (field === 'money') {
			var order_items = this.getAttributeValue('name',data);
			return (
				<div>{order_items}</div>
			);
		}else if (field === 'weizoom_card_order_item_num') {
			var order_items = this.getAttributeValue('weizoom_card_order_item_num',data);
			return (
				<div>{order_items}</div>
			);
		}else if (field === 'total_money') {
			var order_items = this.getAttributeValue('total_money',data);
			return (
				<div>{order_items}</div>
			);
		}else if (field === 'card_kind/valid_restrictions') {
			var card_kind_valid_restrictions = this.getAttributeValue('card_kind/valid_restrictions',data);
			return (
				<div>
					<span>{card_kind_valid_restrictions}</span>
				</div>
			);
		}else if (field === 'weizoom_card_id_first/weizoom_card_id_last') {
			var card_range = this.getAttributeValue('weizoom_card_id_first/weizoom_card_id_last',data);
			return (
				<div>
					<span>{card_range}</span>
				</div>
			);
		}else if (field === 'apply_people/apply_departent') {
			var apply_people = data['apply_people'];
			var apply_departent = data['apply_departent'];
			return (
				<div>
					<span>{apply_people}</span><br></br>
					<span>{apply_departent}</span>
				</div>
			);
		}else if (field === 'expand-row') {
			return (
				<div style={{backgroundColor:'#EFEFEF'}}>
					<div style={{float:'left', color:'#FF0000', padding:'5px', display: 'inline-block'}}>订单编号: {data['order_number']}</div>
					<div style={{float:'right', color:'#FF0000', padding:'5px', display: 'inline-block'}}>订单金额: {data['order_money']}元</div>
					<div style={{float:'right', color:'#FF0000', padding:'5px', display: 'inline-block'}}>实付金额: {data['order_money']}元</div>
					<div style={{clear: 'both'}}></div>
				</div>
				
			)
		}
		else if (field === 'action') {
			if(data.is_activation ==0){
				return (
					<div>
						<a className="btn btn-link btn-xs" onClick={this.onClickActivation.bind(this,data.id,data.is_activation)}>卡激活</a>
						<a className="btn btn-link btn-xs mt5">编辑订单</a>
						<a className="btn btn-link btn-xs" onClick={this.onClickActivation.bind(this,data.id,-1)}>取消订单</a>
						<a className="btn btn-link btn-xs">备注</a>
					</div>
				)
			}else{
				return (
					<div>
						<a className="btn btn-link btn-xs" onClick={this.onClickActivation.bind(this,data.id,data.is_activation)}>停用</a>
						<a className="btn btn-link btn-xs mt5">编辑订单</a>
						<a className="btn btn-link btn-xs">取消订单</a>
						<a className="btn btn-link btn-xs">备注</a>
					</div>
				)
			}
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
		Action.updateOrderStaus(cur_filter);
	},
	render: function() {
		var productsResource = {
			resource: 'order.rule_order',
			data: {
				page: 1,
				count_per_page: 15
			}
		};
		// var cardRechargesNodes = cardRuleOrder.map(function(card_rule_order,index){
		// 	if (card_rule_order.is_activation ==0){
		// 		var card_is_activation =<div><a style={{display:'block'}} onClick={_this.onClickActivation.bind(_this,card_rule_order.id,card_rule_order.is_activation)} >卡激活{card_rule_order.is_activation}</a><a style={{display:'block'}}>编辑订单</a><a style={{display:'block'}} onClick={_this.onClickActivation.bind(_this,card_rule_order.id,-1)}>取消订单</a><a style={{display:'block'}}>备注</a></div>
		// 		var card_rule_order_is_click=<div>{card_rule_order.order_number}</div>
		// 	}else{
		// 		var card_is_activation =<div><a style={{display:'block'}} onClick={_this.onClickActivation.bind(_this,card_rule_order.id,card_rule_order.is_activation)} >停用{card_rule_order.is_activation}</a><a style={{display:'block'}}>编辑订单</a><a style={{display:'block'}}>备注</a></div>
		// 		var card_rule_order_is_click=<div style={{cursor:'pointer'}}><a>{card_rule_order.order_number}</a></div>
		// 	}
		// 	var order_item_list = JSON.parse(card_rule_order.order_item_list).map(function(order_item,index){
		// 		return(
		// 			<tr data-order-id="" key={index}>
		// 				<td>{card_rule_order_is_click}</td>
		// 				<td width="75">
		// 					{order_item.name}
		// 				</td>
		// 				<td width="75">
		// 					{order_item.money}
		// 				</td>
		// 				<td width="75">
		// 					{order_item.weizoom_card_order_item_num}
		// 				</td>
		// 				<td width="100">
		// 					{order_item.total_money}
		// 				</td>
		// 				<td>
		// 					<div>{order_item.card_kind}</div>
		// 					<div>{order_item.card_class}</div>
		// 				</td>
		// 				<td></td>
		// 				<td>{order_item.weizoom_card_id_first}-{order_item.weizoom_card_id_last}</td>

		// 				<td>
		// 					<div>{card_rule_order.order_attribute}</div>
		// 					<div>无</div>
		// 				</td>
		// 				<td>
		// 					<div>{card_rule_order.responsible_person}</div>
		// 					<div>{card_rule_order.company}</div>
		// 				</td>
		// 				<td>{card_rule_order.created_at}</td>
		// 				<td>
		// 					{card_is_activation}
		// 				</td>
		// 			</tr>
		// 		)
		// 	});
		// 	console.log(order_item_list);
		// 	console.log("===========");
		// 	return (
		// 		<tbody>
		// 			{order_item_list}
					
					
		// 		</tbody>
		// 	)
		// });
		
		return (
			<div>
					
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="创建新卡" icon="plus" href="/card/ordinary/" />
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
						<Reactman.TableColumn name="卡名称" field="name" />
						<Reactman.TableColumn name="面值" field="money" />
						<Reactman.TableColumn name="数量" field="weizoom_card_order_item_num" />
						<Reactman.TableColumn name="总额" field="total_money" />
						<Reactman.TableColumn name="卡类型/使用限制" field="card_kind/valid_restrictions"/>
						<Reactman.TableColumn name="专属商家" field="storage_time" />
						<Reactman.TableColumn name="卡号区间" field="weizoom_card_id_first/weizoom_card_id_last"/>
						<Reactman.TableColumn name="订单属性/折扣方式" field="order_attribute"/>
						<Reactman.TableColumn name="领用人/申请部门" field="apply_people/apply_departent" />
						<Reactman.TableColumn name="下单时间" field="created_at" />
						<Reactman.TableColumn name="操作" field="action" width="80px" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
		
	}
});
module.exports = cardRuleOrderList;

