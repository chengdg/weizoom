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
var FormSelect = Reactman.FormSelect;
var FormText =  Reactman.FormText;
var Dispatcher = Reactman.Dispatcher;
require('./ApprovalCard.css');
var ApprovalCard = React.createClass({
	getInitialState: function() {
		return ({
			card_rule_order: [],
			card_rule_list: [],
			orderInfo :{}
		})
	},
	onChangeStore: function() {
		this.setState({
			orderInfo : Store.getData()
		});
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
		if (property =="orderAttributes"){				
			Action.resetProduct();	
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
		}
		Action.updateProduct(property, value);
	},
	// onChooseOrderAttribute: function(){
	// 	Action.resetProduct();
	// 	var value = this.refs.orderAttributes.value;
	// 	if(value == 0){
	// 		this.refs.saleCard.style.display='block';
	// 		this.refs.internalCard.style.display='none';
	// 		this.refs.discountCard.style.display='none';
	// 	}else if(value == 1){
	// 		this.refs.internalCard.style.display='block';
	// 		this.refs.saleCard.style.display='none';
	// 		this.refs.discountCard.style.display='none';
	// 	}
	// 	else if(value == 2){
	// 		this.refs.discountCard.style.display='block';
	// 		this.refs.internalCard.style.display='none';
	// 		this.refs.saleCard.style.display='none';
	// 	}
	// },
	onCardOrderSave: function(){
		var card_list = Store.getDataCardlines();
		var order_infos = this.state.orderInfo;
		var ruleStore = Store.getData();
		var rule_order = this.state.card_rule_order;
		var value =  ruleStore.orderAttributes;
		var remark = ruleStore.remark;
		var date = {
			'rule_order':JSON.stringify(card_list),
			'card_rule_num': order_infos['card_rule_num'],
			'valid_time_from': order_infos['valid_time_from'],
			'valid_time_to': order_infos['valid_time_to'],
			'company_info': order_infos['company_info'],
			'responsible_person': order_infos['responsible_person'],
			'contact': order_infos['contact'],
			'sale_name': order_infos['sale_name'],
			'sale_departent': order_infos['sale_departent'],
			'use_departent': order_infos['use_departent'],
			'project_name': order_infos['project_name'],
			'appliaction': order_infos['appliaction'],
			'use_persion': order_infos['use_persion'],
			'order_number': order_infos['order_number'],
			'order_attributes':value,
			'remark':remark
		}
		Action.saveCardRuleOrder(date);
	},
	addCardLines:function() {
		Action.addCardLines();
	},
	render: function(){
		return (
			<div className="xui-outlineData-page xui-formPage xui-cardruleOrder">
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

			        <fieldset style={{background:'#FFF',marginLeft:'95px'}}>
						<FormSelect label="卡类型:" name="orderAttributes" options={[{"value": "-1", "text": "请选择"},{"value": "0", "text": "发售卡"},{"value": "1", "text": "内部使用卡"},{"value": "2", "text": "返点卡"}]} validate="require-select" onChange={this.onChange} ref="orderAttributes" />
						<div ref="saleCard" className="sale_card">
							<FormInput label="客户企业信息:" type="text" name="company_info" ref="companyInfo" value={this.state.orderInfo.company_info} onChange={this.onChange} />
							<FormInput label="客户经办人信息:" type="text" name="responsible_person" ref="responsiblePerson" value={this.state.orderInfo.responsible_person} onChange={this.onChange} />
							<FormInput label="客户联系方式:" type="text" name="contact" ref="contact" value={this.state.orderInfo.contact} onChange={this.onChange}/>
							<FormInput label="销售员姓名:" type="text" name="sale_name" ref="saleName" value={this.state.orderInfo.sale_name} onChange={this.onChange}/>
							<FormInput label="销售部门:" type="text" name="sale_departent" ref="saleDepartent" value={this.state.orderInfo.sale_departent} onChange={this.onChange}/>
						</div>
						<div ref="internalCard" className="internal_card" style={{display:'none'}}>
							<FormInput label="领用部门:" type="text" name="use_departent" ref="useDepartent" value={this.state.orderInfo.use_departent} onChange={this.onChange}/>
							<FormInput label="项目名称:" type="text" name="project_name" ref="projectName" value={this.state.orderInfo.project_name} onChange={this.onChange}/>
							<FormInput label="用途:" type="text" name="appliaction" ref="appliaction" value={this.state.orderInfo.appliaction} onChange={this.onChange}/>
							<FormInput label="领用人:" type="text" name="use_persion" ref="usePersion" value={this.state.orderInfo.use_persion} onChange={this.onChange}/>
						</div>
						<div ref="discountCard" className="discount_card" style={{display:'none'}}>
							<FormInput label="对应发单号:" type="text" name="order_number" ref="orderNumber" value={this.state.orderInfo.order_number} onChange={this.onChange}/>
						</div>
						<div >
							<FormText label="备注:" type="text" name="remark" value={this.state.orderInfo.remark} width="300" height="150" placeholder="" onChange={this.onChange} />
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
//
var CardListLabel = React.createClass({
	getInitialState: function() {
		return ({
			cardlist:[{rule_id:'',card_name:'',card_rule_num:'',valid_time_from:'',valid_time_to:''}]
		})
	},
	onChangeStore: function() {
		this.setState({
			cardlist:Store.getDataCardlines()
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
				Action.updateCardLines(inputData.index, dialogState.choiced_card);
			}
		});
	},
	render: function() {
		var _this=this;
		var cardlines=this.state.cardlist.map(function(card,index) {
			return (
			<fieldset className="form-inline" key={index}>
				<input name='rule_id' type="text" style={{display:'none'}} value={_this.state.cardlist[index].rule_id}/>
				<FormInput label="卡名称:" type="text" name="card_name" ref="CardName" value={_this.state.cardlist[index].card_name} validate="require-notempty" onChange={_this.onChange.bind(_this,index)}/>
				<a href="javascript:void(0);" style={{display:'inline-block',textAlign:'center',width:'80px'}} onClick={_this.choiceCard.bind(_this,index)}>选择卡库</a>
				<FormInput label="出库数量:" type="text" name="card_rule_num" ref="CardRuleNum" value={_this.state.cardlist[index].card_rule_num} validate="require-positive-int" onChange={_this.onChange.bind(_this,index)}/>
				<FormInput label="有效期:" type="text" name="valid_time_from" ref="valid_time_from" value={_this.state.cardlist[index].valid_time_from} validate="require-notempty" onChange={_this.onChange.bind(_this,index)}/>
				<FormInput type="text" name="valid_time_to" ref="valid_time_to" value={_this.state.cardlist[index].valid_time_to} validate="require-notempty" onChange={_this.onChange.bind(_this,index)}/>
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