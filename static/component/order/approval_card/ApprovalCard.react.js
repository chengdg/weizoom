/**
 * Created by cl on 2016/2/24 024.
 */
var React = require('react');
var debug = require('debug')('m:outline.data:DataPage');

var Store = require('.././rule_order/Store');
var getCardRuleStore = require('.././rule_order/getCardRuleStore');
var Action = require('.././rule_order/Action');
var ReactDOM = require('react-dom');
var ApprovalDialog = require('./ApprovalDialog.react');

var Reactman = require('reactman');
var FormInput = Reactman.FormInput;
var FormSubmit = Reactman.FormSubmit;
var Dispatcher = Reactman.Dispatcher;
var ApprovalCard = React.createClass({
	getInitialState: function() {
		return ({
			card_rule_order: [],
			card_rule_list: [],
		})
	},
	onChangeStore: function() {
		this.setState(
			Store.getData()
		)
	},
	componentWillMount: function() {
		Action.getCardRule();
	},
	componentDidMount: function(){
		getCardRuleStore.addListener(this.getCardRule);
		Store.addListener(this.onChangeStore);
	},
	getCardRule: function(){
		this.setState({
			card_rule_list:getCardRuleStore.getCardRule()
		})
	},
	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},
	onChooseOrderAttribute: function(){
		var value = this.refs.orderAttributes.value;
		if(value == 0){
			this.refs.saleCard.style.display='block';
			this.refs.internalCard.style.display='none';
			this.refs.discountCard.style.display='none';
		}else if(value == 1){
			this.refs.internalCard.style.display='block';
			this.refs.saleCard.style.display='none';
			this.refs.discountCard.style.display='none';
		}
		else if(value == 2){
			this.refs.discountCard.style.display='block';
			this.refs.internalCard.style.display='none';
			this.refs.saleCard.style.display='none';
		}
	},
	onCardOrderSave: function(){
		console.log(Store.getData());
		var ruleStore = Store.getData();
		var rule_order = this.state.card_rule_order;
		// rule_order.push({
		// 	'card_rule_num'
		// })
		var value = this.refs.orderAttributes.value;
		var remark = this.refs.remark.value;
		if(value == 0){
			var date = {
				'rule_order':JSON.stringify(rule_order),
				'card_rule_num': ruleStore.CardRuleNum,
				'valid_time_from': ruleStore.valid_time_from,
				'valid_time_to': ruleStore.valid_time_to,
				'company_info': ruleStore.company_info,
				'responsible_person': ruleStore.responsible_person,
				'contact': ruleStore.contact,
				'sale_name': ruleStore.saleName,
				'sale_departent': ruleStore.sale_departent,
				'order_attributes':value,
				'remark':remark
			}
			console.log("========");
			console.log(date);
		}else if(value == 1){
			this.refs.useDepartent.value;
			this.refs.projectName.value;
			this.refs.appliaction.value;
			this.refs.usePersion.value;
		}
		else if(value == 2){
			this.refs.orderNumber.value;
		}
		Action.saveCardRuleOrder(date);
	},
	addCardLines:function() {
		Action.addCardLines();
	},
	render: function(){
		return (
			<div className="xui-outlineData-page xui-formPage">
				<form className="form-horizontal mt15">
					<header  className="cui-header">
						<span className="xui-fontBold">基本信息</span>
						<span className="xui-fontGary">
							( <i className="star_show pl5"></i>
							表示必填)
						</span>
					</header>

					<CardListLabel />{/*.卡库.*/}
					<legend className="pl10 pt10 pb10"><a href="javascript:void(0);" onClick={this.addCardLines}>添加卡库</a></legend>

					<fieldset style={{marginLeft:'95px'}}>
		                <div>
	                		<label>卡名称：</label>
							<SelectRuleCard  ruleOrder={this.state.card_rule_order} cardRuleList={this.state.card_rule_list} />
		                </div>
					</fieldset>

			        <fieldset style={{background:'#FFF',marginLeft:'95px'}}>
		        		<div className="">
							<label>订单属性：</label>
							<select name="orderAttributes" className="w120 m0" ref="orderAttributes" onChange={this.onChooseOrderAttribute}>
								<option value="-1">请选择</option>
								<option value="0">发售卡</option>
								<option value="1">内部使用卡</option>
								<option value="2">返点卡</option>
							</select>
						</div>
						<div ref="saleCard" className="sale_card">
							<FormInput label="客户企业信息:" type="text" name="company_info" ref="companyInfo" value={this.state.company_info} onChange={this.onChange} />
							<FormInput label="客户经办人信息:" type="text" name="responsible_person" ref="responsiblePerson" value={this.state.responsible_person} onChange={this.onChange} />
							<FormInput label="客户联系方式:" type="text" name="contact" ref="contact" value={this.state.contact} onChange={this.onChange}/>
							<FormInput label="销售员姓名:" type="text" name="sale_name" ref="saleName" value={this.state.sale_name} onChange={this.onChange}/>
							<FormInput label="销售部门:" type="text" name="sale_departent" ref="saleDepartent" value={this.state.sale_departent} onChange={this.onChange}/>
						</div>
						<div ref="internalCard" className="internal_card" style={{display:'none'}}>
							<FormInput label="领用部门:" type="text" name="use_departent" ref="useDepartent" value={this.state.use_departent} onChange={this.onChange}/>
							<FormInput label="项目名称:" type="text" name="project_name" ref="projectName" value={this.state.project_name} onChange={this.onChange}/>
							<FormInput label="用途:" type="text" name="appliaction" ref="appliaction" value={this.state.appliaction} onChange={this.onChange}/>
							<FormInput label="领用人:" type="text" name="use_persion" ref="usePersion" value={this.state.use_persion} onChange={this.onChange}/>
						</div>
						<div ref="discountCard" className="discount_card" style={{display:'none'}}>
							<FormInput label="对应发单号:" type="text" name="order_number" ref="orderNumber" value={this.state.order_number} onChange={this.onChange}/>
						</div>
						<div >
							<label className="">备注：</label>
							<textarea style={{width:'250px',verticalAlign: 'top'}} className="" name="remark" ref="remark" ></textarea>
						</div>
			        </fieldset>
			        <div style={{marginTop:'20px',marginLeft:'158px'}}>
			            <div className="control-group">
			                <div style={{margin: '40px 0 40px 102px'}}>
								<button type="button" className="btn btn-success" onClick={this.onCardOrderSave}>确定</button>
								<button className="btn btn-cancel" style={{marginLeft: '20px'}} onClick={this.props.cancleCardRecharge}>取消</button>
							</div>
			            </div>
			        </div>
		       </form>
			</div>
		)
	}
});

SelectRuleCard = React.createClass({
	onSaveCardRule: function(){
		var rule_name = this.refs.chooseRuleName.value;
		var select_node = this.refs.chooseRuleName.getDOMNode();
		var selected_index = select_node.selectedIndex;
		var rule_id = select_node.options[selected_index].getAttribute('data-rule-id');
		var rule_obj ={
			'rule_name':rule_name,
			'rule_id':rule_id
		}
		var ruleOrder = this.props.ruleOrder;
		console.log(ruleOrder.length);
		ruleOrder.splice(0,1);
		ruleOrder.push(rule_obj);
	},
	render: function(){
		var card_rule_list = this.props.cardRuleList.map(function(rule_list,index){
			return(
				<option ref="ruleName" data-rule-id={rule_list.id} key={index}>{rule_list.name}</option>
			)
		});
		return(
			<div>
				<select onChange={this.onSaveCardRule} ref="chooseRuleName" >
					<option ref="ruleName" data-rule-id='0'>请选择</option>
					{card_rule_list}
				</select>
			</div>
		)
	}
})
//
var CardListLabel = React.createClass({
	getInitialState: function() {
		return ({
			cardlist:[{CardName:'',CardRuleNum:'',CardRuleTimeStart:'',CardRuleTimeEnd:''}]
		})
	},
	onChangeStore: function() {
		this.setState({
			cardlist:Store.getData().cardlines
		})
	},
	componentDidMount: function(){
		Store.addListener(this.onChangeStore);
	},
	onChange: function(index,value,event) {
		var property = event.target.getAttribute('name');
		Action.updateAddProduct(index, property, value);
	},
	choiceCard: function(index) {
		Reactman.PageAction.showDialog({
			title: "选择卡库", 
			component: ApprovalDialog, 
			data: {
				index: index
			},
			success: function(inputData, dialogState) {
				console.log(inputData, dialogState,66666666666)
				// Action.updateProductComment(product, comment);
			}
		});
	},
	render: function() {
		var _this=this;
		var cardlines=this.state.cardlist.map(function(card,index) {
			return (
			<fieldset className="form-inline" key={index}>
				<FormInput label="卡名称:" type="text" name="CardName" ref="CardName" value={_this.state.cardlist[index].CardName} validate="require-notempty" onChange={_this.onChange.bind(_this,index)}/>
				<a href="javascript:void(0);" style={{display:'inline-block',textAlign:'center',width:'80px'}} onClick={_this.choiceCard.bind(_this,index)}>选择卡库</a>
				<FormInput label="出库数量:" type="text" name="CardRuleNum" ref="CardRuleNum" value={_this.state.cardlist[index].CardRuleNum} validate="require-positive-int" onChange={_this.onChange.bind(_this,index)}/>
				<FormInput label="有效期:" type="text" name="valid_time_from" ref="valid_time_from" value={_this.state.cardlist[index].valid_time_from} validate="require-date" onChange={_this.onChange.bind(_this,index)}/>
				<FormInput type="text" name="valid_time_to" ref="valid_time_to" value={_this.state.cardlist[index].valid_time_to} validate="require-date" onChange={_this.onChange.bind(_this,index)}/>
			</fieldset>
			)
		})
		return (
			<div className="CardListLabel">
				{cardlines}
			</div>
		);
	}
});
module.exports = ApprovalCard;